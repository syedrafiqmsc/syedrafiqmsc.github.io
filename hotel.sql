
CREATE DATABASE IF NOT EXISTS hotel;
USE hotel;

CREATE TABLE IF NOT EXISTS Customer (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerName VARCHAR(50) NOT NULL,
    Phone VARCHAR(15),
    Address VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Room (
    RoomNo INT PRIMARY KEY,
    RoomType VARCHAR(20),
    Price DECIMAL(10,2),
    Status VARCHAR(20) DEFAULT 'Available'
);

CREATE TABLE IF NOT EXISTS Booking (
    BookingID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    RoomNo INT,
    CheckIn DATE,
    CheckOut DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (RoomNo) REFERENCES Room(RoomNo)
);

CREATE TABLE IF NOT EXISTS Billing (
    BillID INT PRIMARY KEY AUTO_INCREMENT,
    BookingID INT,
    TotalAmount DECIMAL(10,2),
    PaymentMode VARCHAR(20),
    PaymentStatus VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID)
);

INSERT INTO Customer (CustomerName, Phone, Address)
VALUES
('Rahul Sharma', '9876543210', 'Hyderabad'),
('Priya Reddy', '9876501234', 'Vijayawada');

INSERT INTO Room (RoomNo, RoomType, Price, Status)
VALUES
(101, 'Single', 1000.00, 'Available'),
(102, 'Double', 1800.00, 'Available'),
(103, 'Deluxe', 2500.00, 'Available');

SHOW TABLES;
SELECT * FROM Customer;
SELECT * FROM Room;
SELECT * FROM Booking;
SELECT * FROM Billing;
