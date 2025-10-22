from typing import List, Dict, Optional
from db_manager import DatabaseManager

class RentalCars:
    def __init__(self, initial_cars: List[str]) -> None:
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Add initial cars to database if they don't exist
        for car_name in initial_cars:
            self.db_manager.get_or_create_car(car_name)
        
        # Public attribute name kept as 'Cars' to match existing usage in app.py
        self.Cars: List[str] = list(initial_cars)

    def borrowCars(self, borrower_name: str, car_name: str, user_id: Optional[int] = None) -> bool:
        # Create a new database manager for this operation to avoid thread issues
        db_manager = DatabaseManager()
        try:
            # Use database manager to handle borrowing with user association
            success = db_manager.borrow_car(borrower_name, car_name, user_id)
            if success:
                # Update local Cars list to maintain compatibility
                if car_name in self.Cars:
                    self.Cars.remove(car_name)
            return success
        finally:
            db_manager.close()

    def returnCars(self, borrower_name: str, car_name: str) -> bool:
        # Create a new database manager for this operation to avoid thread issues
        db_manager = DatabaseManager()
        try:
            # Use database manager to handle returning
            success = db_manager.return_car(borrower_name, car_name)
            if success:
                # Update local Cars list to maintain compatibility
                if car_name not in self.Cars:
                    self.Cars.append(car_name)
            return success
        finally:
            db_manager.close()

    def donateCars(self, donor_name: str, car_name: str) -> bool:
        # Create a new database manager for this operation to avoid thread issues
        db_manager = DatabaseManager()
        try:
            # Use database manager to handle donation
            success = db_manager.donate_car(donor_name, car_name)
            if success and car_name not in self.Cars:
                self.Cars.append(car_name)
            return success
        finally:
            db_manager.close()

    def get_borrowed_cars(self, user_id: Optional[int] = None):
        """Get borrowed cars, optionally filtered by user"""
        db_manager = DatabaseManager()
        try:
            if user_id:
                return db_manager.get_borrowed_cars_by_user(user_id)
            else:
                return db_manager.get_borrowed_cars()
        finally:
            db_manager.close()
    
    def get_returned_cars(self, user_id: Optional[int] = None):
        """Get returned cars, optionally filtered by user"""
        db_manager = DatabaseManager()
        try:
            if user_id:
                return db_manager.get_returned_cars_by_user(user_id)
            else:
                return db_manager.get_returned_cars()
        finally:
            db_manager.close()
    
    def get_donated_cars(self):
        """Get all donated cars from database"""
        db_manager = DatabaseManager()
        try:
            return db_manager.get_donated_cars()
        finally:
            db_manager.close()
    
    def get_available_cars(self):
        """Get all available cars from database"""
        db_manager = DatabaseManager()
        try:
            # Ensure initial cars are in the database
            for car_name in self.Cars:
                db_manager.get_or_create_car(car_name)
            return db_manager.get_available_cars()
        finally:
            db_manager.close()


class Person:
    def __init__(self, name: str = "") -> None:
        self.name = name