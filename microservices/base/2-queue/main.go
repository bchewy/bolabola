package main

import (
	"net/http"
	"queue/sender"
	"queue/consumer"
	"queue/common/connection"
	"sync"

	"github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    opsProcessed = prometheus.NewCounter(prometheus.CounterOpts{
        Name: "queue_processed_ops_total",
        Help: "The total number of processed events",
    })
)

func init() {
    // Metrics have to be registered to be exposed:
    prometheus.MustRegister(opsProcessed)
}

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

	http.Handle("/metrics", promhttp.Handler())
	go http.ListenAndServe(":2112", nil)

	wg.Wait()
}