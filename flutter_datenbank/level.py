# Level 1–6 der Datenbankanbindung – je Level: Zielbild, begleiteter Auftrag mit Code-Rahmen, Profi-Auftrag,
# Tipps, Hintergrund und Selbstkontrolle, jeweils in Standardsprache (S) und „Sprache einfach“ (E).
# Code-Rahmen: P = neu (grün), M = löschen (rot), R = steht schon da (grau), LUECKE = unveränderter Code dazwischen.
L = []

def teil(code, nach):
    """Text vor (nach=False) bzw. ab (nach=True) der Zeile 'void openList'."""
    i = code.index('void openList')
    return code[i:] if nach else code[:i].rstrip('\n')

ALT_METHODEN = """void addItem(String item) {
  setState(() {
    todos[item] = false;
  });
  Navigator.of(context).pop();
}

void deleteItem(String key) {
  setState(() {
    todos.remove(key);
  });
}

void checkBoxDone(String key) {
  setState(() {
    todos.update(key, (bool done) => !done);
  });
}"""

ALT_BUILDER_INNEN = """var key = todos.keys.elementAt(i);
return ToDoItem(
  key, // Titel
  todos.values.elementAt(i), // Checkboxstatus
  () => deleteItem(key), // Löschfunktion
  () => checkBoxDone(key), // Checkboxfunktion
);"""
NEU_BUILDER_INNEN = '\n'.join(BUILDER.split('\n')[3:-2])
BTN_ALT_INNEN = '\n'.join(BTN_ALT.split('\n')[3:6])
BTN_B_INNEN = '\n'.join(BTN_B.split('\n')[3:6])
BTN_C_INNEN = '\n'.join(BTN_C.split('\n')[3:11])
BTN_KOPF = R("TextButton(\n  onPressed: _canLogin\n      ? () {", 12)
BTN_FUSS = R("        }\n      : null,\n  child: const Text('Login'),\n),", 12)
LOGIN_KOPF = R("class _MyLoginState extends State<MyLogin> {\n  String _username = '';\n  String _password = '';\n  bool _canLogin = false;")

INFO_LINT = tipp('Blaue Hinweise der IDE zu <code>webRequest.dart</code> oder <code>data_L</code>?',
  'Dart empfiehlt Dateinamen wie <code>web_request.dart</code> und Namen ohne Unterstrich. '
  'Wir behalten die Namen aus dem Skript, damit Skript und Lernpfad übereinstimmen – es sind nur Hinweise, keine Fehler.')
INFO_LINT_E = tipp('Blaue Hinweise zu <code>webRequest.dart</code> oder <code>data_L</code>?',
  'Das sind nur Hinweise. Es sind keine Fehler. Wir nehmen die Namen aus dem Skript.')

# ======================================================================= LEVEL 1  (Skript a + Anfang b)
D1_MANIFEST = D(R('<manifest xmlns:android="http://schemas.android.com/apk/res/android">'),
                P('<uses-permission android:name="android.permission.INTERNET"/>', 4),
                R('<application\n    android:label="meine_app"', 4),
                P('android:usesCleartextTraffic="true"', 8),
                R('...>', 8))
D1_WEB = P(web(1))
D1_LOGIN = D(R("import 'package:flutter/material.dart';\n\nimport 'todo_list.dart';"), P("import 'webRequest.dart';"), LUECKE,
             LOGIN_KOPF, P(''), P(TEST_L1, 2), R('\n  void _checkCanLogin() {'))
L.append(level(1, 'http einbinden und erster Abruf', 'webRequest.dart – ein Datensatz aus flutterTB kommt in der Konsole an',
 ziel=ziel(figur('browser_adresse', 'Firefox-Adresszeile mit …/php-crud-api/api.php/records/flutterTB/1', 'Erst im Browser testen (eigene IP einsetzen)'),
           figur('json_einzeln', 'JSON-Ansicht: id 1, name, passwordLogin', 'So sieht die Map aus, die loadContactData() liefert')) +
      baumkarte('Dateien im Projekt', dateien([('main.dart', '', False), ('my_first_app.dart', '', False), ('my_login.dart', 'Test in initState', True), ('webRequest.dart', 'ip, loadContactData()', True), ('todo_list.dart', '', False), ('todo_item.dart', '', False)])),
 grafik='<h3>Was passiert beim Start?</h3>\n' + kette([('initState()', 'MyLogin startet'), ('loadContactData()', 'Future wird gestartet'), ('http.get', 'GET …/flutterTB/1'), ('await', 'warten auf JSON'), ('jsonDecode', 'JSON → Map'), ('print', 'Ausgabe in der Konsole')]),
 weiter=('level-2', 'Level 2'),
 S=dict(
  ziel='Ihre App holt zum ersten Mal Daten vom Raspberry Pi: den ersten Benutzer der Tabelle <code>flutterTB</code>. Noch ändert sich auf dem Bildschirm nichts – das Ergebnis erscheint in der Konsole.',
  aendern='<code>pubspec.yaml</code>, <code>AndroidManifest.xml</code>, neu: <code>lib/webRequest.dart</code>, <code>lib/my_login.dart</code>',
  skript='a – Einbinden der http-Erweiterung, b – Passwort aus der Datenbank auslesen (erster Teil)',
  schritte=[
   ('browser', 'Testen Sie beide Adressen aus dem Skript – mit der IP <b>Ihres</b> Pi: <code>http://IP/php-crud-api/api.php/records/flutterTB/1</code> und <code>…/records/flutterTB/</code>. Beide zeigen JSON.', None),
   ('terminal', 'Öffnen Sie <code>meine_app</code> und tippen Sie im Terminal <code>flutter pub add http</code>. Danach steht <code>http</code> in der <code>pubspec.yaml</code> unter <code>dependencies</code>.', None),
   ('aendern', '<code>android/app/src/main/AndroidManifest.xml</code>: Internet und unverschlüsseltes HTTP erlauben. Das steht nicht im Skript, Android braucht es aber.', D1_MANIFEST),
   ('neu', '<code>lib/webRequest.dart</code> – hier sammeln Sie alle Zugriffe auf die Datenbank. Setzen Sie bei <code>ip</code> die IP Ihres Pi ein.', D1_WEB),
   ('aendern', '<code>lib/my_login.dart</code>: <code>webRequest.dart</code> importieren und zum Test in <code>initState()</code> das Ergebnis mit <code>print</code> ausgeben.', D1_LOGIN),
   ('test', 'App <b>neu starten</b> (kein Hot Reload – <code>initState</code> läuft nur beim Start) und die Konsole (Run/Debug) lesen: Dort steht der erste Benutzer.', None)],
  profi=['Das Paket <code>http</code> ist eingebunden, Android erlaubt Internet und <code>http://</code>-Adressen.',
         '<code>lib/webRequest.dart</code> enthält die IP des Pi als Konstante <code>ip</code> – sie steht nur an dieser einen Stelle.',
         '<code>Future&lt;Map&gt; loadContactData()</code> holt <code>…/records/flutterTB/1</code> und liefert den Datensatz als Map.',
         'Beim Start von <code>MyLogin</code> erscheinen Datensatz und Passwort in der Konsole.'],
  tipps=[tipp('„Cleartext HTTP traffic … not permitted“?', 'Es fehlt <code>android:usesCleartextTraffic="true"</code> im <code>&lt;application&gt;</code>-Tag. Danach die App komplett neu starten.'),
         tipp('„SocketException“ oder „Connection refused“?', 'IP falsch, Pi aus oder nicht im selben Netz. Testen Sie dieselbe Adresse zuerst im Browser.'),
         tipp('Fehlermeldung zum Primärschlüssel bei flutterTB/1?', 'Die REST-API findet einen Datensatz nur über den Primärschlüssel: <code>ALTER TABLE flutterTB ADD PRIMARY KEY (id);</code>'),
         INFO_LINT],
  erklaert='<p><strong>Die Adresse der REST-API</strong> besteht aus vier Teilen (Skript, Abbildung zur URL):</p>\n'
   + tabelle(['Teil', 'Beispiel'], [['ServerAdresse/IP', '<code>http://192.168.0.10</code>'], ['Ordner-API', '<code>/php-crud-api/api.php/records</code>'], ['DB-Tabelle', '<code>/flutterTB</code>'], ['Datensatz (ID/PK)', '<code>/1</code> – ohne: alle Datensätze']]) +
   '\n<p><strong>Ein Paket für HTTP.</strong> Flutter selbst kann keine Webanfragen – das übernimmt das Paket <code>http</code>. Alle Zugriffe auf die Datenbank sammeln Sie in <code>webRequest.dart</code>. So kennt die Oberfläche weder Adressen noch JSON.</p>\n'
   '<p><strong>Android braucht eine Erlaubnis</strong> für Anfragen ins Netz – und gesondert für unverschlüsselte <code>http://</code>-Adressen.</p>\n'
   '<p>Die Daten kommen <b>zeitverzögert</b> an. Deshalb ist <code>loadContactData()</code> <code>async</code> und gibt ein <code>Future</code> zurück:</p>\n'
   + tabelle(['Baustein', 'Bedeutung'], [
     ['<code>Future&lt;Map&gt;</code>', 'die Map kommt <b>später</b> – wie eine Abholnummer'],
     ['<code>await http.get(url)</code>', 'wartet, bis der Server geantwortet hat – die App bleibt bedienbar'],
     ['<code>jsonDecode</code>', 'wandelt den JSON-Text in eine Dart-<code>Map</code> um'],
     ['<code>.then((data) {…})</code>', 'im Test: „wenn die Map da ist, dann …“']]) +
   '\n<p><strong>Die IP steht nur einmal oben</strong> (<code>$ip</code> in der Adresse). Im Skript steht sie in jeder Adresse – so müssen Sie sie nur an einer Stelle ändern.</p>\n'
   '<p><strong>Merke:</strong> Daten aus dem Netz kommen verzögert. <code>async</code>/<code>await</code> wartet darauf, <code>jsonDecode</code> macht aus JSON eine Map.</p>\n'
   '<p><strong>Denkfrage:</strong> Was würde passieren, wenn die App bei jeder Anfrage „einfrieren“ müsste, bis der Pi antwortet?</p>'),
 E=dict(
  ziel='Deine App holt zum ersten Mal Daten vom Raspberry Pi. Sie holt den ersten Benutzer aus der Tabelle <code>flutterTB</code>. Auf dem Bildschirm ändert sich noch nichts. Das Ergebnis steht in der Konsole.',
  aendern='<code>pubspec.yaml</code>, <code>AndroidManifest.xml</code>, neu: <code>lib/webRequest.dart</code>, <code>lib/my_login.dart</code>',
  skript='a und Anfang von b',
  schritte=[
   ('browser', 'Teste zuerst im Browser. Nimm die IP von <b>deinem</b> Pi. Öffne <code>http://IP/php-crud-api/api.php/records/flutterTB/1</code>. Öffne dann <code>…/records/flutterTB/</code>. Beide Male siehst du JSON.', None),
   ('terminal', 'Öffne dein Projekt <code>meine_app</code>. Tippe im Terminal: <code>flutter pub add http</code>.', None),
   ('aendern', 'Öffne <code>android/app/src/main/AndroidManifest.xml</code>. Tippe die 2 grünen Zeilen ein. Dann darf die App ins Netz.', D1_MANIFEST),
   ('neu', 'Lege die Datei <code>lib/webRequest.dart</code> an. Tippe den Code ab. Schreib bei <code>ip</code> die IP von deinem Pi.', D1_WEB),
   ('aendern', 'Öffne <code>lib/my_login.dart</code>. Tippe die grünen Zeilen ein.', D1_LOGIN),
   ('test', 'Starte die App ganz neu. Hot Reload reicht hier nicht. Schau dann in die Konsole. Dort steht der erste Benutzer.', None)],
  profi=['Das Paket <code>http</code> ist da. Android erlaubt Internet und <code>http://</code>.',
         'In <code>lib/webRequest.dart</code> steht die IP 1-mal als <code>ip</code>.',
         '<code>loadContactData()</code> holt <code>…/flutterTB/1</code>. Sie gibt eine Map zurück.',
         'Beim Start steht der Benutzer in der Konsole.'],
  tipps=[tipp('Fehler „Cleartext HTTP traffic … not permitted“?', 'Im Manifest fehlt <code>android:usesCleartextTraffic="true"</code>. Starte danach die App ganz neu.'),
         tipp('Fehler „SocketException“ oder „Connection refused“?', 'Die App findet den Pi nicht. Ist die IP richtig? Ist der Pi an? Teste die Adresse zuerst im Browser.'),
         tipp('Fehler zum Primärschlüssel?', 'Die Tabelle braucht einen Primärschlüssel. Tippe auf dem Pi: <code>ALTER TABLE flutterTB ADD PRIMARY KEY (id);</code>'),
         INFO_LINT_E],
  erklaert='<p><strong>Die Adresse hat 4 Teile:</strong></p>\n'
   + tabelle(['Teil', 'Beispiel'], [['IP vom Pi', '<code>http://192.168.0.10</code>'], ['Ordner der API', '<code>/php-crud-api/api.php/records</code>'], ['Tabelle', '<code>/flutterTB</code>'], ['Datensatz', '<code>/1</code>. Ohne Zahl kommen alle.']]) +
   '\n<p><strong>Das Paket http</strong> schickt Anfragen ins Netz. Flutter kann das nicht allein.</p>\n'
   '<p><strong>Die Daten brauchen Zeit.</strong> Darum steht <code>async</code> an der Methode. <code>await</code> heißt: Warte auf die Antwort. Die App läuft dabei weiter.</p>\n'
   '<p><code>jsonDecode</code> macht aus dem JSON eine Map.</p>\n'
   '<p><strong>Merke:</strong> Daten aus dem Netz kommen später. <code>await</code> wartet. <code>jsonDecode</code> macht eine Map daraus.</p>\n'
   '<p><strong>Denkfrage:</strong> Was wäre, wenn die App bei jeder Anfrage stehen bleibt?</p>'),
 sk={"check": ['Der Browser zeigt mir `…/flutterTB/1` und `…/flutterTB/` als JSON.', 'Das Paket `http` ist eingebunden, `webRequest.dart` ist angelegt.', 'Beim Start der App erscheint der erste Benutzer in der Konsole.'],
     "fragen": [('Was liefert `…/records/flutterTB/` ohne Zahl am Ende?',
       [('Alle Datensätze der Tabelle – als Liste unter dem Schlüssel `records`.', True, 'Mit /1 kommt nur der Datensatz mit der id 1.'),
        ('Nur den ersten Datensatz.', False, 'Dafür bräuchten Sie …/flutterTB/1.'),
        ('Eine Fehlermeldung.', False, 'Die id ist optional.')]),
      ('Warum ist `loadContactData()` `async`?',
       [('Die Daten kommen verzögert über das Netz – await wartet, ohne die App zu blockieren.', True, 'Deshalb liefert die Methode ein Future.'),
        ('Damit die Datenbank schneller antwortet.', False, 'async ändert nichts an der Geschwindigkeit.'),
        ('Weil jsonDecode sonst nicht funktioniert.', False, 'jsonDecode arbeitet sofort – gewartet wird auf http.get.')])]},
 ske={"check": ['Im Browser sehe ich `…/flutterTB/1` und `…/flutterTB/` als JSON.', 'Das Paket `http` ist da. Die Datei `webRequest.dart` ist da.', 'Beim Start steht der erste Benutzer in der Konsole.'],
      "fragen": [('Was kommt bei `…/records/flutterTB/` ohne Zahl?',
       [('Alle Datensätze. Sie stehen als Liste unter `records`.', 'Mit /1 kommt nur der Datensatz mit der id 1.'),
        ('Nur der erste Datensatz.', 'Dafür brauchst du …/flutterTB/1.'),
        ('Ein Fehler.', 'Die Zahl am Ende darf fehlen.')]),
       ('Warum ist `loadContactData()` `async`?',
       [('Die Daten brauchen Zeit. `await` wartet. Die App läuft weiter.', 'Darum gibt die Methode ein Future zurück.'),
        ('Dann antwortet die Datenbank schneller.', 'async macht nichts schneller.'),
        ('Sonst geht `jsonDecode` nicht.', 'jsonDecode geht sofort. Gewartet wird auf http.get.')])]},
 woerter=['Paket', 'REST-API', 'JSON', 'Map', 'async', 'await', 'Future', 'jsonDecode', 'Konsole', 'initState', 'Hot Reload']))

