// Probe-Server für die Lehrkraft: verhält sich wie ein fertig eingerichteter Pi.
// Damit lassen sich das Prüf-Tool und die Musterlösungen ohne echten Pi testen.
//   dart run test/probe_server.dart [http-Port] [ssh-Port]     (Standard 8088 / 2222)
import 'dart:async';
import 'dart:convert';
import 'dart:io';

final benutzer = [
  {'id': 1, 'name': 'berno', 'passwordLogin': r'Pa$$w0rd'},
  {'id': 2, 'name': 'stoll', 'passwordLogin': r'Pa$$w0rd'},
];
final todos = <int, Map<String, dynamic>>{
  1: {'id': 1, 'name': 'Pi einrichten', 'checkbox': true},
  2: {'id': 2, 'name': 'API testen', 'checkbox': false},
};
var naechsteId = 3;

void main(List<String> args) {
  runZonedGuarded(() => starten(args), (_, __) {});
}

Future<void> starten(List<String> args) async {
  final httpPort = args.isNotEmpty ? int.parse(args[0]) : 8088;
  final sshPort = args.length > 1 ? int.parse(args[1]) : 2222;
  final ssh = await ServerSocket.bind(InternetAddress.loopbackIPv4, sshPort);
  ssh.listen((s) {
    s.done.catchError((_) => s);
    s.write('SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13\r\n');
    s.listen((_) {}, onError: (_) {}, onDone: s.destroy);
  });
  final web = await HttpServer.bind(InternetAddress.loopbackIPv4, httpPort);
  stdout.writeln('Probe-Pi läuft: http $httpPort, ssh $sshPort');
  await for (final req in web) {
    final res = req.response..headers.set('Server', 'Apache/2.4.58 (Ubuntu)');
    final pfad = req.uri.path;
    void json(Object o, [int status = 200]) {
      res.statusCode = status;
      res.headers.contentType = ContentType.json;
      res.write(jsonEncode(o));
    }

    if (pfad == '/') {
      res.headers.contentType = ContentType.html;
      res.write('<html><title>Apache2 Ubuntu Default Page: It works</title></html>');
    } else if (pfad == '/info.php') {
      res.headers.contentType = ContentType.html;
      res.write('<h1>PHP Version 8.3.6</h1><h2>mysqli</h2>');
    } else if (pfad == '/phpmyadmin/') {
      res.headers.contentType = ContentType.html;
      res.write('<title>phpMyAdmin</title>');
    } else if (pfad == '/benutzer.php') {
      json([for (final b in benutzer) {'id': b['id'], 'name': b['name']}]);
    } else if (pfad.startsWith('/php-crud-api/api.php/records/')) {
      final teile = pfad.split('/').skip(4).toList(); // [tabelle, id?]
      final id = teile.length > 1 ? int.tryParse(teile[1]) : null;
      final body = await utf8.decoder.bind(req).join();
      if (teile[0] == 'flutterTB') {
        if (id == null) {
          json({'records': benutzer});
        } else {
          final b = benutzer.where((b) => b['id'] == id);
          b.isEmpty ? json({'code': 1003, 'message': "Record '$id' not found"}, 404) : json(b.first);
        }
      } else if (teile[0] == 'ToDoTB') {
        switch ((req.method, id)) {
          case ('GET', null):
            json({'records': todos.values.toList()});
          case ('POST', null):
            final d = jsonDecode(body) as Map<String, dynamic>;
            todos[naechsteId] = {'id': naechsteId, 'name': d['name'], 'checkbox': d['checkbox'] ?? false};
            json(naechsteId++);
          case ('GET', final int i) when todos.containsKey(i):
            json(todos[i]!);
          case ('PUT', final int i) when todos.containsKey(i):
            todos[i]!.addAll((jsonDecode(body) as Map<String, dynamic>)..remove('id'));
            json(1);
          case ('DELETE', final int i) when todos.containsKey(i):
            todos.remove(i);
            json(1);
          default:
            json({'code': 1003, 'message': "Record '$id' not found"}, 404);
        }
      } else {
        json({'code': 1001, 'message': "Table '${teile[0]}' not found"}, 404);
      }
    } else {
      res.statusCode = 404;
      res.write('Not Found');
    }
    await res.close();
  }
}
