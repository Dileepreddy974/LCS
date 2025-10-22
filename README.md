# Luxury Car Rental (Flask)

A simple Flask web app to browse, borrow, return, donate, and track cars with a modern UI, claymorphism theme, and media-rich visuals.

## Features

- Home gallery of available cars with real images
- Cars list with filter and thumbnails
- Borrow / Return flows with toast feedback
- Donate a car to the fleet with donor information tracking
- Track borrowed cars with thumbnails
- Track returned cars history
- Track donated cars with donor details
- Detailed borrower and donor information
- User registration and login system
- User-specific data isolation
- Blurred fullscreen background video (`static/bg.mp4`)
- Clean, interactive claymorphism styling
- Responsive design with mobile-friendly navigation
- Docker database support for persistent data storage (with fallback to in-memory database)

## Deployment Options

This project includes both a Python Flask version and a Node.js version. For easy deployment, we recommend using the Node.js version with Vercel.

See [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md) for detailed instructions on deploying to Vercel with a custom domain.

## Project Structure

- `app.py` — Flask app and routes
- `Car.py` — RentalCars logic with database integration
- `models.py` — Database models for users, borrowers, cars, and transactions
- `db_manager.py` — Database manager for handling all database operations
- Templates: `base.html`, `home.html`, `list.html`, `borrow.html`, `return.html`, `donate.html`, `track.html`, `login.html`, `register.html`, `profile.html`
- Static: `static/styles.css`, `static/app.js`, `static/bg.mp4`, `static/cars/`
- Docker: `docker-compose.yml`, `init.sql`

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the database using Docker (optional, falls back to in-memory database if not available):
   ```bash
   docker-compose up -d
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Visit `http://localhost:5000` in your browser

## Database Support

The application supports both PostgreSQL with Docker and an in-memory SQLite database:

1. **With Docker**: If Docker is available and running, the application will connect to a PostgreSQL database
2. **Without Docker**: If Docker is not available, the application will automatically fall back to an in-memory SQLite database

## User Authentication

The application now includes a complete user authentication system:

### Registration
- Users can create accounts with name and email
- Profile picture upload with validation
- Secure storage of user information

### Login
- Existing users can log in with their email
- Session-based authentication
- Automatic redirection for authenticated users

### Profile Management
- Users can view their profile information
- Profile pictures displayed in navigation
- Session management with logout functionality

### Data Privacy
- User-specific data isolation
- Users only see their own borrowing history
- Admin view available when not logged in

## Documentation

For complete documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)