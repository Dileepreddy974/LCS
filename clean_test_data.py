#!/usr/bin/env python3
"""
Clean test data from database
"""

from db_manager import DatabaseManager
from models import Borrower, Car, BorrowedCar, ReturnedCar

def clean_test_data():
    print("Cleaning test data from database...")
    
    # Create database manager
    db = DatabaseManager()
    
    try:
        # List of test users to remove
        test_users = ["dileep", "william", "John Doe", "Jane Smith"]
        
        for user_name in test_users:
            # Find borrower
            borrower = db.session.query(Borrower).filter(Borrower.name == user_name).first()
            if borrower:
                print(f"Removing borrower: {user_name}")
                
                # Remove borrowed cars associated with this borrower
                borrowed_cars = db.session.query(BorrowedCar).filter(BorrowedCar.borrower_id == borrower.id).all()
                for borrowed_car in borrowed_cars:
                    print(f"  Removing borrowed car record: {borrowed_car.car.name}")
                    db.session.delete(borrowed_car)
                
                # Remove returned cars associated with this borrower
                returned_cars = db.session.query(ReturnedCar).filter(ReturnedCar.borrower_id == borrower.id).all()
                for returned_car in returned_cars:
                    print(f"  Removing returned car record: {returned_car.car.name}")
                    db.session.delete(returned_car)
                
                # Remove borrower
                db.session.delete(borrower)
        
        # Commit changes
        db.session.commit()
        print("Test data removed successfully!")
        
        # Verify clean state
        borrowers = db.get_all_borrowers()
        borrowed_cars = db.get_borrowed_cars()
        returned_cars = db.get_returned_cars()
        
        print(f"\nAfter cleanup:")
        print(f"Borrowers: {len(borrowers)}")
        print(f"Borrowed Cars: {len(borrowed_cars)}")
        print(f"Returned Cars: {len(returned_cars)}")
            
    except Exception as e:
        print(f"Error cleaning test data: {e}")
        db.session.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_test_data()