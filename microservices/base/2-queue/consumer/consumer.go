package consumer

import (
	"encoding/json"
	"log"
	"queue/common/connection"
	"queue/common/rabbitmq"
	"queue/common/util"
	"strconv"
	"time"

	"github.com/gorilla/websocket"
	amqp "github.com/rabbitmq/amqp091-go"
)

type Server struct {
	ConnectionManager *connection.ConnectionManager
}

var manager *connection.ConnectionManager

var ch *amqp.Channel

var q *amqp.Queue

type Response struct {
	Token     string `json:"token"`
	SecretKey string `json:"secret_key"`
}

type MessageBody struct {
	UserID int `json:"user_id"`
}

func consumeMessages(manager *connection.ConnectionManager) {

	for {
		// Limit the rate of consumption of messages (mainly for demo purposes)
		ticker := time.NewTicker(1 * time.Second)

		// msgs, err := ch.Consume(
		//     q.Name, // queue
		//     "",     // consumer
		//     true,   // auto-ack
		//     false,  // exclusive
		//     false,  // no-local
		//     false,  // no-wait
		//     nil,    // args
		// )

		for range ticker.C {
			msg, ok, err := ch.Get(q.Name, true)

			if err != nil {
				log.Printf("Error trying to consume messages: %v", err)
				return
			}

			if !ok {
				continue
			}

			if string(msg.Body) == "DEMO MESSAGE" {
				continue
			} else {
				var msgBody MessageBody

				err := json.Unmarshal(msg.Body, &msgBody)

				if err != nil {
					log.Printf("Error unmarshaling message body: %v", err)
					continue
				}

                userId := strconv.Itoa(msgBody.UserID)

				// Retrieve the connection
				conn, ok := manager.GetConnection(userId)
				if !ok {
					log.Printf("No connection found for user ID %d", userId)
					continue
				}

				log.Println("Connection found for user ID ", userId)

				// Generate a JWT token
				token, secretKey, err := util.GenerateJWT(userId, 10)
				if err != nil {
					log.Println("Error generating JWT:", err)
					continue
				}

				log.Println("Token is ", token)

				// Send the token and secret key back to the client
				response := Response{
					Token:     token,
					SecretKey: secretKey,
				}

				jsonResponse, err := json.Marshal(response)
				if err != nil {
					log.Println("Error marshaling response to JSON:", err)
					return
				}

				// Send a message back to the client
				if err := conn.WriteMessage(websocket.TextMessage, jsonResponse); err != nil {
					log.Println("Error sending message to client:", err)
				}

				// Close the WebSocket connection
				if err := conn.Close(); err != nil {
					log.Println("Error closing WebSocket connection:", err)
				}
			}
		}
	}
}

func NewServer(connectionManager *connection.ConnectionManager) *Server {
	manager = connectionManager

	return &Server{
		ConnectionManager: manager,
	}
}

func (s *Server) Start() {
	ch, q, _ = rabbitmq.SetupRabbitMQ()
	consumeMessages(manager)
}
