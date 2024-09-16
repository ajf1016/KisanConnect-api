package models

import "time"
import "go.mongodb.org/mongo-driver/bson/primitive"

type Contract struct {
    ID        primitive.ObjectID `bson:"_id,omitempty" json:"id"`
    RequestID primitive.ObjectID `bson:"request_id" json:"request_id"`
    BidID     primitive.ObjectID `bson:"bid_id" json:"bid_id"`
    Status    string             `bson:"status" json:"status"`
    CreatedAt time.Time          `bson:"created_at" json:"created_at"` // Add CreatedAt field
}
