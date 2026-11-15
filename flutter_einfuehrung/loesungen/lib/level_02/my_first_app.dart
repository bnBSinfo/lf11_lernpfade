import 'package:flutter/material.dart';

class MyFirstApp extends StatelessWidget {
  const MyFirstApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        body: Padding(
          padding: EdgeInsets.all(50),
          child: ColoredBox(
            color: Colors.grey,
            child: Center(
              child: Text('hier ist das zentrale Feld der App'),
            ),
          ),
        ),
      ),
    );
  }
}
