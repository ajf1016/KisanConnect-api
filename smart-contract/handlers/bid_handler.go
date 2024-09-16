package handlers

import (
    "context"
    "encoding/json"
    "net/http"
    "smart-contracts-project/database"
    "smart-contracts-project/models"
    "go.mongodb.org/mongo-driver/bson/primitive"
)

// CreateBid handles the creation of a new bid
func CreateBid(w http.ResponseWriter, r *http.Request) {
    var bid models.Bid
    if err := json.NewDecoder(r.Body).Decode(&bid); err != nil {
        http.Error(w, "Invalid request payload", http.StatusBadRequest)
        return
    }

    bid.ID = primitive.NewObjectID()

    _, err := database.BidsCollection.InsertOne(context.TODO(), bid)
    if err != nil {
        http.Error(w, "Error creating bid", http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(bid)
}
