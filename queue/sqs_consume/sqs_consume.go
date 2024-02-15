package sqs_consume

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/gorilla/websocket"
	"log"
	"queue/util/connection"
)

func consumeMessages(sess *session.Session, queueUrl string, manager *connection.ConnectionManager) {
    svc := sqs.New(sess)

    for {
        result, err := svc.ReceiveMessage(&sqs.ReceiveMessageInput{
            QueueUrl:            aws.String(queueUrl),
            MaxNumberOfMessages: aws.Int64(1),
            VisibilityTimeout:   aws.Int64(30),  // 30 seconds
            WaitTimeSeconds:     aws.Int64(0),
        })

        if err != nil {
            log.Println("Error", err)
            return
        }

        if len(result.Messages) == 0 {
            log.Println("Received no messages")
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