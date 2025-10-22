from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    profile_image = Column(String(200), nullable=True)  # Path to profile image
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to borrowers (one user can have multiple borrower identities)
    borrowers = relationship("Borrower", back_populates="user")
    
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

class Borrower(Base):
    __tablename__ = 'borrowers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign key to User
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationship to user
    user = relationship("User", back_populates="borrowers")
    
    # Relationship to borrowed cars
    borrowed_cars = relationship("BorrowedCar", back_populates="borrower")

class Car(Base):
    __tablename__ = 'cars'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    borrowed_records = relationship("BorrowedCar", back_populates="car")
    return_records = relationship("ReturnedCar", back_populates="car")

class BorrowedCar(Base):
    __tablename__ = 'borrowed_cars'
    
    id = Column(Integer, primary_key=True)
    borrower_id = Column(Integer, ForeignKey('borrowers.id'))
    car_id = Column(Integer, ForeignKey('cars.id'))
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    returned = Column(Boolean, default=False)
    
    # Relationships
    borrower = relationship("Borrower", back_populates="borrowed_cars")
    car = relationship("Car", back_populates="borrowed_records")

class ReturnedCar(Base):
    __tablename__ = 'returned_cars'
    
    id = Column(Integer, primary_key=True)
    borrower_id = Column(Integer, ForeignKey('borrowers.id'))
    car_id = Column(Integer, ForeignKey('cars.id'))
    borrowed_at = Column(DateTime)
    returned_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    borrower = relationship("Borrower")
    car = relationship("Car", back_populates="return_records")

class DonatedCar(Base):
    __tablename__ = 'donated_cars'
    
    id = Column(Integer, primary_key=True)
    donor_name = Column(String(100), nullable=False)
    car_name = Column(String(100), nullable=False)
    donated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to car (if it exists in the cars table)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=True)
    car = relationship("Car")