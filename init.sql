-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS borrowers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS borrowed_cars (
    id SERIAL PRIMARY KEY,
    borrower_id INTEGER REFERENCES borrowers(id),
    car_id INTEGER REFERENCES cars(id),
    borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    returned BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS returned_cars (
    id SERIAL PRIMARY KEY,
    borrower_id INTEGER REFERENCES borrowers(id),
    car_id INTEGER REFERENCES cars(id),
    borrowed_at TIMESTAMP,
    returned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial cars if they don't exist
INSERT INTO cars (name, is_available) VALUES
    ('ORACLE REDBULL RB20', TRUE),
    ('AMG GLS', TRUE),
    ('FERRARI 296 GTB', TRUE),
    ('APX GP', TRUE),
    ('MCLAREN 720S', TRUE),
    ('LAMBORGHINI HURACÁN', TRUE),
    ('BUGATTI CHIRON', TRUE),
    ('ASTON MARTIN VANTAGE', TRUE),
    ('PORSCHE 911', TRUE),
    ('BMW M3', TRUE),
    ('AUDI R8', TRUE),
    ('TESLA MODEL S', TRUE)
ON CONFLICT (name) DO NOTHING;