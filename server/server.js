const express = require("express");
const mongoose = require("mongoose");
const path = require("path");
const cookieParser = require("cookie-parser");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();

// Direct MongoDB connection URL
const mongoURI = "mongodb://localhost:27017/mydatabase"; // Replace "mydatabase" with your database name
const PORT = 5000; // Define your port number here

// DB connection
mongoose.set("useFindAndModify", false);
mongoose.set("useCreateIndex", true);

const connectToDB = async () => {
    try {
        await mongoose.connect(mongoURI, {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });
        console.log("MongoDB connected...");
    } catch (err) {
        console.error("MongoDB connection error:", err);
        process.exit(1); // Exit process with failure
    }
};

// Connect to the database
connectToDB();

// Middleware
app.use(express.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(cors()); // Use cors middleware

// Serve static files from the 'frontend' directory
app.use(express.static(path.join(__dirname, "../frontend")));

// Routes
app.use("/auth", require("./routes/auth"));
app.use("/farmer", require("./routes/farmer"));
app.use("/wholesaler", require("./routes/wholesaler"));

// Port
app.listen(PORT, () => {
    console.log(`Server started on http://localhost:${PORT}`);
});
