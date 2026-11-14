// Level 9 – Musterlösung
import 'dart:convert';

import 'package:http/http.dart' as http;

/// Ein Eintrag aus der Tabelle ToDoTB.
class ToDo {
  const ToDo({required this.id, required this.titel, required this.erledigt});

  final int id;
  final String titel;
  final bool erledigt;

  factory ToDo.fromJson(Map<String, dynamic> json) {
    final e = json['erledigt'];
    return ToDo(
      id: json['id'] as int,
      titel: json['titel'] as String,
      erledigt: e == true || e == 1,
    );
  }

  @override
  String toString() => '${erledigt ? '[x]' : '[ ]'} $id: $titel';
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

  Future<int> anlegen(String titel) async {
    final antwort = await http.post(basis,
        headers: _json, body: jsonEncode({'titel': titel, 'erledigt': false}));
    _pruefe(antwort);
    return jsonDecode(antwort.body) as int;
  }

  Future<void> abhaken(int id, bool erledigt) async {
    final antwort = await http.put(_eintrag(id),
        headers: _json, body: jsonEncode({'erledigt': erledigt}));
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
