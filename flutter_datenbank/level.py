L = []
INFO_LINT = tipp('Blaue Hinweise der IDE zu <code>webRequest.dart</code> oder <code>data_L</code>?',
  'Dart empfiehlt Dateinamen wie <code>web_request.dart</code> und Namen ohne Unterstrich. '
  'Wir behalten die Namen aus dem Skript, damit Skript und Lernpfad übereinstimmen – es sind nur Hinweise, keine Fehler.')

# ======================================================================= LEVEL 1  (Skript a + Anfang b)
L.append(level(1, 'http einbinden und erster Abruf', 'webRequest.dart – ein Datensatz aus flutterTB kommt in der Konsole an',
 auftrag('Ihre App holt zum ersten Mal Daten vom Raspberry Pi: den ersten Benutzer der Tabelle <code>flutterTB</code>. Noch ändert sich auf dem Bildschirm nichts – das Ergebnis erscheint in der Konsole.',
   '<code>pubspec.yaml</code>, <code>AndroidManifest.xml</code>, neu: <code>lib/webRequest.dart</code>, <code>lib/my_login.dart</code>',
   'Datenbankanbindung umsetzen – a: Einbinden der http-Erweiterung, b: Passwort aus der Datenbank auslesen (erster Teil)',
   ['Testen Sie im Browser beide Adressen aus dem Skript – mit der IP <b>Ihres</b> Pi: <code>…/records/flutterTB/1</code> und <code>…/records/flutterTB/</code>.',
    'Öffnen Sie <code>meine_app</code>. Im Terminal: <code>flutter pub add http</code>.',
    '<code>android/app/src/main/AndroidManifest.xml</code>: Internet und unverschlüsseltes HTTP erlauben (siehe unten – nicht im Skript, aber für Android nötig).',
    'Erstellen Sie die neue Dart-Datei <code>lib/webRequest.dart</code>: Paket importieren, IP als Konstante, Methode <code>loadContactData()</code>.',
    '<code>my_login.dart</code>: <code>webRequest.dart</code> importieren und zum Test in <code>initState()</code> <code>loadContactData()</code> aufrufen und das Ergebnis mit <code>print</code> ausgeben.',
    'App neu starten (kein Hot Reload – <code>initState</code> läuft nur beim Start) und die Konsole lesen.'],
   '<h3>Erklärt – was passiert hier?</h3>\n'
   '<p><strong>Die Adresse der REST-API</strong> besteht aus vier Teilen (Skript, Abbildung zur URL):</p>\n'
   + tabelle(['Teil', 'Beispiel'], [['ServerAdresse/IP', '<code>http://192.168.0.10</code>'], ['Ordner-API', '<code>/php-crud-api/api.php/records</code>'], ['DB-Tabelle', '<code>/flutterTB</code>'], ['Datensatz (ID/PK)', '<code>/1</code> – ohne: alle Datensätze']]) +
   '\n<p><strong>Ein Paket für HTTP.</strong> Flutter selbst kann keine Webanfragen – das übernimmt das Paket <code>http</code>. Alle Zugriffe auf die Datenbank sammeln Sie in <code>webRequest.dart</code>.</p>\n'
   '<p><strong>Android braucht eine Erlaubnis</strong> für Anfragen an <code>http://</code>-Adressen:</p>\n' + roh(MANIFEST) +
   '<p>Ein einzelner Datensatz lässt sich direkt in eine <code>Map</code> umwandeln. Die Daten kommen zeitverzögert an – deshalb ist die Methode <code>async</code> und gibt ein <code>Future</code> zurück:</p>\n'
   + dart(web(1)) +
   tabelle(['Baustein', 'Bedeutung'], [
     ['<code>Future&lt;Map&gt;</code>', 'die Map kommt <b>später</b> – wie eine Abholnummer'],
     ['<code>await http.get(url)</code>', 'wartet, bis der Server geantwortet hat – die App bleibt bedienbar'],
     ['<code>jsonDecode</code>', 'wandelt den JSON-Text in eine Dart-<code>Map</code> um']]) +
   '\n<p><strong>Die IP steht nur einmal oben</strong> (<code>$ip</code> in der Adresse). Im Skript steht sie in jeder Adresse – so müssen Sie sie nur an einer Stelle ändern.</p>\n'
   '<p>Zum Test in der Login-Maske:</p>\n' + dart(TEST_L1) +
   tipp('„Cleartext HTTP traffic … not permitted“?', 'Es fehlt <code>android:usesCleartextTraffic="true"</code> im <code>&lt;application&gt;</code>-Tag. Danach die App komplett neu starten.')
   + tipp('„SocketException“ oder „Connection refused“?', 'IP falsch, Pi aus oder nicht im selben Netz. Testen Sie dieselbe Adresse zuerst im Browser.')
   + tipp('Fehlermeldung zum Primärschlüssel bei flutterTB/1?', 'Die REST-API findet einen Datensatz nur über den Primärschlüssel: <code>ALTER TABLE flutterTB ADD PRIMARY KEY (id);</code>')
   + INFO_LINT
   + '<p><strong>Merke:</strong> Daten aus dem Netz kommen verzögert. <code>async</code>/<code>await</code> wartet darauf, <code>jsonDecode</code> macht aus JSON eine Map.</p>\n'
   '<p><strong>Denkfrage:</strong> Was würde passieren, wenn die App bei jeder Anfrage „einfrieren“ müsste, bis der Pi antwortet?</p>'),
 ziel(figur('browser_adresse', 'Firefox-Adresszeile mit …/php-crud-api/api.php/records/flutterTB/1', 'Erst im Browser testen (eigene IP einsetzen)'),
      figur('json_einzeln', 'JSON-Ansicht: id 1, name, passwordLogin', 'So sieht die Map aus, die loadContactData() liefert')) +
 baumkarte('Dateien im Projekt', dateien([('main.dart', '', False), ('my_first_app.dart', '', False), ('my_login.dart', 'Test in initState', True), ('webRequest.dart', 'ip, loadContactData()', True), ('todo_list.dart', '', False), ('todo_item.dart', '', False)])),
 '<h3>Was passiert beim Start?</h3>\n' + kette([('initState()', 'MyLogin startet'), ('loadContactData()', 'Future wird gestartet'), ('http.get', 'GET …/flutterTB/1'), ('await', 'warten auf JSON'), ('jsonDecode', 'JSON → Map'), ('print', 'Ausgabe in der Konsole')]),
 selbst(1, ['Der Browser zeigt mir …/flutterTB/1 und …/flutterTB/ als JSON.', 'Das Paket http ist eingebunden, webRequest.dart ist angelegt.', 'Beim Start der App erscheint der erste Benutzer in der Konsole.'],
   [('Was liefert <code>…/records/flutterTB/</code> ohne Zahl am Ende?',
     [('Alle Datensätze der Tabelle – als Liste unter dem Schlüssel <code>records</code>.', True, 'Mit /1 kommt nur der Datensatz mit der id 1.'),
      ('Nur den ersten Datensatz.', False, 'Dafür bräuchten Sie …/flutterTB/1.'),
      ('Eine Fehlermeldung.', False, 'Die id ist optional.')]),
    ('Warum ist <code>loadContactData()</code> <code>async</code>?',
     [('Die Daten kommen verzögert über das Netz – await wartet, ohne die App zu blockieren.', True, 'Deshalb liefert die Methode ein Future.'),
      ('Damit die Datenbank schneller antwortet.', False, 'async ändert nichts an der Geschwindigkeit.'),
      ('Weil jsonDecode sonst nicht funktioniert.', False, 'jsonDecode arbeitet sofort – gewartet wird auf http.get.')])]),
 ('level-2', 'Level 2')))

