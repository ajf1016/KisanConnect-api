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
    
    // API routes
    router.HandleFunc("/api/users", handlers.CreateUser).Methods("POST")
    router.HandleFunc("/api/bids", handlers.CreateBid).Methods("POST")
    router.HandleFunc("/api/contracts", handlers.CreateContract).Methods("POST")
    
    // Serve static files from the /frontend directory
    router.PathPrefix("/").Handler(http.FileServer(http.Dir("frontend")))
    
    


    // Start the server
    log.Println("Server starting on port 8080...")
    log.Fatal(http.ListenAndServe(":8080", router))
}
