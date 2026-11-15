import 'package:flutter/material.dart';
import 'package:flutter_lernpfad/level_02/my_first_app.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Level 2: Padding > ColoredBox > Center > Text', (tester) async {
    await tester.pumpWidget(const MyFirstApp());

    final text = find.text('hier ist das zentrale Feld der App');
    expect(text, findsOneWidget,
        reason: "Hinweis: Der Text muss 'hier ist das zentrale Feld der App' lauten.");

    final center = find.ancestor(of: text, matching: find.byType(Center));
    expect(center, findsWidgets,
        reason: 'Hinweis: Der Text gehört als child in ein Center-Widget.');

    final grau = find.byWidgetPredicate((w) =>
        w is ColoredBox && w.color.toARGB32() == Colors.grey.toARGB32());
    expect(find.ancestor(of: text, matching: grau), findsOneWidget,
        reason: 'Hinweis: Um das Center gehört eine ColoredBox mit color: Colors.grey.');
    expect(find.descendant(of: grau, matching: center), findsWidgets,
        reason: 'Hinweis: Reihenfolge prüfen – das Center ist das child der ColoredBox.');

    final rand = find.byWidgetPredicate(
        (w) => w is Padding && w.padding == const EdgeInsets.all(50));
    expect(find.ancestor(of: grau, matching: rand), findsOneWidget,
        reason: 'Hinweis: Ganz außen steht ein Padding mit padding: EdgeInsets.all(50); '
            'die ColoredBox ist sein child.');
  });
}