# ======================================================================= LEVEL 2  (Skript b)
D2_LOGIN = D(LOGIN_KOPF, R(''), M(TEST_L1, 2), P(LOGIN_B, 2), R('\n  void _checkCanLogin() {'))
D2_BTN = D(BTN_KOPF, M(BTN_ALT_INNEN, 12), P(BTN_B_INNEN, 12), BTN_FUSS)
L.append(level(2, 'Passwort aus der Datenbank verwenden', 'loadDataFromDB() und passwordLog – erster Vergleich',
 ziel=ziel(figur('login', 'Handy mit Login-Maske: Willkommen, Benutzername, Passwort, Login', 'Login-Maske – Passwort kommt aus flutterTB', breit=False)) +
      baumkarte('Widget-Baum', baum(('MyLogin', 'Stateful · passwordLog', True, [('Column', '', False, [('TextField', 'Benutzername', False, None), ('TextField', 'Passwort', False, None), ('TextButton', '_password == passwordLog → openList()', True, None)])]))),
 grafik='<h3>Vom Datensatz zum Vergleich</h3>\n' + kette([('initState()', 'einmal beim Start'), ('loadDataFromDB()', 'await loadContactData()'), ('setState', 'passwordLog = data["passwordLogin"]'), ('Login-Button', '_password == passwordLog?'), ('openList()', 'ToDo-Liste öffnen')]),
 weiter=('level-3', 'Level 3'),
 S=dict(
  ziel='Statt eines festen Passworts im Code vergleicht die Login-Maske jetzt mit dem Passwort aus der Datenbank (erster Datensatz von <code>flutterTB</code>).',
  aendern='<code>lib/my_login.dart</code>', skript='b – Passwort aus der Datenbank auslesen und verwenden',
  schritte=[
   ('aendern', '<code>lib/my_login.dart</code>: Der Test aus Level 1 fliegt raus. Dafür kommen die Variable <code>passwordLog</code>, ein neues <code>initState()</code> und die Methoden <code>loadDataFromDB()</code> und <code>openList()</code>.', D2_LOGIN),
   ('aendern', 'Im <code>build</code> der Login-Button: Die Navigation steht jetzt in <code>openList()</code>. Der Button ruft sie nur auf, wenn das Passwort passt.', D2_BTN),
   ('test', 'App neu starten. Testen Sie mit dem Passwort aus Datensatz 1 – und mit einem falschen.', None)],
  profi=['Kein Passwort steht mehr im Code: Beim Start lädt die Login-Maske einmal das Passwort aus Datensatz 1 von <code>flutterTB</code> in die Variable <code>passwordLog</code>.',
         'Die Navigation zur ToDo-Liste steckt in einer eigenen Methode <code>openList()</code>.',
         'Login öffnet die Liste nur, wenn das eingegebene Passwort gleich <code>passwordLog</code> ist.'],
  tipps=[tipp('Der Login klappt nie?', 'Kommt das Passwort an? Fügen Sie in <code>loadDataFromDB</code> kurz <code>print(passwordLog);</code> ein. Groß-/Kleinschreibung beachten.'),
         tipp('Der Login klappt direkt nach dem Start nicht, kurz danach schon?', 'Die Daten kommen verzögert. Solange <code>passwordLog</code> noch leer ist, passt kein Passwort.')],
  erklaert='<p>Aus der übergebenen Map wird das Passwort ausgelesen und einer Variablen zugewiesen. Gegen diese Variable prüft der Login.</p>\n'
   '<ul><li><code>data[\'passwordLogin\']</code> greift auf den Wert zum Schlüssel <code>passwordLogin</code> der Map zu.</li>'
   '<li><code>setState</code> sorgt dafür, dass der neue Wert im State ankommt.</li>'
   '<li><code>openList()</code> kapselt die Navigation – so bleibt der Button übersichtlich.</li></ul>\n'
   '<p><strong>Kritisch betrachtet:</strong> Es wird nur gegen <b>ein</b> Passwort (Datensatz 1) geprüft, der Benutzername spielt keine Rolle. Das ändern Sie in Level 3.</p>\n'
   '<p><strong>Merke:</strong> Daten laden (<code>loadDataFromDB</code>), im State ablegen (<code>setState</code>), dann vergleichen.</p>\n'
   '<p><strong>Denkfrage:</strong> Sie ändern das Passwort in phpMyAdmin. Was müssen Sie tun, damit die App das neue Passwort kennt?</p>'),
 E=dict(
  ziel='Bisher stand kein echtes Passwort im Spiel. Jetzt prüft die Login-Maske das Passwort aus der Datenbank. Sie nimmt den ersten Datensatz aus <code>flutterTB</code>.',
  aendern='<code>lib/my_login.dart</code>', skript='b',
  schritte=[
   ('aendern', 'Öffne <code>lib/my_login.dart</code>. Lösche die roten Zeilen. Das ist der Test aus Level 1. Tippe dann die grünen Zeilen ein.', D2_LOGIN),
   ('aendern', 'Geh zum Login-Button im <code>build</code>. Lösche die roten Zeilen. Tippe die grünen Zeilen ein.', D2_BTN),
   ('test', 'Starte die App neu. Teste mit dem Passwort aus Datensatz 1. Teste dann mit einem falschen Passwort.', None)],
  profi=['Im Code steht kein Passwort. Beim Start lädt die App das Passwort aus Datensatz 1 in <code>passwordLog</code>.',
         'Die Methode <code>openList()</code> öffnet die ToDo-Liste.',
         'Login öffnet die Liste nur mit dem richtigen Passwort.'],
  tipps=[tipp('Der Login geht nie?', 'Kommt das Passwort an? Schreib in <code>loadDataFromDB</code> kurz <code>print(passwordLog);</code>. Achte auf große und kleine Buchstaben.'),
         tipp('Direkt nach dem Start geht der Login nicht, kurz danach schon?', 'Die Daten brauchen etwas Zeit. Am Anfang ist <code>passwordLog</code> noch leer.')],
  erklaert='<p>Die App holt die Map aus der Datenbank. Sie nimmt daraus das Passwort. Sie legt es in <code>passwordLog</code> ab.</p>\n'
   '<ul><li><code>data[\'passwordLogin\']</code> holt den Wert mit dem Namen <code>passwordLogin</code> aus der Map.</li>'
   '<li><code>setState</code> legt den neuen Wert im State ab.</li>'
   '<li><code>openList()</code> öffnet die Liste. So bleibt der Button kurz.</li></ul>\n'
   '<p><strong>Aber:</strong> Die App prüft nur 1 Passwort. Der Name ist egal. Das änderst du in Level 3.</p>\n'
   '<p><strong>Merke:</strong> Erst Daten laden. Dann im State ablegen. Dann vergleichen.</p>\n'
   '<p><strong>Denkfrage:</strong> Du änderst das Passwort in phpMyAdmin. Was musst du tun, damit die App es kennt?</p>'),
 sk={"check": ['Mit dem Passwort aus Datensatz 1 öffnet sich die ToDo-Liste.', 'Mit einem falschen Passwort passiert nichts.', 'Im Code steht kein Passwort mehr fest.'],
     "fragen": [('Wo wird `loadDataFromDB()` aufgerufen?',
       [('Einmal in `initState()`, beim Start der Login-Maske.', True, 'So liegen die Daten bereit, bevor jemand auf Login tippt.'),
        ('Bei jedem Tastendruck im Passwortfeld.', False, 'Das wäre bei jedem Zeichen eine neue Anfrage an den Pi.'),
        ('Gar nicht – das macht Flutter automatisch.', False, 'Die Methode muss aufgerufen werden.')]),
      ('Was ist die Schwäche dieser Lösung?',
       [('Geprüft wird nur das Passwort des ersten Datensatzes – der Name spielt keine Rolle.', True, 'Darum laden Sie in Level 3 alle Benutzer.'),
        ('Das Passwort steht im Code.', False, 'Gerade das ist jetzt nicht mehr so.'),
        ('Die App kann keine Daten laden.', False, 'Laden funktioniert – nur der Vergleich ist zu einfach.')])]},
 ske={"check": ['Mit dem Passwort aus Datensatz 1 geht die ToDo-Liste auf.', 'Mit einem falschen Passwort passiert nichts.', 'Im Code steht kein Passwort mehr.'],
      "fragen": [('Wo rufst du `loadDataFromDB()` auf?',
       [('1-mal in `initState()`. Also beim Start der Login-Maske.', 'So sind die Daten da, bevor jemand auf Login tippt.'),
        ('Bei jeder Taste im Passwort-Feld.', 'Dann ginge bei jedem Zeichen eine Anfrage an den Pi.'),
        ('Gar nicht. Flutter macht das allein.', 'Du musst die Methode aufrufen.')]),
       ('Was ist hier noch schlecht?',
       [('Die App prüft nur das Passwort aus Datensatz 1. Der Name ist egal.', 'Darum lädst du in Level 3 alle Benutzer.'),
        ('Das Passwort steht im Code.', 'Das ist jetzt nicht mehr so.'),
        ('Die App lädt keine Daten.', 'Laden geht. Nur der Vergleich ist zu einfach.')])]},
 woerter=['Map', 'Variable', 'setState', 'initState', 'Methode', 'Navigator', 'Datensatz']))

