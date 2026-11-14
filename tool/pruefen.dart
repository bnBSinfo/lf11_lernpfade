// Prüft Ihren Raspberry Pi über das Netz – wie ein automatischer Test.
//
//   dart run tool/pruefen.dart       Übersicht über alle Level
//   dart run tool/pruefen.dart 4     Level 4 ausführlich mit Hinweisen
//
// Die IP-Adresse steht in pi.txt.
import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'pi_konfig.dart';

const titel = {
  1: 'Den Pi in Betrieb nehmen',
  2: 'Fernzugriff mit SSH',
  3: 'Der Webserver Apache',
  4: 'PHP auf dem Webserver',
  5: 'MySQL und phpMyAdmin',
  6: 'Datenbank und Tabellen anlegen',
  7: 'Eine eigene PHP-Schnittstelle',
  8: 'Die fertige REST-API',
  9: 'Die REST-API aus Dart nutzen',
};

/// Ergebnis eines Levels: erfüllte Punkte (ok) und Hinweise (rot).
class Ergebnis {
  final ok = <String>[];
  final hinweise = <String>[];
  bool get gruen => hinweise.isEmpty;
  void pruefe(bool bedingung, String erfuellt, String hinweis) =>
      bedingung ? ok.add(erfuellt) : hinweise.add(hinweis);
}

late PiKonfig pi;
const zeitlimit = Duration(seconds: 4);

// ---------------------------------------------------------------- Netzwerk-Helfer
class Antwort {
  Antwort(this.status, this.body, this.typ, this.server);
  final int status;
  final String body;
  final String typ;
  final String server;
}

/// GET-Anfrage. Gibt null zurück, wenn der Server gar nicht antwortet.
Future<Antwort?> holen(String pfad) async {
  final client = HttpClient()..connectionTimeout = zeitlimit;
  try {
    final req = await client.getUrl(Uri.parse('${pi.web}$pfad')).timeout(zeitlimit);
    final res = await req.close().timeout(zeitlimit);
    final body = await res.transform(utf8.decoder).join().timeout(zeitlimit);
    return Antwort(res.statusCode, body, res.headers.contentType?.mimeType ?? '',
        res.headers.value('server') ?? '');
  } catch (_) {
    return null;
  } finally {
    client.close(force: true);
  }
}

/// true = Port offen, false = Pi antwortet, Port zu, null = keine Antwort.
Future<bool?> portOffen(int port) async {
  try {
    final s = await Socket.connect(pi.ip, port, timeout: zeitlimit);
    s.destroy();
    return true;
  } on SocketException catch (e) {
    final code = e.osError?.errorCode;
    final text = '${e.osError?.message} ${e.message}'.toLowerCase();
    if (code == 61 || code == 111 || code == 10061 || text.contains('refused')) return false;
    return null;
  } catch (_) {
    return null;
  }
}

dynamic jsonOderNull(String text) {
  try {
    return jsonDecode(text);
  } catch (_) {
    return null;
  }
}

bool phpNichtAusgefuehrt(Antwort a) => a.body.contains('<?php');

// ---------------------------------------------------------------- Level 1–9
Future<Ergebnis> level1() async {
  final r = Ergebnis();
  r.pruefe(pi.eingetragen, 'IP-Adresse in pi.txt: ${pi.ip}',
      'In pi.txt steht noch keine IP-Adresse. Auf dem Pi im Terminal: hostname -I  '
          '(oder ifconfig) – dann in pi.txt z. B. ip=10.36.13.76 eintragen.');
  if (!r.gruen) return r;
  final erreichbar = await portOffen(pi.ssh) != null || await portOffen(pi.http) != null;
  r.pruefe(erreichbar, 'Der Pi antwortet im Netz',
      'Unter ${pi.ip} antwortet kein Rechner. Prüfen Sie: Pi eingeschaltet? LAN-Kabel im '
          'pädagogischen Netz? IP richtig abgeschrieben? Ihr PC im selben Netz?');
  return r;
}