# ======================================================================= LEVEL 2  (Skript b)
L.append(level(2, 'Passwort aus der Datenbank verwenden', 'loadDataFromDB() und passwordLog – erster Vergleich',
 auftrag('Statt eines festen Passworts im Code vergleicht die Login-Maske jetzt mit dem Passwort aus der Datenbank (erster Datensatz von <code>flutterTB</code>).',
   '<code>lib/my_login.dart</code>', 'b – Passwort aus der Datenbank auslesen und verwenden',
   ['Entfernen Sie den Test aus Level 1 in <code>initState</code>.',
    'Neu im <code>_MyLoginState</code>: die Variable <code>String passwordLog = \'\';</code> und die Methode <code>loadDataFromDB()</code>. Sie holt die Map und weist <code>passwordLog</code> in <code>setState</code> das Passwort zu.',
    'Rufen Sie <code>loadDataFromDB()</code> einmal in <code>initState()</code> auf.',
    'Neue Methode <code>openList()</code>: öffnet mit <code>Navigator.of(context).push</code> die <code>ToDoList</code> (bisher stand das direkt im Button).',
    'Der Login-Button ruft <code>openList()</code> nur noch auf, wenn <code>_password == passwordLog</code>.',
    'Testen Sie mit dem Passwort aus der Datenbank – und mit einem falschen.'],
   '<h3>Erklärt – was passiert hier?</h3>\n'
   '<p>Aus der übergebenen Map wird das Passwort ausgelesen und einer Variablen zugewiesen. Gegen diese Variable prüft der Login.</p>\n'
   + dart(LOGIN_B) +
   '<ul><li><code>data["passwordLogin"]</code> greift auf den Wert zum Schlüssel <code>passwordLogin</code> der Map zu.</li>'
   '<li><code>setState</code> sorgt dafür, dass der neue Wert im State ankommt.</li>'
   '<li><code>openList()</code> kapselt die Navigation – so bleibt der Button übersichtlich.</li></ul>\n'
   + dart(BTN_B) +
   tipp('Der Login klappt nie?', 'Kommt das Passwort an? Fügen Sie in <code>loadDataFromDB</code> kurz <code>print(passwordLog);</code> ein. Groß-/Kleinschreibung beachten.')
   + tipp('Der Login klappt direkt nach dem Start nicht, kurz danach schon?', 'Die Daten kommen verzögert. Solange <code>passwordLog</code> noch leer ist, passt kein Passwort.')
   + '<p><strong>Kritisch betrachtet:</strong> Es wird nur gegen <b>ein</b> Passwort (Datensatz 1) geprüft, der Benutzername spielt keine Rolle. Das ändern Sie in Level 3.</p>\n'
   '<p><strong>Merke:</strong> Daten laden (<code>loadDataFromDB</code>), im State ablegen (<code>setState</code>), dann vergleichen.</p>\n'
   '<p><strong>Denkfrage:</strong> Sie ändern das Passwort in phpMyAdmin. Was müssen Sie tun, damit die App das neue Passwort kennt?</p>'),
 ziel(figur('login', 'Handy mit Login-Maske: Willkommen, Benutzername, Passwort, Login', 'Login-Maske – Passwort kommt aus flutterTB', breit=False)) +
 baumkarte('Widget-Baum', baum(('MyLogin', 'Stateful · passwordLog', True, [('Column', '', False, [('TextField', 'Benutzername', False, None), ('TextField', 'Passwort', False, None), ('TextButton', '_password == passwordLog → openList()', True, None)])]))),
 '<h3>Vom Datensatz zum Vergleich</h3>\n' + kette([('initState()', 'einmal beim Start'), ('loadDataFromDB()', 'await loadContactData()'), ('setState', 'passwordLog = data["passwordLogin"]'), ('Login-Button', '_password == passwordLog?'), ('openList()', 'ToDo-Liste öffnen')]),
 selbst(2, ['Mit dem Passwort aus Datensatz 1 öffnet sich die ToDo-Liste.', 'Mit einem falschen Passwort passiert nichts.', 'Im Code steht kein Passwort mehr fest.'],
   [('Wo wird <code>loadDataFromDB()</code> aufgerufen?',
     [('Einmal in <code>initState()</code>, beim Start der Login-Maske.', True, 'So liegen die Daten bereit, bevor jemand auf Login tippt.'),
      ('Bei jedem Tastendruck im Passwortfeld.', False, 'Das wäre bei jedem Zeichen eine neue Anfrage an den Pi.'),
      ('Gar nicht – das macht Flutter automatisch.', False, 'Die Methode muss aufgerufen werden.')]),
    ('Was ist die Schwäche dieser Lösung?',
     [('Geprüft wird nur das Passwort des ersten Datensatzes – der Name spielt keine Rolle.', True, 'Darum laden Sie in Level 3 alle Benutzer.'),
      ('Das Passwort steht im Code.', False, 'Gerade das ist jetzt nicht mehr so.'),
      ('Die App kann keine Daten laden.', False, 'Laden funktioniert – nur der Vergleich ist zu einfach.')])]),
 ('level-3', 'Level 3')))

