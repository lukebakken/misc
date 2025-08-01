package main

import (
	"log"
	"os"
	"os/signal"
	"time"

    amqp "github.com/rabbitmq/amqp091-go"
)

func main() {
	startTime := time.Now()
	
	connections := make([]*amqp.Connection, 0, 3501)

	amqpURL := "amqp://TODO" // Replace with your RabbitMQ broker details

	for i := 0; i < 3501; i++ {
		if i%1000 == 0 {
			log.Printf("Opened %d amqp 0.9 connections", i)
		}

		conn, err := amqp.Dial(amqpURL)
		if err != nil {
			log.Fatalf("Failed to open connection %d: %v", i, err)
		}

		_, err = conn.Channel()
		if err != nil {
			log.Fatalf("Failed to open channel 1 on connection %d: %v", i, err)
		}
		_, err = conn.Channel()
		if err != nil {
			log.Fatalf("Failed to open channel 2 on connection %d: %v", i, err)
		}

		connections = append(connections, conn)

	}

	log.Println("All connections opened. Holding for 60 minutes or until interrupted.")
	elapsed := time.Since(startTime)
	log.Printf("Finished creating 40000 connections in %s", elapsed)

	// Handle Ctrl+C interrupt
	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt)

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

	log.Println("60 minutes completed. Closing connections.")
	closeAll(connections)
}

func closeAll(conns []*amqp.Connection) {
	for i, conn := range conns {
		if err := conn.Close(); err != nil {
			log.Printf("Failed to close connection %d: %v", i, err)
		}
	}
	log.Println("All connections closed.")
}
