#!/usr/bin/env python3
"""
Check database content
"""

from db_manager import DatabaseManager

def check_database_content():
    print("Checking database content...")
    
    # Create database manager
    db = DatabaseManager()
    
    try:
        # Check borrowers
        borrowers = db.get_all_borrowers()
        print(f"\nBorrowers ({len(borrowers)}):")
        for borrower in borrowers:
            print(f"  - {borrower.name} (ID: {borrower.id})")
        
        # Check cars
        cars = db.get_all_cars()
        print(f"\nCars ({len(cars)}):")
        for car in cars:
            status = "Available" if car.is_available else "Borrowed"
            print(f"  - {car.name} (ID: {car.id}, Status: {status})")
        
        # Check borrowed cars
        borrowed_cars = db.get_borrowed_cars()
        print(f"\nCurrently Borrowed Cars ({len(borrowed_cars)}):")
        for borrowed_car in borrowed_cars:
            print(f"  - {borrowed_car.car.name} borrowed by {borrowed_car.borrower.name}")
        
        # Check returned cars
        returned_cars = db.get_returned_cars()
        print(f"\nReturned Cars ({len(returned_cars)}):")
        for returned_car in returned_cars:
            print(f"  - {returned_car.car.name} returned by {returned_car.borrower.name}")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_database_content()