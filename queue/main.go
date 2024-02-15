package main

import (
	"queue/websocket"
	"queue/sqs_consume"
	"queue/common/connection"
	"sync"
)

func main() {
	manager := connection.NewConnectionManager()
	ws_server := websocket.NewServer(manager)
	consume_server := sqs_consume.NewServer(manager)

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