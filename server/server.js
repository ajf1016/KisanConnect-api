const express = require("express");
const mongoose = require("mongoose");
const path = require("path");
const cookieParser = require("cookie-parser");
const bodyParser = require("body-parser");

const app = express();

// Direct MongoDB connection URL
const mongoURI = "mongodb://localhost:27017/mydatabase"; // Replace "mydatabase" with your database name

// DB connection
mongoose.set("useFindAndModify", false);
mongoose.set("useCreateIndex", true);
mongoose.connect(mongoURI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log("MongoDB connected..."))
.catch(err => {
    console.error("MongoDB connection error:", err);
});

// Middleware
app.use(express.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cookieParser());

// Static files
app.use(express.static(path.join(__dirname, "../frontend")));

// Routes
app.use("/auth", require("./routes/auth"));
app.use("/farmer", require("./routes/farmer"));
app.use("/wholesaler", require("./routes/wholesaler"));

// Port
const PORT = process.env.PORT || 5000;
app.listen(PORT, (err) => {
    if (err) throw err;
    console.log(`Server started on http://localhost:${PORT}`);
});
