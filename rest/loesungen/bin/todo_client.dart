// Level 9 – Musterlösung Hauptprogramm (im Schülerprojekt: bin/todo_client.dart
// mit  import 'package:todo_client/todo_api.dart';)
//   dart run bin/todo_client.dart <IP> [neu "Text" | ab <id> | auf <id> | weg <id>]
import '../lib/todo_api.dart';

Future<void> main(List<String> args) async {
  if (args.isEmpty) {
    print('Aufruf: dart run bin/todo_client.dart <IP> [neu "Text" | ab <id> | auf <id> | weg <id>]');
    return;
  }
  final api = TodoApi(args[0]);
  final befehl = args.length > 1 ? args[1] : '';
  final wert = args.length > 2 ? args[2] : '';
  try {
    switch (befehl) {
      case 'neu':
        print('Neu angelegt mit id ${await api.anlegen(wert)}');
      case 'ab':
        await api.abhaken(int.parse(wert), true);
      case 'auf':
        await api.abhaken(int.parse(wert), false);
      case 'weg':
        await api.loeschen(int.parse(wert));
    }
    for (final t in await api.alle()) {
      print(t);
    }
  } catch (e) {
    print('Fehler: $e');
  }
}
