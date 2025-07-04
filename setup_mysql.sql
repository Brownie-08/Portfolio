-- MySQL Setup Script for Portfolio Database
-- Run this script in MySQL to create the database and user

-- Create the database
CREATE DATABASE IF NOT EXISTS portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create the user (adjust password as needed)
CREATE USER IF NOT EXISTS 'portfolio_user'@'localhost' IDENTIFIED BY 'Brownie@123###';

-- Grant all privileges on the portfolio database to the user
GRANT ALL PRIVILEGES ON portfolio_db.* TO 'portfolio_user'@'localhost';

-- Flush privileges to ensure they take effect
FLUSH PRIVILEGES;

-- Show the created database and user
SHOW DATABASES LIKE 'portfolio_db';
SELECT User, Host FROM mysql.user WHERE User = 'portfolio_user';

-- Display success message
SELECT 'MySQL database setup completed successfully!' AS Status;
