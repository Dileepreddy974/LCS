"""
Test script to verify user login functionality
"""
import os
import sys
import unittest
from db_manager import DatabaseManager
from models import User

class TestUserLogin(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        self.db_manager = DatabaseManager()
    
    def tearDown(self):
        """Clean up test data"""
        # Remove test users if they exist
        test_user = self.db_manager.get_user_by_email('login_test@example.com')
        if test_user:
            self.db_manager.session.delete(test_user)
            self.db_manager.session.commit()
        self.db_manager.close()
    
    def test_user_login(self):
        """Test user login functionality"""
        # Create a test user
        user = self.db_manager.create_user(
            name="Login Test User",
            email="login_test@example.com"
        )
        
        # Test retrieving user by email (simulating login)
        retrieved_user = self.db_manager.get_user_by_email("login_test@example.com")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, user.id)
        self.assertEqual(retrieved_user.name, "Login Test User")
        self.assertEqual(retrieved_user.email, "login_test@example.com")
    
    def test_invalid_login(self):
        """Test login with non-existent email"""
        user = self.db_manager.get_user_by_email("nonexistent@example.com")
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()