# ======================================================================= LEVEL 3  (Skript c)
L.append(level(3, 'Name und Passwort prüfen', 'loadContactData_L(), data_L und where – die Login-Maske ist angebunden',
 auftrag('Zugang zur ToDo-Liste bekommt nur, wer eine Kombination aus Name <b>und</b> Passwort eingibt, die in <code>flutterTB</code> steht. Damit ist die Login-Maske an die Datenbank angebunden.',
   '<code>lib/webRequest.dart</code>, <code>lib/my_login.dart</code>', 'c – Passwort und LoginName aus der Datenbank auslesen und verwenden',
   ['<code>webRequest.dart</code>: Ergänzen Sie <code>loadContactData_L()</code> – sie holt <b>alle</b> Benutzer und gibt die Liste unter <code>records</code> zurück.',
    '<code>my_login.dart</code>: Legen Sie die Liste <code>List data_L = [];</code> in der Instanz an und die Methode <code>loadDataFromDB_L()</code>. <code>passwordLog</code> und <code>loadDataFromDB</code> aus Level 2 brauchen Sie nicht mehr.',
    'Rufen Sie <code>loadDataFromDB_L()</code> einmal in <code>initState()</code> auf.',
    'Im Login-Button: Suchen Sie mit <code>data_L.where(…)</code> ein Paar aus Name und Passwort. Ist <code>validName</code> nicht leer, öffnet <code>openList()</code> die Liste.',
    'Testen Sie mit zwei verschiedenen Benutzern aus der Datenbank und mit einem vertauschten Passwort.'],
   '<h3>Erklärt – was passiert hier?</h3>\n'
   '<p>Nur gegen ein Passwort zu prüfen ist nicht praktikabel. Sie brauchen die <b>Liste aller Benutzer</b> – also eine Methode, die in der Zukunft eine Liste zurückgibt:</p>\n'
   + dart(WEB_C) +
   '<p>Die Liste liegt im JSON unter <code>records</code> und muss deshalb herausgelöst werden.</p>\n' + dart(LOGIN_C) +
   '<p><code>loadDataFromDB_L()</code> muss einmal aufgerufen werden – Achtung, sie reagiert verzögert. Im Button wird dann gesucht:</p>\n' + dart(BTN_C) +
   tabelle(['Baustein', 'Bedeutung'], [
     ['<code>data_L.where(…)</code>', 'geht die Liste durch und behält nur die Einträge, für die die Bedingung <code>true</code> ist'],
     ['<code>validName</code>', 'enthält das passende Benutzer-Objekt – oder ist leer'],
     ['<code>validName.isNotEmpty</code>', 'für die Anmeldung reicht das Wissen, ob ein Objekt gefunden wurde']]) +
   '\n' + INFO_LINT +
   tipp('Login klappt nie, obwohl Name und Passwort stimmen?', 'Lassen Sie sich mit <code>print(data_L);</code> ausgeben, was ankommt. Leerzeichen am Ende des Namens? Groß-/Kleinschreibung?')
   + '<h3>Kritisch betrachtet</h3>\n<p>So funktioniert der Login – aber er ist <strong>nicht sicher</strong>: Die App lädt <b>alle</b> Benutzer mit ihren Passwörtern im Klartext über unverschlüsseltes HTTP. '
   'In einer echten App prüft der <b>Server</b> den Login, Passwörter liegen nur als <b>Hashwert</b> in der Datenbank, und die Verbindung läuft über <b>HTTPS</b>.</p>\n'
   '<p><strong>Merke:</strong> Erst alle Datensätze laden, dann mit <code>where</code> das passende Paar suchen, dann navigieren.</p>\n'
   '<p><strong>Denkfrage:</strong> Ein Mitschüler sitzt im selben WLAN und zeichnet den Netzwerkverkehr auf. Was sieht er, wenn Ihre App startet?</p>'),
 ziel(figur('json_benutzer', 'JSON-Ansicht von records mit mehreren Benutzern und ihren Passwörtern', 'Das steht in data_L – alle Benutzer mit Passwort')) +
 baumkarte('Dateien im Projekt', dateien([('webRequest.dart', '+ loadContactData_L()', True), ('my_login.dart', 'data_L, loadDataFromDB_L, where', True), ('todo_list.dart', '', False), ('todo_item.dart', '', False)])),
 '<h3>Ablauf in der App – Schritte 1 bis 3 gehören zum Login</h3>\n<div class="handys">' + figur('ablauf', 'Ablaufdiagramm: 1 Login öffnen, 2 REST-API liefert Login-Daten als JSON, 3 Prüfung, 4 ToDo-Liste lädt ToDos, 5 Plus-Button, 6 neues ToDo wird gesendet', 'Schritte 1–3: Login (Level 1–3) · Schritte 4–6: ToDo-Liste (Level 4–6)') + '</div>\n'
 + kette([('initState()', 'loadDataFromDB_L()'), ('loadContactData_L()', 'GET …/flutterTB/'), ('data_L', 'Liste aller Benutzer'), ('Login-Button', 'data_L.where(…)'), ('validName.isNotEmpty', 'openList()')]),
 selbst(3, ['Mit Name und Passwort eines Benutzers aus flutterTB komme ich zur ToDo-Liste.', 'Mit dem Namen des einen und dem Passwort eines anderen Benutzers komme ich nicht hinein.', 'Ich kann erklären, warum diese Lösung nicht sicher ist.'],
   [('Was steht in <code>validName</code>, wenn Name und Passwort falsch sind?',
     [('Nichts – die Ergebnisliste von where ist leer.', True, 'Darum wird isNotEmpty geprüft.'),
      ('false', False, 'where liefert eine Sammlung von Einträgen, keinen Wahrheitswert.'),
      ('Der erste Benutzer der Tabelle.', False, 'where behält nur Einträge, für die die Bedingung stimmt.')]),
    ('Warum ist dieser Login in einer echten App unsicher?',
     [('Alle Passwörter werden im Klartext über HTTP an jedes Gerät geschickt.', True, 'Besser: Prüfung auf dem Server, Hashwerte und HTTPS.'),
      ('Weil where zu langsam ist.', False, 'Es geht um die Daten, die über das Netz gehen.'),
      ('Weil der Button grau sein kann.', False, 'Das ist Bedienkomfort, keine Sicherheitsfrage.')])]),
 ('level-4', 'Level 4')))

