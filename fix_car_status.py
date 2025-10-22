#!/usr/bin/env python3
"""
Fix car status in database
"""

from db_manager import DatabaseManager
from models import Car

def fix_car_status():
    print("Fixing car status in database...")
    
    # Create database manager
    db = DatabaseManager()
    
    try:
        # Get all cars and set them as available
        cars = db.session.query(Car).all()
        for car in cars:
            print(f"Setting {car.name} as available")
            setattr(car, 'is_available', True)
            db.session.add(car)
        
        # Commit changes
        db.session.commit()
        print("Car statuses fixed successfully!")
        
        # Verify
        cars = db.get_all_cars()
        print(f"\nAfter fix:")
        for car in cars:
            status = "Available" if getattr(car, 'is_available') else "Borrowed"
            print(f"  - {car.name} (ID: {car.id}, Status: {status})")
            
    except Exception as e:
        print(f"Error fixing car status: {e}")
        db.session.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_car_status()