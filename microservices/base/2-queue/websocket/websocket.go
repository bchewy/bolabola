package websocket

import (
	"encoding/json"
	// "fmt"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
	"queue/common/connection"
	"queue/common/awsutil"
	"strconv"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

var manager *connection.ConnectionManager

var sess *session.Session

type RequestBody struct {
	UserID int `json:"user_id"`
}

type SQSMessage struct {
	UserID			string	`json:"user_id"`
	ConnectionToken	string	`json:"connection_token"`
}

type Server struct {
	ConnectionManager *connection.ConnectionManager
}

func WSEndpoint(w http.ResponseWriter, r *http.Request) {
	// allow all origins to prevent CORS errors
	// TODO: Limit this later to only specific endpoints
	upgrader.CheckOrigin = func(r *http.Request) bool { return true }

	// upgrade to a websocket connection
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
	}

	log.Println("Client connected")

	err = ws.WriteMessage(1, []byte("Connected to queue_sender server"))
	if err != nil {
		log.Println(err)
	}

	WSHandler(ws)
}

func ConnectionManagerTestEndpoint(w http.ResponseWriter, r *http.Request) {
	// allow all origins to prevent CORS errors
	_ , exists := manager.GetConnection("1")

	if exists {
		w.Write([]byte("Connection exists"))
	} else {
		w.Write([]byte("Connection does not exist"))
	}
}

func WSHandler(conn *websocket.Conn) {
	for {
		messageType, p, err := conn.ReadMessage()
		if err != nil {
			log.Println(err)
			return
		}

		var userId int

		// Parse JSON request
		if messageType == websocket.TextMessage {
			var user RequestBody
			if err := json.Unmarshal(p, &user); err != nil {
				log.Println("Error parsing JSON:", err)
				return
			}

			log.Printf("Received JSON: %+v", user)

			userId = user.UserID
		}

		// Send the received user ID to SQS

		const queueUrl string = "https://sqs.ap-southeast-1.amazonaws.com/145339479675/TicketboostQueue.fifo"

		messageBody := strconv.Itoa(userId)

		manager.AddConnection(strconv.Itoa(userId), conn)

		if err := awsutil.SendToSQS(sess, queueUrl, messageBody); err != nil {
			log.Printf("Error trying to send message to queue: %v", err)
			return
		}

		log.Println("Sent message to queue")

		if err := conn.WriteMessage(messageType, []byte(messageBody)); err != nil {
			log.Println(err)
			return
		}
	}
}

func SetupRoutes() {
	http.HandleFunc("/ws", WSEndpoint)
	http.HandleFunc("/test", ConnectionManagerTestEndpoint)
}

func NewServer(connection_manager *connection.ConnectionManager) *Server {
	manager = connection_manager

	return &Server{
		ConnectionManager: manager,
	}
}

func (s *Server) Start() {
	SetupRoutes()
	sess = awsutil.SetupAWSSession()
	log.Fatal(http.ListenAndServe(":9002", nil))
}