Future<Ergebnis> level2() async {
  final r = Ergebnis();
  String? banner;
  try {
    final s = await Socket.connect(pi.ip, pi.ssh, timeout: zeitlimit);
    banner = await s.cast<List<int>>().transform(utf8.decoder).first.timeout(zeitlimit);
    s.destroy();
  } catch (_) {}
  r.pruefe(banner != null, 'Port ${pi.ssh} (SSH) ist offen',
      'Auf Port ${pi.ssh} wartet kein SSH-Server. Auf dem Pi: apt install openssh-server  '
          'und danach systemctl enable --now ssh');
  if (banner != null) {
    r.pruefe(banner.startsWith('SSH-2.0'), 'SSH-Server meldet sich: ${banner.trim()}',
        'Auf Port ${pi.ssh} antwortet etwas, aber kein SSH-Server.');
  }
  return r;
}

Future<Ergebnis> level3() async {
  final r = Ergebnis();
  final a = await holen('/');
  r.pruefe(a != null, 'Webserver antwortet auf ${pi.web}/',
      'Auf Port ${pi.http} antwortet kein Webserver. Auf dem Pi: apt install apache2  '
          '– danach im Browser ${pi.web} aufrufen.');
  if (a == null) return r;
  r.pruefe(a.status == 200, 'Startseite wird geliefert (HTTP 200)',
      'Der Webserver antwortet mit HTTP ${a.status} statt 200.');
  r.pruefe(a.server.toLowerCase().contains('apache') || a.body.contains('Apache2'),
      'Es ist Apache', 'Hier läuft ein anderer Webserver (${a.server}) – gefordert ist Apache.');
  return r;
}

Future<Ergebnis> level4() async {
  final r = Ergebnis();
  final a = await holen('/info.php');
  if (a == null) {
    r.hinweise.add('Der Webserver antwortet nicht – erst Level 3 lösen.');
    return r;
  }
  r.pruefe(a.status != 404, 'Datei info.php gefunden',
      '${pi.web}/info.php gibt es nicht (404). Die Datei muss genau info.php heißen und in '
          '/var/www/html liegen:  nano /var/www/html/info.php');
  if (a.status == 404) return r;
  r.pruefe(!phpNichtAusgefuehrt(a), 'PHP wird vom Webserver ausgeführt',
      'Der Browser bekommt den PHP-Quelltext statt der Ausgabe – PHP fehlt im Apache: '
          'apt install php libapache2-mod-php  und  systemctl restart apache2');
  if (phpNichtAusgefuehrt(a)) return r;
  r.pruefe(a.body.contains('PHP Version'), 'phpinfo() zeigt die PHP-Version',
      'info.php liefert keine phpinfo()-Seite. Inhalt der Datei: <?php phpinfo(); ?>');
  r.pruefe(a.body.contains('mysqli'), 'Erweiterung mysqli ist geladen (für die Datenbank)',
      'PHP kann noch nicht mit MySQL sprechen: apt install php-mysql  und  systemctl restart apache2');
  return r;
}

Future<Ergebnis> level5() async {
  final r = Ergebnis();
  final a = await holen('/phpmyadmin/');
  if (a == null) {
    r.hinweise.add('Der Webserver antwortet nicht – erst Level 3 lösen.');
    return r;
  }
  r.pruefe(a.status != 404, '${pi.web}/phpmyadmin/ ist erreichbar',
      'phpMyAdmin ist im Apache nicht eingebunden (404). Haben Sie bei der Installation '
          '„apache2“ mit der Leertaste markiert? Nachholen: dpkg-reconfigure phpmyadmin');
  if (a.status == 404) return r;
  r.pruefe(!phpNichtAusgefuehrt(a), 'PHP läuft', 'PHP läuft nicht – siehe Level 4.');
  r.pruefe(a.status == 200 && a.body.contains('phpMyAdmin'), 'Anmeldeseite von phpMyAdmin erscheint',
      'phpMyAdmin meldet einen Fehler (HTTP ${a.status}). Oft fehlen Pakete: '
          'apt install php-mbstring php-zip php-gd php-json php-curl  und  systemctl restart apache2');
  return r;
}

/// SQL ohne Kommentare, klein geschrieben, in Anweisungen zerlegt.
List<String> sqlAnweisungen(String text) {
  final ohne = text
      .replaceAll(RegExp(r'/\*.*?\*/', dotAll: true), ' ')
      .replaceAll(RegExp(r'--[^\n]*'), ' ')
      .replaceAll(RegExp(r'#[^\n]*'), ' ')
      .toLowerCase()
      .replaceAll(RegExp(r'[`"]'), "'")
      .replaceAll(RegExp(r'\s+'), ' ');
  return ohne.split(';').map((s) => s.trim()).where((s) => s.isNotEmpty).toList();
}

