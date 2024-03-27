package sender

import (
	"encoding/json"
	// "fmt"
	"log"
	"net/http"
	"queue/common/connection"
	"strconv"
	"github.com/gorilla/websocket"
	"golang.org/x/net/context"
	"queue/common/rabbitmq"

	amqp "github.com/rabbitmq/amqp091-go"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

var manager *connection.ConnectionManager

var ch *amqp.Channel

var q *amqp.Queue

type RequestBody struct {
	UserID int `json:"user_id"`
	Demo   bool `json:"demo"`
}

type ResponseBody struct {
	QueuePosition int `json:"queue_position"`
}

type MessageBody struct {
	UserID int `json:"user_id"`
}

type Server struct {
	ConnectionManager *connection.ConnectionManager
}

type MockConn struct {
	*websocket.Conn
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

	err = ws.WriteMessage(1, []byte("Connected to sender server"))
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
			var wsMessage RequestBody
			if err := json.Unmarshal(p, &wsMessage); err != nil {
				log.Println("Error parsing JSON:", err)
				return
			}

			log.Printf("Received JSON: %+v", wsMessage)

			userId = wsMessage.UserID

			if (wsMessage.Demo) {
				// Add 10 messages to the queue for demo purpose
				rabbitmq.CreateDemoMessages(ch, q, manager)
			}
		}

		// Send message to RabbitMQ
		messageBody, err := json.Marshal(MessageBody{UserID: userId})

		if err != nil {
			log.Println("Error marshaling JSON:", err)
			return
		}

		manager.AddConnection(strconv.Itoa(userId), conn)

		// Send message to RabbitMQ
		ctx, cancel := context.WithTimeout(context.Background(), 5)
		defer cancel()

		err = ch.PublishWithContext(ctx,
			"",     // exchange
			q.Name, // routing key
			false,  // mandatory
			false,  // immediate
			amqp.Publishing{
				ContentType: "text/plain",
				Body:        []byte(messageBody),
			})

		if err != nil {
			log.Printf("Error trying to publish message: %v", err)
			return
		}

		responseBody, _ := json.Marshal(ResponseBody{QueuePosition: manager.TotalConnections()})

		conn.WriteMessage(websocket.TextMessage, responseBody)
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
	ch, q, _ = rabbitmq.SetupRabbitMQ()
	log.Fatal(http.ListenAndServe(":9002", nil))
}