# ======================================================================= LEVEL 4  (Skript d, e)
L.append(level(4, 'ToDo-Objekte und Liste', 'ToDoListObject, List statt Map, ToDoItem mit id',
 auftrag('Jedes ToDo bekommt eine eindeutige <code>id</code> – die braucht die Datenbank. Aus der Map der Einführung wird eine Liste von <code>ToDoListObject</code>-Objekten. Noch arbeitet die Liste ohne Datenbank.',
   'neu: <code>lib/todo_list_object.dart</code>, <code>lib/todo_item.dart</code>, <code>lib/todo_list.dart</code>', 'd – Erstellen einer Liste mit ToDo-Objekten, e – ToDo-Objekt, ToDoItem/Widget und Liste anlegen',
   ['Legen Sie <code>lib/todo_list_object.dart</code> an mit der Klasse <code>ToDoListObject</code>: <code>id</code>, <code>name</code>, <code>checkbox</code> und dem Konstruktor <code>ToDoListObject(this.id, this.checkbox, this.name)</code>.',
    '<code>todo_item.dart</code>: <code>ToDoItem</code> bekommt als erstes Feld <code>final int id;</code> – auch im Konstruktor an erster Stelle.',
    '<code>todo_list.dart</code>: Ersetzen Sie die <code>Map&lt;String, bool&gt; todos</code> durch <code>List&lt;ToDoListObject&gt; todos = [];</code>.',
    'Bauen Sie den <code>ListView.builder</code> um: Er gibt <code>id</code>, <code>name</code> und <code>checkbox</code> aus <code>todos[i]</code> an das <code>ToDoItem</code> weiter.',
    'Passen Sie <code>addItem</code>, <code>deleteItem(int id)</code> und <code>checkBoxDone(int id)</code> an die Liste an (siehe unten).',
    'Testen Sie: anlegen, abhaken, löschen – noch ohne Datenbank.'],
   '<h3>Erklärt – was passiert hier?</h3>\n'
   '<p><strong>Warum keine Map mehr?</strong> Bisher hatte ein ToDo zwei Eigenschaften (<code>checkbox</code>, <code>name</code>), der Name war der Schlüssel. '
   'Für die Datenbank braucht jedes ToDo eine eindeutige <b>id</b>. Das erlaubt die Map nicht – deshalb eine Liste von Objekten.</p>\n'
   + dart(OBJEKT) +
   '<p>Damit aus der Datenbank und aus dem Alert-Dialog Daten übergeben werden können, wird diese Klasse benötigt. Achtung: Im Konstruktor steht <code>checkbox</code> <b>vor</b> <code>name</code>.</p>\n'
   + tabelle(['Tabelle ToDoTB', 'ToDoListObject', 'ToDoItem'], [['<code>id</code>', '<code>int id</code>', '<code>final int id</code> (neu)'], ['<code>name</code>', '<code>String name</code>', '<code>final String title</code>'], ['<code>checkbox</code>', '<code>bool checkbox</code>', '<code>final bool done</code>']]) +
   '\n<p>Der <code>ListView.builder</code> geht die Liste durch und gibt die Werte an das <code>ToDoItem</code> weiter:</p>\n' + dart(BUILDER) +
   '<p>Die Methoden arbeiten jetzt mit der <code>id</code>:</p>\n' + dart(M4_ADD + '\n\n' + M4_DEL + '\n\n' + M4_CHECK) +
   '<ul><li><code>firstWhere</code> sucht das erste Element mit dieser id.</li><li><code>removeWhere</code> entfernt alle Elemente, für die die Bedingung stimmt.</li>'
   '<li><code>todos.length + 1</code> als neue id – so steht es im Skript. In Level 6 sehen Sie, wo das an Grenzen stößt.</li></ul>\n'
   + tipp('„Too many positional arguments“ beim ToDoItem?', 'Haben Sie das Feld <code>id</code> in <code>todo_item.dart</code> auch im Konstruktor ergänzt – an erster Stelle?')
   + tipp('„The getter \'name\' isn\'t defined for the type \'String\'“?', 'Irgendwo steht noch Code der alten Map, z. B. <code>todos.keys</code>. <code>todos[i]</code> ist jetzt ein <code>ToDoListObject</code>.')
   + '<p><strong>Merke:</strong> Ein Objekt bündelt die Werte eines Datensatzes – die <code>id</code> macht jedes ToDo eindeutig.</p>\n'
   '<p><strong>Denkfrage:</strong> Zwei ToDos heißen „Einkaufen“. Was wäre mit der Map passiert – und was passiert jetzt?</p>'),
 ziel(figur('datenfluss', 'Datenfluss: Eingabedialog mit addItem, Objekt mit id 6, checkbox false, name Netzplan, Liste todos, Datenbank todoListDB mit loadDataFromDBToDo', 'Vom Eingabedialog zum Objekt in der Liste todos')) +
 baumkarte('Widget-Baum', baum(('ToDoList', 'Stateful · List&lt;ToDoListObject&gt; todos', True, [('Scaffold', '', False, [('ListView.builder', 'todos[i] → ToDoItem', True, [('ToDoItem', 'id, name, checkbox, …', True, None)]), ('FloatingActionButton', 'newEntry', False, None)])]))),
 '<h3>Von der Map zur Liste von Objekten</h3>\n<div class="zwei">'
 '<div class="kasten"><b>Flutter-Einführung</b><small>Map&lt;String, bool&gt;</small><table><tr><td>\'Milch kaufen\'</td><td>true</td></tr><tr><td>\'LF11 lernen\'</td><td>false</td></tr></table></div>'
 '<div class="verbindung"><span>→</span></div>'
 '<div class="kasten state"><b>Jetzt</b><small>List&lt;ToDoListObject&gt;</small><table><tr><td>id 1</td><td>false</td><td>Projektplan</td></tr><tr><td>id 2</td><td>true</td><td>Gruppeneinteilung</td></tr></table></div></div>\n'
 '<p class="klein">Der Name ist kein Schlüssel mehr – jedes ToDo wird über seine <code>id</code> eindeutig erkannt.</p>',
 selbst(4, ['Ich kann ToDos anlegen, abhaken und löschen – jetzt mit der Liste von ToDoListObject.', 'ToDoItem bekommt die id als ersten Wert.', 'Zwei ToDos mit gleichem Namen werden beide angezeigt.'],
   [('Warum wird aus der Map eine Liste von Objekten?',
     [('Jedes ToDo braucht eine eindeutige id für die Datenbank – das erlaubt die Map mit dem Namen als Schlüssel nicht.', True, 'Die id ist der Primärschlüssel in ToDoTB.'),
      ('Weil Listen schneller sind.', False, 'Es geht um die eindeutige id.'),
      ('Weil Flutter keine Maps mehr unterstützt.', False, 'Maps gibt es weiterhin.')]),
    ('Was liefert <code>todos.firstWhere((element) =&gt; element.id == id)</code>?',
     [('Das erste ToDo-Objekt mit dieser id.', True, 'Danach kann dessen checkbox geändert werden.'),
      ('Die Position in der Liste.', False, 'Dafür gäbe es indexWhere.'),
      ('Alle ToDos mit dieser id als Liste.', False, 'Das wäre where.')])]),
 ('level-5', 'Level 5')))

