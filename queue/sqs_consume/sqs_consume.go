package sqs_consume

import (
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/gorilla/websocket"
	"log"
    "queue/common/awsutil"
	"queue/common/connection"
    "queue/common/util"
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

        log.Println("Messages", result.Messages)

        // Assume the message body is the user ID
        userId := *result.Messages[0].Body

        // Retrieve the connection
        conn, ok := manager.GetConnection(userId)
        if !ok {
            log.Printf("No connection found for user ID %s", userId)
            continue
        }

        log.Println("Connection found for user ID ", userId)

        // Generate a JWT token
        token, err := util.GenerateJWT(userId, 10)

        log.Println("Token is ", token)

        if err != nil {
            log.Println(err)
            return
        }

        // Send a message back to the client
        if err := conn.WriteMessage(websocket.TextMessage, []byte(token)); err != nil {
            log.Println(err)
            return
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
	// SetupRoutes()
	sess = awsutil.SetupAWSSession()
    consumeMessages(sess, "https://sqs.ap-southeast-1.amazonaws.com/145339479675/TicketboostQueue.fifo", manager)
}