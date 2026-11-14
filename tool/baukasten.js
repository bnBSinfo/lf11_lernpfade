/* Interaktive Baukästen für den Flutter-Lernpfad.
   <div class="baukasten" data-baukasten="scaffold"></div>  oder  data-baukasten="layout"
   Vorschau ist eine Nachbildung im Material-3-Stil (kein echtes Flutter) – der Code daneben ist echtes Dart. */
(function () {
  "use strict";
  var esc = function (s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  var dartStr = function (s) { return "'" + String(s).replace(/\\/g, "\\\\").replace(/'/g, "\\'") + "'"; };

  // Gemeinsames Gerüst: Steuerung | Handy | Code + Erklärung
  function geruest(root, steuerHtml) {
    root.innerHTML =
      '<div class="bk-steuer">' + steuerHtml + "</div>" +
      '<div class="bk-handy"><div class="bk-schirm"></div></div>' +
      '<div class="bk-rechts"><div class="bk-codeleiste">' +
      '<label class="bk-schalter"><input type="checkbox" data-voll> Ganzen Quellcode zeigen</label>' +
      '<button type="button" class="bk-kopieren">📋 Kopieren</button></div>' +
      '<pre class="bk-code"><code></code></pre>' +
      '<p class="bk-spielwiese klein">Selbst ausprobieren: Ganzen Quellcode kopieren, in <code>lib/spielwiese.dart</code> einfügen und starten – ' +
      'Android Studio: Rechtsklick auf die Datei → <i>Run</i>, VS Code/Terminal: <code>flutter run -t lib/spielwiese.dart</code></p>' +
      '<div class="bk-info" role="status"><b>Tipp:</b> Fahren Sie mit der Maus über einen Teil im Handy oder im Code – oder tippen Sie darauf.</div></div>';
    var kopf = root.querySelector(".bk-kopieren");
    kopf.addEventListener("click", function () {
      var text = root.querySelector(".bk-code").textContent;
      var fertig = function () { kopf.textContent = "✓ Kopiert"; setTimeout(function () { kopf.textContent = "📋 Kopieren"; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(fertig, function () { kopf.textContent = "Bitte markieren + Strg/Cmd+C"; });
    });
    return {
      voll: root.querySelector("[data-voll]"),
      schirm: root.querySelector(".bk-schirm"),
      code: root.querySelector(".bk-code code"),
      info: root.querySelector(".bk-info"),
    };
  }

  function verknuepfen(root, teile, infos) {
    var aktiv = null;
    function markiere(teil) {
      root.querySelectorAll(".hl").forEach(function (el) { el.classList.remove("hl"); });
      if (!teil) return;
      root.querySelectorAll('[data-teil="' + teil + '"]').forEach(function (el) { el.classList.add("hl"); });
    }
    function erklaere(teil) {
      if (infos[teil]) teile.info.innerHTML = infos[teil];
    }
    root.addEventListener("mouseover", function (ev) {
      var t = ev.target.closest("[data-teil]");
      markiere(t ? t.dataset.teil : aktiv);
      if (t) erklaere(t.dataset.teil);
    });
    root.addEventListener("mouseleave", function () { markiere(aktiv); });
    root.addEventListener("click", function (ev) {
      var t = ev.target.closest("[data-teil]");
      if (!t || t.closest(".bk-steuer")) return;
      aktiv = t.dataset.teil;
      markiere(aktiv);
      erklaere(aktiv);
    });
    root.addEventListener("focusin", function (ev) {
      var t = ev.target.closest("[data-teil]");
      if (t && !t.closest(".bk-steuer")) { markiere(t.dataset.teil); erklaere(t.dataset.teil); }
    });
  }

  // Erklärungen für die ergänzten Zeilen des ganzen Quellcodes
  var RAHMEN_INFO = {
    "r-import": "<b>import</b> holt die Material-Widgets (Text, Scaffold, AppBar …) in die Datei. Ohne diese Zeile kennt Dart sie nicht.",
    "r-main": "<b>main()</b> ist der Startpunkt jedes Dart-Programms. <code>runApp()</code> bekommt das erste Widget – die Wurzel des Widget-Baums.",
    "r-klasse": "<b>class MyFirstApp extends StatelessWidget</b> – Ihr eigenes Widget. Es hat keinen Zustand und gibt in <code>build</code> den Widget-Baum zurück.",
    "r-build": "<b>build(BuildContext context)</b> ruft Flutter auf, wenn das Widget gezeichnet wird. Was hier mit <code>return</code> zurückkommt, erscheint auf dem Bildschirm.",
    "r-app": "<b>MaterialApp</b> ist die App selbst (Design, Navigation). <code>home:</code> ist die Startseite – hier unser Scaffold.",
  };

  function einruecken(zeilen, n) {
    var pad = new Array(n + 1).join(" ");
    return zeilen.map(function (z) { return [z[0] ? pad + z[0] : z[0], z[1]]; });
  }

  /** Bettet Zeilen, die mit "Scaffold(" beginnen und mit ")" enden, in eine lauffähige main.dart ein. */
  function ganzeDatei(scaffoldZeilen) {
    var sc = scaffoldZeilen.map(function (z) { return [z[0], z[1]]; });
    sc[0][0] = "home: " + sc[0][0];
    sc[sc.length - 1][0] += ",";
    return [
      ["import 'package:flutter/material.dart';", "r-import"], ["", null],
      ["void main() {", "r-main"], ["  runApp(const MyFirstApp());", "r-main"], ["}", "r-main"], ["", null],
      ["class MyFirstApp extends StatelessWidget {", "r-klasse"], ["  const MyFirstApp({super.key});", "r-klasse"], ["", null],
      ["  @override", "r-build"], ["  Widget build(BuildContext context) {", "r-build"],
      ["    return MaterialApp(", "r-app"],
    ].concat(einruecken(sc, 6)).concat([
      ["    );", "r-app"], ["  }", "r-build"], ["}", "r-klasse"],
    ]);
  }

  function codeZeilen(zeilen) {
    // zeilen: [[text, teil|null], ...]
    return zeilen.map(function (z) {
      return z[1]
        ? '<span class="bk-zeile' + (z[1].indexOf("r-") === 0 ? " rahmen-zeile" : "") + '" data-teil="' + z[1] + '" tabindex="0">' + esc(z[0]) + "</span>"
        : '<span class="bk-zeile">' + esc(z[0]) + "</span>";
    }).join("\n");
  }

  /* ------------------------------------------------------------ Scaffold */
  function scaffold(root) {
    var st = { appBar: true, drawer: false, body: true, fab: true, bottom: false,
               titel: "Meine erste App", text: "Das ist der body" };
    var infos = {
      scaffold: "<b>Scaffold</b> ist das Grundgerüst einer Seite. Es teilt den Bildschirm in feste Bereiche auf – Sie füllen nur die Bereiche, die Sie brauchen.",
      appBar: "<b>appBar:</b> die Leiste oben. Meist ein <code>AppBar</code>-Widget mit <code>title:</code>. Sie bleibt beim Scrollen stehen.",
      titel: "<b>title:</b> das Widget in der AppBar – fast immer ein <code>Text</code>.",
      drawer: "<b>drawer:</b> ein Menü, das von links hereinfährt. Gibt es eine AppBar, erscheint dort automatisch das ☰-Symbol zum Öffnen.",
      body: "<b>body:</b> der Hauptbereich – hier steht der eigentliche Inhalt Ihrer Seite. Er bekommt den ganzen Platz, den AppBar und Leisten übrig lassen.",
      fab: "<b>floatingActionButton:</b> der runde Knopf unten rechts für die wichtigste Aktion – in der ToDo-App: neuen Eintrag hinzufügen.",
      bottom: "<b>bottomNavigationBar:</b> die Leiste unten zum Wechseln zwischen Bereichen der App, hier ein <code>NavigationBar</code> mit zwei Zielen.",
    };
    var steuer =
      '<p class="bk-titel">Scaffold-Bereiche</p>' +
      [["appBar", "appBar"], ["drawer", "drawer"], ["body", "body"], ["fab", "floatingActionButton"], ["bottom", "bottomNavigationBar"]]
        .map(function (p) {
          return '<label class="bk-schalter"><input type="checkbox" data-st="' + p[0] + '"' + (st[p[0]] ? " checked" : "") +
            "> <code>" + p[1] + "</code></label>";
        }).join("") +
      '<label class="bk-feld">Titel <input type="text" data-text="titel" maxlength="24" value="' + esc(st.titel) + '"></label>' +
      '<label class="bk-feld">Text im body <input type="text" data-text="text" maxlength="30" value="' + esc(st.text) + '"></label>';
    var t = geruest(root, steuer);
    var drawerOffen = false;

    function zeichne() {
      var h = "";
      if (st.appBar) {
        h += '<div class="m-appbar" data-teil="appBar" tabindex="0">' +
          (st.drawer ? '<button class="m-menu" data-teil="drawer" aria-label="Menü öffnen">☰</button>' : "") +
          '<span class="m-titel" data-teil="titel">' + esc(st.titel) + "</span></div>";
      }
      h += '<div class="m-body' + (st.body ? "" : " leer") + '" data-teil="' + (st.body ? "body" : "scaffold") + '" tabindex="0">' +
        (st.body ? '<span class="m-text">' + esc(st.text) + "</span>" : '<span class="m-leer">body ist leer</span>') + "</div>";
      if (st.fab) h += '<button class="m-fab" data-teil="fab" aria-label="Hinzufügen">+</button>';
      if (st.bottom) {
        h += '<div class="m-bottom" data-teil="bottom" tabindex="0"><span class="m-ziel aktiv"><i>⌂</i>Start</span><span class="m-ziel"><i>⚙</i>Einstellungen</span></div>';
      }
      if (st.drawer && drawerOffen) {
        h += '<div class="m-schleier"></div><div class="m-drawer" data-teil="drawer" tabindex="0"><b>Menü</b><span>Start</span><span>Einstellungen</span></div>';
      }
      t.schirm.innerHTML = h;
      t.schirm.dataset.teil = "scaffold";

      var z = [["Scaffold(", "scaffold"]];
      if (st.appBar) z.push(["  appBar: AppBar(", "appBar"], ["    title: Text(" + dartStr(st.titel) + "),", "titel"], ["  ),", "appBar"]);
      if (st.drawer) z.push(["  drawer: Drawer(", "drawer"], ["    child: ListView(", "drawer"], ["      children: const [", "drawer"],
        ["        ListTile(title: Text('Start')),", "drawer"], ["        ListTile(title: Text('Einstellungen')),", "drawer"],
        ["      ],", "drawer"], ["    ),", "drawer"], ["  ),", "drawer"]);
      if (st.body) z.push(["  body: Center(", "body"], ["    child: Text(" + dartStr(st.text) + "),", "body"], ["  ),", "body"]);
      if (st.fab) z.push(["  floatingActionButton: FloatingActionButton(", "fab"], ["    onPressed: () {},", "fab"], ["    child: Icon(Icons.add),", "fab"], ["  ),", "fab"]);
      if (st.bottom) z.push(["  bottomNavigationBar: NavigationBar(", "bottom"], ["    destinations: [", "bottom"],
        ["      NavigationDestination(icon: Icon(Icons.home), label: 'Start'),", "bottom"],
        ["      NavigationDestination(icon: Icon(Icons.settings), label: 'Einstellungen'),", "bottom"],
        ["    ],", "bottom"], ["  ),", "bottom"]);
      z.push([")", "scaffold"]);
      t.code.innerHTML = codeZeilen(t.voll.checked ? ganzeDatei(z) : z);
    }

    t.voll.addEventListener("change", zeichne);
    root.querySelector(".bk-steuer").addEventListener("input", function (ev) {
      var el = ev.target;
      if (el.dataset.st) { st[el.dataset.st] = el.checked; if (!st.drawer) drawerOffen = false; }
      if (el.dataset.text) st[el.dataset.text] = el.value;
      zeichne();
    });
    t.schirm.addEventListener("click", function (ev) {
      if (ev.target.closest(".m-menu")) { drawerOffen = true; zeichne(); }
      else if (ev.target.closest(".m-schleier")) { drawerOffen = false; zeichne(); }
    });
    verknuepfen(root, t, Object.assign({}, RAHMEN_INFO, infos));
    zeichne();
  }

  /* ------------------------------------------------------------ Layout */
  function layout(root) {
    var FARBEN = { grey: "#9e9e9e", amber: "#ffc107", lightBlue: "#03a9f4", green: "#4caf50" };
    var st = { padding: 50, farbe: "grey", center: true, inhalt: "text", ausr: "center" };
    var infos = {
      padding: "<b>Padding</b> schafft Abstand nach innen. <code>EdgeInsets.all(50)</code> = 50 Pixel auf allen vier Seiten. Sein Kind wird um diesen Rand kleiner.",
      farbe: "<b>ColoredBox</b> füllt ihre ganze Fläche mit einer Farbe – und sonst nichts. In HTML wäre das <code>background</code>.",
      center: "<b>Center</b> setzt sein Kind in die Mitte des verfügbaren Platzes – waagerecht und senkrecht.",
      text: "<b>Text</b> zeigt eine Zeichenkette an. Er ist so groß wie sein Inhalt.",
      column: "<b>Column</b> stapelt ihre <code>children</code> <b>untereinander</b>. <code>mainAxisAlignment</code> verteilt sie senkrecht (Hauptachse = senkrecht).",
      row: "<b>Row</b> legt ihre <code>children</code> <b>nebeneinander</b>. <code>mainAxisAlignment</code> verteilt sie waagerecht (Hauptachse = waagerecht).",
      kind: "Ein <b>Kind</b> in <code>children:</code> – jedes ist selbst wieder ein Widget.",
      body: "<b>body:</b> der Hauptbereich des Scaffold – hier beginnt Ihre Verschachtelung.",
    };
    var steuer =
      '<p class="bk-titel">Verschachtelung</p>' +
      '<label class="bk-feld"><span>Padding: <output data-zeige="padding">50</output> px</span><input type="range" min="0" max="80" step="10" value="50" data-st="padding"></label>' +
      '<label class="bk-feld">ColoredBox-Farbe <select data-st="farbe"><option value="grey">Colors.grey</option><option value="amber">Colors.amber</option>' +
      '<option value="lightBlue">Colors.lightBlue</option><option value="green">Colors.green</option><option value="">keine ColoredBox</option></select></label>' +
      '<label class="bk-schalter"><input type="checkbox" data-st="center" checked> <code>Center</code></label>' +
      '<label class="bk-feld">Inhalt <select data-st="inhalt"><option value="text">ein Text</option><option value="column">Column (untereinander)</option>' +
      '<option value="row">Row (nebeneinander)</option></select></label>' +
      '<label class="bk-feld" data-nur="liste">mainAxisAlignment <select data-st="ausr"><option value="start">start</option><option value="center" selected>center</option>' +
      '<option value="end">end</option><option value="spaceEvenly">spaceEvenly</option><option value="spaceBetween">spaceBetween</option></select></label>';
    var t = geruest(root, steuer);
    var JUSTIFY = { start: "flex-start", center: "center", end: "flex-end", spaceEvenly: "space-evenly", spaceBetween: "space-between" };

    function zeichne() {
      var skala = t.schirm.clientWidth / 360 || 0.6;
      var liste = st.inhalt !== "text";
      root.querySelector('[data-nur="liste"]').hidden = !liste;
      root.querySelector('[data-zeige="padding"]').textContent = st.padding;

      var innen;
      if (!liste) innen = '<span class="l-text" data-teil="text">Hallo Flutter</span>';
      else {
        var kinder = ["A", "B", "C"].map(function (b) { return '<span class="l-kind" data-teil="kind">' + b + "</span>"; }).join("");
        innen = '<div class="l-liste l-' + st.inhalt + (st.center ? " zentriert" : "") + '" data-teil="' + st.inhalt +
          '" style="justify-content:' + JUSTIFY[st.ausr] + '">' + kinder + "</div>";
      }
      if (st.center) innen = '<div class="l-center" data-teil="center">' + innen + "</div>";
      if (st.farbe) innen = '<div class="l-farbe" data-teil="farbe" style="background:' + FARBEN[st.farbe] + '">' + innen + "</div>";
      if (st.padding) innen = '<div class="l-padding" data-teil="padding" style="padding:' + st.padding * skala + 'px">' + innen + "</div>";
      t.schirm.innerHTML = '<div class="m-appbar"><span class="m-titel">Layout</span></div><div class="l-body" data-teil="body">' + innen + "</div>";

      // Code von innen nach außen aufbauen
      var block;
      if (!liste) block = [["Text('Hallo Flutter')", "text"]];
      else {
        var w = st.inhalt === "column" ? "Column" : "Row";
        block = [[w + "(", st.inhalt], ["  mainAxisAlignment: MainAxisAlignment." + st.ausr + ",", st.inhalt], ["  children: [", st.inhalt],
          ["    Text('A'),", "kind"], ["    Text('B'),", "kind"], ["    Text('C'),", "kind"], ["  ],", st.inhalt], [")", st.inhalt]];
      }
      function huelle(name, teil, attr) {
        var neu = [[name + "(", teil]];
        if (attr) neu.push(["  " + attr + ",", teil]);
        block.forEach(function (z, i) { neu.push([(i === 0 ? "  child: " : "  ") + z[0], z[1]]); });
        neu[neu.length - 1][0] += ",";
        neu.push([")", teil]);
        block = neu;
      }
      if (st.center) huelle("Center", "center");
      if (st.farbe) huelle("ColoredBox", "farbe", "color: Colors." + st.farbe);
      if (st.padding) huelle("Padding", "padding", "padding: const EdgeInsets.all(" + st.padding + ")");
      var z = [["body: " + block[0][0], block[0][1]]].concat(block.slice(1)).map(function (zz) { return [zz[0], zz[1]]; });
      z[z.length - 1][0] += ",";
      if (t.voll.checked) {
        var sc = [["Scaffold(", "body"], ["  appBar: AppBar(title: const Text('Layout')),", "r-app"]]
          .concat(einruecken(z, 2)).concat([[")", "body"]]);
        t.code.innerHTML = codeZeilen(ganzeDatei(sc));
      } else t.code.innerHTML = codeZeilen(z);
    }

    root.querySelector(".bk-steuer").addEventListener("input", function (ev) {
      var el = ev.target, k = el.dataset.st;
      if (!k) return;
      st[k] = el.type === "checkbox" ? el.checked : el.type === "range" ? Number(el.value) : el.value;
      zeichne();
    });
    t.voll.addEventListener("change", zeichne);
    verknuepfen(root, t, Object.assign({}, RAHMEN_INFO, infos));
    window.addEventListener("resize", zeichne);
    window.addEventListener("hashchange", function () { setTimeout(zeichne, 0); });
    zeichne();
  }

  var ARTEN = { scaffold: scaffold, layout: layout };
  document.querySelectorAll("[data-baukasten]").forEach(function (root) {
    var f = ARTEN[root.dataset.baukasten];
    if (f) f(root);
  });
})();
