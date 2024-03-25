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

	amqp "github.com/rabbitmq/amqp091-go"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

var manager *connection.ConnectionManager

var ch *amqp.Channel

var q amqp.Queue

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

		// const queueUrl string = "https://sqs.ap-southeast-1.amazonaws.com/442029411374/bolabola_queue.fifo"

		messageBody := strconv.Itoa(userId)

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
	}
}

func SetupRoutes() {
	http.HandleFunc("/ws", WSEndpoint)
	http.HandleFunc("/test", ConnectionManagerTestEndpoint)
}

func SetupRabbitMQ() {
	amqpConn, err := amqp.Dial("amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/")

	if err != nil {
		log.Printf("Error trying to connect to RabbitMQ: %v", err)
		return
	}

	ch, err = amqpConn.Channel()

	if err != nil {
		log.Printf("Error trying to open a channel: %v", err)
		return
	}

	q, err = ch.QueueDeclare(
		"virtual_queue", // name
		true,             // durable
		false,            // delete when unused
		false,            // exclusive
		false,            // no-wait
		nil,              // arguments
	)

	if err != nil {
		log.Printf("Error trying to declare a queue: %v", err)
		return
	}
}

func NewServer(connection_manager *connection.ConnectionManager) *Server {
	manager = connection_manager

	return &Server{
		ConnectionManager: manager,
	}
}

func (s *Server) Start() {
	SetupRoutes()
	SetupRabbitMQ()
	log.Fatal(http.ListenAndServe(":9002", nil))
}