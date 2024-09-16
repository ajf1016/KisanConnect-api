package main

import (
    "log"
    "net/http"
    "smart-contracts-project/database"
    "smart-contracts-project/handlers"
    "github.com/gorilla/mux"
)

func main() {
    // Initialize database connection
    err := database.Connect("mongodb://localhost:27017")
    if err != nil {
        log.Fatal(err)
    }

    // Set up the router
    router := mux.NewRouter()
    router.HandleFunc("/api/users", handlers.CreateUser).Methods("POST")
    router.HandleFunc("/api/bids", handlers.CreateBid).Methods("POST")
    router.HandleFunc("/api/contracts", handlers.CreateContract).Methods("POST")

    // Start the server
    log.Fatal(http.ListenAndServe(":8080", router))
}
