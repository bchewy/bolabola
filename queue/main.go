package main

import (
	"queue/websocket"
	"queue/util/connection"
	"sync"
)

func main() {
	manager := connection.NewConnectionManager()
	server := websocket.NewServer(manager)

	var wg sync.WaitGroup
	wg.Add(1)

	go func() {
		defer wg.Done()
		server.Start()
	}()

	wg.Wait()
}