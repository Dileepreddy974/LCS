# Luxury Car Rental Service - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Installation and Setup](#installation-and-setup)
5. [Running the Application](#running-the-application)
6. [Core Features](#core-features)
7. [Architecture](#architecture)
8. [API Endpoints](#api-endpoints)
9. [Frontend Components](#frontend-components)
10. [Styling and UI](#styling-and-ui)
11. [Data Management](#data-management)
12. [Database Implementation](#database-implementation)
13. [Security Considerations](#security-considerations)
14. [Development Guidelines](#development-guidelines)
15. [Troubleshooting](#troubleshooting)
16. [Future Enhancements](#future-enhancements)

## Project Overview

Luxury Car Rental is a modern web application that allows users to browse, borrow, return, donate, and track luxury cars. The application features a sleek claymorphism UI design with media-rich elements including a fullscreen background video and high-quality car images.

The project implements a dual-backend architecture:
- **Primary Backend**: Python Flask for core car rental functionality
- **Secondary Backend**: Node.js/Express for alternative implementation

### Key Features
- Browse available luxury cars with high-quality images
- Borrow and return car functionality with tracking
- Donate cars to expand the fleet with donor information tracking
- Track borrowed, returned, and donated cars with detailed history
- Detailed borrower and donor information
- User registration and login system
- User-specific data isolation
- Responsive design with mobile-friendly navigation
- Modern claymorphism UI with 3D animations
- Media-rich interface with background video
- Docker database support for persistent data storage

## Technology Stack

### Backend
- **Primary**: Python 3.x with Flask framework
- **Secondary**: Node.js with Express framework
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Template Engine**: Jinja2 (Flask) and direct HTML rendering (Node.js)

### Frontend
- **HTML5** with semantic markup
- **CSS3** with custom properties and animations
- **JavaScript** for client-side interactions
- **Responsive Design** with mobile-first approach

### Styling
- **Claymorphism Design**: Soft UI with neumorphic effects
- **Custom CSS**: Handcrafted styles without external frameworks
- **Animations**: CSS transitions and keyframe animations

### Media
- **Background Video**: Fullscreen looping background video
- **Car Images**: High-quality images from various sources
- **Responsive Images**: Adaptive sizing for different devices

## Project Structure

```
luxury-car-rental/
├── app.py                 # Flask application entry point
├── Car.py                 # Business logic and data models
├── models.py              # Database models for users, borrowers, cars, and transactions
├── db_manager.py          # Database manager for handling all database operations
├── server.js              # Node.js Express server
├── package.json           # Node.js dependencies and scripts
├── docker-compose.yml     # Docker configuration for PostgreSQL database
├── init.sql               # Database initialization script
├── requirements.txt       # Python dependencies
├── DOCUMENTATION.md       # This documentation file
├── README.md              # Project overview
├── NODEJS_README.md       # Node.js specific documentation
├── base.html              # Base template with common layout and navigation
├── home.html              # Home page template
├── list.html              # Car listing page
├── borrow.html            # Car borrowing page
├── return.html            # Car return page
├── donate.html            # Car donation page
├── track.html             # Borrowed cars tracking page
├── login.html             # User login page
├── register.html          # User registration page
├── profile.html           # User profile page
├── static/
│   ├── styles.css         # Main stylesheet
│   ├── app.js             # Client-side JavaScript
│   ├── bg.mp4             # Background video
│   └── cars/              # Car images directory
└── __pycache__/           # Python cache files
```

## Installation and Setup

### Prerequisites
- Python 3.6 or higher
- Node.js 14.0.0 or higher
- npm (comes with Node.js)
- Docker and Docker Compose

### Python Flask Setup

1. Clone or download the repository
2. Navigate to the project directory:
   ```bash
   cd luxury-car-rental
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Node.js Setup

1. Install Node.js dependencies:
   ```bash
   npm install
   ```

### Database Setup

1. Start the PostgreSQL database using Docker:
   ```bash
   docker-compose up -d
   ```

## Running the Application

### Running the Flask Application

1. Start the database:
   ```bash
   docker-compose up -d
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

### Running the Node.js Application

Development mode:
```bash
npm run dev
```

Production mode:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Core Features

### 1. Home Page
- Displays a gallery of available cars
- Features a 3D animated car showcase
- Includes a background video for immersive experience
- Shows quick access buttons to all features

### 2. Car Listing
- Comprehensive list of all available cars
- Filter functionality to search for specific cars
- Thumbnail images for each car
- Direct links to borrow specific cars

### 3. Borrow Car
- Form-based interface to borrow a car
- Validation for user input
- Real-time feedback through toast notifications
- Automatic tracking of borrowed cars

### 4. Return Car
- Interface to return borrowed cars
- Preview of car image during return process
- Confirmation of successful return
- Automatic removal from tracking system

### 5. Donate Car
- Form to add new cars to the fleet with donor information
- Requests donor name along with car details
- Confirmation of successful donation
- Automatic tracking of donated cars

### 6. Track Borrowed, Returned, and Donated Cars
- View of all currently borrowed cars with borrower details
- History of all returned cars with borrowing and return timestamps
- History of all donated cars with donor information and donation timestamps
- Visual representation with car thumbnails
- Detailed information about borrowers, donors, and cars
- **User-specific data isolation**: Logged-in users only see their own borrowing history

### 7. User Registration and Login
- **Registration**: Users can create accounts with name, email, and profile picture
- **Login**: Existing users can log in with their email
- **Profile Management**: Users can view their profile information
- **Session Management**: Secure user sessions with automatic logout

## Architecture

### Flask Backend Architecture

The Flask application follows a Model-View-Controller (MVC) pattern:

#### Models (Car.py, models.py, db_manager.py)
- `RentalCars`: Manages the car inventory and borrowing logic
- `Person`: Simple user representation
- `User`, `Borrower`, `Car`, `BorrowedCar`, `ReturnedCar`, `DonatedCar`: Database models
- `DatabaseManager`: Handles all database operations

#### Views (HTML Templates)
- `base.html`: Base template with common layout and navigation
- Page-specific templates for each feature
- Responsive design with mobile-first approach
- User authentication UI elements

#### Controllers (app.py)
- Route handlers for all application endpoints
- Business logic integration
- Flash messaging for user feedback
- User session management

### Node.js Backend Architecture

The Node.js application is a simpler implementation:

#### Server (server.js)
- Express.js routing for core pages
- Session management

## Database Implementation

### Database Schema

The application uses PostgreSQL with the following tables:

#### Users Table
- `id`: Primary key
- `name`: User's name (required)
- `email`: User's email (required, unique)
- `profile_image`: Path to profile image (optional)
- `created_at`: Timestamp of when the user was added

#### Borrowers Table
- `id`: Primary key
- `name`: Borrower's name (required)
- `email`: Borrower's email (optional)
- `phone`: Borrower's phone number (optional)
- `user_id`: Foreign key to users table (optional)
- `created_at`: Timestamp of when the borrower was added

#### Cars Table
- `id`: Primary key
- `name`: Car name (required, unique)
- `is_available`: Boolean indicating if the car is available
- `created_at`: Timestamp of when the car was added

#### Borrowed Cars Table
- `id`: Primary key
- `borrower_id`: Foreign key to borrowers table
- `car_id`: Foreign key to cars table
- `borrowed_at`: Timestamp of when the car was borrowed
- `returned`: Boolean indicating if the car has been returned

#### Returned Cars Table
- `id`: Primary key
- `borrower_id`: Foreign key to borrowers table
- `car_id`: Foreign key to cars table
- `borrowed_at`: Timestamp of when the car was borrowed
- `returned_at`: Timestamp of when the car was returned

#### Donated Cars Table
- `id`: Primary key
- `donor_name`: Donor's name (required)
- `car_name`: Car name (required)
- `car_id`: Foreign key to cars table (optional)
- `donated_at`: Timestamp of when the car was donated

### Database Manager

The `db_manager.py` file provides a high-level interface for all database operations:
- Adding and retrieving users
- Adding and retrieving borrowers
- Managing car availability
- Recording borrowing, return, and donation transactions
- Querying borrowed, returned, and donated cars
- **User-specific data queries**: Retrieving data filtered by user ID

### User Data Isolation

The application implements user data isolation to ensure privacy:
- When a user is logged in, they only see their own borrowed and returned cars
- Borrowers are associated with users when cars are borrowed
- The track page filters data based on the logged-in user
- Admin view (when not logged in) shows all data

## Security Considerations

### Authentication
- Session-based authentication for user login
- Secure password-less authentication using email
- Profile picture upload with file type validation
- Session timeout and cleanup

### Data Privacy
- User-specific data isolation
- No sharing of personal data between users
- Secure handling of user sessions
- Proper cleanup of session data on logout

### File Upload Security
- File type validation for profile pictures
- Secure filename generation to prevent conflicts
- Storage in dedicated uploads directory
- Size limitations for uploaded files

## Development Guidelines

### Code Structure
- Follow MVC pattern for Flask application
- Maintain separation of concerns
- Use meaningful variable and function names
- Add comments for complex logic

### Database Design
- Use SQLAlchemy ORM for database operations
- Implement proper relationships between models
- Use foreign keys to maintain data integrity
- Handle database connection errors gracefully

### User Experience
- Provide clear feedback for user actions
- Implement responsive design for all devices
- Use consistent styling across all pages
- Ensure accessibility standards are met

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure Docker is running and the PostgreSQL container is active
   - Check database credentials in environment variables
   - The application will automatically fall back to SQLite if PostgreSQL is unavailable

2. **File Upload Issues**
   - Ensure the `static/uploads` directory exists and is writable
   - Check file size limits in application configuration
   - Verify allowed file types in the upload validation

3. **User Session Issues**
   - Clear browser cookies if experiencing login problems
   - Ensure the application secret key is properly configured
   - Check for proper session handling in route implementations

### Debugging Tips

- Use the browser's developer tools to inspect network requests
- Check the application console for error messages
- Review database logs for connection issues
- Use test scripts to verify functionality

## Future Enhancements

### Planned Features
1. **Enhanced User Profiles**
   - Additional profile information fields
   - User activity history
   - Statistics and achievements

2. **Advanced Tracking Features**
   - Graphical representation of borrowing history
   - Export functionality for user data
   - Notifications for due returns

3. **Social Features**
   - User ratings and reviews
   - Car recommendations based on borrowing history
   - Community features for car enthusiasts

4. **Mobile Application**
   - Native mobile app for iOS and Android
   - Push notifications for borrowing reminders
   - Offline functionality for basic features

### Technical Improvements
1. **Performance Optimization**
   - Database query optimization
   - Caching for frequently accessed data
   - Image optimization for faster loading

2. **Security Enhancements**
   - Two-factor authentication
   - Enhanced session security
   - Data encryption for sensitive information

3. **Scalability**
   - Load balancing for high traffic
   - Database sharding for large datasets
   - Microservices architecture for better separation