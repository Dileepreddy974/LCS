#!/usr/bin/env python3
"""
Test script to verify database creation
"""

from sqlalchemy import create_engine
from models import Base
import os

print("Current working directory:", os.getcwd())

# Create SQLite database
print("Creating SQLite database...")
engine = create_engine('sqlite:///car_rental.db', echo=True)
print("Engine created:", engine)

# Create tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

# Check if file exists
if os.path.exists('car_rental.db'):
    print("Database file created successfully!")
    print("File size:", os.path.getsize('car_rental.db'), "bytes")
else:
    print("Database file was not created!")