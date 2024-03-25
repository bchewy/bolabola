package main

import (
	"queue/sender"
	"queue/consumer"
	"queue/common/connection"
	"sync"
)

func main() {
	manager := connection.NewConnectionManager()
	ws_server := sender.NewServer(manager)
	consume_server := consumer.NewServer(manager)

	var wg sync.WaitGroup
	wg.Add(2)

	go func() {
		defer wg.Done()
		ws_server.Start()
	}()

	go func() {
		defer wg.Done()
		consume_server.Start()
	}()

	wg.Wait()
}