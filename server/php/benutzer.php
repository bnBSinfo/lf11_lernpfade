<?php
// Level 7 – Eine eigene kleine Schnittstelle zur Datenbank
// Kopieren Sie diese Datei auf den Pi nach /var/www/html/benutzer.php
// Aufruf im Browser:  http://<IP>/benutzer.php
// Ergebnis: JSON-Liste aller Benutzer – nur id und name, NIEMALS das Passwort!

// TODO 1: Dem Browser mitteilen, dass JSON kommt (Content-Type: application/json; charset=utf-8)


// Verbindung zur Datenbank (Zugangsdaten aus Level 6)
// TODO 2: Verbindung mit new mysqli(host, benutzer, passwort, datenbank) öffnen
$db = null;

if ($db === null || $db->connect_errno) {
    http_response_code(500);
    echo json_encode(['fehler' => 'Keine Verbindung zur Datenbank']);
    exit;
}
$db->set_charset('utf8mb4');

// TODO 3: SQL-Abfrage: nur id und name aus flutterTB, sortiert nach id
$ergebnis = $db->query('');

// TODO 4: alle Zeilen als Liste von assoziativen Arrays holen (fetch_all mit MYSQLI_ASSOC)
$benutzer = [];

echo json_encode($benutzer, JSON_UNESCAPED_UNICODE);
