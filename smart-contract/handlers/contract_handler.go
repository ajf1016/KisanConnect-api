package handlers

import (
    "context"
    "encoding/json"
    "net/http"
    "smart-contracts-project/database"
    "smart-contracts-project/models"
    "go.mongodb.org/mongo-driver/bson/primitive"
)

// CreateContract handles the creation of a new contract based on an accepted bid
func CreateContract(w http.ResponseWriter, r *http.Request) {
    var contract models.Contract
    if err := json.NewDecoder(r.Body).Decode(&contract); err != nil {
        http.Error(w, "Invalid request payload", http.StatusBadRequest)
        return
    }

    // Set the contract ID and default status
    contract.ID = primitive.NewObjectID()
    contract.Status = "Pending" // or any default status you prefer

    // Insert the contract into the MongoDB collection
    _, err := database.ContractsCollection.InsertOne(context.TODO(), contract)
    if err != nil {
        http.Error(w, "Error creating contract", http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(contract)
}