# ======================================================================= LEVEL 3  (Skript c)
D3_WEB = D(R('  return responseJson;\n}'), P(''), P(WEB_C))
D3_LOGIN = D(LOGIN_KOPF, R(''), M(teil(LOGIN_B, False), 2), P(teil(LOGIN_C, False), 2), R(''), R('  void openList() {'), LUECKE)
D3_BTN = D(BTN_KOPF, M(BTN_B_INNEN, 12), P(BTN_C_INNEN, 12), BTN_FUSS)
L.append(level(3, 'Name und Passwort prüfen', 'loadContactData_L(), data_L und where – die Login-Maske ist angebunden',
 ziel=ziel(figur('json_benutzer', 'JSON-Ansicht von records mit mehreren Benutzern und ihren Passwörtern', 'Das steht in data_L – alle Benutzer mit Passwort')) +
      baumkarte('Dateien im Projekt', dateien([('webRequest.dart', '+ loadContactData_L()', True), ('my_login.dart', 'data_L, loadDataFromDB_L, where', True), ('todo_list.dart', '', False), ('todo_item.dart', '', False)])),
 grafik='<h3>Ablauf in der App – Schritte 1 bis 3 gehören zum Login</h3>\n' + ablauf_html([1, 2, 3], 'l3') + '\n'
   + kette([('initState()', 'loadDataFromDB_L()'), ('loadContactData_L()', 'GET …/flutterTB/'), ('data_L', 'Liste aller Benutzer'), ('Login-Button', 'data_L.where(…)'), ('validName.isNotEmpty', 'openList()')]),
 weiter=('level-4', 'Level 4'),
 S=dict(
  ziel='Zugang zur ToDo-Liste bekommt nur, wer eine Kombination aus Name <b>und</b> Passwort eingibt, die in <code>flutterTB</code> steht. Damit ist die Login-Maske an die Datenbank angebunden.',
  aendern='<code>lib/webRequest.dart</code>, <code>lib/my_login.dart</code>', skript='c – Passwort und LoginName aus der Datenbank auslesen und verwenden',
  schritte=[
   ('aendern', '<code>lib/webRequest.dart</code>: Unter <code>loadContactData()</code> kommt <code>loadContactData_L()</code> – sie holt <b>alle</b> Benutzer und gibt die Liste unter <code>records</code> zurück.', D3_WEB),
   ('aendern', '<code>lib/my_login.dart</code>: <code>passwordLog</code> und <code>loadDataFromDB</code> aus Level 2 werden ersetzt durch die Liste <code>data_L</code> und <code>loadDataFromDB_L()</code>. <code>openList()</code> bleibt.', D3_LOGIN),
   ('aendern', 'Im Login-Button: Mit <code>data_L.where(…)</code> ein Paar aus Name und Passwort suchen. Ist <code>validName</code> nicht leer, öffnet <code>openList()</code> die Liste.', D3_BTN),
   ('test', 'Testen Sie mit zwei verschiedenen Benutzern aus der Datenbank – und mit Name des einen und Passwort des anderen.', None)],
  profi=['<code>webRequest.dart</code>: <code>Future&lt;List&gt; loadContactData_L()</code> liefert alle Datensätze von <code>flutterTB</code> (die Liste unter <code>records</code>).',
         'Die Login-Maske lädt beim Start alle Benutzer in die Liste <code>data_L</code>.',
         'Login öffnet die ToDo-Liste nur, wenn es in <code>data_L</code> einen Eintrag mit genau diesem Namen <b>und</b> diesem Passwort gibt.',
         'Vom Ansatz aus Level 2 bleibt nur <code>openList()</code> übrig.'],
  tipps=[tipp('Login klappt nie, obwohl Name und Passwort stimmen?', 'Lassen Sie sich mit <code>print(data_L);</code> ausgeben, was ankommt. Leerzeichen am Ende des Namens? Groß-/Kleinschreibung?'), INFO_LINT],
  erklaert='<p>Nur gegen ein Passwort zu prüfen ist nicht praktikabel. Sie brauchen die <b>Liste aller Benutzer</b> – also eine Methode, die in der Zukunft eine Liste zurückgibt. '
   'Die Liste liegt im JSON unter <code>records</code> und muss deshalb herausgelöst werden.</p>\n'
   '<p><code>loadDataFromDB_L()</code> muss einmal aufgerufen werden – Achtung, sie reagiert verzögert. Im Button wird dann gesucht:</p>\n'
   + tabelle(['Baustein', 'Bedeutung'], [
     ['<code>data_L.where(…)</code>', 'geht die Liste durch und behält nur die Einträge, für die die Bedingung <code>true</code> ist'],
     ['<code>validName</code>', 'enthält das passende Benutzer-Objekt – oder ist leer'],
     ['<code>validName.isNotEmpty</code>', 'für die Anmeldung reicht das Wissen, ob ein Objekt gefunden wurde']]) +
   '<h3>Kritisch betrachtet</h3>\n<p>So funktioniert der Login – aber er ist <strong>nicht sicher</strong>: Die App lädt <b>alle</b> Benutzer mit ihren Passwörtern im Klartext über unverschlüsseltes HTTP. '
   'In einer echten App prüft der <b>Server</b> den Login, Passwörter liegen nur als <b>Hashwert</b> in der Datenbank, und die Verbindung läuft über <b>HTTPS</b>.</p>\n'
   '<p><strong>Merke:</strong> Erst alle Datensätze laden, dann mit <code>where</code> das passende Paar suchen, dann navigieren.</p>\n'
   '<p><strong>Denkfrage:</strong> Ein Mitschüler sitzt im selben WLAN und zeichnet den Netzwerkverkehr auf. Was sieht er, wenn Ihre App startet?</p>'),
 E=dict(
  ziel='Nur wer Name <b>und</b> Passwort richtig eingibt, kommt zur ToDo-Liste. Name und Passwort müssen zusammen in <code>flutterTB</code> stehen.',
  aendern='<code>lib/webRequest.dart</code>, <code>lib/my_login.dart</code>', skript='c',
  schritte=[
   ('aendern', 'Öffne <code>lib/webRequest.dart</code>. Tippe unten die neue Methode <code>loadContactData_L()</code> ein. Sie holt <b>alle</b> Benutzer.', D3_WEB),
   ('aendern', 'Öffne <code>lib/my_login.dart</code>. Lösche die roten Zeilen aus Level 2. Tippe die grünen Zeilen ein. <code>openList()</code> bleibt.', D3_LOGIN),
   ('aendern', 'Geh zum Login-Button. Lösche die rote Zeile. Tippe die grünen Zeilen ein.', D3_BTN),
   ('test', 'Teste mit 2 Benutzern aus der Datenbank. Teste dann den Namen von Benutzer 1 mit dem Passwort von Benutzer 2. Das darf nicht gehen.', None)],
  profi=['<code>loadContactData_L()</code> gibt alle Benutzer als Liste zurück.',
         'Beim Start lädt die App alle Benutzer in <code>data_L</code>.',
         'Login geht nur, wenn Name <b>und</b> Passwort zusammen in <code>data_L</code> stehen.'],
  tipps=[tipp('Der Login geht nie, obwohl alles stimmt?', 'Schreib kurz <code>print(data_L);</code>. Dann siehst du, was ankommt. Steht ein Leerzeichen am Ende vom Namen? Stimmen große und kleine Buchstaben?'), INFO_LINT_E],
  erklaert='<p>1 Passwort reicht nicht. Die App braucht <b>alle</b> Benutzer. Die Methode gibt deshalb eine Liste zurück. Im JSON steht die Liste unter <code>records</code>.</p>\n'
   + tabelle(['Baustein', 'Was er macht'], [
     ['<code>data_L.where(…)</code>', 'Geht die Liste durch. Behält nur die Einträge, die passen.'],
     ['<code>validName</code>', 'Hier steht der passende Benutzer. Oder nichts.'],
     ['<code>validName.isNotEmpty</code>', 'Ist etwas gefunden? Dann ja.']]) +
   '<h3>Ist das sicher?</h3>\n<p><strong>Nein.</strong> Die App lädt <b>alle</b> Passwörter. Sie gehen offen über das Netz. '
   'Eine echte App macht das anders: Der <b>Server</b> prüft den Login. Passwörter stehen nur als <b>Hashwert</b> in der Datenbank. Die Verbindung läuft über <b>HTTPS</b>.</p>\n'
   '<p><strong>Merke:</strong> Erst alle Benutzer laden. Dann mit <code>where</code> suchen. Dann die Liste öffnen.</p>\n'
   '<p><strong>Denkfrage:</strong> Jemand im selben WLAN schaut den Netzverkehr an. Was sieht er beim Start deiner App?</p>'),
 sk={"check": ['Mit Name und Passwort eines Benutzers aus flutterTB komme ich zur ToDo-Liste.', 'Mit dem Namen des einen und dem Passwort eines anderen Benutzers komme ich nicht hinein.', 'Ich kann erklären, warum diese Lösung nicht sicher ist.'],
     "fragen": [('Was steht in `validName`, wenn Name und Passwort falsch sind?',
       [('Nichts – die Ergebnisliste von where ist leer.', True, 'Darum wird isNotEmpty geprüft.'),
        ('`false`', False, 'where liefert eine Sammlung von Einträgen, keinen Wahrheitswert.'),
        ('Der erste Benutzer der Tabelle.', False, 'where behält nur Einträge, für die die Bedingung stimmt.')]),
      ('Warum ist dieser Login in einer echten App unsicher?',
       [('Alle Passwörter werden im Klartext über HTTP an jedes Gerät geschickt.', True, 'Besser: Prüfung auf dem Server, Hashwerte und HTTPS.'),
        ('Weil where zu langsam ist.', False, 'Es geht um die Daten, die über das Netz gehen.'),
        ('Weil der Button grau sein kann.', False, 'Das ist Bedienkomfort, keine Sicherheitsfrage.')])]},
 ske={"check": ['Mit Name und Passwort aus flutterTB komme ich zur ToDo-Liste.', 'Name von Benutzer 1 und Passwort von Benutzer 2: Ich komme nicht hinein.', 'Ich kann sagen, warum das nicht sicher ist.'],
      "fragen": [('Was steht in `validName`, wenn Name und Passwort falsch sind?',
       [('Nichts. Die Liste von where ist leer.', 'Darum prüfst du isNotEmpty.'),
        ('`false`', 'where gibt Einträge zurück. Nicht wahr oder falsch.'),
        ('Der erste Benutzer.', 'where behält nur Einträge, die passen.')]),
       ('Warum ist der Login nicht sicher?',
       [('Alle Passwörter gehen offen über das Netz.', 'Besser: Der Server prüft. Dazu Hashwerte und HTTPS.'),
        ('where ist zu langsam.', 'Es geht um die Daten im Netz.'),
        ('Der Button kann grau sein.', 'Das hat nichts mit Sicherheit zu tun.')])]},
 woerter=['Liste', 'records', 'where', 'Klartext', 'Hashwert', 'HTTPS', 'Bedingung']))

