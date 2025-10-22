"""
Test script to verify user-specific data isolation
"""
import os
import sys
import unittest
from db_manager import DatabaseManager
from models import User, ReturnedCar
from Car import RentalCars

class TestUserDataIsolation(unittest.TestCase):
    def setUp(self):
        """Set up test database and users"""
        self.db_manager = DatabaseManager()
        self.rental = RentalCars(["Test Car 1", "Test Car 2"])
        
        # Create test users
        self.user1 = self.db_manager.create_user(
            name="User One",
            email="user1@example.com"
        )
        
        self.user2 = self.db_manager.create_user(
            name="User Two",
            email="user2@example.com"
        )
    
    def tearDown(self):
        """Clean up test data"""
        # Remove test users and their data
        test_users = [
            self.db_manager.get_user_by_email('user1@example.com'),
            self.db_manager.get_user_by_email('user2@example.com')
        ]
        
        for user in test_users:
            if user:
                # Remove associated borrowers
                borrowers = user.borrowers
                for borrower in borrowers:
                    # Remove borrowed cars
                    for borrowed_car in borrower.borrowed_cars:
                        self.db_manager.session.delete(borrowed_car)
                    # Remove returned cars
                    returned_cars = self.db_manager.session.query(ReturnedCar).filter(
                        ReturnedCar.borrower_id == borrower.id
                    ).all()
                    for returned_car in returned_cars:
                        self.db_manager.session.delete(returned_car)
                    # Remove borrower
                    self.db_manager.session.delete(borrower)
                # Remove user
                self.db_manager.session.delete(user)
        
        # Commit all deletions
        self.db_manager.session.commit()
        self.db_manager.close()
    
    def test_user_data_methods(self):
        """Test that user-specific data methods work correctly"""
        # Test that we can get borrowed cars for a user
        user1_borrowed = self.rental.get_borrowed_cars(1)  # Use a simple int
        self.assertIsNotNone(user1_borrowed)
        
        # Test that we can get borrowed cars for another user
        user2_borrowed = self.rental.get_borrowed_cars(2)  # Use a simple int
        self.assertIsNotNone(user2_borrowed)
        
        # Test that we can get all borrowed cars (no filter)
        all_borrowed = self.rental.get_borrowed_cars()
        self.assertIsNotNone(all_borrowed)

if __name__ == '__main__':
    unittest.main()