# ======================================================================= LEVEL 5  (Skript f, g)
L.append(level(5, 'CRUD-Methoden und ToDos laden', 'webRequest erweitern, loadDataFromDBToDo() in initState',
 auftrag('<code>webRequest.dart</code> bekommt die vier CRUD-Methoden. Die ToDo-Liste lädt beim Öffnen die ToDos aus der Tabelle <code>ToDoTB</code>.',
   'Datenbank auf dem Pi, <code>lib/webRequest.dart</code>, <code>lib/todo_list.dart</code>', 'f – Anbindung an die Datenbank erweitern – CRUD-REST-API, g – Aktualisieren der Methoden (loadDataFromDBToDo, initState)',
   ['Legen Sie auf dem Pi die Tabelle <code>ToDoTB</code> an (SQL unten) und prüfen Sie <code>…/records/ToDoTB/</code> im Browser.',
    '<code>webRequest.dart</code>: <code>todo_list_object.dart</code> importieren und die Methoden <code>loadDataToDo()</code>, <code>sendDS()</code>, <code>deletDS()</code> und <code>updateDS()</code> ergänzen.',
    '<code>todo_list.dart</code>: <code>webRequest.dart</code> importieren, die Liste <code>List dataToDo = [];</code> und die Methode <code>loadDataFromDBToDo()</code> anlegen.',
    'Überschreiben Sie <code>initState()</code> und rufen Sie darin <code>loadDataFromDBToDo()</code> auf.',
    'Testen Sie: Nach dem Login erscheinen die ToDos aus der Datenbank.'],
   '<h3>Erklärt – was passiert hier?</h3>\n'
   '<p><strong>Die Tabelle für die ToDos</strong> muss in der Datenbank noch angelegt werden (Skript, Kapitel d):</p>\n' + roh(SQL_TODO) +
   tipp('Sie haben ToDoTB schon im REST-Lernpfad angelegt (Spalten titel/erledigt)?', 'Benennen Sie die Spalten wie im Skript um:<br><code>ALTER TABLE ToDoTB RENAME COLUMN titel TO name, RENAME COLUMN erledigt TO checkbox;</code>') +
   '<p><strong>CRUD</strong> – die php-crud-api auf dem Pi ermöglicht vier Operationen:</p>\n'
   + tabelle(['CRUD', 'HTTP', 'Methode in webRequest.dart', 'Adresse'], [
       ['Create – anlegen', 'POST', '<code>sendDS(newItem)</code>', '…/ToDoTB/'],
       ['Read – auslesen', 'GET', '<code>loadDataToDo()</code>', '…/ToDoTB/'],
       ['Update – ändern', 'PUT', '<code>updateDS(updItem)</code>', '…/ToDoTB/ + id'],
       ['Delete – löschen', 'DELETE', '<code>deletDS(newItem)</code>', '…/ToDoTB/ + id']]) +
   '\n' + dart(WEB_F_READ) + dart(WEB_F_CREATE) + dart(WEB_F_DELETE) + dart(WEB_F_UPDATE) +
   '<p>Beim Abruf der ToDos kommt eine Liste. Sie wird beim Aufbau des Screens in Objekte umgewandelt und in <code>todos</code> abgelegt:</p>\n' + dart(LADEN) +
   '<p><code>initState()</code> wird beim Aufruf des States eines Stateful Widgets ausgeführt. Sie können die Methode überschreiben und so die Daten der Datenbank in die Liste übertragen.</p>\n'
   + tipp('„type \'int\' is not a subtype of type \'bool\'“?', 'Die Spalte <code>checkbox</code> kommt als 0/1 statt true/false an. Legen Sie sie als <code>BOOLEAN</code> an – oder schreiben Sie <code>element[\'checkbox\'] == true || element[\'checkbox\'] == 1</code>.')
   + tipp('Liste bleibt leer?', 'Steht etwas in ToDoTB? Fehlt <code>setState(() {});</code> am Ende von <code>loadDataFromDBToDo</code>?')
   + INFO_LINT
   + '<p><strong>Merke:</strong> Daten aus dem Netz werden in <code>initState</code> angestoßen und mit <code>setState</code> angezeigt, sobald sie da sind.</p>\n'
   '<p><strong>Denkfrage:</strong> Legen Sie jetzt ein ToDo an und starten Sie die App neu. Warum ist es weg – die ToDos aus der Datenbank aber nicht?</p>'),
 ziel(figur('ablauf', 'Ablaufdiagramm: Schritt 4 – die ToDo-Liste lädt die ToDos als JSON von der REST-API', 'Schritt 4: Die ToDo-Liste lädt die ToDos aus der Datenbank')) +
 baumkarte('Dateien im Projekt', dateien([('webRequest.dart', '+ loadDataToDo, sendDS, deletDS, updateDS', True), ('todo_list_object.dart', '', False), ('todo_list.dart', 'dataToDo, loadDataFromDBToDo, initState', True), ('todo_item.dart', '', False)])),
 '<h3>Vom Datensatz zum ToDo auf dem Bildschirm</h3>\n' + kette([('initState()', 'ToDo-Liste öffnet'), ('loadDataToDo()', 'GET …/ToDoTB/'), ('dataToDo', 'Liste aus records'), ('ToDoListObject(…)', 'je Datensatz ein Objekt'), ('todos.add', 'in die Liste'), ('setState', 'neu zeichnen')]),
 selbst(5, ['Die Tabelle ToDoTB existiert, …/records/ToDoTB/ zeigt meine Test-ToDos.', 'Nach dem Login sehe ich die ToDos aus der Datenbank.', 'webRequest.dart enthält loadDataToDo, sendDS, deletDS und updateDS.'],
   [('Welche HTTP-Methode benutzt <code>sendDS</code>?',
     [('POST – Create', True, 'POST legt einen neuen Datensatz an.'), ('GET – Read', False, 'GET liest nur.'), ('PUT – Update', False, 'PUT ändert einen vorhandenen Datensatz.')]),
    ('Warum steht bei <code>deletDS</code> und <code>updateDS</code> die id in der Adresse?',
     [('Die API muss wissen, welcher Datensatz gemeint ist – über den Primärschlüssel.', True, 'Z. B. …/ToDoTB/3 für das ToDo mit der id 3.'),
      ('Damit die Adresse länger ist.', False, 'Die id bestimmt den Datensatz.'),
      ('Weil sonst die ganze Datenbank gelöscht wird.', False, 'Ohne id meldet die API einen Fehler – sie braucht die id.')])]),
 ('level-6', 'Level 6')))

