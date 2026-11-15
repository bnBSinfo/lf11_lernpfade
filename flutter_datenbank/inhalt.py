# Code des Lernpfads "Flutter – Datenbankanbindung" (Level 1–6)
# Folgt dem Skript (Kapitel "Datenbankanbindung umsetzen", Abschnitte a–g, Aufgabe 3):
# webRequest.dart · ToDoListObject · Tabellen flutterTB (name, passwordLogin) und ToDoTB (id, name, checkbox)
from html import escape as e

def dart(code):
    return f'<pre class="dart"><code>{e(code.strip(chr(10)))}</code></pre>'

def roh(code):
    return f'<pre><code>{e(code.strip(chr(10)))}</code></pre>'

def tipp(titel, text):
    return f'<details><summary>Tipp – {titel}</summary>\n<p>{text}</p>\n</details>'

def tabelle(kopf, zeilen):
    h = ''.join(f'<th>{k}</th>' for k in kopf)
    z = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in zeilen)
    return f'<table>\n<thead><tr>{h}</tr></thead>\n<tbody>{z}</tbody>\n</table>'

def kette(schritte):
    teile = []
    for i, (b, s) in enumerate(schritte):
        if i:
            teile.append('<span class="pfeil" aria-hidden="true">→</span>')
        teile.append(f'<div class="schritt-box"><b>{b}</b><span>{s}</span></div>')
    return '<div class="kette">' + ''.join(teile) + '</div>'

def ind(code, n):
    return '\n'.join((' ' * n + z) if z.strip() else '' for z in code.split('\n'))

# ---------------------------------------------------------------- webRequest.dart
WEB_KOPF = """import 'dart:convert';

import 'package:http/http.dart' as http;
@@IMPORT@@
// IP-Adresse Ihres Raspberry Pi – nur hier ändern
const String ip = '192.168.0.10';
"""

WEB_B = """// einen Datensatz (den ersten) der Tabelle flutterTB abrufen
Future<Map> loadContactData() async { // asynchrone Methode
  var url = Uri.parse('http://$ip/php-crud-api/api.php/records/flutterTB/1');
  var response = await http.get(url); // await wartet, bis die Daten da sind
  var responseJson = jsonDecode(response.body); // wandelt den JSON in eine Map um
  return responseJson;
}"""

WEB_C = """// Abruf aller Daten der Tabelle
Future<List> loadContactData_L() async {
  var url = Uri.parse('http://$ip/php-crud-api/api.php/records/flutterTB/');
  var response = await http.get(url); // await wartet, bis die Daten da sind
  var responseJson = jsonDecode(response.body);
  var userList = responseJson['records']; // die Liste liegt unter records
  return userList;
}"""

WEB_F_READ = """// Abruf der Daten für die ToDoListe
Future<List> loadDataToDo() async {
  var url = Uri.parse('http://$ip/php-crud-api/api.php/records/ToDoTB/');
  var response = await http.get(url);
  var responseJson = jsonDecode(response.body);
  var toDoList = responseJson['records'];
  return toDoList;
}"""

WEB_F_CREATE = """// Senden eines kompletten Datensatzes an die Datenbank
Future<void> sendDS(ToDoListObject newItem) async {
  var url = Uri.parse('http://$ip/php-crud-api/api.php/records/ToDoTB/');
  await http.post(url, body: {
    'id': newItem.id.toString(),
    'checkbox': '0',
    'name': newItem.name,
  });
}"""

WEB_F_DELETE = """// Löschen eines Datensatzes – die id steht im Pfad
Future<void> deletDS(ToDoListObject newItem) async {
  var url = Uri.parse(
      'http://$ip/php-crud-api/api.php/records/ToDoTB/' + newItem.id.toString());
  await http.delete(url);
}"""

WEB_F_UPDATE = """// Update eines Attributes aus dem Datensatz
Future<void> updateDS(ToDoListObject updItem) async {
  var url = Uri.parse(
      'http://$ip/php-crud-api/api.php/records/ToDoTB/' + updItem.id.toString());
  int updI = updItem.checkbox ? 1 : 0; // Kurzschreibweise
  await http.put(url, body: {'checkbox': updI.toString()}); // put = Update
}"""

def web(level):
    teile = [WEB_B]
    if level >= 3:
        teile.append(WEB_C)
    if level >= 5:
        teile += [WEB_F_READ, WEB_F_CREATE, WEB_F_DELETE, WEB_F_UPDATE]
    imp = "\nimport 'todo_list_object.dart';\n" if level >= 5 else ''
    return WEB_KOPF.replace('@@IMPORT@@', imp) + '\n' + '\n\n'.join(teile) + '\n'

# ---------------------------------------------------------------- my_login.dart
TEST_L1 = """@override
void initState() {
  super.initState();
  loadContactData().then((data) {
    print(data);                   // erscheint in der Konsole (Run/Debug)
    print(data['passwordLogin']);
  });
}"""

