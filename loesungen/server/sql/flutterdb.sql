-- Level 6 – Musterlösung
-- Ausführen auf dem Pi:   sudo mysql < flutterdb.sql

DROP DATABASE IF EXISTS flutterDB;
CREATE DATABASE flutterDB CHARACTER SET utf8mb4;
USE flutterDB;

DROP USER IF EXISTS 'flutterUser'@'localhost';
CREATE USER 'flutterUser'@'localhost' IDENTIFIED BY 'Pa$$w0rd';
GRANT ALL PRIVILEGES ON flutterDB.* TO 'flutterUser'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE flutterTB (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(20) NOT NULL,
  passwordLogin VARCHAR(20) NOT NULL
);

INSERT INTO flutterTB (name, passwordLogin) VALUES
  ('berno', 'Pa$$w0rd'),
  ('stoll', 'Pa$$w0rd');

CREATE TABLE ToDoTB (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  name     VARCHAR(100) NOT NULL,
  checkbox BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO ToDoTB (name, checkbox) VALUES
  ('Pi einrichten', TRUE),
  ('API testen', FALSE);
