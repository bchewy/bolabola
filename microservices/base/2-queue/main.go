package main

import (
	"queue/sender"
	"queue/consumer"
	"queue/common/connection"
	"sync"
)

func main() {
	manager := connection.NewConnectionManager()
	sender_server := sender.NewServer(manager)
	consumer_server := consumer.NewServer(manager)

	var wg sync.WaitGroup
	wg.Add(2)

	go func() {
		defer wg.Done()
		sender_server.Start()
	}()

	go func() {
		defer wg.Done()
		consumer_server.Start()
	}()

	wg.Wait()
}