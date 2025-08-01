package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"time"

	"github.com/Azure/go-amqp"
)

func main() {
	startTime := time.Now()
	connections := make([]*amqp.Conn, 0, 3501)

	for i := 0; i < 3500; i++ {
		if i%1000 == 0 {
			log.Printf("Opened %d connections", i)
		}

		conn, err := amqp.Dial(
			context.TODO(),
			"amqp://TODO",
			&amqp.ConnOptions{SASLType: amqp.SASLTypeAnonymous()},
		)
		if err != nil {
			log.Fatalf("Failed to open connection %d: %v", i, err)
		}

		_, err = conn.NewSession(context.TODO(), nil)
		if err != nil {
			log.Fatalf("Failed to open session 1 on connection %d: %v", i, err)
		}
		_, err = conn.NewSession(context.TODO(), nil)
		if err != nil {
			log.Fatalf("Failed to open session 2 on connection %d: %v", i, err)
		}

		connections = append(connections, conn)
	}


	log.Println("All connections opened. Waiting for up to 60 minutes. Press Ctrl+C to exit early.")
	elapsed := time.Since(startTime)
	log.Printf("Finished creating 3500 connections in %s", elapsed)

	// Handle interrupt signal
	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt)

	// Wait with minute-by-minute logging
	for minute := 1; minute <= 60; minute++ {
		select {
		case <-sig:
			log.Println("Interrupted by user. Closing connections.")
			closeAll(connections)
			return
		case <-time.After(1 * time.Minute):
			log.Printf("Waited %d minute(s)...", minute)
		}
	}

	log.Println("60 minutes passed. Closing connections.")
	closeAll(connections)
}

// Helper to close all connections
func closeAll(conns []*amqp.Conn) {
	for i, conn := range conns {
		if err := conn.Close(); err != nil {
			log.Printf("Failed to close connection %d: %v", i, err)
		}
	}
	log.Println("All connections closed.")
}
