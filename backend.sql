-- Create the database (if not already created)
CREATE DATABASE IF NOT EXISTS water;

-- Switch to the water database
USE water;

-- Create the customer table (if not already created)
CREATE TABLE IF NOT EXISTS customer (
    cusid INT PRIMARY KEY,
    cusname VARCHAR(100),
    address VARCHAR(255),
    type ENUM('Household', 'Agriculture', 'Industrial')
);

-- Insert dummy customers data
INSERT INTO customer (cusid, cusname, address, type) VALUES
(1, 'John Doe', '123 Main St, Kochi', 'Household'),
(2, 'Jane Smith', '456 Elm St, Trivandrum', 'Agriculture'),
(3, 'Raj Kumar', '789 Palm Ave, Calicut', 'Industrial'),
(4, 'Lisa Thomas', '321 Oak Rd, Kottayam', 'Household'),
(5, 'Mohammed Ali', '654 Pine Dr, Alappuzha', 'Agriculture');

-- Create the bill table (if not already created)
CREATE TABLE IF NOT EXISTS bill (
    billid INT PRIMARY KEY,
    cusid INT,
    amount DECIMAL(10, 2),
    dp DATE,   -- Date of Payment
    dl DATE,   -- Last Date of Payment
    status ENUM('Not paid', 'Paid'),
    reading INT,  -- Water reading (units used)
    FOREIGN KEY (cusid) REFERENCES customer(cusid)
);

-- Insert dummy bill data based on customer readings and calculated amounts
INSERT INTO bill (billid, cusid, amount, dp, dl, status, reading) VALUES
(101, 1, 250.00, '2024-12-01', '2024-12-15', 'Not paid', 120),  -- Household customer with 120 units
(102, 2, 400.00, '2024-12-02', '2024-12-16', 'Paid', 180),      -- Agriculture customer with 180 units
(103, 3, 600.00, '2024-12-03', '2024-12-17', 'Not paid', 300),  -- Industrial customer with 300 units
(104, 4, 150.00, '2024-12-01', '2024-12-15', 'Paid', 90),       -- Household customer with 90 units
(105, 5, 250.00, '2024-12-04', '2024-12-18', 'Not paid', 160);  -- Agriculture customer with 160 units

-- Optional: Create a table for payment records (if you want to track payment history separately)
CREATE TABLE IF NOT EXISTS payment (
    paymentid INT AUTO_INCREMENT PRIMARY KEY,
    billid INT,
    amount DECIMAL(10, 2),
    payment_date DATE,
    FOREIGN KEY (billid) REFERENCES bill(billid)
);

-- Insert dummy payment data (only for paid bills)
INSERT INTO payment (billid, amount, payment_date) VALUES
(102, 400.00, '2024-12-02'),   -- Payment for Bill 102 (Jane Smith)
(104, 150.00, '2024-12-01');   -- Payment for Bill 104 (Lisa Thomas)

-- Optional: Table for logging errors or system activity
CREATE TABLE IF NOT EXISTS activity_log (
    logid INT AUTO_INCREMENT PRIMARY KEY,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action_description TEXT
);

-- Insert dummy logs into the activity_log table
INSERT INTO activity_log (action_description) VALUES
('User Sachin logged in successfully'),
('Customer John Doe added to the system'),
('Bill generated for Customer Jane Smith'),
('Bill payment recorded for Customer Lisa Thomas');
