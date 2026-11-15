<?php
// Level 7 – Musterlösung
header('Content-Type: application/json; charset=utf-8');

$db = new mysqli('localhost', 'flutterUser', 'Pa$$w0rd', 'flutterDB');

if ($db === null || $db->connect_errno) {
    http_response_code(500);
    echo json_encode(['fehler' => 'Keine Verbindung zur Datenbank']);
    exit;
}
$db->set_charset('utf8mb4');

$ergebnis = $db->query('SELECT id, name FROM flutterTB ORDER BY id');

$benutzer = $ergebnis->fetch_all(MYSQLI_ASSOC);

echo json_encode($benutzer, JSON_UNESCAPED_UNICODE);
