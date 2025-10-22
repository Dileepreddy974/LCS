import app from './server.js';

// Vercel expects the server to listen on process.env.PORT
const PORT = process.env.PORT || 3000;

// For Vercel, we don't actually start the server here
// Vercel will handle that for us
// But for local development, we still want to start the server
if (process.env.NODE_ENV !== 'production') {
  app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

// Export the app for Vercel
export default app;