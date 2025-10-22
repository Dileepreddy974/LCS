#!/usr/bin/env python3
"""
Simple test script to verify database functionality
"""

from db_manager import DatabaseManager, init_db

def test_database_functionality():
    print("Testing database functionality...")
    
    # Initialize database
    init_db()
    print("Database initialized")
    
    # Create database manager
    db = DatabaseManager()
    
    # Test borrower creation
    print("\n1. Testing borrower creation...")
    borrower = db.add_borrower("Alice Smith", "alice@example.com", "555-1234")
    print(f"Created borrower: {borrower.name} (ID: {borrower.id})")
    
    # Test car creation
    print("\n2. Testing car creation...")
    car = db.get_or_create_car("Tesla Model S")
    print(f"Created/get car: {car.name} (ID: {car.id})")
    
    # Test borrowing
    print("\n3. Testing car borrowing...")
    success = db.borrow_car("Alice Smith", "Tesla Model S")
    print(f"Borrowing success: {success}")
    
    # Check borrowed cars
    print("\n4. Checking borrowed cars...")
    borrowed_cars = db.get_borrowed_cars()
    print(f"Found {len(borrowed_cars)} borrowed cars:")
    for bc in borrowed_cars:
        print(f"  - {bc.car.name} borrowed by {bc.borrower.name} at {bc.borrowed_at}")
    
    # Test returning
    print("\n5. Testing car returning...")
    success = db.return_car("Alice Smith", "Tesla Model S")
    print(f"Returning success: {success}")
    
    # Check returned cars
    print("\n6. Checking returned cars...")
    returned_cars = db.get_returned_cars()
    print(f"Found {len(returned_cars)} returned cars:")
    for rc in returned_cars:
        print(f"  - {rc.car.name} returned by {rc.borrower.name} at {rc.returned_at}")
    
    # Close database connection
    db.close()
    print("\nDatabase test completed successfully!")

if __name__ == "__main__":
    test_database_functionality()