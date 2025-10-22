#!/usr/bin/env python3
"""
Test script to verify car database functionality
"""

from db_manager import DatabaseManager, init_db

def test_car_database():
    print("Testing car database functionality...")
    
    # Initialize database
    init_db()
    print("Database initialized")
    
    # Create database manager
    db = DatabaseManager()
    
    # Test car creation
    print("\n1. Testing car creation...")
    car_names = [
        "ORACLE REDBULL RB20",
        "AMG GLS",
        "FERRARI 296 GTB",
        "APX GP",
        "MCLAREN 720S",
        "LAMBORGHINI HURACÁN",
        "BUGATTI CHIRON",
        "ASTON MARTIN VANTAGE",
        "PORSCHE 911",
        "BMW M3",
        "AUDI R8",
        "TESLA MODEL S"
    ]
    
    for car_name in car_names:
        car = db.get_or_create_car(car_name)
        print(f"Created/get car: {car.name} (ID: {car.id}, Available: {car.is_available})")
    
    # Check available cars
    print("\n2. Checking available cars...")
    available_cars = db.get_available_cars()
    print(f"Found {len(available_cars)} available cars:")
    for car in available_cars:
        print(f"  - {car.name}")
    
    # Close database connection
    db.close()
    print("\nCar database test completed successfully!")

if __name__ == "__main__":
    test_car_database()