LOGIN_B = """String passwordLog = '';

@override
void initState() {
  super.initState();
  loadDataFromDB(); // einmal beim Start der Login-Maske
}

void loadDataFromDB() async {
  Map data = await loadContactData();
  setState(() {
    passwordLog = data['passwordLogin'];
  });
}

void openList() {
  Navigator.of(context).push(
    MaterialPageRoute(builder: (context) => const ToDoList()),
  );
}"""

BTN_B = """TextButton(
  onPressed: _canLogin
      ? () {
          if (_password == passwordLog) {
            openList();
          }
        }
      : null,
  child: const Text('Login'),
),"""

LOGIN_C = """List data_L = []; // Liste aller Benutzer

@override
void initState() {
  super.initState();
  loadDataFromDB_L(); // einmal beim Start – die Daten kommen verzögert
}

void loadDataFromDB_L() async {
  data_L = await loadContactData_L();
}

void openList() {
  Navigator.of(context).push(
    MaterialPageRoute(builder: (context) => const ToDoList()),
  );
}"""

BTN_C = """TextButton(
  onPressed: _canLogin
      ? () {
          // iteriert die Liste und sucht ein passendes Paar aus Name und Passwort
          var validName = data_L.where((element) {
            return element['name'] == _username &&
                element['passwordLogin'] == _password;
          });
          if (_canLogin == true && validName.isNotEmpty) {
            openList();
          }
        }
      : null,
  child: const Text('Login'),
),"""

BTN_ALT = """TextButton(
  onPressed: _canLogin
      ? () {
          Navigator.of(context).push(
            MaterialPageRoute(builder: (context) => const ToDoList()),
          );
        }
      : null,
  child: const Text('Login'),
),"""

LOGIN_FULL = """import 'package:flutter/material.dart';

import 'todo_list.dart';
import 'webRequest.dart';

class MyLogin extends StatefulWidget {
  const MyLogin({super.key});

  @override
  State<MyLogin> createState() => _MyLoginState();
}

class _MyLoginState extends State<MyLogin> {
  String _username = '';
  String _password = '';
  bool _canLogin = false;
@@EXTRA@@
  void _checkCanLogin() {
    setState(() {
      _canLogin = _username.isNotEmpty && _password.isNotEmpty;
    });
  }

  void _onChangedUsername(String username) {
    _username = username;
    _checkCanLogin();
  }

  void _onChangedPassword(String password) {
    _password = password;
    _checkCanLogin();
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: SizedBox(
        width: 300,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Willkommen'),
            TextField(
              onChanged: _onChangedUsername,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Benutzername',
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              onChanged: _onChangedPassword,
              obscureText: true,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Passwort',
              ),
            ),
@@BUTTON@@
          ],
        ),
      ),
    );
  }
}
"""

def login(level):
    extra, btn = {1: (TEST_L1, BTN_ALT), 2: (LOGIN_B, BTN_B), 3: (LOGIN_C, BTN_C)}[level]
    return LOGIN_FULL.replace('@@EXTRA@@', '\n' + ind(extra, 2) + '\n').replace('@@BUTTON@@', ind(btn, 12))

# ---------------------------------------------------------------- ToDo-Teil
OBJEKT = """class ToDoListObject {
  int id;
  String name;
  bool checkbox;

  ToDoListObject(this.id, this.checkbox, this.name);
}"""

ITEM = """import 'package:flutter/material.dart';

class ToDoItem extends StatelessWidget {
  final int id; // neu: eindeutige id aus der Datenbank
  final String title;
  final bool done;
  final VoidCallback remove;
  final VoidCallback checkBoxDone;

  const ToDoItem(this.id, this.title, this.done, this.remove, this.checkBoxDone,
      {super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8),
      child: Row(
        children: [
          Checkbox(
            value: done,
            onChanged: (value) => checkBoxDone(),
          ),
          Expanded(child: Text(title)),
          IconButton(
            icon: const Icon(Icons.delete),
            onPressed: () => remove(),
          ),
        ],
      ),
    );
  }
}
"""

BUILDER = """body: ListView.builder(
  itemCount: todos.length,
  itemBuilder: (context, i) {
    var name = todos[i].name;
    int id = todos[i].id;
    return ToDoItem( // Werte aus der Liste todos an das ToDoItem übergeben
      id,
      name, // Titel
      todos[i].checkbox, // Checkboxstatus
      () => deleteItem(todos[i].id), // Löschfunktion
      () => checkBoxDone(todos[i].id), // Checkboxfunktion
    );
  },
),"""

M4_ADD = """void addItem(String itemName) {
  setState(() {
    ToDoListObject newtodo = ToDoListObject(todos.length + 1, false, itemName);
    todos.add(newtodo);
  });
  Navigator.of(context).pop();
}"""
M4_DEL = """void deleteItem(int id) {
  setState(() {
    todos.removeWhere((element) {
      return element.id == id;
    });
  });
}"""
M4_CHECK = """void checkBoxDone(int id) {
  setState(() {
    ToDoListObject item = todos.firstWhere((element) => element.id == id);
    item.checkbox = !item.checkbox;
  });
}"""

