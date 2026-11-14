// Level 9 – Musterlösung
import 'dart:convert';

import 'package:http/http.dart' as http;

/// Ein Eintrag aus der Tabelle ToDoTB (Spalten wie im Skript: id, name, checkbox).
///
/// Nur für den Dart-Client aus Level 9. Die Flutter-App nutzt im Lernpfad
/// Flutter-Datenbankanbindung wie im Skript webRequest.dart und ToDoListObject.
class ToDo {
  const ToDo({required this.id, required this.name, required this.checkbox});

  final int id;
  final String name;
  final bool checkbox;

  factory ToDo.fromJson(Map<String, dynamic> json) {
    final c = json['checkbox'];
    return ToDo(
      id: json['id'] as int,
      name: json['name'] as String,
      checkbox: c == true || c == 1,
    );
  }

  @override
  String toString() => '${checkbox ? '[x]' : '[ ]'} $id: $name';
}

/// Zugriff auf die Tabelle ToDoTB über die php-crud-api auf dem Pi.
class TodoApi {
  /// ip darf auch einen Port enthalten, z. B. '127.0.0.1:8088' (Probe-Server der Lehrkraft).
  TodoApi(String ip) : basis = Uri.parse('http://$ip/php-crud-api/api.php/records/ToDoTB');

  final Uri basis;

  Uri _eintrag(int id) => Uri.parse('$basis/$id');

  static const _json = {'Content-Type': 'application/json'};

  Future<List<ToDo>> alle() async {
    final antwort = await http.get(basis);
    _pruefe(antwort);
    final daten = jsonDecode(antwort.body) as Map<String, dynamic>;
    return (daten['records'] as List)
        .map((r) => ToDo.fromJson(r as Map<String, dynamic>))
        .toList();
  }

  Future<int> anlegen(String name) async {
    final antwort = await http.post(basis,
        headers: _json, body: jsonEncode({'name': name, 'checkbox': false}));
    _pruefe(antwort);
    return jsonDecode(antwort.body) as int;
  }

  Future<void> abhaken(int id, bool checkbox) async {
    final antwort = await http.put(_eintrag(id),
        headers: _json, body: jsonEncode({'checkbox': checkbox}));
    _pruefe(antwort);
  }

  Future<void> loeschen(int id) async {
    _pruefe(await http.delete(_eintrag(id)));
  }

  void _pruefe(http.Response antwort) {
    if (antwort.statusCode != 200) {
      throw Exception('Server meldet ${antwort.statusCode}: ${antwort.body}');
    }
  }
}
