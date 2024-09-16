package handlers

import (
    "context"
    "encoding/json"
    "net/http"
    "smart-contracts-project/database"
    "smart-contracts-project/models"
    "go.mongodb.org/mongo-driver/bson/primitive"
    "time"
)

func CreateContract(w http.ResponseWriter, r *http.Request) {
    var contract models.Contract
    if err := json.NewDecoder(r.Body).Decode(&contract); err != nil {
        http.Error(w, "Invalid request payload", http.StatusBadRequest)
        return
    }

    contract.ID = primitive.NewObjectID()
    contract.CreatedAt = time.Now() // If you have CreatedAt field

    _, err := database.ContractsCollection.InsertOne(context.TODO(), contract)
    if err != nil {
        http.Error(w, "Error creating contract", http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(contract)
}
