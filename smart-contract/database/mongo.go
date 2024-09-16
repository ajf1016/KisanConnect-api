package database

import (
    "context"
    "log"
    "time"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

var (
    Client *mongo.Client
    UsersCollection    *mongo.Collection
    RequestsCollection *mongo.Collection
    BidsCollection     *mongo.Collection
    ContractsCollection *mongo.Collection
)

func ConnectMongoDB() {
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")
    var err error
    Client, err = mongo.Connect(ctx, clientOptions)
    if err != nil {
        log.Fatal(err)
    }

    // Check the connection
    err = Client.Ping(ctx, nil)
    if err != nil {
        log.Fatal("Failed to connect to MongoDB:", err)
    }

    log.Println("Connected to MongoDB!")
    
    // Get references to collections
    db := Client.Database("your_database")
    UsersCollection = db.Collection("users")
    RequestsCollection = db.Collection("requests")
    BidsCollection = db.Collection("bids")
    ContractsCollection = db.Collection("contracts")
}