# ======================================================================= LEVEL 4  (Skript d, e)
D4_ITEM = D(R('class ToDoItem extends StatelessWidget {'), P('final int id; // neu: eindeutige id aus der Datenbank', 2), R('  final String title;'), LUECKE,
            M('const ToDoItem(this.title, this.done, this.remove, this.checkBoxDone,', 2),
            P('const ToDoItem(this.id, this.title, this.done, this.remove, this.checkBoxDone,', 2), R('      {super.key});'))
D4_LISTE = D(R("import 'todo_item.dart';"), P("import 'todo_list_object.dart';"), LUECKE,
             R('class _ToDoListState extends State<ToDoList> {'), M('Map<String, bool> todos = {};', 2),
             P('// Liste für den ListView.builder\nList<ToDoListObject> todos = [];', 2), R(''))
D4_METH = D(M(ALT_METHODEN, 2), P(M4_ADD + '\n\n' + M4_DEL + '\n\n' + M4_CHECK, 2), R('\n  void newEntry() {'))
D4_BUILDER = D(R('body: ListView.builder(\n  itemCount: todos.length,\n  itemBuilder: (context, i) {', 6),
               M(ALT_BUILDER_INNEN, 10), P(NEU_BUILDER_INNEN, 6), R('  },\n),', 6))
