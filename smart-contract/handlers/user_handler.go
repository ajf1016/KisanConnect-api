package handlers

import (
    "context"
    "encoding/json"
    "net/http"
    "smart-contracts-project/database"
    "smart-contracts-project/models"
    "go.mongodb.org/mongo-driver/bson/primitive"
)

func CreateUser(w http.ResponseWriter, r *http.Request) {
    var user models.User
    if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
        http.Error(w, "Invalid request payload", http.StatusBadRequest)
        return
    }

    user.ID = primitive.NewObjectID()

    _, err := database.UsersCollection.InsertOne(context.TODO(), user)
    if err != nil {
        http.Error(w, "Error creating user", http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}
