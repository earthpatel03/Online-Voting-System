create database voting_system;

use voting_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    has_voted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    votes INT DEFAULT 0
);

INSERT INTO candidates (name) VALUES
('BJP'),
('Congress'),
('AAP'),
('Other');

SELECT * FROM candidates;

ALTER TABLE users ADD COLUMN state VARCHAR(50);

select * from users;

