// Für die Lehrkraft: erzeugt die Zielbilder (docs/bilder/*.png) aus den Musterlösungen.
// Aufruf: ./tool/bilder_erzeugen.sh
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_lernpfad/level_01/my_first_app.dart' as l1;
import 'package:flutter_lernpfad/level_02/my_first_app.dart' as l2;
import 'package:flutter_lernpfad/level_03/my_first_app.dart' as l3;
import 'package:flutter_lernpfad/level_04/my_first_app.dart' as l4;
import 'package:flutter_lernpfad/level_05/app.dart' as l5;
import 'package:flutter_lernpfad/level_06/app.dart' as l6;
import 'package:flutter_lernpfad/level_07/app.dart' as l7;
import 'package:flutter_lernpfad/level_08/app.dart' as l8;

Future<void> schrift(String familie, List<String> dateien) async {
  final fonts = Platform.environment['MATERIAL_FONTS']!;
  final loader = FontLoader(familie);
  for (final d in dateien) {
    final bytes = File('$fonts/$d').readAsBytesSync();
    loader.addFont(Future.value(ByteData.view(bytes.buffer)));
  }
  await loader.load();
}

Future<void> eintrag(WidgetTester t, String titel) async {
  await t.tap(find.byType(FloatingActionButton));
  await t.pumpAndSettle();
  await t.enterText(find.byType(TextField), titel);
  await t.testTextInput.receiveAction(TextInputAction.done);
  await t.pumpAndSettle();
}

/// Gemessene Markierungen je Bild: Name -> [{text, x, y, w, h}] in logischen Pixeln (360 x 640).
final marken = <String, List<Map<String, Object>>>{};

typedef Marke = (String text, Finder finder);

void main() {
  tearDownAll(() {
    File('test/bilder/marken.json')
        .writeAsStringSync(const JsonEncoder.withIndent(' ').convert(marken));
  });

  setUpAll(() async {
    await schrift('Roboto', ['Roboto-Regular.ttf', 'Roboto-Medium.ttf', 'Roboto-Bold.ttf']);
    await schrift('MaterialIcons', ['MaterialIcons-Regular.otf']);
  });

  Future<void> bild(WidgetTester t, Widget app, String name,
      [Future<void> Function(WidgetTester)? aktion, List<Marke> m = const []]) async {
    t.view.physicalSize = const Size(360 * 2, 640 * 2);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    debugDisableShadows = false;
    await t.pumpWidget(app);
    await t.pumpAndSettle();
    if (aktion != null) await aktion(t);
    await t.pump(const Duration(seconds: 1)); // Cursor/Animationen ruhig
    marken[name] = [
      for (final (text, f) in m)
        if (f.evaluate().isNotEmpty)
          () {
            final r = t.getRect(f.first);
            return {'text': text, 'x': r.left, 'y': r.top, 'w': r.width, 'h': r.height};
          }()
    ];
    await expectLater(find.byWidget(app), matchesGoldenFile('bilder/$name.png'));
    debugDisableShadows = true;
  }

  final appBar = find.byType(AppBar);
  final fab = find.byType(FloatingActionButton);
  Finder txt(String t) => find.text(t);

  testWidgets('1', (t) => bild(t, const l1.MyFirstApp(), 'level_1', null, [
        (" Text – steht im body ganz oben links", txt('Das ist mein Grundgerüst')),
        (" Scaffold – füllt den ganzen Bildschirm", find.byType(Scaffold)),
      ]));
  testWidgets('2', (t) => bild(t, const l2.MyFirstApp(), 'level_2', null, [
        ("Padding – 50 px Rand rundherum", find.byWidgetPredicate((w) => w is Padding && w.padding == const EdgeInsets.all(50))),
        ("ColoredBox – graue Fläche", find.byWidgetPredicate((w) => w is ColoredBox && w.color == Colors.grey)),
        ("Center → Text in der Mitte", txt('hier ist das zentrale Feld der App')),
      ]));
  testWidgets('3', (t) => bild(t, const l3.MyFirstApp(), 'level_3', null, [
        ("AppBar mit title", appBar),
        ("body: MyLogin (Stateful Widget)", txt('Willkommen im Stateful Widget')),
      ]));
  final felder = find.byType(TextField);
  final login = find.byType(TextButton);
  testWidgets('4a', (t) => bild(t, const l4.MyFirstApp(), 'level_4_leer', null, [
        ("Text 'Willkommen'", txt('Willkommen')),
        ("TextField Benutzername", felder.at(0)),
        ("TextField Passwort (verdeckt)", felder.at(1)),
        ("TextButton – grau, weil _canLogin false", login),
      ]));
  testWidgets('4b', (t) => bild(t, const l4.MyFirstApp(), 'level_4', (t) async {
        await t.enterText(felder.at(0), 'anna');
        await t.enterText(felder.at(1), 'geheim');
        FocusManager.instance.primaryFocus?.unfocus();
        await t.pumpAndSettle();
      }, [
        ("onChanged speichert _username", felder.at(0)),
        ("obscureText: true → Punkte", felder.at(1)),
        ("TextButton – aktiv nach setState", login),
      ]));
  testWidgets('5', (t) => bild(t, const l5.ToDoApp(), 'level_5', null, [
        ("ein ToDoItem = eine Row", find.byType(Row).first),
        ("Checkbox (noch inaktiv)", find.byType(Checkbox).first),
        ("Expanded → Text(title)", txt('Einkaufen')),
        ("IconButton Mülleimer", find.byType(IconButton).first),
      ]));
  testWidgets('6a', (t) => bild(t, const l6.ToDoApp(), 'level_6_dialog', (t) async {
        await eintrag(t, 'Milch kaufen');
        await t.tap(fab);
        await t.pumpAndSettle();
        await t.enterText(felder, 'LF11 lernen');
        await t.pumpAndSettle();
      }, [
        ("AlertDialog aus showDialog", find.byType(AlertDialog)),
        ("TextField – Enter ruft addItem", felder),
      ]));
  testWidgets('6b', (t) => bild(t, const l6.ToDoApp(), 'level_6', (t) async {
        await eintrag(t, 'Milch kaufen');
        await eintrag(t, 'LF11 lernen');
      }, [
        ("AppBar 'ToDo Liste'", appBar),
        ("ListView.builder – ein ToDoItem je Eintrag", find.byType(ListView)),
        ("FloatingActionButton → newEntry", fab),
      ]));
  testWidgets('7', (t) => bild(t, const l7.ToDoApp(), 'level_7', (t) async {
        for (final e in ['Milch kaufen', 'LF11 lernen', 'Sport']) {
          await eintrag(t, e);
        }
      }, [
        ("Mülleimer ruft remove() → deleteItem(1)", find.byType(IconButton).at(1)),
      ]));
  testWidgets('8', (t) => bild(t, const l8.ToDoApp(), 'level_8', (t) async {
        for (final e in ['Milch kaufen', 'LF11 lernen', 'Sport']) {
          await eintrag(t, e);
        }
        await t.tap(find.byType(Checkbox).first);
        await t.pumpAndSettle();
      }, [
        ("Checkbox: done = true", find.byType(Checkbox).first),
        ("Checkbox: done = false", find.byType(Checkbox).at(1)),
      ]));
}
