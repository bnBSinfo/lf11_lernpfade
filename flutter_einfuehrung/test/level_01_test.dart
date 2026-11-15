import 'package:flutter/material.dart';
import 'package:flutter_lernpfad/level_01/my_first_app.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Level 1: Grundgerüst mit MaterialApp und Scaffold', (tester) async {
    await tester.pumpWidget(const MyFirstApp());

    expect(find.byType(Placeholder), findsNothing,
        reason: 'Hinweis: Ersetzen Sie "return const Placeholder();" durch Ihre MaterialApp.');
    expect(find.byType(MaterialApp), findsOneWidget,
        reason: 'Hinweis: Die build-Methode soll eine MaterialApp zurückgeben.');
    expect(find.byType(Scaffold), findsOneWidget,
        reason: 'Hinweis: Weisen Sie home ein Scaffold zu.');
    expect(find.text('Das ist mein Grundgerüst'), findsOneWidget,
        reason: "Hinweis: Der body des Scaffold ist Text('Das ist mein Grundgerüst') – "
            'genau so geschrieben.');
  });
}