L.append(level(4, 'ToDo-Objekte und Liste', 'ToDoListObject, List statt Map, ToDoItem mit id',
 ziel=ziel(figur('datenfluss_l4', 'Datenfluss ohne Datenbank: Eingabedialog mit addItem, Objekt ToDoListObject newtodo mit id 6, checkbox false, name Netzplan, Liste todos, neues ToDo in der App', 'Vom Eingabedialog über ToDoListObject in die Liste todos')) +
      baumkarte('Widget-Baum', baum(('ToDoList', 'Stateful · List&lt;ToDoListObject&gt; todos', True, [('Scaffold', '', False, [('ListView.builder', 'todos[i] → ToDoItem', True, [('ToDoItem', 'id, name, checkbox, …', True, None)]), ('FloatingActionButton', 'newEntry', False, None)])]))),
 grafik='<h3>Von der Map zur Liste von Objekten</h3>\n<div class="zwei">'
   '<div class="kasten"><b>Flutter-Einführung</b><small>Map&lt;String, bool&gt;</small><table><tr><td>\'Milch kaufen\'</td><td>true</td></tr><tr><td>\'LF11 lernen\'</td><td>false</td></tr></table></div>'
   '<div class="verbindung"><span>→</span></div>'
   '<div class="kasten state"><b>Jetzt</b><small>List&lt;ToDoListObject&gt;</small><table><tr><td>id 1</td><td>false</td><td>Projektplan</td></tr><tr><td>id 2</td><td>true</td><td>Gruppeneinteilung</td></tr></table></div></div>\n'
   '<p class="klein">Der Name ist kein Schlüssel mehr – jedes ToDo wird über seine <code>id</code> eindeutig erkannt.</p>',
 weiter=('level-5', 'Level 5'),
 S=dict(
  ziel='Jedes ToDo bekommt eine eindeutige <code>id</code> – die braucht die Datenbank. Aus der Map der Einführung wird eine Liste von <code>ToDoListObject</code>-Objekten. Noch arbeitet die Liste ohne Datenbank.',
  aendern='neu: <code>lib/todo_list_object.dart</code>, <code>lib/todo_item.dart</code>, <code>lib/todo_list.dart</code>', skript='d – Liste mit ToDo-Objekten, e – ToDo-Objekt, ToDoItem und Liste anlegen',
  schritte=[
   ('neu', '<code>lib/todo_list_object.dart</code> mit der Klasse <code>ToDoListObject</code>. Achtung: Im Konstruktor steht <code>checkbox</code> <b>vor</b> <code>name</code>.', P(OBJEKT)),
   ('aendern', '<code>lib/todo_item.dart</code>: <code>ToDoItem</code> bekommt als erstes Feld <code>final int id;</code> – auch im Konstruktor an erster Stelle.', D4_ITEM),
   ('aendern', '<code>lib/todo_list.dart</code>: Die Map <code>todos</code> wird zur Liste von <code>ToDoListObject</code>.', D4_LISTE),
   ('aendern', 'Die drei Methoden arbeiten jetzt mit der Liste und der <code>id</code> statt mit dem Namen als Schlüssel.', D4_METH),
   ('aendern', 'Im <code>build</code>: Der <code>ListView.builder</code> gibt <code>id</code>, Name und Checkbox aus <code>todos[i]</code> an das <code>ToDoItem</code> weiter.', D4_BUILDER),
   ('test', 'Testen Sie: anlegen, abhaken, löschen – noch ohne Datenbank. Legen Sie auch zwei ToDos mit gleichem Namen an.', None)],
  profi=['Neue Klasse <code>ToDoListObject</code> mit <code>int id</code>, <code>String name</code>, <code>bool checkbox</code> und dem Konstruktor <code>(id, checkbox, name)</code> wie im Skript.',
         '<code>ToDoItem</code> bekommt die <code>id</code> als ersten Konstruktor-Wert.',
         '<code>ToDoList</code> verwaltet <code>List&lt;ToDoListObject&gt; todos</code> statt der Map.',
         '<code>addItem</code>, <code>deleteItem(int id)</code> und <code>checkBoxDone(int id)</code> arbeiten über die id; neue id: <code>todos.length + 1</code>.',
         'Anlegen, Abhaken, Löschen funktionieren wie vorher – auch bei zwei ToDos mit gleichem Namen.'],
  tipps=[tipp('„Too many positional arguments“ beim ToDoItem?', 'Haben Sie das Feld <code>id</code> in <code>todo_item.dart</code> auch im Konstruktor ergänzt – an erster Stelle?'),
         tipp('„The getter \'name\' isn\'t defined for the type \'String\'“?', 'Irgendwo steht noch Code der alten Map, z. B. <code>todos.keys</code>. <code>todos[i]</code> ist jetzt ein <code>ToDoListObject</code>.')],
  erklaert='<p><strong>Warum keine Map mehr?</strong> Bisher hatte ein ToDo zwei Eigenschaften (<code>checkbox</code>, <code>name</code>), der Name war der Schlüssel. '
   'Für die Datenbank braucht jedes ToDo eine eindeutige <b>id</b>. Das erlaubt die Map nicht – deshalb eine Liste von Objekten.</p>\n'
   '<p>Damit aus der Datenbank und aus dem Alert-Dialog Daten übergeben werden können, wird die Klasse <code>ToDoListObject</code> benötigt:</p>\n'
   + tabelle(['Tabelle ToDoTB', 'ToDoListObject', 'ToDoItem'], [['<code>id</code>', '<code>int id</code>', '<code>final int id</code> (neu)'], ['<code>name</code>', '<code>String name</code>', '<code>final String title</code>'], ['<code>checkbox</code>', '<code>bool checkbox</code>', '<code>final bool done</code>']]) +
   '\n<ul><li><code>firstWhere</code> sucht das erste Element mit dieser id.</li><li><code>removeWhere</code> entfernt alle Elemente, für die die Bedingung stimmt.</li>'
   '<li><code>todos.length + 1</code> als neue id – so steht es im Skript. In Level 6 sehen Sie, wo das an Grenzen stößt.</li></ul>\n'
   '<p><strong>Merke:</strong> Ein Objekt bündelt die Werte eines Datensatzes – die <code>id</code> macht jedes ToDo eindeutig.</p>\n'
   '<p><strong>Denkfrage:</strong> Zwei ToDos heißen „Einkaufen“. Was wäre mit der Map passiert – und was passiert jetzt?</p>'),
 E=dict(
  ziel='Jedes ToDo bekommt eine eigene Nummer: die <code>id</code>. Die Datenbank braucht sie. Statt der Map gibt es jetzt eine Liste mit Objekten. Die Datenbank kommt erst in Level 5 dazu.',
  aendern='neu: <code>lib/todo_list_object.dart</code>, <code>lib/todo_item.dart</code>, <code>lib/todo_list.dart</code>', skript='d und e',
  schritte=[
   ('neu', 'Lege <code>lib/todo_list_object.dart</code> an. Tippe die Klasse ab. Achtung: <code>checkbox</code> steht <b>vor</b> <code>name</code>.', P(OBJEKT)),
   ('aendern', 'Öffne <code>lib/todo_item.dart</code>. Tippe die grüne Zeile ein. Ersetze die rote Zeile durch die grüne.', D4_ITEM),
   ('aendern', 'Öffne <code>lib/todo_list.dart</code>. Ersetze die Map durch die Liste.', D4_LISTE),
   ('aendern', 'Lösche die 3 alten Methoden. Tippe die 3 neuen Methoden ein.', D4_METH),
   ('aendern', 'Geh zum <code>ListView.builder</code> im <code>build</code>. Lösche die roten Zeilen. Tippe die grünen ein.', D4_BUILDER),
   ('test', 'Teste: anlegen, abhaken, löschen. Lege auch 2 ToDos mit gleichem Namen an.', None)],
  profi=['Neue Klasse <code>ToDoListObject</code> mit <code>id</code>, <code>name</code> und <code>checkbox</code>.',
         '<code>ToDoItem</code> bekommt die <code>id</code> als ersten Wert.',
         '<code>todos</code> ist eine Liste von <code>ToDoListObject</code>.',
         'Die 3 Methoden arbeiten mit der id.',
         'Alles geht wie vorher. Auch 2 ToDos mit gleichem Namen.'],
  tipps=[tipp('Fehler „Too many positional arguments“?', 'Hast du <code>id</code> in <code>todo_item.dart</code> auch im Konstruktor ergänzt? Sie muss an erster Stelle stehen.'),
         tipp('Fehler „The getter \'name\' isn\'t defined for the type \'String\'“?', 'Irgendwo steht noch Code von der alten Map. Zum Beispiel <code>todos.keys</code>. Lösche ihn.')],
  erklaert='<p><strong>Warum keine Map mehr?</strong> In der Map war der Name der Schlüssel. 2 ToDos mit gleichem Namen gingen nicht. Die Datenbank braucht für jedes ToDo eine eigene <b>id</b>. Darum gibt es jetzt Objekte.</p>\n'
   + tabelle(['Tabelle ToDoTB', 'ToDoListObject', 'ToDoItem'], [['<code>id</code>', '<code>int id</code>', '<code>final int id</code> (neu)'], ['<code>name</code>', '<code>String name</code>', '<code>final String title</code>'], ['<code>checkbox</code>', '<code>bool checkbox</code>', '<code>final bool done</code>']]) +
   '\n<ul><li><code>firstWhere</code> sucht das erste ToDo mit dieser id.</li><li><code>removeWhere</code> löscht alle ToDos, die passen.</li>'
   '<li><code>todos.length + 1</code> ist die neue id. In Level 6 siehst du, wo das Probleme macht.</li></ul>\n'
   '<p><strong>Merke:</strong> Ein Objekt hält alle Werte von einem ToDo zusammen. Die id macht jedes ToDo eindeutig.</p>\n'
   '<p><strong>Denkfrage:</strong> 2 ToDos heißen „Einkaufen“. Was war mit der Map? Was passiert jetzt?</p>'),
 sk={"check": ['Ich kann ToDos anlegen, abhaken und löschen – jetzt mit der Liste von ToDoListObject.', 'ToDoItem bekommt die id als ersten Wert.', 'Zwei ToDos mit gleichem Namen werden beide angezeigt.'],
     "fragen": [('Warum wird aus der Map eine Liste von Objekten?',
       [('Jedes ToDo braucht eine eindeutige id für die Datenbank – das erlaubt die Map mit dem Namen als Schlüssel nicht.', True, 'Die id ist der Primärschlüssel in ToDoTB.'),
        ('Weil Listen schneller sind.', False, 'Es geht um die eindeutige id.'),
        ('Weil Flutter keine Maps mehr unterstützt.', False, 'Maps gibt es weiterhin.')]),
      ('Was liefert `todos.firstWhere((element) => element.id == id)`?',
       [('Das erste ToDo-Objekt mit dieser id.', True, 'Danach kann dessen checkbox geändert werden.'),
        ('Die Position in der Liste.', False, 'Dafür gäbe es indexWhere.'),
        ('Alle ToDos mit dieser id als Liste.', False, 'Das wäre where.')])]},
 ske={"check": ['Ich kann ToDos anlegen, abhaken und löschen. Jetzt mit der Liste.', 'ToDoItem bekommt die id als ersten Wert.', '2 ToDos mit gleichem Namen stehen beide da.'],
      "fragen": [('Warum gibt es jetzt eine Liste mit Objekten?',
       [('Jedes ToDo braucht eine eigene id. Mit der Map geht das nicht.', 'Die id ist der Primärschlüssel in ToDoTB.'),
        ('Listen sind schneller.', 'Es geht um die id.'),
        ('Flutter kann keine Maps mehr.', 'Maps gibt es weiter.')]),
       ('Was gibt `todos.firstWhere((element) => element.id == id)` zurück?',
       [('Das erste ToDo mit dieser id.', 'Dann kannst du seine checkbox ändern.'),
        ('Die Stelle in der Liste.', 'Dafür gibt es indexWhere.'),
        ('Alle ToDos mit dieser id.', 'Das macht where.')])]},
 woerter=['Objekt', 'Klasse', 'Konstruktor', 'id', 'Liste', 'Map', 'firstWhere', 'removeWhere']))

# ======================================================================= LEVEL 5  (Skript f, g)
D5_WEB = D(R("import 'package:http/http.dart' as http;"), P("\nimport 'todo_list_object.dart';"), LUECKE,
           R('  var userList = responseJson[\'records\']; // die Liste liegt unter records\n  return userList;\n}'),
           P(''), P(WEB_F_READ + '\n\n' + WEB_F_CREATE + '\n\n' + WEB_F_DELETE + '\n\n' + WEB_F_UPDATE))
D5_LISTE = D(R("import 'todo_list_object.dart';"), P("import 'webRequest.dart';"), LUECKE,
             R('class _ToDoListState extends State<ToDoList> {\n  // Liste für den ListView.builder\n  List<ToDoListObject> todos = [];'),
             P(''), P(LADEN, 2), R('\n  void addItem(String itemName) {'))