LADEN = """List dataToDo = [];

void loadDataFromDBToDo() async {
  dataToDo = await loadDataToDo();
  for (var element in dataToDo) {
    ToDoListObject newItem =
        ToDoListObject(element['id'], element['checkbox'], element['name']);
    todos.add(newItem); // legt die geladenen Werte in die Liste todos
  }
  setState(() {});
}

@override
void initState() {
  super.initState();
  loadDataFromDBToDo();
}"""

M6_ADD = """void addItem(String itemName) {
  setState(() {
    ToDoListObject newtodo = ToDoListObject(todos.length + 1, false, itemName);
    todos.add(newtodo);
    sendDS(newtodo); // Create
  });
  Navigator.of(context).pop();
}"""
M6_DEL = """void deleteItem(int id) {
  setState(() {
    ToDoListObject item = todos.firstWhere((element) => element.id == id);
    ToDoListObject deltodo = ToDoListObject(item.id, item.checkbox, item.name);
    deletDS(deltodo); // Delete
    todos.removeWhere((element) {
      return element.id == id;
    });
  });
}"""
M6_CHECK = """void checkBoxDone(int id) {
  setState(() {
    ToDoListObject item = todos.firstWhere((element) => element.id == id);
    item.checkbox = !item.checkbox;
    ToDoListObject upttodo = ToDoListObject(item.id, item.checkbox, item.name);
    updateDS(upttodo); // Update
  });
}"""

LIST_FULL = """import 'package:flutter/material.dart';

import 'todo_item.dart';
import 'todo_list_object.dart';
@@IMPORT@@
class ToDoList extends StatefulWidget {
  const ToDoList({super.key});

  @override
  State<ToDoList> createState() => _ToDoListState();
}

class _ToDoListState extends State<ToDoList> {
  // Liste für den ListView.builder
  List<ToDoListObject> todos = [];
@@LADEN@@
@@METHODEN@@

  void newEntry() {
    showDialog<AlertDialog>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          content: TextField(
            autofocus: true,
            onSubmitted: addItem,
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ToDo Liste')),
@@BODY@@
      floatingActionButton: FloatingActionButton(
        onPressed: newEntry,
        child: const Icon(Icons.add),
      ),
    );
  }
}
"""

def liste(level):
    m = [M4_ADD, M4_DEL, M4_CHECK] if level < 6 else [M6_ADD, M6_DEL, M6_CHECK]
    laden = '\n' + ind(LADEN, 2) + '\n' if level >= 5 else ''
    imp = "import 'webRequest.dart';\n" if level >= 5 else ''
    return (LIST_FULL.replace('@@IMPORT@@', imp).replace('@@LADEN@@', laden)
            .replace('@@METHODEN@@', '\n' + ind('\n\n'.join(m), 2))
            .replace('@@BODY@@', ind(BUILDER, 6)))

SQL_TODO = """USE flutterDB;

CREATE TABLE ToDoTB (
  id       INT PRIMARY KEY,
  name     VARCHAR(50),
  checkbox BOOLEAN DEFAULT 0
);

INSERT INTO ToDoTB VALUES (1, 'Projektplan', 0), (2, 'Gruppeneinteilung', 1);"""

SQL_REST = """-- Tabelle aus dem REST-Lernpfad (titel/erledigt) an das Skript anpassen:
ALTER TABLE ToDoTB RENAME COLUMN titel TO name, RENAME COLUMN erledigt TO checkbox;"""

MANIFEST = """<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <application
        android:label="meine_app"
        android:usesCleartextTraffic="true"
        ...>"""

LOESUNGEN = {
    '1': [{'datei': 'Terminal im Projektordner meine_app', 'code': 'flutter pub add http'},
          {'datei': 'android/app/src/main/AndroidManifest.xml (Ausschnitt)', 'code': MANIFEST},
          {'datei': 'lib/webRequest.dart', 'code': web(1)},
          {'datei': 'lib/my_login.dart', 'code': login(1)}],
    '2': [{'datei': 'lib/my_login.dart', 'code': login(2)}],
    '3': [{'datei': 'lib/webRequest.dart', 'code': web(3)},
          {'datei': 'lib/my_login.dart', 'code': login(3)}],
    '4': [{'datei': 'lib/todo_list_object.dart', 'code': OBJEKT + '\n'},
          {'datei': 'lib/todo_item.dart', 'code': ITEM},
          {'datei': 'lib/todo_list.dart', 'code': liste(4)}],
    '5': [{'datei': 'SQL auf dem Raspberry Pi', 'code': SQL_TODO + '\n\n' + SQL_REST},
          {'datei': 'lib/webRequest.dart', 'code': web(5)},
          {'datei': 'lib/todo_list.dart', 'code': liste(5)}],
    '6': [{'datei': 'lib/todo_list.dart', 'code': liste(6)}],
}
