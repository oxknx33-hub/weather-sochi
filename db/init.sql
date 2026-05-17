CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    value FLOAT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    wind_speed FLOAT,
    wind_direction VARCHAR(20),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