Future<Ergebnis> level6() async {
  final r = Ergebnis();
  final datei = File('server/sql/flutterdb.sql');
  if (!datei.existsSync()) {
    r.hinweise.add('Die Datei server/sql/flutterdb.sql fehlt.');
    return r;
  }
  final s = sqlAnweisungen(datei.readAsStringSync());
  String? finde(Pattern p) => s.cast<String?>().firstWhere((a) => a!.contains(p), orElse: () => null);

  r.pruefe(finde(RegExp(r"create user (if not exists )?'?flutteruser'?@'?localhost'? identified by")) != null,
      'TODO 1: Benutzer flutterUser@localhost mit Passwort',
      "TODO 1: Es fehlt CREATE USER 'flutterUser'@'localhost' IDENTIFIED BY '…';");
  final grant = finde('grant ');
  r.pruefe(grant != null && RegExp(r"on flutterdb\.\* to '?flutteruser'?@'?localhost").hasMatch(grant),
      'TODO 2: Rechte auf flutterDB.*',
      grant != null && grant.contains('on flutterdb to')
          ? 'TODO 2: ON flutterDB gibt Rechte auf eine TABELLE namens flutterDB – richtig ist ON flutterDB.*'
          : "TODO 2: Es fehlt GRANT ALL PRIVILEGES ON flutterDB.* TO 'flutterUser'@'localhost';");

  bool idOk(String? t) =>
      t != null && RegExp(r'\bid int\b[^,]*auto_increment').hasMatch(t) && t.contains('primary key');
  final flutterTB = finde(RegExp(r'create table (if not exists )?flutter_?tb\b'));
  r.pruefe(idOk(flutterTB), 'TODO 3: flutterTB.id ist Primärschlüssel mit AUTO_INCREMENT',
      'TODO 3: In flutterTB fehlt die Spalte  id INT AUTO_INCREMENT PRIMARY KEY  '
          '(ohne Primärschlüssel findet die REST-API in Level 8 keine einzelnen Datensätze).');

  final todo = finde(RegExp(r'create table (if not exists )?todotb\b'));
  r.pruefe(todo != null, 'TODO 4: Tabelle ToDoTB wird angelegt', 'TODO 4: CREATE TABLE ToDoTB fehlt.');
  if (todo != null) {
    r.pruefe(idOk(todo), 'ToDoTB.id ist Primärschlüssel mit AUTO_INCREMENT',
        'TODO 4: ToDoTB braucht  id INT AUTO_INCREMENT PRIMARY KEY');
    r.pruefe(RegExp(r'titel varchar\(100\) not null').hasMatch(todo), 'Spalte titel VARCHAR(100) NOT NULL',
        'TODO 4: Spalte  titel VARCHAR(100) NOT NULL  fehlt oder ist anders geschrieben.');
    r.pruefe(RegExp(r'erledigt (boolean|bool|tinyint\(1\)) not null default (false|0)').hasMatch(todo),
        'Spalte erledigt BOOLEAN NOT NULL DEFAULT FALSE',
        'TODO 4: Spalte  erledigt BOOLEAN NOT NULL DEFAULT FALSE  fehlt oder ist anders geschrieben.');
  }
  final insert = s.where((a) => RegExp(r'^insert (into )?todotb\b').hasMatch(a)).join(' ');
  r.pruefe(insert.contains("'pi einrichten'") && insert.contains("'api testen'"),
      "TODO 5: Beispiel-ToDos 'Pi einrichten' und 'API testen'",
      "TODO 5: INSERT INTO ToDoTB mit 'Pi einrichten' und 'API testen' fehlt.");
  if (r.gruen) {
    r.ok.add('Jetzt auf dem Pi ausführen:  mysql < flutterdb.sql  – ob es geklappt hat, zeigt Level 7.');
  }
  return r;
}

