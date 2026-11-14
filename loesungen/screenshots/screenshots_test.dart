// Für die Lehrkraft: erzeugt die Zielbilder (docs/bilder/*.png) aus den Musterlösungen.
// Aufruf: ./tool/bilder_erzeugen.sh
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

void main() {
  setUpAll(() async {
    await schrift('Roboto', ['Roboto-Regular.ttf', 'Roboto-Medium.ttf', 'Roboto-Bold.ttf']);
    await schrift('MaterialIcons', ['MaterialIcons-Regular.otf']);
  });

  Future<void> bild(WidgetTester t, Widget app, String name,
      [Future<void> Function(WidgetTester)? aktion]) async {
    t.view.physicalSize = const Size(360 * 2, 640 * 2);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);
    debugDisableShadows = false;
    await t.pumpWidget(app);
    await t.pumpAndSettle();
    if (aktion != null) await aktion(t);
    await t.pump(const Duration(seconds: 1)); // Cursor/Animationen ruhig
    await expectLater(find.byWidget(app), matchesGoldenFile('bilder/$name.png'));
    debugDisableShadows = true;
  }

  testWidgets('1', (t) => bild(t, const l1.MyFirstApp(), 'level_1'));
  testWidgets('2', (t) => bild(t, const l2.MyFirstApp(), 'level_2'));
  testWidgets('3', (t) => bild(t, const l3.MyFirstApp(), 'level_3'));
  testWidgets('4a', (t) => bild(t, const l4.MyFirstApp(), 'level_4_leer'));
  testWidgets('4b', (t) => bild(t, const l4.MyFirstApp(), 'level_4', (t) async {
        await t.enterText(find.byType(TextField).at(0), 'anna');
        await t.enterText(find.byType(TextField).at(1), 'geheim');
        FocusManager.instance.primaryFocus?.unfocus();
        await t.pumpAndSettle();
      }));
  testWidgets('5', (t) => bild(t, const l5.ToDoApp(), 'level_5'));
  testWidgets('6a', (t) => bild(t, const l6.ToDoApp(), 'level_6_dialog', (t) async {
        await eintrag(t, 'Milch kaufen');
        await t.tap(find.byType(FloatingActionButton));
        await t.pumpAndSettle();
        await t.enterText(find.byType(TextField), 'LF11 lernen');
        await t.pumpAndSettle();
      }));
  testWidgets('6b', (t) => bild(t, const l6.ToDoApp(), 'level_6', (t) async {
        await eintrag(t, 'Milch kaufen');
        await eintrag(t, 'LF11 lernen');
      }));
  testWidgets('7', (t) => bild(t, const l7.ToDoApp(), 'level_7', (t) async {
        for (final e in ['Milch kaufen', 'LF11 lernen', 'Sport']) {
          await eintrag(t, e);
        }
      }));
  testWidgets('8', (t) => bild(t, const l8.ToDoApp(), 'level_8', (t) async {
        for (final e in ['Milch kaufen', 'LF11 lernen', 'Sport']) {
          await eintrag(t, e);
        }
        await t.tap(find.byType(Checkbox).first);
        await t.pumpAndSettle();
      }));
}
