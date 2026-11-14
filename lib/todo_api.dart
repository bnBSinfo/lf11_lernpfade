// ignore_for_file: unused_import, unused_element, unused_field
// (Die Zeile oben blendet Warnungen aus, solange die TODOs offen sind.)
// Level 9 – Die REST-API aus Dart ansprechen
// Diese Klasse verwenden Sie später unverändert in Ihrer Flutter-App.
// Ausprobieren:  dart run tool/todo_konsole.dart
import 'dart:convert';

import 'package:http/http.dart' as http;

/// Ein Eintrag aus der Tabelle ToDoTB.
class ToDo {
  const ToDo({required this.id, required this.titel, required this.erledigt});

  final int id;
  final String titel;
  final bool erledigt;

  /// Baut ein ToDo aus einem JSON-Objekt der API,
  /// z. B. {"id": 1, "titel": "Pi einrichten", "erledigt": true}
  factory ToDo.fromJson(Map<String, dynamic> json) {
    // TODO 1: Werte aus json lesen. Achtung: erledigt kann je nach Server
    // true/false ODER 1/0 sein – beides muss funktionieren.
    throw UnimplementedError('TODO 1: ToDo.fromJson');
  }

  @override
  String toString() => '${erledigt ? '[x]' : '[ ]'} $id: $titel';
}

/// Zugriff auf die Tabelle ToDoTB über die php-crud-api auf dem Pi.
class TodoApi {
  TodoApi(String ip, {int port = 80})
      : basis = Uri.parse('http://$ip:$port/php-crud-api/api.php/records/ToDoTB');

  /// z. B. http://10.36.13.76:80/php-crud-api/api.php/records/ToDoTB
  final Uri basis;

  /// Adresse eines einzelnen Datensatzes, z. B. …/records/ToDoTB/3
  Uri _eintrag(int id) => Uri.parse('$basis/$id');

  static const _json = {'Content-Type': 'application/json'};

  /// GET – alle ToDos lesen.
  Future<List<ToDo>> alle() async {
    // TODO 2: GET auf basis senden, Statuscode prüfen (_pruefe),
    // Antwort mit jsonDecode lesen und die Liste unter 'records' in ToDos umwandeln.
    throw UnimplementedError('TODO 2: alle()');
  }

  /// POST – neues ToDo anlegen. Gibt die neue id zurück.
  Future<int> anlegen(String titel) async {
    // TODO 3: POST auf basis mit headers: _json und
    // body: jsonEncode({'titel': titel, 'erledigt': false}).
    // Die API antwortet nur mit der neuen id, z. B. 7
    throw UnimplementedError('TODO 3: anlegen()');
  }

  /// PUT – ein ToDo abhaken oder wieder öffnen.
  Future<void> abhaken(int id, bool erledigt) async {
    // TODO 4: PUT auf _eintrag(id) mit {'erledigt': erledigt}
    throw UnimplementedError('TODO 4: abhaken()');
  }

  /// DELETE – ein ToDo löschen.
  Future<void> loeschen(int id) async {
    // TODO 5: DELETE auf _eintrag(id)
    throw UnimplementedError('TODO 5: loeschen()');
  }

  /// Wirft eine verständliche Fehlermeldung, wenn der Server nicht mit 200 antwortet.
  void _pruefe(http.Response antwort) {
    if (antwort.statusCode != 200) {
      throw Exception('Server meldet ${antwort.statusCode}: ${antwort.body}');
    }
  }
}