L.append(level(5, 'CRUD-Methoden und ToDos laden', 'webRequest erweitern, loadDataFromDBToDo() in initState',
 ziel='<div class="card"><h3>So soll es aussehen – Schritt 4: die ToDo-Liste lädt ihre Daten</h3>' + ablauf_html([4], 'l5') + '</div>' +
      baumkarte('Dateien im Projekt', dateien([('webRequest.dart', '+ loadDataToDo, sendDS, deletDS, updateDS', True), ('todo_list_object.dart', '', False), ('todo_list.dart', 'dataToDo, loadDataFromDBToDo, initState', True), ('todo_item.dart', '', False)])),
 grafik='<h3>Vom Datensatz zum ToDo auf dem Bildschirm</h3>\n' + kette([('initState()', 'ToDo-Liste öffnet'), ('loadDataToDo()', 'GET …/ToDoTB/'), ('dataToDo', 'Liste aus records'), ('ToDoListObject(…)', 'je Datensatz ein Objekt'), ('todos.add', 'in die Liste'), ('setState', 'neu zeichnen')]),
 weiter=('level-6', 'Level 6'),
 S=dict(
  ziel='<code>webRequest.dart</code> bekommt die vier CRUD-Methoden. Die ToDo-Liste lädt beim Öffnen die ToDos aus der Tabelle <code>ToDoTB</code>.',
  aendern='Datenbank auf dem Pi, <code>lib/webRequest.dart</code>, <code>lib/todo_list.dart</code>', skript='f – CRUD-REST-API, g – loadDataFromDBToDo und initState',
  schritte=[
   ('pi', 'Legen Sie auf dem Pi (phpMyAdmin oder Konsole) die Tabelle <code>ToDoTB</code> an und prüfen Sie danach <code>…/records/ToDoTB/</code> im Browser.', roh(SQL_TODO)),
   ('aendern', '<code>lib/webRequest.dart</code>: <code>todo_list_object.dart</code> importieren und unten die vier CRUD-Methoden ergänzen.', D5_WEB),
   ('aendern', '<code>lib/todo_list.dart</code>: <code>webRequest.dart</code> importieren, unter <code>todos</code> die Liste <code>dataToDo</code>, die Methode <code>loadDataFromDBToDo()</code> und <code>initState()</code> ergänzen.', D5_LISTE),
   ('test', 'App neu starten und einloggen: Die ToDos aus der Datenbank erscheinen.', None)],
  profi=['Auf dem Pi gibt es die Tabelle <code>ToDoTB</code> (<code>id</code> als Primärschlüssel, <code>name</code>, <code>checkbox</code>) mit zwei Test-ToDos.',
         '<code>webRequest.dart</code> enthält die CRUD-Methoden mit den Namen aus dem Skript: <code>loadDataToDo()</code> (GET), <code>sendDS()</code> (POST), <code>deletDS()</code> (DELETE), <code>updateDS()</code> (PUT, nur <code>checkbox</code>).',
         'Beim Öffnen lädt <code>ToDoList</code> einmal alle ToDos aus <code>ToDoTB</code>, wandelt jeden Datensatz in ein <code>ToDoListObject</code> um und zeigt sie an.'],
  tipps=[tipp('Sie haben ToDoTB schon im REST-Lernpfad angelegt (Spalten titel/erledigt)?', 'Benennen Sie die Spalten wie im Skript um:<br><code>ALTER TABLE ToDoTB RENAME COLUMN titel TO name, RENAME COLUMN erledigt TO checkbox;</code>'),
         tipp('„type \'int\' is not a subtype of type \'bool\'“?', 'Die Spalte <code>checkbox</code> kommt als 0/1 statt true/false an. Legen Sie sie als <code>BOOLEAN</code> an – oder schreiben Sie <code>element[\'checkbox\'] == true || element[\'checkbox\'] == 1</code>.'),
         tipp('Liste bleibt leer?', 'Steht etwas in ToDoTB? Fehlt <code>setState(() {});</code> am Ende von <code>loadDataFromDBToDo</code>?'),
         INFO_LINT],
  erklaert='<p><strong>CRUD</strong> – die php-crud-api auf dem Pi ermöglicht vier Operationen:</p>\n'
   + tabelle(['CRUD', 'HTTP', 'Methode in webRequest.dart', 'Adresse'], [
       ['Create – anlegen', 'POST', '<code>sendDS(newItem)</code>', '…/ToDoTB/'],
       ['Read – auslesen', 'GET', '<code>loadDataToDo()</code>', '…/ToDoTB/'],
       ['Update – ändern', 'PUT', '<code>updateDS(updItem)</code>', '…/ToDoTB/ + id'],
       ['Delete – löschen', 'DELETE', '<code>deletDS(newItem)</code>', '…/ToDoTB/ + id']]) +
   '\n<p>Beim Abruf der ToDos kommt eine Liste. Sie wird beim Aufbau des Screens in Objekte umgewandelt und in <code>todos</code> abgelegt.</p>\n'
   '<p><code>initState()</code> wird beim Aufruf des States eines Stateful Widgets ausgeführt. Sie können die Methode überschreiben und so die Daten der Datenbank in die Liste übertragen.</p>\n'
   '<p><strong>Merke:</strong> Daten aus dem Netz werden in <code>initState</code> angestoßen und mit <code>setState</code> angezeigt, sobald sie da sind.</p>\n'
   '<p><strong>Denkfrage:</strong> Legen Sie jetzt ein ToDo an und starten Sie die App neu. Warum ist es weg – die ToDos aus der Datenbank aber nicht?</p>'),
 E=dict(
  ziel='<code>webRequest.dart</code> bekommt 4 neue Methoden. Mit ihnen kann die App ToDos lesen, anlegen, ändern und löschen. Die ToDo-Liste lädt beim Start die ToDos aus der Tabelle <code>ToDoTB</code>.',
  aendern='Datenbank auf dem Pi, <code>lib/webRequest.dart</code>, <code>lib/todo_list.dart</code>', skript='f und g',
  schritte=[
   ('pi', 'Lege auf dem Pi die Tabelle <code>ToDoTB</code> an. Nimm phpMyAdmin oder die Konsole. Öffne danach <code>…/records/ToDoTB/</code> im Browser.', roh(SQL_TODO)),
   ('aendern', 'Öffne <code>lib/webRequest.dart</code>. Tippe oben den Import ein. Tippe unten die 4 Methoden ein.', D5_WEB),
   ('aendern', 'Öffne <code>lib/todo_list.dart</code>. Tippe die grünen Zeilen ein.', D5_LISTE),
   ('test', 'Starte die App neu. Logge dich ein. Jetzt siehst du die ToDos aus der Datenbank.', None)],
  profi=['Auf dem Pi gibt es die Tabelle <code>ToDoTB</code> mit 2 Test-ToDos.',
         '<code>webRequest.dart</code> hat 4 Methoden: <code>loadDataToDo()</code>, <code>sendDS()</code>, <code>deletDS()</code>, <code>updateDS()</code>.',
         'Beim Start lädt die ToDo-Liste alle ToDos aus <code>ToDoTB</code> und zeigt sie.'],
  tipps=[tipp('Du hast ToDoTB schon im REST-Lernpfad angelegt?', 'Dann heißen die Spalten anders. Benenne sie um:<br><code>ALTER TABLE ToDoTB RENAME COLUMN titel TO name, RENAME COLUMN erledigt TO checkbox;</code>'),
         tipp('Fehler „type \'int\' is not a subtype of type \'bool\'“?', 'Die Spalte <code>checkbox</code> kommt als 0 oder 1. Lege sie als <code>BOOLEAN</code> an.'),
         tipp('Die Liste bleibt leer?', 'Steht etwas in ToDoTB? Steht <code>setState(() {});</code> am Ende von <code>loadDataFromDBToDo</code>?'),
         INFO_LINT_E],
  erklaert='<p><strong>CRUD</strong> heißt: anlegen, lesen, ändern, löschen. Die API auf dem Pi kann alle 4:</p>\n'
   + tabelle(['CRUD', 'HTTP', 'Methode', 'Adresse'], [
       ['Create – anlegen', 'POST', '<code>sendDS</code>', '…/ToDoTB/'],
       ['Read – lesen', 'GET', '<code>loadDataToDo</code>', '…/ToDoTB/'],
       ['Update – ändern', 'PUT', '<code>updateDS</code>', '…/ToDoTB/ + id'],
       ['Delete – löschen', 'DELETE', '<code>deletDS</code>', '…/ToDoTB/ + id']]) +
   '\n<p>Die App bekommt eine Liste. Aus jedem Datensatz macht sie ein Objekt. Das Objekt kommt in <code>todos</code>.</p>\n'
   '<p><code>initState()</code> läuft 1-mal beim Start. Dort lädst du die Daten.</p>\n'
   '<p><strong>Merke:</strong> In <code>initState</code> laden. Mit <code>setState</code> anzeigen.</p>\n'
   '<p><strong>Denkfrage:</strong> Lege jetzt ein ToDo an. Starte die App neu. Warum ist es weg? Warum sind die ToDos aus der Datenbank noch da?</p>'),
 sk={"check": ['Die Tabelle ToDoTB existiert, `…/records/ToDoTB/` zeigt meine Test-ToDos.', 'Nach dem Login sehe ich die ToDos aus der Datenbank.', '`webRequest.dart` enthält `loadDataToDo`, `sendDS`, `deletDS` und `updateDS`.'],
     "fragen": [('Welche HTTP-Methode benutzt `sendDS`?',
       [('POST – Create', True, 'POST legt einen neuen Datensatz an.'), ('GET – Read', False, 'GET liest nur.'), ('PUT – Update', False, 'PUT ändert einen vorhandenen Datensatz.')]),
      ('Warum steht bei `deletDS` und `updateDS` die id in der Adresse?',
       [('Die API muss wissen, welcher Datensatz gemeint ist – über den Primärschlüssel.', True, 'Z. B. …/ToDoTB/3 für das ToDo mit der id 3.'),
        ('Damit die Adresse länger ist.', False, 'Die id bestimmt den Datensatz.'),
        ('Weil sonst die ganze Datenbank gelöscht wird.', False, 'Ohne id meldet die API einen Fehler – sie braucht die id.')])]},
 ske={"check": ['Die Tabelle ToDoTB ist da. `…/records/ToDoTB/` zeigt meine Test-ToDos.', 'Nach dem Login sehe ich die ToDos aus der Datenbank.', 'In `webRequest.dart` stehen `loadDataToDo`, `sendDS`, `deletDS` und `updateDS`.'],
      "fragen": [('Welche HTTP-Methode nimmt `sendDS`?',
       [('POST – anlegen', 'POST legt einen neuen Datensatz an.'), ('GET – lesen', 'GET liest nur.'), ('PUT – ändern', 'PUT ändert einen Datensatz.')]),
       ('Warum steht bei `deletDS` und `updateDS` die id in der Adresse?',
       [('Die API muss wissen, welcher Datensatz gemeint ist.', 'Zum Beispiel …/ToDoTB/3 für das ToDo mit der id 3.'),
        ('Damit die Adresse länger ist.', 'Die id sagt, welcher Datensatz.'),
        ('Sonst löscht sie die ganze Datenbank.', 'Ohne id kommt ein Fehler.')])]},
 woerter=['CRUD', 'GET', 'POST', 'PUT', 'DELETE', 'Tabelle', 'Primärschlüssel', 'initState', 'setState']))

# ======================================================================= LEVEL 6  (Aufgabe 3)
D6_ADD = D(R('void addItem(String itemName) {\n  setState(() {\n    ToDoListObject newtodo = ToDoListObject(todos.length + 1, false, itemName);\n    todos.add(newtodo);', 2),
           P('sendDS(newtodo); // Create', 6), R('  });\n  Navigator.of(context).pop();\n}', 2))
D6_DEL = D(R('void deleteItem(int id) {\n  setState(() {', 2),
           P('ToDoListObject item = todos.firstWhere((element) => element.id == id);\nToDoListObject deltodo = ToDoListObject(item.id, item.checkbox, item.name);\ndeletDS(deltodo); // Delete', 6),
           R('    todos.removeWhere((element) {', 2), LUECKE)
D6_CHECK = D(R('void checkBoxDone(int id) {\n  setState(() {\n    ToDoListObject item = todos.firstWhere((element) => element.id == id);\n    item.checkbox = !item.checkbox;', 2),
             P('ToDoListObject upttodo = ToDoListObject(item.id, item.checkbox, item.name);\nupdateDS(upttodo); // Update', 6), R('  });\n}', 2))
