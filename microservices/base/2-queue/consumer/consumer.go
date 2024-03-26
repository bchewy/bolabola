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
    Token string `json:"token"`
    SecretKey string `json:"secret_key"`
}

func consumeMessages(manager *connection.ConnectionManager) {

    // Limit the rate of consumption of messages (mainly for demo purposes)
    ticker := time.NewTicker(2 * time.Second)

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
            token, secretKey, err := util.GenerateJWT(userIdStr, 10)
            if err != nil {
                log.Println("Error generating JWT:", err)
                continue
            }

            log.Println("Token is ", token)

            // Send the token and secret key back to the client
            response := Response{
                Token: token,
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

        if err := msg.Ack(false); err != nil {
            log.Printf("Error acknowledging message: %v", err)
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