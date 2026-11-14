-- Level 6 – Datenbank, Benutzer und Tabellen für die App
-- Ausführen auf dem Pi:   sudo mysql < flutterdb.sql
-- Ersetzen Sie jedes TODO durch den passenden SQL-Befehl.

DROP DATABASE IF EXISTS flutterDB;
CREATE DATABASE flutterDB CHARACTER SET utf8mb4;
USE flutterDB;

-- Datenbank-Benutzer für PHP und die REST-API (nicht root!)
DROP USER IF EXISTS 'flutterUser'@'localhost';
-- TODO 1: Benutzer 'flutterUser'@'localhost' mit Passwort 'Pa$$w0rd' anlegen

-- TODO 2: flutterUser alle Rechte auf ALLE Tabellen von flutterDB geben (Achtung: .*)

FLUSH PRIVILEGES;

-- Tabelle für den Login der App
CREATE TABLE flutterTB (
  -- TODO 3: id als ganze Zahl, Primärschlüssel, automatisch hochzählend
  name          VARCHAR(20) NOT NULL,
  passwordLogin VARCHAR(20) NOT NULL
);

INSERT INTO flutterTB (name, passwordLogin) VALUES
  ('berno', 'Pa$$w0rd'),
  ('stoll', 'Pa$$w0rd');

-- Tabelle für die ToDo-Liste der App
-- TODO 4: Tabelle ToDoTB anlegen mit
--   id       ganze Zahl, Primärschlüssel, automatisch hochzählend
--   titel    Text bis 100 Zeichen, Pflichtfeld
--   erledigt BOOLEAN, Pflichtfeld, Standardwert FALSE

-- TODO 5: zwei Beispiel-ToDos einfügen: 'Pi einrichten' (erledigt) und 'API testen' (offen)
