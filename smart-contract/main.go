package main

import (
    "log"
    "net/http"
	"smart-contracts-project/database"
    "smart-contracts-project/handlers" 
    "github.com/gorilla/mux"
)

func main() {
    // Connect to MongoDB
    database.ConnectMongoDB()
    
    // Initialize the router
    router := mux.NewRouter()

    // Define routes
    router.HandleFunc("/api/users", handlers.CreateUser).Methods("POST")
    router.HandleFunc("/api/bids", handlers.CreateBid).Methods("POST")

    // Start the server
    log.Println("Server is running on port 8080")
    log.Fatal(http.ListenAndServe(":8080", router))
}
