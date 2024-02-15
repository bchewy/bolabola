package connection

import (
    "sync"

    "github.com/gorilla/websocket"
)

type ConnectionManager struct {
    connections map[string]*websocket.Conn
    mutex       sync.Mutex
}

func NewConnectionManager() *ConnectionManager {
    return &ConnectionManager{
        connections: make(map[string]*websocket.Conn),
    }
}

func (manager *ConnectionManager) AddConnection(userID string, conn *websocket.Conn) {
    manager.mutex.Lock()
    manager.connections[userID] = conn
    manager.mutex.Unlock()
}

func (manager *ConnectionManager) GetConnection(userID string) (*websocket.Conn, bool) {
    manager.mutex.Lock()
    conn, exists := manager.connections[userID]
    manager.mutex.Unlock()
    return conn, exists
}

func (manager *ConnectionManager) RemoveConnection(userID string) {
    manager.mutex.Lock()
    delete(manager.connections, userID)
    manager.mutex.Unlock()
}