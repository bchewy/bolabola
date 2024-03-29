package rabbitmq;

import (
	"encoding/json"
	"log"
	"time"
	"math/rand"
	"golang.org/x/net/context"
	"queue/common/connection"
	"strconv"
	amqp "github.com/rabbitmq/amqp091-go"
)

type MessageBody struct {
	UserID string `json:"user_id"`
}

func connectToRabbitMQ(uri string) (*amqp.Connection, error) {
    for {
        conn, err := amqp.Dial(uri)
        if err == nil {
            return conn, nil
        }

        log.Printf("Failed to connect to RabbitMQ: %v", err)

        // Exponential backoff with jitter
        delay := time.Second << 3 // Start with 1 second delay
        delay += time.Duration(rand.Intn(1000)) * time.Millisecond // Add jitter
        log.Printf("Retrying in %s", delay)
        time.Sleep(delay)
    }
}

func CreateDemoMessages(ch *amqp.Channel, q *amqp.Queue, manager *connection.ConnectionManager) {
	// Send a message to RabbitMQ
	ctx, cancel := context.WithTimeout(context.Background(), 5)
	defer cancel()

	rand.Seed(time.Now().UnixNano())

	numMessages := rand.Intn(6) + 10

	counter := 0

	for i := 0; i < numMessages; i++ {
		connectionId := "DEMO_" + strconv.Itoa(i)

		mockConn := connection.NewMockConn()

		if !manager.AddConnection(connectionId, mockConn) {
			log.Printf("Connection already exists: %v", connectionId)
			continue
		}

		messageBody, err := json.Marshal(MessageBody{UserID: connectionId})

		if err != nil {
			log.Println("Error marshaling JSON:", err)
			return
		}

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
		}

		counter++
	}

	log.Printf("Number of messages queued: %d", counter)
}

func SetupRabbitMQ() (*amqp.Channel, *amqp.Queue, error) {
	rabbitMQURI := "amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/"

	conn, err := connectToRabbitMQ(rabbitMQURI);

	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ in this line: %v", err)
		return nil, nil, err
	}

	ch, err := conn.Channel()

	if err != nil {
		log.Printf("Failed to open a channel: %v", err)
		return nil, nil, err
	}

	q, err := ch.QueueDeclare(
		"virtual_queue", // name
		true,             // durable
		false,            // delete when unused
		false,            // exclusive
		false,            // no-wait
		nil,              // arguments
	)

	if err != nil {
		log.Printf("Failed to declare a queue: %v", err)
		return nil, nil, err
	}

	log.Printf("Connected to RabbitMQ and declared a queue: %v", q.Name)

	return ch, &q, err
}