# ======================================================================= LEVEL 6  (Aufgabe 3)
L.append(level(6, 'Methoden anpassen', 'Aufgabe 3 – Anlegen, Löschen und Abhaken landen in der Datenbank',
 auftrag('Die Methoden der ToDo-Liste rufen jetzt die passenden Methoden aus <code>webRequest.dart</code> auf. Damit ist auch die ToDo-Liste vollständig an die Datenbank angebunden.',
   '<code>lib/todo_list.dart</code>', 'Aufgabe 3: Methoden anpassen',
   ['<code>addItem</code>: Nach <code>todos.add(newtodo)</code> das neue Objekt mit <code>sendDS(newtodo)</code> an die Datenbank schicken.',
    '<code>deleteItem</code>: Das Objekt mit <code>firstWhere</code> suchen, mit <code>deletDS(…)</code> in der Datenbank löschen, dann aus der Liste entfernen.',
    '<code>checkBoxDone</code>: Nach dem Umschalten mit <code>updateDS(…)</code> den neuen Status speichern.',
    'Abschlusstest: anlegen, abhaken, löschen – App beenden, neu starten, einloggen. Alles muss so sein wie vorher. Prüfen Sie zusätzlich <code>…/records/ToDoTB/</code> im Browser.'],
   '<h3>Erklärt – was passiert hier?</h3>\n'
   '<p>Die Oberfläche bleibt, wie sie ist. Jede Methode, die Daten verändert, gibt die Änderung zusätzlich an die Datenbank weiter:</p>\n'
   + dart(M6_ADD) + dart(M6_DEL) + dart(M6_CHECK) +
   tabelle(['Methode in todo_list.dart', 'ruft auf', 'CRUD'], [['<code>loadDataFromDBToDo</code>', '<code>loadDataToDo()</code>', 'Read'], ['<code>addItem</code>', '<code>sendDS()</code>', 'Create'], ['<code>checkBoxDone</code>', '<code>updateDS()</code>', 'Update'], ['<code>deleteItem</code>', '<code>deletDS()</code>', 'Delete']]) +
   '\n' + tipp('Neues ToDo ist nach dem Neustart weg?', 'Steht es im Browser in ToDoTB? Wenn nicht: Gibt es die id schon? Siehe „Kritisch betrachtet“.')
   + '<h3>Kritisch betrachtet</h3>\n'
   '<p><strong>Die id <code>todos.length + 1</code>:</strong> Sie haben die ToDos 1, 2 und 3 und löschen ToDo 2. Das nächste neue ToDo bekommt die id 3 – die gibt es schon. '
   'Die Datenbank lehnt den Datensatz ab, die App zeigt ihn trotzdem an. Bessere Lösungen: die höchste vorhandene id + 1 – oder die Datenbank vergibt die id selbst (<code>AUTO_INCREMENT</code>) und die API meldet sie nach dem POST zurück.</p>\n'
   '<p><strong>Keine Fehlerprüfung:</strong> Die Methoden warten nicht auf die Antwort des Servers. Ist der Pi aus, zeigt die App Änderungen, die nie gespeichert werden.</p>\n'
   '<p><strong>Merke:</strong> POST legt an, GET liest, PUT ändert, DELETE löscht – die id in der Adresse sagt, <b>welcher</b> Datensatz gemeint ist.</p>\n'
   '<p><strong>Denkfrage:</strong> Zwei Handys sind eingeloggt. Auf dem einen wird ein ToDo abgehakt. Wann sieht das andere Handy den Haken? (Skript: Refresh-Button)</p>'),
 ziel(figur('methoden', 'Dart-Methoden addItem, deleteItem und checkBoxDone mit Kommentaren', 'Diese drei Methoden sprechen jetzt mit der Datenbank')) +
 baumkarte('Dateien im Projekt', dateien([('webRequest.dart', 'Login und CRUD', False), ('my_login.dart', 'Login gegen flutterTB', False), ('todo_list_object.dart', 'id, name, checkbox', False), ('todo_list.dart', 'sendDS, deletDS, updateDS', True), ('todo_item.dart', 'mit id', False)])),
 '<h3>Ablauf in der App – Schritte 5 und 6</h3>\n<div class="handys">' + figur('ablauf', 'Ablaufdiagramm: Schritt 5 Plus-Button öffnet Eingabe, Schritt 6 neues ToDo geht als JSON an die REST-API und erscheint in der Liste', 'Schritt 5: neues ToDo eingeben · Schritt 6: in die Liste und an die Datenbank') + '</div>\n'
 + kette([('Create', 'addItem → sendDS'), ('Read', 'loadDataFromDBToDo → loadDataToDo'), ('Update', 'checkBoxDone → updateDS'), ('Delete', 'deleteItem → deletDS')]),
 selbst(6, ['Ein neues ToDo steht nach dem Anlegen in ToDoTB (Browser prüfen).', 'Abhaken und Löschen sind nach einem Neustart der App noch so.', 'Ich kann zu jeder Methode in todo_list.dart die Methode aus webRequest.dart und die CRUD-Operation nennen.'],
   [('Welche Methode aus <code>webRequest.dart</code> ruft <code>checkBoxDone</code> auf?',
     [('<code>updateDS</code> – Update mit PUT', True, 'Sie schickt nur die geänderte Spalte checkbox.'),
      ('<code>sendDS</code>', False, 'sendDS legt einen neuen Datensatz an.'),
      ('<code>loadDataToDo</code>', False, 'loadDataToDo liest nur.')]),
    ('Was passiert mit <code>todos.length + 1</code>, nachdem ein ToDo aus der Mitte gelöscht wurde?',
     [('Die neue id kann es schon geben – die Datenbank lehnt den Datensatz ab.', True, 'Abhilfe: höchste id + 1 oder AUTO_INCREMENT.'),
      ('Nichts – die id ist immer eindeutig.', False, 'Nach dem Löschen stimmt die Anzahl nicht mehr mit der höchsten id überein.'),
      ('Die App stürzt sofort ab.', False, 'Die App zeigt das ToDo – gespeichert wird es aber nicht.')])]),
 ('wissen', '📘 Wissen')))

