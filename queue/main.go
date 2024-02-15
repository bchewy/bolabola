package main

import (
	"queue/websocket"
	"queue/connection_manager"
	"sync"
)

func main() {
	manager := connection_manager.NewConnectionManager()
	server := websocket.NewServer(manager)

	var wg sync.WaitGroup
	wg.Add(1)

	go func() {
		defer wg.Done()
		server.Start()
	}()

	wg.Wait()
}