Future<Ergebnis> level7() async {
  final r = Ergebnis();
  final datei = File('server/php/benutzer.php');
  final php = datei.existsSync() ? datei.readAsStringSync() : '';
  final code = php.replaceAll(RegExp(r'//[^\n]*'), '');
  r.pruefe(RegExp(r'header\s*\(\s*.Content-Type:\s*application/json', caseSensitive: false).hasMatch(code),
      'TODO 1: Content-Type application/json',
      "TODO 1: In benutzer.php fehlt  header('Content-Type: application/json; charset=utf-8');");
  r.pruefe(code.contains('new mysqli('), 'TODO 2: Verbindung mit new mysqli(…)',
      "TODO 2: Verbindung fehlt:  \$db = new mysqli('localhost', 'flutterUser', '…', 'flutterDB');");
  final select = RegExp(r'select\s+(.*?)\s+from\s+flutter_?tb', caseSensitive: false).firstMatch(code);
  r.pruefe(select != null && !select.group(1)!.contains('*') && !select.group(1)!.contains('password'),
      'TODO 3: SELECT nur mit id und name',
      'TODO 3: Die Abfrage soll nur id und name lesen – nie SELECT * und nie das Passwort!');
  r.pruefe(code.contains('fetch_all'), 'TODO 4: Zeilen mit fetch_all(MYSQLI_ASSOC) holen',
      'TODO 4: Zeilen holen mit  \$ergebnis->fetch_all(MYSQLI_ASSOC)');
  if (!r.gruen) return r;

  final a = await holen('/benutzer.php');
  if (a == null) {
    r.hinweise.add('Der Webserver antwortet nicht – erst Level 3 lösen.');
    return r;
  }
  r.pruefe(a.status != 404, 'benutzer.php liegt auf dem Pi',
      'Ihre Datei liegt noch nicht auf dem Pi. Vom PC aus:  scp server/php/benutzer.php '
          'administrator@${pi.ip}:/tmp/  und auf dem Pi:  cp /tmp/benutzer.php /var/www/html/');
  if (a.status == 404) return r;
  r.pruefe(!phpNichtAusgefuehrt(a), 'PHP läuft', 'PHP läuft nicht – siehe Level 4.');
  r.pruefe(a.status == 200, 'Antwort ohne Fehler (HTTP 200)',
      'benutzer.php meldet HTTP ${a.status}. Meist stimmen Zugangsdaten oder SQL nicht, oder '
          'flutterdb.sql wurde noch nicht ausgeführt. Fehlermeldung auf dem Pi:  '
          'tail /var/log/apache2/error.log');
  if (a.status != 200) return r;
  r.pruefe(a.typ == 'application/json', 'Content-Type ist application/json',
      'Der Server schickt ${a.typ.isEmpty ? 'keinen Content-Type' : a.typ} – liegt die neue Datei auf dem Pi?');
  final daten = jsonOderNull(a.body);
  r.pruefe(daten is List, 'Antwort ist eine JSON-Liste',
      'Die Antwort ist keine JSON-Liste. Anfang der Antwort: ${a.body.substring(0, a.body.length.clamp(0, 80))}');
  if (daten is! List) return r;
  final namen = daten.whereType<Map>().map((m) => m['name']).toSet();
  r.pruefe(namen.contains('berno') && namen.contains('stoll'), 'Benutzer berno und stoll kommen aus der DB',
      'In der Liste fehlen berno und/oder stoll – wurde flutterdb.sql auf dem Pi ausgeführt?');
  r.pruefe(daten.whereType<Map>().every((m) => m.containsKey('id')), 'Jeder Eintrag hat eine id',
      'Den Einträgen fehlt die id.');
  r.pruefe(daten.whereType<Map>().every((m) => !m.containsKey('passwordLogin')),
      'Kein Passwort in der Antwort', 'Die Antwort enthält passwordLogin – Passwörter gehören nie in eine API-Antwort!');
  return r;
}

const api = '/php-crud-api/api.php/records';
const apiDownload = 'https://bnbsinfo.github.io/rest_lernpfad_schueler/downloads/api.php';

