package database

import (
    "context"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

// Global MongoDB client and collections
var (
    Client              *mongo.Client
    UsersCollection     *mongo.Collection
    BidsCollection      *mongo.Collection
    ContractsCollection *mongo.Collection
)

// Connect initializes the MongoDB client and collections
func Connect(uri string) error {
    clientOptions := options.Client().ApplyURI(uri)
    var err error
    Client, err = mongo.Connect(context.TODO(), clientOptions)
    if err != nil {
        return err
    }

    // Set up the collections
    UsersCollection = Client.Database("your_database").Collection("users")
    BidsCollection = Client.Database("your_database").Collection("bids")
    ContractsCollection = Client.Database("your_database").Collection("contracts")

    return nil
}
