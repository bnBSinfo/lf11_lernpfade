import 'package:flutter/material.dart';

class MyFirstApp extends StatelessWidget {
  const MyFirstApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        body: Text('Das ist mein Grundgerüst'),
      ),
    );
  }
}