L.append(level(6, 'Methoden anpassen', 'Aufgabe 3 – Anlegen, Löschen und Abhaken landen in der Datenbank',
 ziel=ziel(figur('methoden', 'Dart-Methoden addItem, deleteItem und checkBoxDone mit Kommentaren', 'Diese drei Methoden sprechen jetzt mit der Datenbank')) +
      baumkarte('Dateien im Projekt', dateien([('webRequest.dart', 'Login und CRUD', False), ('my_login.dart', 'Login gegen flutterTB', False), ('todo_list_object.dart', 'id, name, checkbox', False), ('todo_list.dart', 'sendDS, deletDS, updateDS', True), ('todo_item.dart', 'mit id', False)])),
 grafik='<h3>Ablauf in der App – Schritte 5 und 6</h3>\n' + ablauf_html([5, 6], 'l6') + '\n'
   + kette([('Create', 'addItem → sendDS'), ('Read', 'loadDataFromDBToDo → loadDataToDo'), ('Update', 'checkBoxDone → updateDS'), ('Delete', 'deleteItem → deletDS')]),
 weiter=('wissen', '📘 Wissen'),
 S=dict(
  ziel='Die Methoden der ToDo-Liste rufen jetzt die passenden Methoden aus <code>webRequest.dart</code> auf. Damit ist auch die ToDo-Liste vollständig an die Datenbank angebunden.',
  aendern='<code>lib/todo_list.dart</code>', skript='Aufgabe 3: Methoden anpassen',
  schritte=[
   ('aendern', '<code>addItem</code>: Nach <code>todos.add(newtodo)</code> das neue Objekt mit <code>sendDS</code> an die Datenbank schicken.', D6_ADD),
   ('aendern', '<code>deleteItem</code>: Das Objekt mit <code>firstWhere</code> suchen, mit <code>deletDS</code> in der Datenbank löschen – erst dann aus der Liste entfernen.', D6_DEL),
   ('aendern', '<code>checkBoxDone</code>: Nach dem Umschalten mit <code>updateDS</code> den neuen Status speichern.', D6_CHECK),
   ('test', 'Abschlusstest: anlegen, abhaken, löschen – App beenden, neu starten, einloggen. Alles muss so sein wie vorher. Prüfen Sie zusätzlich <code>…/records/ToDoTB/</code> im Browser.', None)],
  profi=['Jede Änderung an der Liste landet zusätzlich in <code>ToDoTB</code>: Anlegen (Create), Abhaken (Update), Löschen (Delete).',
         'Dafür rufen <code>addItem</code>, <code>checkBoxDone</code> und <code>deleteItem</code> die Methoden aus <code>webRequest.dart</code> auf.',
         'Nach einem Neustart der App ist alles so wie vorher; der Browser zeigt denselben Stand in <code>ToDoTB</code>.'],
  tipps=[tipp('Neues ToDo ist nach dem Neustart weg?', 'Steht es im Browser in ToDoTB? Wenn nicht: Gibt es die id schon? Siehe „Kritisch betrachtet“ unter 💡 Hintergrund.')],
  erklaert='<p>Die Oberfläche bleibt, wie sie ist. Jede Methode, die Daten verändert, gibt die Änderung zusätzlich an die Datenbank weiter:</p>\n'
   + tabelle(['Methode in todo_list.dart', 'ruft auf', 'CRUD'], [['<code>loadDataFromDBToDo</code>', '<code>loadDataToDo()</code>', 'Read'], ['<code>addItem</code>', '<code>sendDS()</code>', 'Create'], ['<code>checkBoxDone</code>', '<code>updateDS()</code>', 'Update'], ['<code>deleteItem</code>', '<code>deletDS()</code>', 'Delete']]) +
   '<h3>Kritisch betrachtet</h3>\n'
   '<p><strong>Die id <code>todos.length + 1</code>:</strong> Sie haben die ToDos 1, 2 und 3 und löschen ToDo 2. Das nächste neue ToDo bekommt die id 3 – die gibt es schon. '
   'Die Datenbank lehnt den Datensatz ab, die App zeigt ihn trotzdem an. Bessere Lösungen: die höchste vorhandene id + 1 – oder die Datenbank vergibt die id selbst (<code>AUTO_INCREMENT</code>) und die API meldet sie nach dem POST zurück.</p>\n'
   '<p><strong>Keine Fehlerprüfung:</strong> Die Methoden warten nicht auf die Antwort des Servers. Ist der Pi aus, zeigt die App Änderungen, die nie gespeichert werden.</p>\n'
   '<p><strong>Merke:</strong> POST legt an, GET liest, PUT ändert, DELETE löscht – die id in der Adresse sagt, <b>welcher</b> Datensatz gemeint ist.</p>\n'
   '<p><strong>Denkfrage:</strong> Zwei Handys sind eingeloggt. Auf dem einen wird ein ToDo abgehakt. Wann sieht das andere Handy den Haken? (Skript: Refresh-Button)</p>'),
 E=dict(
  ziel='Jetzt speichert die ToDo-Liste alles in der Datenbank. Anlegen, abhaken und löschen gehen an <code>webRequest.dart</code>. Dann ist die ToDo-Liste fertig angebunden.',
  aendern='<code>lib/todo_list.dart</code>', skript='Aufgabe 3',
  schritte=[
   ('aendern', 'Geh zu <code>addItem</code>. Tippe die grüne Zeile ein. Sie schickt das neue ToDo an die Datenbank.', D6_ADD),
   ('aendern', 'Geh zu <code>deleteItem</code>. Tippe die 3 grünen Zeilen ein. Sie löschen das ToDo in der Datenbank.', D6_DEL),
   ('aendern', 'Geh zu <code>checkBoxDone</code>. Tippe die 2 grünen Zeilen ein. Sie speichern den Haken in der Datenbank.', D6_CHECK),
   ('test', 'Teste alles: anlegen, abhaken, löschen. Beende die App. Starte sie neu. Logge dich ein. Alles muss noch so sein. Schau auch im Browser in <code>…/records/ToDoTB/</code>.', None)],
  profi=['Anlegen, abhaken und löschen landen auch in <code>ToDoTB</code>.',
         'Dafür rufen die 3 Methoden die Methoden aus <code>webRequest.dart</code> auf.',
         'Nach einem Neustart ist alles noch da.'],
  tipps=[tipp('Ein neues ToDo ist nach dem Neustart weg?', 'Steht es im Browser in ToDoTB? Wenn nicht: Gibt es die id schon? Lies dazu unter 💡 Hintergrund.')],
  erklaert='<p>Die Oberfläche bleibt gleich. Jede Methode, die etwas ändert, sagt es jetzt auch der Datenbank:</p>\n'
   + tabelle(['Methode', 'ruft auf', 'CRUD'], [['<code>loadDataFromDBToDo</code>', '<code>loadDataToDo()</code>', 'lesen'], ['<code>addItem</code>', '<code>sendDS()</code>', 'anlegen'], ['<code>checkBoxDone</code>', '<code>updateDS()</code>', 'ändern'], ['<code>deleteItem</code>', '<code>deletDS()</code>', 'löschen']]) +
   '<h3>Was ist noch nicht gut?</h3>\n'
   '<p><strong>Die id:</strong> Du hast die ToDos 1, 2 und 3. Du löschst ToDo 2. Dann gibt es 2 ToDos. Das neue ToDo bekommt die id 3. Die gibt es aber schon. '
   'Die Datenbank speichert es nicht. Besser: die größte id + 1. Oder die Datenbank gibt die id selbst.</p>\n'
   '<p><strong>Keine Prüfung:</strong> Die App wartet nicht auf die Antwort vom Pi. Ist der Pi aus, geht die Änderung verloren.</p>\n'
   '<p><strong>Merke:</strong> POST legt an. GET liest. PUT ändert. DELETE löscht. Die id in der Adresse sagt, welcher Datensatz.</p>\n'
   '<p><strong>Denkfrage:</strong> 2 Handys sind eingeloggt. Auf einem hakst du ein ToDo ab. Wann sieht das andere Handy den Haken?</p>'),
 sk={"check": ['Ein neues ToDo steht nach dem Anlegen in ToDoTB (Browser prüfen).', 'Abhaken und Löschen sind nach einem Neustart der App noch so.', 'Ich kann zu jeder Methode in `todo_list.dart` die Methode aus `webRequest.dart` und die CRUD-Operation nennen.'],
     "fragen": [('Welche Methode aus `webRequest.dart` ruft `checkBoxDone` auf?',
       [('`updateDS` – Update mit PUT', True, 'Sie schickt nur die geänderte Spalte checkbox.'),
        ('`sendDS`', False, 'sendDS legt einen neuen Datensatz an.'),
        ('`loadDataToDo`', False, 'loadDataToDo liest nur.')]),
      ('Was passiert mit `todos.length + 1`, nachdem ein ToDo aus der Mitte gelöscht wurde?',
       [('Die neue id kann es schon geben – die Datenbank lehnt den Datensatz ab.', True, 'Abhilfe: höchste id + 1 oder AUTO_INCREMENT.'),
        ('Nichts – die id ist immer eindeutig.', False, 'Nach dem Löschen stimmt die Anzahl nicht mehr mit der höchsten id überein.'),
        ('Die App stürzt sofort ab.', False, 'Die App zeigt das ToDo – gespeichert wird es aber nicht.')])]},
 ske={"check": ['Ein neues ToDo steht danach in ToDoTB. Ich prüfe es im Browser.', 'Abhaken und Löschen sind nach einem Neustart noch so.', 'Ich kann zu jeder Methode in `todo_list.dart` sagen: Welche Methode aus `webRequest.dart`? Welcher CRUD-Teil?'],
      "fragen": [('Welche Methode ruft `checkBoxDone` auf?',
       [('`updateDS`. Das ist Update mit PUT.', 'Sie schickt nur die Spalte checkbox.'),
        ('`sendDS`', 'sendDS legt ein neues ToDo an.'),
        ('`loadDataToDo`', 'loadDataToDo liest nur.')]),
       ('Du löschst ein ToDo aus der Mitte. Was passiert dann mit `todos.length + 1`?',
       [('Die neue id gibt es vielleicht schon. Die Datenbank speichert das ToDo nicht.', 'Besser: größte id + 1 oder AUTO_INCREMENT.'),
        ('Nichts. Die id ist immer neu.', 'Nach dem Löschen passt die Anzahl nicht mehr zur größten id.'),
        ('Die App stürzt ab.', 'Die App zeigt das ToDo. Gespeichert wird es aber nicht.')])]},
 woerter=['CRUD', 'POST', 'PUT', 'DELETE', 'id', 'AUTO_INCREMENT', 'Methode']))

