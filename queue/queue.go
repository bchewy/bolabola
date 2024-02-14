package main

import (
	"encoding/json"
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
	"strconv"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

type RequestBody struct {
	UserID int `json:"user_id"`
}

func wsEndpoint(w http.ResponseWriter, r *http.Request) {
	// allow all origins to prevent CORS errors
	// TODO: Limit this later to only specific endpoints
	upgrader.CheckOrigin = func(r *http.Request) bool { return true }

	// upgrade to a websocket connection
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
	}

	log.Println("Client connected")

	err = ws.WriteMessage(1, []byte("Hi client!"))
	if err != nil {
		log.Println(err)
	}

	reader(ws)
}

func reader(conn *websocket.Conn) {
	for {
		messageType, p, err := conn.ReadMessage()
		if err != nil {
			log.Println(err)
			return
		}

		// fmt.Println(string(p))
		var user_id int

		if messageType == websocket.TextMessage {
			var user RequestBody
			if err := json.Unmarshal(p, &user); err != nil {
				log.Println("Error parsing JSON:", err)
				return
			}

			log.Printf("Received JSON: %+v", user)

			user_id = user.UserID
		}

		// TODO: Send the received user ID to SQS
		creds := credentials.NewEnvCredentials()

		sess, err := session.NewSessionWithOptions(session.Options{
			Profile:  "default",
			Config: aws.Config{
				Region: 	 aws.String("ap-southeast-1"),
				Credentials: creds,
			},
		})

		const queueUrl string = "https://sqs.ap-southeast-1.amazonaws.com/145339479675/TicketboostQueue.fifo"

		messageBody := "This is a test message"

		if err := sendMessage(sess, queueUrl, messageBody); err != nil {
			log.Printf("Error trying to send message to queue: %v", err)
			return
		}

		if err := conn.WriteMessage(messageType, []byte(strconv.Itoa(user_id))); err != nil {
			log.Println(err)
			return
		}
	}
}

func sendMessage(sess *session.Session, queueUrl string, messageBody string) error {
	sqsClient := sqs.New(sess)

	_, err := sqsClient.SendMessage(&sqs.SendMessageInput{
		QueueUrl:				&queueUrl,
		MessageBody:			aws.String(messageBody),
		MessageGroupId: 		aws.String("waiting-room-queue"),
		MessageDeduplicationId: aws.String("waiting"),
	})

	return err
}

func homePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Home Page")
}

func setupRoutes() {
	http.HandleFunc("/", homePage)
	http.HandleFunc("/ws", wsEndpoint)
}

func main() {
	fmt.Println("Hello World")
	setupRoutes()
	log.Fatal(http.ListenAndServe(":8080", nil))
}
