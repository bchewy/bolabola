package connection

import (
    "sync"
    "log"

    "github.com/gorilla/websocket"
)

type Conn interface {
    Close() error
    ReadMessage() (messageType int, p []byte, err error)
    WriteMessage(messageType int, data []byte) error
    // Add other methods you use from websocket.Conn
}

type ConnectionManager struct {
    connections map[string]Conn
    mutex       sync.Mutex
}

type MockConn struct {
    *websocket.Conn
}

func NewMockConn() *MockConn {
    return &MockConn{}
}

func (mc *MockConn) ReadMessage() (messageType int, p []byte, err error) {
    // Implement your mock logic here
    return websocket.TextMessage, []byte("mock message"), nil
}

func (mc *MockConn) WriteMessage(messageType int, data []byte) error {
    // Implement your mock logic here
    return nil
}

func NewConnectionManager() *ConnectionManager {
    return &ConnectionManager{
        connections: make(map[string]Conn),
    }
}

func (manager *ConnectionManager) AddConnection(userID string, conn Conn) bool {
    manager.mutex.Lock()

    defer manager.mutex.Unlock()

    if _, exists := manager.connections[userID]; exists {
        // Connection already exists
        return false
    }

    // Add new connection
    manager.connections[userID] = conn
    return true
}

func (manager *ConnectionManager) GetConnection(userID string) (Conn, bool) {
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

func (manager *ConnectionManager) TotalConnections() int {
    manager.mutex.Lock()
    defer manager.mutex.Unlock()
    return len(manager.connections)
}

func (manager *ConnectionManager) BroadcastMessage(message []byte) {
    manager.mutex.Lock()
    defer manager.mutex.Unlock()

    for _, conn := range manager.connections {
        // Assuming conn has a Send method to send a message
        err := conn.WriteMessage(websocket.TextMessage, message)
        if err != nil {
            log.Printf("Failed to send message to connection: %v", err)
        }
    }
}