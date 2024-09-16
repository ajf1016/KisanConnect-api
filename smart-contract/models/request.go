package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Request struct {
    ID          primitive.ObjectID `bson:"_id,omitempty" json:"id"`
    Title       string             `bson:"title" json:"title"`
    Description string             `bson:"description" json:"description"`
    UserID      primitive.ObjectID `bson:"user_id" json:"user_id"`
}
