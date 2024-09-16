package handlers

import (
    "context"
    "encoding/json"
    "net/http"
    "smart-contracts-project/database"
    "smart-contracts-project/models"  // Fix: Uncommented this import
    
    "go.mongodb.org/mongo-driver/bson/primitive"
)

func CreateUser(w http.ResponseWriter, r *http.Request) {
    var user models.User
    // Decode the JSON request body into the user struct
    err := json.NewDecoder(r.Body).Decode(&user)
    if err != nil {
        http.Error(w, "Invalid request payload", http.StatusBadRequest)
        return
    }
    
    // Generate a new ObjectID for the user
    user.ID = primitive.NewObjectID()

    // Insert the user into the MongoDB collection
    _, err = database.UsersCollection.InsertOne(context.TODO(), user)
    if err != nil {
        http.Error(w, "Error creating user", http.StatusInternalServerError)
        return
    }
    
    // Respond with the created user
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}
