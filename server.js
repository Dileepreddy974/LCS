// server.js

import express from "express";
import session from "express-session";
import path from "path";
import { fileURLToPath } from 'url';

// Environment variables are now expected to be set in the system environment

// Get __dirname equivalent in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(session({ 
  secret: "luxury-car-rental-secret-key-change-in-production", 
  resave: false, 
  saveUninitialized: true,
  cookie: { secure: false } // Set to true in production with HTTPS
}));

// Serve static files
app.use(express.static(path.join(__dirname, 'static')));

// Health check endpoint
app.get("/health", (req, res) => {
  res.sendFile(path.join(__dirname, "health.html"));
});

// Routes
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "login.html"));
});

app.get("/register", (req, res) => {
  res.sendFile(path.join(__dirname, "register.html"));
});

app.post("/login", (req, res) => {
  const { email } = req.body;
  
  // Simple validation
  if (!email) {
    return res.redirect("/?error=Email is required");
  }
  
  // Simple email format validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.redirect("/?error=Please enter a valid email address");
  }
  
  // In a real application, you would validate against a database
  // For this demo, we'll just create a session
  req.session.user = { email: email, name: email.split('@')[0] };
  req.session.save(() => {
    res.redirect("/dashboard");
  });
});

app.get("/dashboard", (req, res) => {
  // Check if user is logged in
  if (!req.session.user) {
    return res.redirect("/?error=Please log in to access the dashboard");
  }
  
  res.sendFile(path.join(__dirname, "dashboard.html"));
});

app.post("/register", (req, res) => {
  const { name, email } = req.body;
  
  // Simple validation
  if (!name || !email) {
    return res.redirect("/register?error=Name and email are required");
  }
  
  // Simple email format validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.redirect("/register?error=Please enter a valid email address");
  }
  
  // In a real application, you would save to a database
  // For this demo, we'll just create a session
  req.session.user = { email: email, name: name };
  req.session.save(() => {
    res.redirect("/dashboard?success=Account created successfully!");
  });
});

app.get("/logout", (req, res) => {
  req.session.destroy(() => {
    res.redirect("/?success=You have been logged out");
  });
});

// Vercel requires us to export the app
export default app;

// Add actual port configuration
const PORT = process.env.PORT || 3000;

// Only start the server if this file is run directly (not imported)
if (import.meta.url === `file://${process.argv[1]}`) {
  app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}