# ======================================================================= WISSEN
WISSEN = '''<section class="ansicht" id="wissen">
  <div class="card level-kopf"><span class="nummer" aria-hidden="true">📘</span>
    <div><h2>Wissen: Flutter und REST</h2><p class="stich">Zum Nachschlagen – alles, was die Level voraussetzen</p></div></div>
  <nav class="card inhalt-navi" aria-label="Inhalt"><a href="#w-weg">1 · Der Weg der Daten</a> · <a href="#w-crud">2 · CRUD in webRequest.dart</a> · <a href="#w-json">3 · JSON in Dart</a> · <a href="#w-async">4 · async und await</a> · <a href="#w-fehler">5 · Typische Fehler</a></nav>
  <div class="card" id="w-weg"><h3>1 · Der Weg der Daten</h3>
    ''' + kette([('Widget', 'Button, Checkbox …'), ('State-Methode', 'addItem, loadDataFromDB_L …'), ('webRequest.dart', 'sendDS, loadDataToDo …'), ('HTTP', 'GET, POST, PUT, DELETE'), ('php-crud-api', 'auf dem Pi'), ('MariaDB', 'flutterDB')]) + '''
    <p>Die Oberfläche kennt keine Adressen und kein JSON – das steckt in <code>webRequest.dart</code>.</p></div>
  <div class="card" id="w-crud"><h3>2 · CRUD in webRequest.dart</h3>
    ''' + tabelle(['CRUD', 'HTTP', 'Adresse', 'SQL', 'webRequest.dart', 'aufgerufen von'], [
        ['Create', 'POST', '…/records/ToDoTB/', 'INSERT', '<code>sendDS</code>', '<code>addItem</code>'],
        ['Read', 'GET', '…/records/ToDoTB/', 'SELECT', '<code>loadDataToDo</code>', '<code>loadDataFromDBToDo</code>'],
        ['Update', 'PUT', '…/records/ToDoTB/3', 'UPDATE', '<code>updateDS</code>', '<code>checkBoxDone</code>'],
        ['Delete', 'DELETE', '…/records/ToDoTB/3', 'DELETE', '<code>deletDS</code>', '<code>deleteItem</code>']]) + '''
    <p>Für den Login: <code>loadContactData()</code> (ein Datensatz, <code>…/flutterTB/1</code>) und <code>loadContactData_L()</code> (alle, <code>…/flutterTB/</code>).</p></div>
  <div class="card" id="w-json"><h3>3 · JSON in Dart</h3>
    ''' + tabelle(['JSON', 'Dart nach jsonDecode', 'Zugriff'], [
        ['<code>{"id":1,"name":"berno","passwordLogin":"…"}</code>', 'Map', "<code>data['passwordLogin']</code>"],
        ['<code>[ {…}, {…} ]</code>', 'List', '<code>data_L[0]</code>'],
        ['<code>{"records":[{…},{…}]}</code>', 'Map mit einer List darin', "<code>responseJson['records']</code>"]]) + '''</div>
  <div class="card" id="w-async"><h3>4 · async und await</h3>
    <p>Eine Anfrage ans Netz dauert. Statt die App anzuhalten, liefert sie ein <code>Future</code> – ein Versprechen auf ein späteres Ergebnis.</p>
    ''' + dart("""Future<List> loadContactData_L() async {   // async: hier darf gewartet werden
  var response = await http.get(url);        // await: warten, App läuft weiter
  return jsonDecode(response.body)['records'];
}

void loadDataFromDB_L() async {
  data_L = await loadContactData_L();       // Ergebnis abholen
}""") + '''
    <p>Solche Methoden werden einmal in <code>initState()</code> aufgerufen. Erst <code>setState</code> zeigt neue Daten auf dem Bildschirm an.</p></div>
  <div class="card" id="w-fehler"><h3>5 · Typische Fehler</h3>
    ''' + tabelle(['Meldung / Verhalten', 'Ursache', 'Abhilfe'], [
        ['SocketException, Connection refused', 'IP falsch, Pi nicht erreichbar', 'Adresse zuerst im Browser testen, ip in webRequest.dart prüfen'],
        ['Cleartext HTTP traffic not permitted', 'Android blockiert http://', '<code>usesCleartextTraffic="true"</code> im Manifest'],
        ['Nichts passiert nach Änderung in initState', 'Hot Reload führt initState nicht erneut aus', 'App neu starten'],
        ['Fehler zum Primärschlüssel', 'Tabelle ohne PRIMARY KEY', '<code>ALTER TABLE … ADD PRIMARY KEY (id)</code>'],
        ["type 'int' is not a subtype of type 'bool'", 'checkbox kommt als 0/1', 'Spalte als BOOLEAN anlegen'],
        ['Neues ToDo nach Neustart weg', 'id doppelt (todos.length + 1)', 'höchste id + 1 verwenden'],
        ['Blaue Hinweise zu webRequest.dart, data_L', 'Namenskonventionen von Dart', 'Namen bleiben wie im Skript – nur Hinweise']]) + '''</div>
  <div class="card lp-fuss"><a class="knopf" href="#level-6">◀ Level 6</a><a class="knopf primaer" href="#start">Zum Start ▶</a></div>
</section>
'''

