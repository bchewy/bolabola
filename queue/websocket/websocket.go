package websocket

import (
	"encoding/json"
	// "fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
	"queue/connection_manager"
	"strconv"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

type RequestBody struct {
	UserID int `json:"user_id"`
}

type SQSMessage struct {
	UserID			string	`json:"user_id"`
	ConnectionToken	string	`json:"connection_token"`
}

type Server struct {
	ConnectionManager *connection_manager.ConnectionManager
}

func SetupAWSSession() *session.Session {
	creds := credentials.NewEnvCredentials()

	return session.Must(session.NewSessionWithOptions(session.Options{
		Profile:  "default",
		Config: aws.Config{
			Region: 	 aws.String("ap-southeast-1"),
			Credentials: creds,
		},
	}))
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

func WSHandler(conn *websocket.Conn) {
	for {
		messageType, p, err := conn.ReadMessage()
		if err != nil {
			log.Println(err)
			return
		}

		var user_id int

		// Parse JSON request
		if messageType == websocket.TextMessage {
			var user RequestBody
			if err := json.Unmarshal(p, &user); err != nil {
				log.Println("Error parsing JSON:", err)
				return
			}

			log.Printf("Received JSON: %+v", user)

			user_id = user.UserID
		}

		// Send the received user ID to SQS
		sess := SetupAWSSession()

		const queueUrl string = "https://sqs.ap-southeast-1.amazonaws.com/145339479675/TicketboostQueue.fifo"

		messageBody := strconv.Itoa(user_id)

		if err := SendToSQS(sess, queueUrl, messageBody); err != nil {
			log.Printf("Error trying to send message to queue: %v", err)
			return
		}

		if err := conn.WriteMessage(messageType, []byte(messageBody)); err != nil {
			log.Println(err)
			return
		}
	}
}

func SendToSQS(sess *session.Session, queueUrl string, messageBody string) error {
	sqsClient := sqs.New(sess)

	_, err := sqsClient.SendMessage(&sqs.SendMessageInput{
		QueueUrl:				&queueUrl,
		MessageBody:			aws.String(messageBody),
		MessageGroupId: 		aws.String("waiting-room-queue"),
		MessageDeduplicationId: aws.String("waiting"),
	})

	return err
}

func SetupRoutes() {
	http.HandleFunc("/ws", WSEndpoint)
}

func NewServer(manager *connection_manager.ConnectionManager) *Server {
	return &Server{
		ConnectionManager: manager,
	}
}

func (s *Server) Start() {
	http.HandleFunc("/ws", WSEndpoint)
	log.Fatal(http.ListenAndServe(":8080", nil))
}