package consumer

import (
	"github.com/gorilla/websocket"
	"log"
	"queue/common/connection"
    "queue/common/util"
    "strconv"
    amqp "github.com/rabbitmq/amqp091-go"
)

type Server struct {
	ConnectionManager *connection.ConnectionManager
}

var manager *connection.ConnectionManager

var ch *amqp.Channel

var q amqp.Queue

func consumeMessages(manager *connection.ConnectionManager) {
    msgs, err := ch.Consume(
        q.Name, // queue
        "",     // consumer
        true,   // auto-ack
        false,  // exclusive
        false,  // no-local
        false,  // no-wait
        nil,    // args
    )

    if err != nil {
        log.Printf("Error trying to consume messages: %v", err)
        return
    }

    for msg := range msgs {
        userIdStr := string(msg.Body)

        // Parse user ID
        userId, err := strconv.Atoi(userIdStr)
        if err != nil {
            log.Printf("Error parsing user ID: %v", err)
            continue
        }

        // Retrieve the connection
        conn, ok := manager.GetConnection(userIdStr)
        if !ok {
            log.Printf("No connection found for user ID %d", userId)
            continue
        }

        log.Println("Connection found for user ID ", userId)

        // Generate a JWT token
        token, err := util.GenerateJWT(userIdStr, 10)
        if err != nil {
            log.Println("Error generating JWT:", err)
            continue
        }

        log.Println("Token is ", token)

        // Send a message back to the client
        if err := conn.WriteMessage(websocket.TextMessage, []byte(token)); err != nil {
            log.Println("Error sending message to client:", err)
        }

        // Close the WebSocket connection
        if err := conn.Close(); err != nil {
            log.Println("Error closing WebSocket connection:", err)
        }
    }
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

func NewServer(connectionManager *connection.ConnectionManager) *Server {
	manager = connectionManager

	return &Server{
		ConnectionManager: manager,
	}
}

func (s *Server) Start() {
    SetupRabbitMQ()
    consumeMessages(manager)
}