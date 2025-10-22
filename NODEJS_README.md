# Luxury Car Rental Service - Node.js Version

This is a Node.js implementation of the Luxury Car Rental Service.

## Prerequisites

- Node.js (version 14 or higher)
- npm (comes with Node.js)

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Run the Application

```bash
# Run in development mode
npm run dev

# Or run in production mode
npm start
```

The application will be available at `http://localhost:3000`

## Features

- Simple car rental dashboard
- Responsive design
- Session management

## Project Structure

- `server.js` - Main application file
- `package.json` - Project dependencies and scripts
- `static/` - Static assets (existing folder from Flask project)

## Ports

The application runs on port 3000 by default.

## Dependencies

- Express.js - Web framework
- Express-Session - Session management

## Development

For development with auto-restart on file changes:

```bash
npm run dev
```

This uses nodemon to automatically restart the server when files change.