# ======================================================================= WISSEN (Reiter je Abschnitt)
W = [('w-weg', '1 · Der Weg der Daten', kette([('Widget', 'Button, Checkbox …'), ('State-Methode', 'addItem, loadDataFromDB_L …'), ('webRequest.dart', 'sendDS, loadDataToDo …'), ('HTTP', 'GET, POST, PUT, DELETE'), ('php-crud-api', 'auf dem Pi'), ('MariaDB', 'flutterDB')]) +
      '<p>Die Oberfläche kennt keine Adressen und kein JSON – das steckt in <code>webRequest.dart</code>.</p>'),
     ('w-crud', '2 · CRUD in webRequest.dart', tabelle(['CRUD', 'HTTP', 'Adresse', 'SQL', 'webRequest.dart', 'aufgerufen von'], [
        ['Create', 'POST', '…/records/ToDoTB/', 'INSERT', '<code>sendDS</code>', '<code>addItem</code>'],
        ['Read', 'GET', '…/records/ToDoTB/', 'SELECT', '<code>loadDataToDo</code>', '<code>loadDataFromDBToDo</code>'],
        ['Update', 'PUT', '…/records/ToDoTB/3', 'UPDATE', '<code>updateDS</code>', '<code>checkBoxDone</code>'],
        ['Delete', 'DELETE', '…/records/ToDoTB/3', 'DELETE', '<code>deletDS</code>', '<code>deleteItem</code>']]) +
      '<p>Für den Login: <code>loadContactData()</code> (ein Datensatz, <code>…/flutterTB/1</code>) und <code>loadContactData_L()</code> (alle, <code>…/flutterTB/</code>).</p>'),
     ('w-json', '3 · JSON in Dart', tabelle(['JSON', 'Dart nach jsonDecode', 'Zugriff'], [
        ['<code>{"id":1,"name":"berno","passwordLogin":"…"}</code>', 'Map', "<code>data['passwordLogin']</code>"],
        ['<code>[ {…}, {…} ]</code>', 'List', '<code>data_L[0]</code>'],
        ['<code>{"records":[{…},{…}]}</code>', 'Map mit einer List darin', "<code>responseJson['records']</code>"]])),
     ('w-async', '4 · async und await', '<p>Eine Anfrage ans Netz dauert. Statt die App anzuhalten, liefert sie ein <code>Future</code> – ein Versprechen auf ein späteres Ergebnis.</p>' + dart("""Future<List> loadContactData_L() async {   // async: hier darf gewartet werden
  var response = await http.get(url);        // await: warten, App läuft weiter
  return jsonDecode(response.body)['records'];
}

void loadDataFromDB_L() async {
  data_L = await loadContactData_L();       // Ergebnis abholen
}""") + '<p>Solche Methoden werden einmal in <code>initState()</code> aufgerufen. Erst <code>setState</code> zeigt neue Daten auf dem Bildschirm an.</p>'),
     ('w-fehler', '5 · Typische Fehler', tabelle(['Meldung / Verhalten', 'Ursache', 'Abhilfe'], [
        ['SocketException, Connection refused', 'IP falsch, Pi nicht erreichbar', 'Adresse zuerst im Browser testen, ip in webRequest.dart prüfen'],
        ['Cleartext HTTP traffic not permitted', 'Android blockiert http://', '<code>usesCleartextTraffic="true"</code> im Manifest'],
        ['Nichts passiert nach Änderung in initState', 'Hot Reload führt initState nicht erneut aus', 'App neu starten'],
        ['Fehler zum Primärschlüssel', 'Tabelle ohne PRIMARY KEY', '<code>ALTER TABLE … ADD PRIMARY KEY (id)</code>'],
        ["type 'int' is not a subtype of type 'bool'", 'checkbox kommt als 0/1', 'Spalte als BOOLEAN anlegen'],
        ['Neues ToDo nach Neustart weg', 'id doppelt (todos.length + 1)', 'höchste id + 1 verwenden'],
        ['Blaue Hinweise zu webRequest.dart, data_L', 'Namenskonventionen von Dart', 'Namen bleiben wie im Skript – nur Hinweise']]))]

def _wissen():
    reiter = ''.join(f'<button type="button" role="tab" data-schritt="{i}">{t}</button>' for i, t, _ in W)
    teile = ''
    for n, (i, t, inhalt) in enumerate(W):
        zur = f'<button type="button" class="knopf" data-geh="{W[n-1][0]}">◀ {W[n-1][1]}</button>' if n else ''
        vor = f'<button type="button" class="knopf primaer" data-geh="{W[n+1][0]}">Weiter: {W[n+1][1]} ▶</button>' if n + 1 < len(W) else ''
        teile += (f'<div class="schritt" data-schritt="{i}" role="tabpanel"><div class="card" id="{i}"><h3>{t}</h3>\n{inhalt}</div>'
                  f'<p class="schritt-weiter">{zur}{vor}</p></div>\n')
    return f'''<section class="ansicht" id="wissen">
  <div class="card level-kopf"><span class="nummer" aria-hidden="true">📘</span>
    <div><h2>Wissen: Flutter und REST</h2><p class="stich">Zum Nachschlagen – alles, was die Level voraussetzen</p></div></div>
  <nav class="schritt-reiter viele" role="tablist" aria-label="Abschnitte">{reiter}</nav>
{teile}  <p class="druck-fuss">Flutter-Datenbankanbindung LF11 · Version {VERSION} · Stand {DATUM} · bnbsinfo.github.io/lf11_lernpfade/datenbank/</p>
  <div class="card lp-fuss"><a class="knopf" href="#level-6">◀ Level 6</a><button type="button" class="knopf druck-knopf" data-drucken>🖨️ Wissen drucken</button><a class="knopf primaer" href="#start">Zum Start ▶</a></div>
</section>
'''
WISSEN = _wissen()

# ======================================================================= START
UEB = [('level-1', 'json_einzeln', '1 · http und erster Abruf', 'webRequest.dart, loadContactData()'),
       ('level-2', 'login', '2 · Passwort aus der Datenbank', 'loadDataFromDB(), passwordLog'),
       ('level-3', 'json_benutzer', '3 · Name und Passwort prüfen', 'loadContactData_L(), where'),
       ('level-4', 'datenfluss_l4', '4 · ToDo-Objekte und Liste', 'ToDoListObject, ToDoItem mit id'),
       ('level-5', 'ablauf', '5 · CRUD und ToDos laden', 'loadDataToDo, initState'),
       ('level-6', 'methoden', '6 · Methoden anpassen', 'sendDS, deletDS, updateDS')]
START = '''<section class="ansicht" id="start">
    <div class="card echt"><span aria-hidden="true">🗄️</span><div>
      <b>Sie bauen weiter an Ihrer App aus der <a href="../flutter/">Flutter-Einführung</a>.</b> Dieser Lernpfad folgt dem Skript, Kapitel
      <i>Datenbankanbindung umsetzen – WebRequest in Flutter</i> (Abschnitte a–g und Aufgabe 3): Zuerst binden Sie die <b>Login-Maske</b>,
      danach die <b>ToDo-Liste</b> an die Datenbank auf Ihrem Raspberry Pi an.</div></div>
    <div class="card"><h2>Wählen Sie Ihren Pfad</h2>
      <p>Beide Pfade bauen <b>dieselbe App</b> mit denselben Leveln und derselben Selbstkontrolle. Sie können jederzeit
      oben im Seitenkopf umschalten – auch mitten in einem Level.</p>
      <div class="pfad-karten">
        <button type="button" class="pfad-karte" data-modus="begleitet">
          <span class="pk-titel">🧭 Begleiteter Pfad</span>
          <span class="pk-unter">mit sehr viel Unterstützung</span>
          <span class="pk-liste">✔ jeder Schritt einzeln: neue Datei, ändern oder löschen<br>
          ✔ Code-Rahmen zeigen genau die Stelle in der Datei<br>✔ Erklärungen und Tipps zu jedem Level</span>
          <span class="pk-fuer">Für alle, denen async, JSON und REST noch neu sind.</span>
        </button>
        <button type="button" class="pfad-karte" data-modus="profi">
          <span class="pk-titel">🚀 Profipfad</span>
          <span class="pk-unter">nur Anforderungen – den Weg finden Sie selbst</span>
          <span class="pk-liste">✔ je Level eine knappe Liste: Was muss die App können?<br>
          ✔ kein Code vorgegeben, Erklärungen nur auf Klick<br>✔ Methodennamen wie im Skript</span>
          <span class="pk-fuer">Für alle, die die Einführung sicher geschafft haben.</span>
        </button>
      </div>
    </div>
    <div class="card"><h2>Voraussetzungen</h2>
      <div class="start-raster">
        <div><h3>1 · Ihre App</h3><p>Projekt <code>meine_app</code> mit Login-Maske und ToDo-Liste – Level 9 der Flutter-Einführung ist geschafft.</p></div>
        <div><h3>2 · Ihr Pi</h3><p>Datenbank <code>flutterDB</code> mit Tabelle <code>flutterTB</code> und die REST-API <code>php-crud-api</code> sind eingerichtet (Skript Aufgabe 2 bzw. <a href="https://bnbsinfo.github.io/lf11_lernpfade/rest/">REST-Lernpfad</a>).</p></div>
        <div><h3>3 · Abtippen</h3><p>Code wird <b>abgetippt</b> – Kopieren ist gesperrt. Dateien und Methoden heißen wie im Skript.</p></div>
        <div><h3>4 · Selbstkontrolle</h3><p>Im Reiter ✅ Prüfen: Haken setzen, was wirklich funktioniert, Kontrollfragen beantworten – dann ist das Level geschafft.</p></div>
      </div></div>
    <div class="card"><h2>Ihre Lernziele</h2><ul>
      <li>Ich kann mit dem Paket <code>http</code>, <code>async</code>/<code>await</code> und <code>jsonDecode</code> Daten von der REST-API laden.</li>
      <li>Ich kann den Login gegen Name und Passwort aus der Datenbank prüfen – und seine Schwächen benennen.</li>
      <li>Ich kann ToDos als Objekte mit id verwalten und beim Start aus der Datenbank laden.</li>
      <li>Ich kann die CRUD-Operationen den HTTP-Methoden und meinen Methoden zuordnen.</li></ul></div>
    <div class="card"><h2>Grundlagen zum Nachschlagen</h2>
      <p><a href="#wissen">📘 Wissen: Flutter und REST</a> – Weg der Daten, CRUD in webRequest.dart, JSON in Dart, async/await und typische Fehler.</p></div>
    <div class="card"><h2>Ihr Weg in 6 Leveln</h2><p class="klein">Level 1–3: <b>Login-Maske</b> (Skript a–c) · Level 4–6: <b>ToDo-Liste</b> (Skript d–g, Aufgabe 3)</p><div class="uebersicht">''' + ''.join(
    f'<a href="#{z}" data-ziel="{z}"><img src="{b64(f, 360)}" alt="" loading="lazy"><b>{t}</b><span class="klein">{k}</span><span class="fertig-marke">✓ geschafft</span></a>' for z, f, t, k in UEB) + '''</div>
      <p style="margin-top:14px"><a class="knopf primaer" href="#level-1">Los geht's mit Level 1 ▶</a></p></div>
  </section>
'''
