import 'package:flutter/material.dart';
import 'package:flutter_lernpfad/level_03/my_first_app.dart';
import 'package:flutter_lernpfad/level_03/my_login.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Level 3: AppBar und erstes Stateful Widget', (tester) async {
    await tester.pumpWidget(const MyFirstApp());

    expect(find.byType(AppBar), findsOneWidget,
        reason: 'Hinweis: Das Scaffold braucht eine appBar: AppBar(...).');
    expect(find.descendant(of: find.byType(AppBar), matching: find.text('Meine erste App')),
        findsOneWidget,
        reason: "Hinweis: Die AppBar hat den title: Text('Meine erste App').");

    expect(find.byType(MyLogin), findsOneWidget,
        reason: 'Hinweis: Setzen Sie im Scaffold body: const MyLogin().');
    expect(tester.widget(find.byType(MyLogin)), isA<StatefulWidget>(),
        reason: 'Hinweis: MyLogin muss "extends StatefulWidget" sein und eine '
            'createState-Methode haben (Kürzel stful).');
    expect(find.text('Willkommen im Stateful Widget'), findsOneWidget,
        reason: "Hinweis: Die build-Methode im State zeigt Text('Willkommen im Stateful Widget').");
    expect(find.ancestor(of: find.text('Willkommen im Stateful Widget'), matching: find.byType(Center)),
        findsWidgets,
        reason: 'Hinweis: Der Text soll zentriert sein (Center).');
  });
}
