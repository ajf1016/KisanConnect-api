package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var client *mongo.Client

func main() {
	var err error
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")
	client, err = mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		log.Fatal(err)
	}

	err = client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}

	http.HandleFunc("/api/submit", submitHandler)
	fmt.Println("Server started at :8080")
	http.ListenAndServe(":8080", nil)
}

func submitHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodPost {
		// Handle ticket submission here
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Ticket submitted successfully"))
	} else {
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}
