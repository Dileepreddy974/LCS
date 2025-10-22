"""
Test script to verify user registration functionality
"""
import os
import sys
import unittest
from db_manager import DatabaseManager
from models import User

class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        self.db_manager = DatabaseManager()
    
    def tearDown(self):
        """Clean up test data"""
        # Remove test users if they exist
        test_user = self.db_manager.get_user_by_email('test@example.com')
        if test_user:
            self.db_manager.session.delete(test_user)
            self.db_manager.session.commit()
        self.db_manager.close()
    
    def test_create_user(self):
        """Test creating a new user"""
        user = self.db_manager.create_user(
            name="Test User",
            email="test@example.com",
            profile_image="uploads/test.jpg"
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.profile_image, "uploads/test.jpg")
        
        # Test retrieving user by email
        retrieved_user = self.db_manager.get_user_by_email("test@example.com")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, user.id)
    
    def test_duplicate_email(self):
        """Test that duplicate emails are not allowed"""
        # Create first user
        user1 = self.db_manager.create_user(
            name="Test User 1",
            email="duplicate@test.com"
        )
        
        # Attempt to create second user with same email
        with self.assertRaises(Exception):
            user2 = self.db_manager.create_user(
                name="Test User 2",
                email="duplicate@test.com"
            )

if __name__ == '__main__':
    unittest.main()