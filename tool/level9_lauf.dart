// Hilfsprogramm für  dart run tool/pruefen.dart 9  – testet mit der Musterlösung TodoApi,
// ob auf dem Schüler-Pi Lesen, Anlegen, Ändern und Löschen über die API funktionieren.
// Gibt Zeilen "OK: …" und "HINWEIS: …" aus.
import 'dart:io';

import '../loesungen/lib/todo_api.dart';
import 'pi_konfig.dart';

void ok(String t) => stdout.writeln('OK: $t');
void hinweis(String t) => stdout.writeln('HINWEIS: $t');

String grund(Object e) {
  if (e is UnimplementedError) return 'noch nicht programmiert (UnimplementedError).';
  if (e is SocketException) return 'Der Pi ist nicht erreichbar (${e.message}).';
  if (e is TypeError) return 'Falscher Datentyp: $e';
  return '$e';
}

Future<void> main() async {
  final pi = PiKonfig.lesen();
  final api = TodoApi(pi.http == 80 ? pi.ip : '${pi.ip}:${pi.http}');

  // TODO 1 + 2: lesen
  try {
    final t = ToDo.fromJson({'id': 1, 'name': 'A', 'checkbox': 1});
    final f = ToDo.fromJson({'id': 2, 'name': 'B', 'checkbox': false});
    if (t.id == 1 && t.name == 'A' && t.checkbox && !f.checkbox) {
      ok('TODO 1: ToDo.fromJson versteht true/false und 1/0');
    } else {
      hinweis('TODO 1: ToDo.fromJson liest die Werte falsch (checkbox: 1 → true, false → false).');
    }
  } catch (e) {
    hinweis('TODO 1: ${grund(e)}');
  }
  List<ToDo> liste;
  try {
    liste = await api.alle();
    ok('TODO 2: alle() liefert ${liste.length} ToDos');
    if (!liste.any((t) => t.name == 'API testen')) {
      hinweis("TODO 2: In der Liste fehlt 'API testen' – stimmt die Tabelle ToDoTB (Level 6)?");
    }
  } catch (e) {
    hinweis('TODO 2: alle(): ${grund(e)}');
    return;
  }

  // TODO 3–5: schreiben
  final text = 'Prüfung ${DateTime.now().millisecondsSinceEpoch}';
  int id;
  try {
    id = await api.anlegen(text);
    final neu = (await api.alle()).where((t) => t.id == id).toList();
    if (neu.length == 1 && neu.first.name == text && !neu.first.checkbox) {
      ok('TODO 3: anlegen() legt ein offenes ToDo an (id $id)');
    } else {
      hinweis('TODO 3: Nach anlegen() steht das ToDo nicht (offen) in der Liste.');
      return;
    }
  } catch (e) {
    hinweis('TODO 3: anlegen(): ${grund(e)}');
    return;
  }
  try {
    await api.abhaken(id, true);
    final t = (await api.alle()).firstWhere((t) => t.id == id);
    t.checkbox
        ? ok('TODO 4: abhaken() setzt checkbox auf true')
        : hinweis('TODO 4: Nach abhaken(id, true) ist das ToDo immer noch offen.');
  } catch (e) {
    hinweis('TODO 4: abhaken(): ${grund(e)}');
  }
  try {
    await api.loeschen(id);
    (await api.alle()).any((t) => t.id == id)
        ? hinweis('TODO 5: Nach loeschen() ist das ToDo noch da.')
        : ok('TODO 5: loeschen() entfernt das ToDo');
  } catch (e) {
    hinweis('TODO 5: loeschen(): ${grund(e)} – das Prüf-ToDo "$text" bitte von Hand löschen.');
  }
}
