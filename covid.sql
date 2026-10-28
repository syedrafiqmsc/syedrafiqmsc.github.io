-- COVID-19 DATA ANALYSIS SYSTEM
-- CBSE Class XII Informatics Practices (065)
-- Database name: covid | Table name: covid
-- Sample values are illustrative, not verified historical statistics.

CREATE DATABASE IF NOT EXISTS covid;
USE covid;

CREATE TABLE IF NOT EXISTS covid (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    report_date DATE NOT NULL,
    location VARCHAR(50) NOT NULL,
    confirmed INT NOT NULL,
    recovered INT NOT NULL,
    deaths INT NOT NULL
);

-- Sample data: do not run this INSERT block again if these rows already exist.
INSERT INTO covid (report_date, location, confirmed, recovered, deaths)
VALUES
('2021-05-01', 'Andhra Pradesh', 100000, 90000, 1000),
('2021-05-02', 'Andhra Pradesh', 105000, 94000, 1050),
('2021-05-03', 'Andhra Pradesh', 110000, 98000, 1100),
('2021-05-01', 'Telangana', 80000, 70000, 800),
('2021-05-02', 'Telangana', 85000, 75000, 850);

-- DQL: Display all records
SELECT * FROM covid;

-- DQL: Search by location
SELECT * FROM covid WHERE location = 'Andhra Pradesh';

-- DQL: Sort by confirmed cases
SELECT * FROM covid ORDER BY confirmed DESC;

-- DQL: Calculate active cases
SELECT report_date, location, confirmed, recovered, deaths,
       confirmed - recovered - deaths AS active_cases
FROM covid
ORDER BY location, report_date;

-- DQL: Latest record for each location
SELECT c.report_date, c.location, c.confirmed, c.recovered, c.deaths
FROM covid AS c
JOIN (
    SELECT location, MAX(report_date) AS latest_date
    FROM covid
    GROUP BY location
) AS latest
ON c.location = latest.location
AND c.report_date = latest.latest_date
ORDER BY c.location;

-- DDL: View table structure
DESCRIBE covid;

-- Optional DDL demonstration; run only once:
-- ALTER TABLE covid ADD COLUMN testing INT DEFAULT 0;

-- Optional DML demonstrations; uncomment and run individually:
-- UPDATE covid SET recovered = 91000 WHERE record_id = 1;
-- DELETE FROM covid WHERE record_id = 1;

-- WARNING: TRUNCATE deletes all records. Keep commented unless intentional.
-- TRUNCATE TABLE covid;
