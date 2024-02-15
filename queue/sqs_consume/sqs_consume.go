package sqs_consume

import (
	// "github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/gorilla/websocket"
	"log"
    "queue/common/awsutil"
	"queue/common/connection"
)

type Server struct {
	ConnectionManager *connection.ConnectionManager
}

var manager *connection.ConnectionManager

var sess *session.Session

func consumeMessages(sess *session.Session, queueUrl string, manager *connection.ConnectionManager) {
    sqsClient := sqs.New(sess)

    for {
        result, err := awsutil.ConsumeFromSQS(sqsClient, queueUrl)

        if err != nil {
            log.Println("Error", err)
            return
        }

        if len(result.Messages) == 0 {
            continue
        }

        // Assume the message body is the user ID
        user_id := *result.Messages[0].Body

        // Retrieve the connection
        conn, ok := manager.GetConnection(user_id)
        if !ok {
            log.Printf("No connection found for user ID %s", user_id)
            continue
        }

        // Send a message back to the client
        if err := conn.WriteMessage(websocket.TextMessage, []byte("Your message has been dequeued")); err != nil {
            log.Println(err)
            return
        }
    }
}

func NewServer(connection_manager *connection.ConnectionManager) *Server {
	manager = connection_manager

	return &Server{
		ConnectionManager: manager,
	}
}

func (s *Server) Start() {
	// SetupRoutes()
	sess = awsutil.SetupAWSSession()
    consumeMessages(sess, "https://sqs.ap-southeast-1.amazonaws.com/145339479675/TicketboostQueue.fifo", manager)
}