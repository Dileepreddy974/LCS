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
  res.status(200).json({ status: "OK", timestamp: new Date().toISOString() });
});

// Routes
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "login.html"));
});

app.get("/dashboard", (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Luxury Car Rental Service - Dashboard</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body { 
          font-family: Arial, sans-serif; 
          margin: 0; 
          padding: 20px; 
          background: #f5f5f5;
        }
        .container { 
          max-width: 800px; 
          margin: 0 auto; 
          background: white; 
          padding: 20px; 
          border-radius: 8px; 
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header { 
          display: flex; 
          justify-content: space-between; 
          align-items: center; 
          border-bottom: 1px solid #eee; 
          padding-bottom: 10px; 
          margin-bottom: 20px;
        }
        .user-info { 
          display: flex; 
          align-items: center; 
          gap: 10px;
        }
        .user-photo { 
          width: 40px; 
          height: 40px; 
          border-radius: 50%;
        }
        .car-grid { 
          display: grid; 
          grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); 
          gap: 20px; 
          margin-top: 20px;
        }
        .car-card { 
          border: 1px solid #ddd; 
          border-radius: 8px; 
          padding: 15px; 
          text-align: center;
        }
        .car-image { 
          width: 100%; 
          height: 120px; 
          object-fit: cover; 
          border-radius: 4px;
        }
        .btn { 
          background: #007bff; 
          color: white; 
          border: none; 
          padding: 10px 15px; 
          border-radius: 4px; 
          cursor: pointer; 
          text-decoration: none; 
          display: inline-block;
        }
        .btn:hover { 
          background: #0056b3;
        }
        .btn.logout { 
          background: #dc3545;
        }
        .btn.logout:hover { 
          background: #c82333;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>Luxury Car Rental Service</h1>
          <div class="user-info">
            <span>Welcome, User!</span>
            <a href="/" class="btn logout">Logout</a>
          </div>
        </div>
        
        <h2>Available Luxury Cars</h2>
        <div class="car-grid">
          <div class="car-card">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/2019_Aston_Martin_Vantage_V8_Automatic_4.0_Front.jpg/640px-2019_Aston_Martin_Vantage_V8_Automatic_4.0_Front.jpg" alt="Aston Martin" class="car-image">
            <h3>Aston Martin Vantage</h3>
            <p>Luxury Sports Car</p>
            <button class="btn">Rent Now</button>
          </div>
          
          <div class="car-card">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Porsche_911_Carrera_4S_%28992%29_%2849446177797%29.jpg/640px-Porsche_911_Carrera_4S_%28992%29_%2849446177797%29.jpg" alt="Porsche 911" class="car-image">
            <h3>Porsche 911</h3>
            <p>Iconic Sports Car</p>
            <button class="btn">Rent Now</button>
          </div>
          
          <div class="car-card">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Ferrari_LaFerrari_%2819384139886%29.jpg/640px-Ferrari_LaFerrari_%2819384139886%29.jpg" alt="Ferrari" class="car-image">
            <h3>Ferrari LaFerrari</h3>
            <p>Ultimate Hypercar</p>
            <button class="btn">Rent Now</button>
          </div>
          
          <div class="car-card">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Lamborghini_Aventador_LP700-4_2012_%2813364719004%29.jpg/640px-Lamborghini_Aventador_LP700-4_2012_%2813364719004%29.jpg" alt="Lamborghini" class="car-image">
            <h3>Lamborghini Aventador</h3>
            <p>Italian Supercar</p>
            <button class="btn">Rent Now</button>
          </div>
        </div>
      </div>
    </body>
    </html>
  `);
});

app.get("/logout", (req, res) => {
  res.redirect("/");
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