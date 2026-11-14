// Zeigt Ihren Fortschritt über alle Level.
// Aufruf im Projektordner:   dart run tool/fortschritt.dart
import 'dart:convert';
import 'dart:io';

const titel = {
  1: 'Das Grundgerüst',
  2: 'Widget im Widget',
  3: 'Das erste Stateful Widget',
  4: 'Die Login-Maske',
  5: 'Ein Widget für ein Listenelement',
  6: 'Die ToDo-Liste',
  7: 'Löschen',
  8: 'Abhaken mit Checkbox',
  9: 'Login öffnet die ToDo-Liste',
};

Future<void> main() async {
  final version = RegExp(r'^version:\s*([\d.]+)', multiLine: true)
          .firstMatch(File('pubspec.yaml').readAsStringSync())
          ?.group(1) ??
      '?';
  stdout.writeln('Flutter-Einführung LF11 · Version $version');
  stdout.writeln('Tests laufen … (dauert einige Sekunden)\n');
  final p = await Process.start('flutter', ['test', '--reporter', 'json'],
      runInShell: true);
  final suitePfad = <int, String>{};
  final testSuite = <int, int>{};
  final testName = <int, String>{};
  final fehler = <int, List<String>>{}; // level -> Hinweise
  final ok = <int, int>{};
  final gesamt = <int, int>{};

  int? levelVon(int testId) {
    final pfad = suitePfad[testSuite[testId]] ?? '';
    final m = RegExp(r'level_0(\d)_test').firstMatch(pfad);
    return m == null ? null : int.parse(m.group(1)!);
  }

  await for (final zeile
      in p.stdout.transform(utf8.decoder).transform(const LineSplitter())) {
    if (!zeile.startsWith('{')) continue;
    final e = jsonDecode(zeile) as Map<String, dynamic>;
    switch (e['type']) {
      case 'suite':
        suitePfad[e['suite']['id']] = e['suite']['path'] ?? '';
      case 'testStart':
        testSuite[e['test']['id']] = e['test']['suiteID'];
        testName[e['test']['id']] = e['test']['name'];
      case 'print':
      case 'error':
        final lvl = levelVon(e['testID']);
        if (lvl == null) break;
        final text = (e['error'] ?? e['message']).toString();
        if (e['type'] == 'print' && !text.contains('Hinweis:')) break;
        final hinweis = RegExp(r'Hinweis:[^\n]*(\n[^\n]+)*')
            .firstMatch(text)
            ?.group(0);
        final istLadefehler =
            (testName[e['testID']] ?? '').startsWith('loading');
        fehler.putIfAbsent(lvl, () => []).add(istLadefehler
            ? 'Der Code lässt sich nicht kompilieren. Rote Unterstreichungen in der '
                'IDE prüfen oder: flutter test test/level_0${lvl}_test.dart'
            : hinweis ?? text.split('\n').take(3).join(' '));
      case 'testDone':
        if (e['hidden'] == true) break;
        final lvl = levelVon(e['testID']);
        if (lvl == null) break;
        gesamt[lvl] = (gesamt[lvl] ?? 0) + 1;
        if (e['result'] == 'success') ok[lvl] = (ok[lvl] ?? 0) + 1;
    }
  }
  await p.exitCode;

  int? naechstes;
  for (final lvl in titel.keys) {
    final geschafft = fehler[lvl] == null &&
        (gesamt[lvl] ?? 0) > 0 &&
        ok[lvl] == gesamt[lvl];
    final symbol = geschafft ? '✅' : '⬜';
    stdout.writeln('$symbol  Level $lvl – ${titel[lvl]}');
    if (!geschafft) naechstes ??= lvl;
  }
  final erledigt = titel.keys
      .where((l) => fehler[l] == null && (gesamt[l] ?? 0) > 0 && ok[l] == gesamt[l])
      .length;
  stdout.writeln('\nGeschafft: $erledigt von ${titel.length} Leveln');
  if (naechstes == null) {
    stdout.writeln('🎉 Alle Level geschafft! Weiter mit docs/bonus.md');
  } else {
    stdout.writeln('\n▶ Weiter mit Level $naechstes: docs/level_0$naechstes.md');
    final alle = fehler[naechstes] ?? [];
    final h = [
      ...alle.where((t) => t.startsWith('Hinweis') || t.startsWith('Der Code')),
      ...alle,
    ];
    if (h.isNotEmpty) {
      stdout.writeln('  Erster Hinweis aus den Tests:');
      stdout.writeln('  ${h.first.replaceAll(RegExp(r'\s+'), ' ').trim()}');
    }
  }
}