Future<Ergebnis> level8() async {
  final r = Ergebnis();
  final a = await holen('$api/flutterTB');
  if (a == null) {
    r.hinweise.add('Der Webserver antwortet nicht – erst Level 3 lösen.');
    return r;
  }
  r.pruefe(a.status != 404 || a.typ == 'application/json', 'php-crud-api ist installiert',
      'Unter ${pi.web}/php-crud-api/api.php gibt es nichts. Auf dem Pi:  mkdir -p /var/www/html/php-crud-api  '
          'und dort  wget $apiDownload');
  if (a.status == 404 && a.typ != 'application/json') return r;
  final daten = jsonOderNull(a.body);
  final fehler = daten is Map && daten.containsKey('code') ? ' (API meldet: ${daten['message']})' : '';
  r.pruefe(a.status == 200 && daten is Map && daten['records'] is List,
      'GET records/flutterTB liefert {"records": [...]}',
      'GET records/flutterTB klappt nicht – HTTP ${a.status}$fehler. Stehen in api.php unten bei '
          "\$config die richtigen Werte für username, password und database?");
  if (!r.gruen) return r;
  final namen = (daten['records'] as List).whereType<Map>().map((m) => m['name']).toSet();
  r.pruefe(namen.contains('berno'), 'Datensätze aus flutterTB sind sichtbar', 'flutterTB ist leer – Level 6 auf dem Pi ausführen.');

  final eins = await holen('$api/flutterTB/1');
  final e1 = eins == null ? null : jsonOderNull(eins.body);
  r.pruefe(eins?.status == 200 && e1 is Map && e1['id'] == 1, 'GET records/flutterTB/1 liefert genau einen Datensatz',
      'GET records/flutterTB/1 klappt nicht – hat flutterTB einen Primärschlüssel id (Level 6, TODO 3)?');

  final t = await holen('$api/ToDoTB');
  final td = t == null ? null : jsonOderNull(t.body);
  r.pruefe(t?.status == 200 && td is Map && td['records'] is List, 'GET records/ToDoTB funktioniert',
      'Die Tabelle ToDoTB ist über die API nicht erreichbar – Level 6 (TODO 4) auf dem Pi ausgeführt?');
  return r;
}

Future<Ergebnis> level9() async {
  final r = Ergebnis();
  final lauf = await Process.run(Platform.resolvedExecutable, ['run', 'tool/level9_lauf.dart'],
      stdoutEncoding: utf8, stderrEncoding: utf8, runInShell: Platform.isWindows);
  final zeilen = '${lauf.stdout}'.split('\n');
  for (final z in zeilen) {
    if (z.startsWith('OK: ')) r.ok.add(z.substring(4));
    if (z.startsWith('HINWEIS: ')) r.hinweise.add(z.substring(9));
  }
  if (lauf.exitCode != 0 && r.hinweise.isEmpty) {
    final fehler = '${lauf.stderr}${lauf.stdout}'
        .split('\n')
        .where((z) => z.contains('Error') || z.contains('error'))
        .take(3)
        .join('\n    ');
    r.hinweise.add('lib/todo_api.dart lässt sich nicht übersetzen:\n    $fehler');
  }
  return r;
}

final level = <int, Future<Ergebnis> Function()>{
  1: level1, 2: level2, 3: level3, 4: level4, 5: level5,
  6: level6, 7: level7, 8: level8, 9: level9,
};

// ---------------------------------------------------------------- Ausgabe
Future<void> main(List<String> args) async {
  pi = PiKonfig.lesen();
  final version = RegExp(r'^version:\s*([\d.]+)', multiLine: true)
          .firstMatch(File('pubspec.yaml').readAsStringSync())
          ?.group(1) ??
      '?';
  stdout.writeln('Pi-Server & REST-API LF11 · Version $version · Pi: ${pi.eingetragen ? pi.web : '–'}\n');

  final nr = args.isEmpty ? null : int.tryParse(args.first);
  if (nr != null && level.containsKey(nr)) {
    final r = await level[nr]!();
    stdout.writeln('Level $nr – ${titel[nr]}');
    for (final t in r.ok) {
      stdout.writeln('  ✓ $t');
    }
    for (final t in r.hinweise) {
      stdout.writeln('  ✗ Hinweis: $t');
    }
    stdout.writeln(r.gruen ? '\n✅ Level $nr geschafft!' : '\n❌ Noch nicht geschafft.');
    exitCode = r.gruen ? 0 : 1;
    return;
  }

  // Übersicht: ohne erreichbaren Pi werden die Netzwerk-Level übersprungen.
  final l1 = await level1();
  var geschafft = 0;
  for (final n in level.keys) {
    final offline = !l1.gruen && n != 1 && n != 6;
    final r = n == 1 ? l1 : (offline ? null : await level[n]!());
    if (r?.gruen ?? false) geschafft++;
    final zeichen = r == null ? '⏸️ ' : (r.gruen ? '✅' : '❌');
    final rest = r == null
        ? '  (Pi nicht erreichbar)'
        : (r.gruen ? '' : '  → ${r.hinweise.first.split('\n').first}');
    stdout.writeln('$zeichen Level $n  ${titel[n]!.padRight(32)}$rest');
  }
  stdout.writeln('\n$geschafft / ${level.length} Level geschafft. Details: dart run tool/pruefen.dart <Level>');
}
