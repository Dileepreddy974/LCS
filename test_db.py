#!/usr/bin/env python3
"""
Test script to verify database integration
"""

from db_manager import DatabaseManager, init_db

def test_database():
    # Initialize the database
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Test adding a borrower
    print("\nTesting borrower creation...")
    borrower = db_manager.add_borrower("John Doe", "john@example.com", "123-456-7890")
    print(f"Created borrower: {borrower.name} (ID: {borrower.id})")
    
    # Test adding a car
    print("\nTesting car creation...")
    car = db_manager.get_or_create_car("Test Car")
    print(f"Created/get car: {car.name} (ID: {car.id}, Available: {car.is_available})")
    
    # Test borrowing a car
    print("\nTesting car borrowing...")
    success = db_manager.borrow_car("John Doe", "Test Car")
    print(f"Borrowing success: {success}")
    
    # Check car availability
    car = db_manager.get_or_create_car("Test Car")
    print(f"Car availability after borrowing: {car.is_available}")
    
    # Check borrowed cars
    borrowed_cars = db_manager.get_borrowed_cars()
    print(f"\nBorrowed cars count: {len(borrowed_cars)}")
    for borrowed in borrowed_cars:
        print(f"  - {borrowed.car.name} borrowed by {borrowed.borrower.name}")
    
    # Test returning a car
    print("\nTesting car returning...")
    success = db_manager.return_car("John Doe", "Test Car")
    print(f"Returning success: {success}")
    
    # Check car availability after return
    car = db_manager.get_or_create_car("Test Car")
    print(f"Car availability after returning: {car.is_available}")
    
    # Check returned cars
    returned_cars = db_manager.get_returned_cars()
    print(f"\nReturned cars count: {len(returned_cars)}")
    for returned in returned_cars:
        print(f"  - {returned.car.name} returned by {returned.borrower.name}")
    
    # Close database connection
    db_manager.close()
    print("\nDatabase test completed successfully!")

if __name__ == "__main__":
    test_database()