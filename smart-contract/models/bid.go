package models

import "go.mongodb.org/mongo-driver/bson/primitive"

// Bid represents a bid placed by a user on a request
type Bid struct {
    ID        primitive.ObjectID `bson:"_id,omitempty" json:"id"`          // MongoDB ObjectID
    Amount    float64            `bson:"amount" json:"amount"`             // Bid amount
    RequestID primitive.ObjectID `bson:"request_id,omitempty" json:"request_id"` // ID of the related request
    UserID    primitive.ObjectID `bson:"user_id,omitempty" json:"user_id"` // ID of the user placing the bid
}