# ======================================================================= START
UEB = [('level-1', 'json_einzeln', '1 · http und erster Abruf', 'webRequest.dart, loadContactData()'),
       ('level-2', 'login', '2 · Passwort aus der Datenbank', 'loadDataFromDB(), passwordLog'),
       ('level-3', 'json_benutzer', '3 · Name und Passwort prüfen', 'loadContactData_L(), where'),
       ('level-4', 'datenfluss', '4 · ToDo-Objekte und Liste', 'ToDoListObject, ToDoItem mit id'),
       ('level-5', 'ablauf', '5 · CRUD und ToDos laden', 'loadDataToDo, initState'),
       ('level-6', 'methoden', '6 · Methoden anpassen', 'sendDS, deletDS, updateDS')]
START = '''<section class="ansicht" id="start">
    <div class="card echt"><span aria-hidden="true">🗄️</span><div>
      <b>Sie bauen weiter an Ihrer App aus der <a href="../flutter/">Flutter-Einführung</a>.</b> Dieser Lernpfad folgt dem Skript, Kapitel
      <i>Datenbankanbindung umsetzen – WebRequest in Flutter</i> (Abschnitte a–g und Aufgabe 3): Zuerst binden Sie die <b>Login-Maske</b>,
      danach die <b>ToDo-Liste</b> an die Datenbank auf Ihrem Raspberry Pi an.</div></div>
    <div class="card"><h2>Voraussetzungen</h2>
      <div class="start-raster">
        <div><h3>1 · Ihre App</h3><p>Projekt <code>meine_app</code> mit Login-Maske und ToDo-Liste – Level 9 der Flutter-Einführung ist geschafft.</p></div>
        <div><h3>2 · Ihr Pi</h3><p>Datenbank <code>flutterDB</code> mit Tabelle <code>flutterTB</code> und die REST-API <code>php-crud-api</code> sind eingerichtet (Skript Aufgabe 2 bzw. <a href="https://bnbsinfo.github.io/lf11_lernpfade/rest/">REST-Lernpfad</a>).</p></div>
        <div><h3>3 · Abtippen</h3><p>Code wird <b>abgetippt</b> – Kopieren ist gesperrt. Dateien und Methoden heißen wie im Skript.</p></div>
        <div><h3>4 · Selbstkontrolle</h3><p>Unter jedem Level: Haken setzen, was wirklich funktioniert, Kontrollfragen beantworten – dann ist das Level geschafft.</p></div>
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
