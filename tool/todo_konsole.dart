// Spielwiese für Level 9: Ihre TodoApi im Terminal ausprobieren.
//   dart run tool/todo_konsole.dart                 alle ToDos anzeigen
//   dart run tool/todo_konsole.dart neu "Milch kaufen"
//   dart run tool/todo_konsole.dart ab 3            ToDo 3 abhaken
//   dart run tool/todo_konsole.dart auf 3           ToDo 3 wieder öffnen
//   dart run tool/todo_konsole.dart weg 3           ToDo 3 löschen
import '../lib/todo_api.dart';
import 'pi_konfig.dart';

Future<void> main(List<String> args) async {
  final pi = PiKonfig.lesen();
  final api = TodoApi(pi.ip, port: pi.http);
  final befehl = args.isEmpty ? 'liste' : args.first;
  final wert = args.length > 1 ? args[1] : '';
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
  print('${api.basis}\n');
  (await api.alle()).forEach(print);
}
