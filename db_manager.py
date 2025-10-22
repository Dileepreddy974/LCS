import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
from models import Base, User, Borrower, Car, BorrowedCar, ReturnedCar, DonatedCar
from datetime import datetime

# Database connection with fallback
try:
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://car_user:car_password@localhost:5432/car_rental')
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Test connection
    engine.connect()
    database_available = True
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Falling back to persistent SQLite storage")
    # Fallback to persistent SQLite database file instead of in-memory
    engine = create_engine('sqlite:///car_rental.db', connect_args={'check_same_thread': False}, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    database_available = False

def init_db():
    """Initialize the database tables"""
    Base.metadata.create_all(bind=engine)

# Initialize the database immediately
init_db()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session():
    """Get a database session"""
    return SessionLocal()

class DatabaseManager:
    def __init__(self):
        self.session = get_session()
    
    def add_borrower(self, name, email=None, phone=None, user_id=None):
        """Add a new borrower to the database"""
        try:
            borrower = Borrower(name=name, email=email, phone=phone, user_id=user_id)
            self.session.add(borrower)
            self.session.commit()
            self.session.refresh(borrower)
            return borrower
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
    
    def get_or_create_borrower(self, name, user_id=None):
        """Get existing borrower or create new one"""
        borrower = self.session.query(Borrower).filter(Borrower.name == name).first()
        if not borrower:
            borrower = self.add_borrower(name, user_id=user_id)
        return borrower
    
    def get_or_create_car(self, car_name):
        """Get existing car or create new one"""
        car = self.session.query(Car).filter(Car.name == car_name).first()
        if not car:
            car = Car(name=car_name, is_available=True)
            self.session.add(car)
            self.session.commit()
            self.session.refresh(car)
        return car
    
    def borrow_car(self, borrower_name, car_name, user_id=None):
        """Record a car borrowing transaction"""
        try:
            # Get or create borrower
            borrower = self.get_or_create_borrower(borrower_name, user_id)
            
            # Get or create car
            car = self.get_or_create_car(car_name)
            
            # Check if car is available using getattr for proper column access
            if not getattr(car, 'is_available'):
                return False
            
            # Mark car as unavailable
            setattr(car, 'is_available', False)
            self.session.add(car)
            
            # Record borrowing
            borrowed_car = BorrowedCar(
                borrower_id=borrower.id,
                car_id=car.id,
                borrowed_at=datetime.now(),
                returned=False
            )
            
            self.session.add(borrowed_car)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
    
    def return_car(self, borrower_name, car_name):
        """Record a car return transaction"""
        try:
            # Get borrower
            borrower = self.session.query(Borrower).filter(Borrower.name == borrower_name).first()
            if not borrower:
                return False
            
            # Get car
            car = self.session.query(Car).filter(Car.name == car_name).first()
            if not car:
                return False
            
            # Find borrowed car record
            borrowed_car = self.session.query(BorrowedCar).filter(
                BorrowedCar.borrower_id == borrower.id,
                BorrowedCar.car_id == car.id,
                BorrowedCar.returned == False
            ).first()
            
            if not borrowed_car:
                return False
            
            # Mark as returned
            setattr(borrowed_car, 'returned', True)
            self.session.add(borrowed_car)
            
            # Mark car as available
            setattr(car, 'is_available', True)
            self.session.add(car)
            
            # Record return
            returned_car = ReturnedCar(
                borrower_id=borrower.id,
                car_id=car.id,
                borrowed_at=borrowed_car.borrowed_at,
                returned_at=datetime.now()
            )
            
            self.session.add(returned_car)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
    
    def donate_car(self, donor_name, car_name):
        """Record a car donation"""
        try:
            # Get or create car
            car = self.get_or_create_car(car_name)
            
            # Mark car as available
            setattr(car, 'is_available', True)
            self.session.add(car)
            
            # Record donation
            donated_car = DonatedCar(
                donor_name=donor_name,
                car_name=car_name,
                car_id=car.id,
                donated_at=datetime.now()
            )
            
            self.session.add(donated_car)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
    
    def get_borrowed_cars(self):
        """Get all currently borrowed cars with eager loading of relationships"""
        return self.session.query(BorrowedCar).options(
            joinedload(BorrowedCar.borrower),
            joinedload(BorrowedCar.car)
        ).filter(BorrowedCar.returned == False).all()
    
    def get_borrowed_cars_by_user(self, user_id):
        """Get borrowed cars for a specific user"""
        return self.session.query(BorrowedCar).options(
            joinedload(BorrowedCar.borrower),
            joinedload(BorrowedCar.car)
        ).join(Borrower).filter(
            BorrowedCar.returned == False,
            Borrower.user_id == user_id
        ).all()
    
    def get_returned_cars(self):
        """Get all returned cars with eager loading of relationships"""
        return self.session.query(ReturnedCar).options(
            joinedload(ReturnedCar.borrower),
            joinedload(ReturnedCar.car)
        ).all()
    
    def get_returned_cars_by_user(self, user_id):
        """Get returned cars for a specific user"""
        return self.session.query(ReturnedCar).options(
            joinedload(ReturnedCar.borrower),
            joinedload(ReturnedCar.car)
        ).join(Borrower).filter(
            Borrower.user_id == user_id
        ).all()
    
    def get_donated_cars(self):
        """Get all donated cars"""
        return self.session.query(DonatedCar).all()
    
    def get_all_borrowers(self):
        """Get all borrowers"""
        return self.session.query(Borrower).all()
    
    def get_all_cars(self):
        """Get all cars"""
        return self.session.query(Car).all()
    
    def get_available_cars(self):
        """Get all available cars"""
        return self.session.query(Car).filter(Car.is_available == True).all()
    
    # User management methods
    def create_user(self, name, email, profile_image=None):
        """Create a new user"""
        try:
            user = User(name=name, email=email, profile_image=profile_image)
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return self.session.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.session.query(User).filter(User.id == user_id).first()
    
    def update_user_profile_image(self, user_id, profile_image_path):
        """Update user's profile image"""
        try:
            user = self.session.query(User).filter(User.id == user_id).first()
            if user:
                user.profile_image = profile_image_path
                self.session.commit()
                return user
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
    
    def close(self):
        """Close the database session"""
        self.session.close()