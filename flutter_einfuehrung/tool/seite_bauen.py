#!/usr/bin/env python3
"""Baut docs/index.html (GitHub-Pages-Seite) aus docs/level_*.md und docs/bonus.md.

Aufruf im Projektordner:  python3 tool/seite_bauen.py   (braucht pandoc)
Passwort für die Musterlösungen: Eingabe oder Umgebungsvariable LOESUNG_PASSWORT.
Zielbilder: docs/bilder/*.png (erzeugt mit tool/bilder_erzeugen.sh).
Stil: css/stil.css aus den Lernpaketen (Lernpaket-Kompass), Welt "technik".
"""
import base64
import getpass
import hashlib
import html
import json
import os
import pathlib
import re
import secrets
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lernpfad_bausteine as bausteine  # noqa: E402
from kontrolle import KONTROLLE  # noqa: E402
from woerter import WOERTER, LEVEL_WOERTER  # noqa: E402
from kontrolle_einfach import KONTROLLE_EINFACH  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGO = ('<img class="kopf-logo" alt="BS Info München" width="239" height="160" src="data:image/png;base64,'
        + base64.b64encode((ROOT.parent / "logo-bsinfo.png").read_bytes()).decode() + '">')
DOCS = ROOT / "docs"
REPO = "bnBSinfo/lf11_lernpfade"
ITERATIONEN = 600_000
# Versionsnummer aus pubspec.yaml (vor dem Veröffentlichen dort erhöhen), Datum = Tag des Bauens
VERSION = re.search(r"^version:\s*([\d.]+)", (ROOT / "pubspec.yaml").read_text(encoding="utf-8"), re.M).group(1)
import datetime as _dt
STAND = _dt.date.today().strftime("%d.%m.%Y")
MARKER = "LOESUNG-OK\n"
e = html.escape

# ---------------------------------------------------------------- Inhalte je Level
# Baum-Knoten: (Name, Art, neu?, [Kinder], Notiz)   Art: stateless | stateful | state | widget
def k(name, art="widget", neu=False, kinder=(), notiz=""):
    return (name, art, neu, list(kinder), notiz)


LEVEL = {
    1: dict(
        titel="Das Grundgerüst", stich="main, runApp, MaterialApp, Scaffold",
        bilder=[("level_1", "So sieht Ihre App am Ende aus")],
        baum=k("MyFirstApp", "stateless", kinder=[
            k("MaterialApp", neu=True, kinder=[
                k("Scaffold", neu=True, notiz="home:", kinder=[
                    k("Text", neu=True, notiz="body:")])])]),
        grafik="start", baukasten="scaffold",
    ),
    2: dict(
        titel="Widget im Widget", stich="Padding, ColoredBox, Center",
        bilder=[("level_2", "Grauer Kasten mit 50 Pixel Rand, Text in der Mitte")],
        baum=k("MyFirstApp", "stateless", kinder=[k("MaterialApp", kinder=[k("Scaffold", kinder=[
            k("Padding", neu=True, notiz="body:", kinder=[
                k("ColoredBox", neu=True, notiz="child:", kinder=[
                    k("Center", neu=True, notiz="child:", kinder=[
                        k("Text", notiz="child:")])])])])])]),
        grafik="schachteln", baukasten="layout",
    ),
    3: dict(
        titel="Das erste Stateful Widget", stich="StatefulWidget, State, eigene Datei",
        bilder=[("level_3", "AppBar oben, Text aus dem Stateful Widget in der Mitte")],
        baum=k("MyFirstApp", "stateless", kinder=[k("MaterialApp", kinder=[k("Scaffold", kinder=[
            k("AppBar", neu=True, notiz="appBar:", kinder=[k("Text")]),
            k("MyLogin", "stateful", neu=True, notiz="body:", kinder=[
                k("_MyLoginState", "state", neu=True, notiz="createState()", kinder=[
                    k("Center", kinder=[k("Text")])])])])])]),
        grafik="stateful", baukasten="scaffold", wissen=True,
    ),
    4: dict(
        titel="Die Login-Maske", stich="TextField, setState, aktiver Button",
        bilder=[("level_4_leer", "Vorher: Felder leer – Login ist grau"),
                ("level_4", "Nachher: beide Felder gefüllt – Login ist aktiv")],
        baum=k("MyLogin", "stateful", kinder=[k("_MyLoginState", "state",
            notiz="_username · _password · _canLogin", kinder=[
            k("Center", kinder=[k("SizedBox", neu=True, notiz="width: 300", kinder=[
                k("Column", neu=True, notiz="children:", kinder=[
                    k("Text", notiz="'Willkommen'"),
                    k("TextField", neu=True, notiz="Benutzername"),
                    k("TextField", neu=True, notiz="Passwort · obscureText"),
                    k("TextButton", neu=True, notiz="aktiv, wenn _canLogin", kinder=[k("Text")])])])])])]),
        grafik="setstate", wissen=True,
    ),
    5: dict(
        titel="Ein ToDo-Element", stich="Row, Checkbox, Expanded, IconButton",
        bilder=[("level_5", "Drei ToDoItems – Checkbox und Mülleimer noch ohne Funktion")],
        baum=k("ToDoItem", "stateless", notiz="title", kinder=[
            k("Row", neu=True, notiz="children:", kinder=[
                k("Checkbox", neu=True, notiz="value: false"),
                k("Expanded", neu=True, kinder=[k("Text", notiz="title")]),
                k("IconButton", neu=True, kinder=[k("Icon", notiz="Icons.delete")])])]),
        grafik="row", wissen=True,
    ),
    6: dict(
        titel="Die ToDo-Liste", stich="ListView.builder, FloatingActionButton, Dialog",
        bilder=[("level_6_dialog", "Tippen auf + öffnet den Dialog"),
                ("level_6", "Nach Enter: neuer Eintrag in der Liste")],
        baum=k("ToDoList", "stateful", kinder=[k("_ToDoListState", "state", notiz="todos (List)", kinder=[
            k("Scaffold", kinder=[
                k("AppBar", notiz="appBar:", kinder=[k("Text", notiz="'ToDo Liste'")]),
                k("ListView.builder", neu=True, notiz="body:", kinder=[
                    k("ToDoItem", "stateless", notiz="für jedes todos[i]")]),
                k("FloatingActionButton", neu=True, kinder=[k("Icon", notiz="Icons.add")])]),
            k("AlertDialog", neu=True, notiz="über showDialog", kinder=[
                k("TextField", notiz="onSubmitted: addItem")])])]),
        grafik="liste", wissen=True,
    ),
    7: dict(
        titel="Löschen", stich="Funktionen als Parameter (VoidCallback)",
        bilder=[("level_7", "Jeder Mülleimer löscht genau seinen Eintrag")],
        baum=k("ToDoList", "stateful", kinder=[k("_ToDoListState", "state", notiz="deleteItem(i)", kinder=[
            k("Scaffold", kinder=[k("ListView.builder", kinder=[
                k("ToDoItem", "stateless", neu=True, notiz="title, remove", kinder=[
                    k("Row", kinder=[k("Checkbox"), k("Expanded"),
                                     k("IconButton", neu=True, notiz="onPressed: remove")])])])])])]),
        grafik="callback",
    ),
    8: dict(
        titel="Abhaken", stich="Map statt List, Checkbox aktiv",
        bilder=[("level_8", "Abgehakt bleibt abgehakt – auch nach dem Neuzeichnen")],
        baum=k("ToDoList", "stateful", kinder=[k("_ToDoListState", "state",
            notiz="todos (Map) · checkBoxDone(key)", kinder=[
            k("Scaffold", kinder=[k("ListView.builder", kinder=[
                k("ToDoItem", "stateless", neu=True, notiz="title, done, remove, checkBoxDone", kinder=[
                    k("Row", kinder=[k("Checkbox", neu=True, notiz="value: done"),
                                     k("Expanded"), k("IconButton")])])])])])]),
        grafik="map",
    ),
    9: dict(
        titel="Login → ToDo-Liste", stich="Navigator.push verbindet beide Teile zu einer App",
        bilder=[("level_9_login", "Start: die Login-Maske aus Level 4"),
                ("level_9", "Nach dem Login: die ToDo-Liste – mit Zurück-Pfeil")],
        baum=k("MaterialApp", kinder=[k("Navigator", neu=True, notiz="Stapel der Seiten", kinder=[
            k("Scaffold", notiz="unten: Login-Seite", kinder=[k("MyLogin", "stateful", notiz="onPressed → push")]),
            k("ToDoList", "stateful", neu=True, notiz="oben: nach dem Login")])]),
        grafik="navigator",
    ),
}

# ---------------------------------------------------------------- Grafiken (HTML/CSS)
def kette(schritte, kreis=False):
    teile = []
    for i, (titel, text) in enumerate(schritte):
        if i:
            teile.append('<span class="pfeil" aria-hidden="true">→</span>')
        teile.append(f'<div class="schritt-box"><b>{titel}</b><span>{text}</span></div>')
    if kreis:
        teile.append('<span class="pfeil kreis" aria-hidden="true">↺ wieder von vorn</span>')
    return f'<div class="kette">{"".join(teile)}</div>'


GRAFIK = {
    "start": ("Was passiert beim Start?", kette([
        ("main()", "Hier startet jedes Dart-Programm"),
        ("runApp(…)", "bekommt das erste Widget"),
        ("MyFirstApp", "Ihr Stateless Widget"),
        ("build()", "liefert den Widget-Baum"),
        ("Bildschirm", "Flutter zeichnet die App")])),
    "schachteln": ("Widgets sind wie Schachteln", """
<div class="schachtel s1"><span class="etikett">Padding · 50 px Rand</span>
  <div class="schachtel s2"><span class="etikett">ColoredBox · grau</span>
    <div class="schachtel s3"><span class="etikett">Center · mittig</span>
      <div class="schachtel s4">Text</div></div></div></div>
<p class="klein">Jede Schachtel hat genau eine Aufgabe und steckt ihr Kind in <code>child:</code>.
In HTML wären das CSS-Eigenschaften – in Flutter sind es Widgets.</p>"""),
    "stateful": ("Stateful Widget = zwei Klassen", """
<div class="zwei">
  <div class="kasten stateful"><b>MyLogin</b><small>extends StatefulWidget</small>
    <ul><li>unveränderlich</li><li>erzeugt seinen State</li></ul></div>
  <div class="verbindung"><code>createState()</code><span>→</span></div>
  <div class="kasten state"><b>_MyLoginState</b><small>extends State&lt;MyLogin&gt;</small>
    <ul><li>merkt sich Daten</li><li>hat die <code>build()</code>-Methode</li><li>bleibt beim Neuzeichnen erhalten</li></ul></div>
</div>"""),
    "setstate": ("Der setState-Kreislauf", kette([
        ("Tippen", "Text im Feld ändert sich"),
        ("onChanged", "ruft _onChangedUsername"),
        ("Variable", "_username = 'anna'"),
        ("_checkCanLogin()", "prüft beide Felder"),
        ("setState(…)", "_canLogin = true"),
        ("build()", "läuft neu – Button wird aktiv")], kreis=True)
        + '<p class="klein">Ohne <code>setState</code> ändert sich die Variable, aber <b>build()</b> läuft nicht neu – der Button bleibt grau.</p>'),
    "row": ("Row: nebeneinander", """
<div class="reihe-demo">
  <div class="zelle"><span class="cb"></span><small>Checkbox</small></div>
  <div class="zelle breit"><span>Einkaufen</span><small>Expanded → Text (nimmt den Rest)</small></div>
  <div class="zelle"><span>🗑</span><small>IconButton</small></div>
</div>
<p class="klein"><code>Row</code> legt Kinder <b>nebeneinander</b>, <code>Column</code> <b>untereinander</b>.</p>"""),
    "liste": ("Vom + bis zum neuen Eintrag", kette([
        ("+ tippen", "onPressed: newEntry"),
        ("showDialog", "AlertDialog mit TextField"),
        ("Enter", "onSubmitted: addItem"),
        ("setState", "todos.add(item)"),
        ("pop()", "Dialog schließt"),
        ("ListView.builder", "baut je Eintrag ein ToDoItem")])
        + """<div class="liste-demo"><code>todos</code>
<span class="idx"><i>[0]</i>'Milch kaufen'</span><span class="idx"><i>[1]</i>'LF11 lernen'</span>
<span class="pfeil">→</span><span class="kl">2 × ToDoItem</span></div>"""),
    "callback": ("Wer löscht? Die Funktion wandert nach unten", """
<div class="ebenen">
  <div class="kasten state"><b>_ToDoListState</b><small>besitzt die Liste und <code>deleteItem(i)</code></small></div>
  <div class="runter"><span>↓ übergibt <code>() =&gt; deleteItem(i)</code> als <code>remove</code></span>
    <span class="hoch">↑ <code>remove()</code> ruft <code>deleteItem(i)</code> auf</span></div>
  <div class="kasten stateless"><b>ToDoItem</b><small>kennt nur den „Knopf“ <code>remove</code> – 🗑 <code>onPressed: () =&gt; remove()</code></small></div>
</div>
<p class="klein">Danach: <code>setState</code> → <code>todos.removeAt(i)</code> → die Liste wird neu gebaut.</p>"""),
    "navigator": ("Der Navigator: ein Stapel von Seiten", """
<div class="zwei">
  <div class="kasten"><b>Vor dem Login</b><small>eine Seite im Stapel</small>
    <table><tr><td>🔐 Login-Maske (MyLogin)</td></tr></table></div>
  <div class="verbindung"><span>push →<br>← pop</span></div>
  <div class="kasten state"><b>Nach dem Login</b><small>neue Seite liegt oben</small>
    <table><tr><td>📝 ToDoList</td></tr><tr><td>🔐 Login-Maske (verdeckt)</td></tr></table></div>
</div>
<p class="klein">Login-Button → <code>Navigator.of(context).push(MaterialPageRoute(...))</code>. Zurück-Pfeil → <code>pop()</code>.
Die ToDos liegen nur lokal im State der Liste – keine Datenbank, nach dem Zurück sind sie weg.</p>"""),
    "map": ("Von der List zur Map", """
<div class="zwei">
  <div class="kasten"><b>List&lt;String&gt;</b><small>nur Titel</small>
    <table><tr><th>Index</th><th>Wert</th></tr><tr><td>0</td><td>'Milch kaufen'</td></tr><tr><td>1</td><td>'LF11 lernen'</td></tr></table></div>
  <div class="verbindung"><span>→</span></div>
  <div class="kasten state"><b>Map&lt;String, bool&gt;</b><small>Titel <i>und</i> Haken</small>
    <table><tr><th>Schlüssel</th><th>Wert</th></tr><tr><td>'Milch kaufen'</td><td>✅ true</td></tr><tr><td>'LF11 lernen'</td><td>⬜ false</td></tr></table></div>
</div>
<p class="klein">Checkbox antippen → <code>checkBoxDone(key)</code> → <code>todos.update(key, (done) =&gt; !done)</code> in <code>setState</code>.</p>"""),
}

# ---------------------------------------------------------------- Bausteine
CODEBLOCK = re.compile(r'^([ \t]*)(```\w*\n.*?^\1```)[ \t]*$', re.M | re.S)


def code_einsetzen(text: str, quelle: pathlib.Path) -> str:
    """Ersetzt {{code N}} durch den N-ten Code-Block der Standardfassung (gleicher Code in beiden Sprachstufen)."""
    bloecke = [(m.group(1), m.group(2)) for m in CODEBLOCK.finditer(quelle.read_text(encoding="utf-8"))]

    def ersetze(m):
        einzug, (alt, block) = m.group(1), bloecke[int(m.group(2))]
        zeilen = [z[len(alt):] if z.startswith(alt) else z for z in block.split("\n")]
        return "\n".join((einzug + z) if z else z for z in zeilen)
    return re.sub(r"^([ \t]*)\{\{code (\d+)\}\}[ \t]*$", ersetze, text, flags=re.M)


def md_zu_html(pfad: pathlib.Path, code_quelle: pathlib.Path | None = None) -> str:
    text = re.sub(r"^# .*\n", "", pfad.read_text(encoding="utf-8"), count=1)
    if code_quelle:
        text = code_einsetzen(text, code_quelle)
    out = subprocess.run(["pandoc", "-f", "gfm", "-t", "html", "--no-highlight"],
                         input=text, capture_output=True, text=True, check=True).stdout
    out = out.replace("<h2", "<h3").replace("</h2>", "</h3>")
    # ```diff-Blöcke: grau = Rahmen (steht schon da), grün + = neu tippen, rot - = löschen
    out = re.sub(r'<pre class="diff"><code>(.*?)</code></pre>', rahmen_code, out, flags=re.S)
    legende = ('<p class="rahmen-legende"><b>So lesen Sie die Code-Kästen:</b> '
               '<span class="lg rahmen">grau</span> steht schon in Ihrer Datei – nur zur Orientierung, wo Sie sind · '
               '<span class="lg neu">+ grün</span> neu eintippen · '
               '<span class="lg weg">− rot</span> löschen · '
               '<span class="lg rahmen">…</span> unveränderter Code dazwischen</p>')
    out = out.replace('<pre class="rahmen-code">', legende + '<pre class="rahmen-code">', 1)
    # Abschnitte bis zur nächsten Überschrift einpacken:
    #   Auftrag (begleiteter Pfad) und Profi-Auftrag je im hellroten Kasten, Erklärt zum Einklappen im Profipfad
    for kopf, klasse in (('<h3 id="auftrag">', "auftrags-kasten nur-begleitet"),
                         ('<h3 id="profi-auftrag">', "auftrags-kasten profi-kasten nur-profi"),
                         ('<h3 id="erkl', "erklaert"),
                         ('<h3 id="ausblick', "ausblick")):
        hg = klasse in ("erklaert", "ausblick")   # gehört in den Reiter „Hintergrund“
        out = re.sub(r'(' + re.escape(kopf) + r'.*?)(?=<h3 |\Z)',
                     lambda m: ("<!--hg-->" if hg else "") + f'<div class="{klasse}">{m.group(1)}</div>'
                     + ("<!--/hg-->" if hg else ""), out, count=1, flags=re.S)
    return out


def wissen_reiter(html: str) -> str:
    """Wissen-Seite: Inhaltsverzeichnis wird zur Reiterleiste, je Abschnitt ein Reiter mit Zurück/Weiter."""
    links = re.findall(r'<a href="#(w-[\w-]+)">(.*?)</a>', re.search(r"<nav class=\"card inhalt-navi\".*?</nav>", html, re.S).group(0))
    reiter = ('<nav class="schritt-reiter viele" role="tablist" aria-label="Abschnitte">'
              + "".join(f'<button type="button" role="tab" data-schritt="{i}">{t}</button>' for i, t in links) + "</nav>")
    html = re.sub(r"<nav class=\"card inhalt-navi\".*?</nav>", reiter, html, flags=re.S)
    teile = re.split(r'(?=<div class="card" id="w-)', html)
    out = teile[0]
    for n, teil in enumerate(teile[1:]):
        wid = links[n][0]
        zurueck = f'<button type="button" class="knopf" data-geh="{links[n-1][0]}">◀ {links[n-1][1]}</button>' if n else ""
        weiter = (f'<button type="button" class="knopf primaer" data-geh="{links[n+1][0]}">Weiter: {links[n+1][1]} ▶</button>'
                  if n + 1 < len(links) else "")
        out += (f'<div class="schritt" data-schritt="{wid}" role="tabpanel">{teil}'
                f'<p class="schritt-weiter">{zurueck}{weiter}</p></div>\n')
    return out


def hintergrund_abtrennen(html: str) -> tuple[str, str]:
    """Trennt „Erklärt“ und „Ausblick“ vom Auftrag ab (für den Reiter „Hintergrund“)."""
    hg = "".join(re.findall(r"<!--hg-->(.*?)<!--/hg-->", html, flags=re.S))
    rest = re.sub(r"<!--hg-->.*?<!--/hg-->", "", html, flags=re.S)
    # Tipps (aufklappbar) bleiben beim Auftrag – dort braucht man sie beim Tippen
    tipps = re.findall(r"<details>.*?</details>", hg, flags=re.S)
    hg = re.sub(r"<details>.*?</details>", "", hg, flags=re.S)
    if tipps:
        rest += '<div class="tipps"><h3>💡 Tipps, falls es hakt</h3>' + "".join(tipps) + "</div>"
    return rest, hg


def rahmen_code(m) -> str:
    zeilen = []
    for z in m.group(1).split("\n"):
        if z[:1] == "+" and z[1:2] in (" ", ""):
            art, zeichen = "neu", "+"
        elif z[:1] == "-" and z[1:2] in (" ", ""):
            art, zeichen = "weg", "−"
        else:
            art, zeichen = "rahmen", ""
        inhalt = z[2:] if len(z) >= 2 else ""
        zeilen.append(f'<span class="z {art}"><i>{zeichen}</i>{inhalt or "&#8203;"}</span>')
    return '<pre class="rahmen-code"><code>' + "".join(zeilen) + "</code></pre>"


def baum_html(knoten) -> str:
    name, art, neu, kinder, notiz = knoten
    klassen = f"knoten {art}" + (" neu" if neu else "")
    n = f'<small>{e(notiz)}</small>' if notiz else ""
    marke = '<em class="neu-marke">neu</em>' if neu else ""
    kinder_html = "".join(f"<li>{baum_html(c)}</li>" for c in kinder)
    sub = f"<ul>{kinder_html}</ul>" if kinder else ""
    return f'<span class="{klassen}"><b>{e(name)}</b>{n}{marke}</span>{sub}'


MARKEN = json.loads((DOCS / "bilder" / "marken.json").read_text(encoding="utf-8")) \
    if (DOCS / "bilder" / "marken.json").exists() else {}
NUM = "①②③④⑤⑥⑦⑧⑨"


def handy(bild, text):
    """Zielbild mit nummerierten Markierungen (Positionen aus marken.json, logische Pixel 360 x 640)."""
    kaesten, legende, belegt = [], [], []
    for i, m in enumerate(MARKEN.get(bild, [])):
        x, y, w, h = (m[k] for k in ("x", "y", "w", "h"))
        # Nummer rechts neben den Kasten (verdeckt nichts); passt das nicht, oben links hinein
        if w * h > 0.5 * 360 * 640:      # großer Kasten: Nummer unten links
            bx, by = x + 6, y + h - 26
        elif x + w + 26 <= 360:          # rechts daneben
            bx, by = x + w + 4, y
        else:                            # oben links hinein
            bx, by = x + 4, y + 4
        while any(abs(bx - ux) < 22 and abs(by - uy) < 22 for ux, uy in belegt):
            by += 24  # Nummern nicht übereinander legen
        belegt.append((bx, by))
        pc = lambda v, ges: f"{v / ges * 100:.2f}%"
        kaesten.append(
            f'<span class="marke" data-marke="{i}" style="left:{pc(x,360)};top:{pc(y,640)};width:{pc(w,360)};height:{pc(h,640)}"></span>'
            f'<span class="marke-nr" data-marke="{i}" style="left:{pc(bx,360)};top:{pc(by,640)}">{NUM[i]}</span>')
        legende.append(f'<li data-marke="{i}"><span>{NUM[i]}</span> {e(m["text"].strip())}</li>')
    leg = f'<ol class="marken-legende">{"".join(legende)}</ol>' if legende else ""
    # Vergrößerter Ausschnitt, wenn der Inhalt nur einen kleinen Teil des Bildschirms füllt
    klein = [m for m in MARKEN.get(bild, []) if m["w"] * m["h"] < 0.5 * 360 * 640]
    lupe = ""
    if klein:
        x0 = max(0, min(m["x"] for m in klein) - 10); y0 = max(0, min(m["y"] for m in klein) - 10)
        x1 = min(360, max(m["x"] + m["w"] for m in klein) + 10); y1 = min(640, max(m["y"] + m["h"] for m in klein) + 10)
        if (x1 - x0) * (y1 - y0) < 0.3 * 360 * 640:
            w, h = x1 - x0, max(y1 - y0, 40)
            pos_x = 0 if w >= 360 else x0 / (360 - w) * 100
            pos_y = 0 if h >= 640 else y0 / (640 - h) * 100
            lupe = (f'<div class="ausschnitt"><span class="ausschnitt-titel">🔍 Ausschnitt vergrößert</span>'
                    f'<span class="ausschnitt-bild" role="img" aria-label="Vergrößerter Ausschnitt: {e(text)}" '
                    f'style="background-image:url(bilder/{bild}.png);aspect-ratio:{w:.0f}/{h:.0f};'
                    f'background-size:{360 / w * 100:.2f}% auto;background-position:{pos_x:.2f}% {pos_y:.2f}%"></span></div>')
    return f"""<figure class="handy"><button class="rahmen" type="button" aria-label="Bild groß anzeigen: {e(text)}">
      <span class="bild"><img src="bilder/{bild}.png" width="360" height="640" alt="{e(text)}" loading="lazy">{"".join(kaesten)}</span>
      <span class="lupe" aria-hidden="true">🔍</span></button>
      <figcaption>{e(text)}</figcaption>{lupe}{leg}</figure>"""


BAUKASTEN = {
    "scaffold": "🧩 Ausprobieren: Die Bereiche des Scaffold",
    "layout": "🧩 Ausprobieren: Widgets verschachteln",
}


def woerter_html(nr: int) -> str:
    return "".join(f"<dt>{e(w)}<small>{e(WOERTER[w][0])}</small></dt><dd>{e(WOERTER[w][1])}</dd>"
                   for w in LEVEL_WOERTER[nr])


def level_ansicht(nr: int, d: dict) -> str:
    g_titel, g_html = GRAFIK[d["grafik"]]
    bk = d.get("baukasten")
    baukasten = (f'<div class="card nur-begleitet"><h3>{BAUKASTEN[bk]}</h3><p class="klein">Schalten Sie Teile ein und aus und '
                 f'beobachten Sie Handy und Code. Fahren Sie mit der Maus über einen Bereich – im Handy und im Code '
                 f'leuchtet dieselbe Stelle auf.</p><div class="baukasten" data-baukasten="{bk}"></div></div>') if bk else ""
    wissen = ('<p class="wissen-link"><a class="knopf" href="#wissen">📘 Ausführlich erklärt: Aufbau von Stateless &amp; '
              'Stateful Widgets</a></p>') if d.get("wissen") else ""
    bilder = "".join(handy(b, t) for b, t in d["bilder"])
    zurueck = f'<a class="knopf" href="#level-{nr-1}">◀ Level {nr-1}</a>' if nr > 1 else '<a class="knopf" href="#start">◀ Start</a>'
    weiter = f'<a class="knopf primaer" href="#level-{nr+1}">Level {nr+1} ▶</a>' if nr < max(LEVEL) else '<a class="knopf primaer" href="#bonus">Bonus ▶</a>'
    std, std_hg = hintergrund_abtrennen(md_zu_html(DOCS / f"level_0{nr}.md"))
    ein, ein_hg = hintergrund_abtrennen(md_zu_html(DOCS / "einfach" / f"level_0{nr}.md", DOCS / f"level_0{nr}.md"))
    return f"""
<section class="ansicht level" id="level-{nr}" data-level="{nr}">
  <div class="card level-kopf">
    <span class="nummer" aria-hidden="true">{nr}</span>
    <div><h2>Level {nr} – {e(d['titel'])}</h2><p class="stich">{e(d['stich'])}</p></div>
  </div>
  <nav class="schritt-reiter" role="tablist" aria-label="Teile von Level {nr}">
    <button type="button" role="tab" data-schritt="ziel">🎯 Ziel</button>
    <button type="button" role="tab" data-schritt="auftrag">🛠️ Auftrag</button>
    <button type="button" role="tab" data-schritt="hintergrund">💡 Hintergrund</button>
    <button type="button" role="tab" data-schritt="pruefen">✅ Prüfen</button>
  </nav>
  <div class="schritt" data-schritt="ziel" role="tabpanel">
    <div class="ziel-raster">
      <div class="card ziel"><h3>So soll es aussehen</h3><div class="handys">{bilder}</div></div>
      <div class="card"><h3>Widget-Baum</h3>
        <ul class="baum"><li>{baum_html(d['baum'])}</li></ul>
        <p class="legende"><span class="knoten stateless"><b>Stateless</b></span>
        <span class="knoten stateful"><b>Stateful</b></span><span class="knoten state"><b>State</b></span>
        <span class="knoten neu"><b>neu</b></span></p>
      </div>
    </div>
    {baukasten}
    <p class="schritt-weiter"><button type="button" class="knopf primaer" data-geh="auftrag">Weiter: 🛠️ Auftrag ▶</button></p>
  </div>
  <div class="schritt" data-schritt="auftrag" role="tabpanel">
    <div class="card lp-auftrag"><div class="sprache-standard">{std}</div>
      <div class="sprache-einfach">{ein}
        <div class="woerter"><h3>📖 Wichtige Wörter</h3><dl>{woerter_html(nr)}</dl></div></div>
      <details class="loesung" data-loesung="{nr}" hidden><summary>🔓 Musterlösung Level {nr}</summary></details>
    </div>
    <p class="schritt-weiter"><button type="button" class="knopf" data-geh="ziel">◀ 🎯 Ziel</button><button type="button" class="knopf primaer" data-geh="hintergrund">Weiter: 💡 Hintergrund ▶</button></p>
  </div>
  <div class="schritt" data-schritt="hintergrund" role="tabpanel">
    <div class="card lp-hintergrund"><div class="sprache-standard">{std_hg}</div><div class="sprache-einfach">{ein_hg}</div></div>
    <div class="card grafik"><h3>{e(g_titel)}</h3>{g_html}{wissen}</div>
    <p class="schritt-weiter"><button type="button" class="knopf" data-geh="auftrag">◀ 🛠️ Auftrag</button><button type="button" class="knopf primaer" data-geh="pruefen">Weiter: ✅ Prüfen ▶</button></p>
  </div>
  <div class="schritt" data-schritt="pruefen" role="tabpanel">
  {bausteine.selbstkontrolle_html(nr, KONTROLLE[nr], KONTROLLE_EINFACH.get(nr))}
  </div>
  <div class="card lp-fuss">
    {zurueck}
    <div class="pruefen"><button class="erledigt" data-level="{nr}" disabled>Level geschafft</button></div>
    {weiter}
  </div>
</section>"""


def loesungen_verschluesseln(passwort: str) -> str:
    """Musterlösungen als JSON, AES-256-CBC, Schlüssel per PBKDF2-SHA256 aus dem Passwort."""
    daten = {}
    for ordner in sorted((ROOT / "loesungen" / "lib").glob("level_0*")):
        daten[ordner.name[-1]] = [
            {"datei": "lib/" + ("todo_app.dart" if f.name == "app.dart" else f.name),
             "code": f.read_text(encoding="utf-8").replace("import 'app.dart'", "import 'todo_app.dart'")}
            for f in sorted(ordner.glob("*.dart"))]
    # main.dart im Schülerprojekt (Level 1: MyFirstApp, ab Level 5: ToDoApp)
    main_dart = ("import 'package:flutter/material.dart';\n\nimport '{datei}';\n\n"
                 "void main() {{\n  runApp(const {klasse}());\n}}\n")
    daten["1"].insert(0, {"datei": "lib/main.dart", "code": main_dart.format(datei="my_first_app.dart", klasse="MyFirstApp")})
    daten["5"].insert(0, {"datei": "lib/main.dart", "code": main_dart.format(datei="todo_app.dart", klasse="ToDoApp")})
    daten["9"].insert(0, {"datei": "lib/main.dart", "code": main_dart.format(datei="my_first_app.dart", klasse="MyFirstApp")})
    klartext = (MARKER + json.dumps(daten, ensure_ascii=False)).encode("utf-8")
    salt, iv = secrets.token_bytes(16), secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", passwort.encode("utf-8"), salt, ITERATIONEN, 32)
    geheim = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-K", key.hex(), "-iv", iv.hex()],
                            input=klartext, capture_output=True, check=True).stdout
    b64 = lambda b: base64.b64encode(b).decode()
    return json.dumps({"salt": b64(salt), "iv": b64(iv), "iter": ITERATIONEN, "daten": b64(geheim)})


def passwort_holen() -> str:
    pw = os.environ.get("LOESUNG_PASSWORT", "")
    if not pw and sys.stdin.isatty():
        pw = getpass.getpass("Passwort für die Lösungen: ")
        if pw and pw != getpass.getpass("Passwort wiederholen: "):
            sys.exit("Die Passwörter stimmen nicht überein – abgebrochen.")
    if not pw:
        sys.exit("Kein Passwort angegeben (Eingabe oder LOESUNG_PASSWORT) – abgebrochen.")
    if len(pw) < 10:
        sys.exit("Bitte mindestens 10 Zeichen – die Seite ist öffentlich und kann durchprobiert werden.")
    return pw


CSS = """
.app{max-width:1280px}
.kopf{padding:20px 22px;position:relative}
.kopf{padding-right:140px}
.kopf{display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:18px;align-items:center}
.kopf>:not(.kopf-logo):not(.kopf-handy){grid-column:2}
.kopf>.schalter-zeile{grid-column:1/-1;margin-top:4px}
.kopf-logo{grid-column:1;grid-row:1/span 2;align-self:start;height:77px;width:auto;background:#fff;padding:6px 8px;border-radius:10px}
@media (max-width:640px){.kopf{display:block}.kopf-logo{display:block;height:59px;margin:0 0 10px}}
@media print{.kopf-logo{padding:0}}
.kopf-handy{position:absolute;right:28px;top:50%;margin:0;width:84px;aspect-ratio:9/17.5;transform:translateY(-50%) rotate(6deg);
  background:#11131c;border-radius:13px;padding:4px;box-shadow:0 10px 24px rgba(0,0,0,.35),0 0 0 2px rgba(255,255,255,.25)}
.begriff{border-bottom:2px dotted currentColor;cursor:help;border-radius:2px}
code.begriff{border-bottom-color:#6750a4}
.begriff:focus{outline:2px solid #f59e0b;outline-offset:1px}
#begriff-tipp{position:absolute;z-index:9999;max-width:min(300px,90vw);background:#1b2333;color:#fff;padding:8px 10px;border-radius:8px;font-size:.9rem;line-height:1.4;box-shadow:0 4px 14px #0004;pointer-events:none}
#begriff-tipp b{display:block;margin-bottom:2px}
@media print{.begriff{border:0}#begriff-tipp{display:none}}
.kh-app{position:relative;display:flex;flex-direction:column;gap:5px;width:100%;height:100%;border-radius:10px;background:#fdf8ff;overflow:hidden}
.kh-leiste{background:#6750a4;color:#fff;font:700 8px/1 system-ui,sans-serif;padding:13px 6px 6px}
.kh-zeile{display:flex;align-items:center;gap:4px;padding:0 6px}
.kh-zeile i{flex:none;width:7px;height:7px;border:1.5px solid #6750a4;border-radius:2px}
.kh-zeile.an i{background:#6750a4}
.kh-zeile b{height:4px;border-radius:2px;background:#9a93ad}
.kh-zeile.an b{background:#cbc5d8}
.kh-zeile u{margin-left:auto;width:5px;height:6px;border-radius:1px;background:#4b4560}
.kh-plus{position:absolute;right:6px;bottom:7px;width:18px;height:18px;border-radius:6px;background:#e8def8;color:#21005d;font:700 13px/18px system-ui,sans-serif;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.25)}
.kh-kerbe{position:absolute;top:6px;left:50%;transform:translateX(-50%);width:20px;height:4px;border-radius:3px;background:#11131c;z-index:1}
@media (max-width:700px){.kopf{padding-right:16px}.kopf-handy{display:none}}
.kopf a.chip{text-decoration:none}
.kopf a.chip.ok{background:rgba(255,255,255,.95);color:var(--ok);border-color:#fff}
.kopf a.chip.aktiv{outline:2px solid #fff;outline-offset:1px;font-weight:700}
.zaehler{font-weight:700}
a{color:var(--accent)}
.sr{position:absolute;left:-9999px}
.klein{font-size:.9rem;color:var(--ink-soft)}
.knopf{display:inline-flex;align-items:center;gap:6px;border-radius:12px;border:1px solid var(--line);background:var(--card2);
  color:var(--ink);padding:8px 14px;min-height:42px;text-decoration:none;font-weight:700}
.knopf.primaer{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.ansicht{display:flex;flex-direction:column;gap:12px}
.js .ansicht[hidden]{display:none}
.level-kopf{display:flex;gap:14px;align-items:center}
.level-kopf h2{margin:0}
.nummer{flex:0 0 52px;height:52px;border-radius:14px;display:grid;place-items:center;font-family:var(--titel);
  font-weight:800;font-size:1.5rem;background:var(--accent);color:#fff}
.level.fertig .nummer{background:var(--ok)}
.stich{margin:0;color:var(--muted)}
.ziel-raster{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;align-items:start}
.ziel-raster h3,.grafik h3{margin-top:0}
.schritt-reiter{position:sticky;top:0;z-index:5;display:flex;gap:6px;flex-wrap:wrap;padding:8px;margin:0 0 12px;
  background:var(--karte,#fff);border-radius:14px;box-shadow:0 2px 8px rgba(20,30,60,.12)}
.schritt-reiter button{flex:1 1 0;min-width:0;font:inherit;font-weight:600;padding:8px 10px;border-radius:10px;
  border:2px solid transparent;background:#eef0f7;color:#2a3150;cursor:pointer;white-space:nowrap}
.schritt-reiter.viele button{flex:1 1 auto;font-size:.9rem;padding:6px 10px}
.schritt-reiter button:hover{border-color:#b9c0dd}
.schritt-reiter button[aria-selected="true"]{background:#2d2f8f;color:#fff}
.schritt>*+*{margin-top:12px}
.schritt-weiter{display:flex;justify-content:flex-end;gap:8px;flex-wrap:wrap}
.schritt-weiter .knopf:first-child:not(.primaer){margin-right:auto}
.lp-auftrag{min-width:0}
.handys{display:flex;gap:10px;justify-content:center}
.handy{margin:0;flex:1;max-width:220px;min-width:0;text-align:center}
.handy .rahmen{display:block;width:100%;position:relative;background:#1a2130;border:0;border-radius:22px;padding:8px;
  box-shadow:var(--shadow);cursor:zoom-in;min-height:0}
.handy .rahmen:hover{background:#1a2130;outline:3px solid var(--accent)}
.bild{display:block;position:relative;border-radius:14px;overflow:hidden;background:#fff}
.bild img{display:block;width:100%;height:auto}
.marke{position:absolute;border:2px solid #f59e0b;border-radius:4px;box-shadow:0 0 0 1px rgba(255,255,255,.8);pointer-events:auto}
.marke-nr{position:absolute;transform:translate(-2px,-2px);min-width:18px;height:18px;border-radius:9px;background:#f59e0b;color:#1a2130;
  font-size:12px;font-weight:800;line-height:18px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.35)}
.marke.marke-hl{border-width:3px;background:rgba(245,158,11,.22)}
.marke-nr.marke-hl{transform:translate(-2px,-2px) scale(1.25)}
.lupe{position:absolute;right:12px;bottom:12px;background:rgba(255,255,255,.9);border-radius:50%;width:28px;height:28px;
  display:grid;place-items:center;font-size:14px}
.auftrags-kasten{background:#fdecec;border:2px solid #f3b4b4;border-left:6px solid #d9534f;border-radius:14px;
  padding:4px 16px 8px;margin:12px 0}
.auftrags-kasten h3{color:#b42318;margin-top:.6rem}
.auftrags-kasten h3::before{content:"✏️ "}
.auftrags-kasten :not(pre)>code{background:#fff;color:#1a2130}
pre.rahmen-code{padding:10px 0;line-height:1.45}
.modus-profi .nur-begleitet{display:none!important}
.schalter-zeile{flex-basis:100%;min-width:0;display:flex;flex-wrap:nowrap;align-items:center;gap:6px}
.schalter-zeile .pfad-wahl{padding:3px}.schalter-zeile .sprach-wahl{padding-left:3px}
.schalter-zeile .pfad-wahl button,.schalter-zeile .druck-kopf{padding:5px 9px;white-space:nowrap;font-size:.92rem}
@media (max-width:540px){.schalter-zeile{flex-wrap:wrap}}
.druck-kopf{display:none;align-items:center;gap:6px;border:1px solid rgba(255,255,255,.6);background:#fff;color:#1e3a8a;
  border-radius:999px;padding:8px 16px;font:inherit;font-weight:700;cursor:pointer}
.druck-kopf:hover{background:#e0e7ff}
:root:has(#wissen:not([hidden])) .druck-kopf{display:inline-flex}
.druck-fuss{display:none}
@media print{
  @page{size:A4;margin:14mm 12mm}
  html,body{background:#fff!important}
  body{font-size:10pt;line-height:1.4;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .schritt-reiter,.schritt-weiter,.kopf,.druck-kopf,.lp-fuss,.druck-knopf,.inhalt-navi,.pfad-wahl{display:none!important}
  .schritt[hidden]{display:block!important}
  html.druck-wissen .ansicht:not(#wissen){display:none!important}
  html.druck-wissen #wissen,#wissen{display:block!important}
  #wissen>*{margin:0 0 4mm}
  #wissen .card{display:block;padding:3mm 4mm!important;border-radius:6px!important}
  .app{max-width:none!important;padding:0!important}
  .card{box-shadow:none!important;border:1px solid #ccc!important;break-inside:avoid-page;page-break-inside:avoid}
  #wissen .card{break-inside:avoid;page-break-inside:avoid}
  #wissen .card:has(.anatomie){break-inside:auto;page-break-inside:auto}
  #wissen .anatomie{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr)!important;gap:4mm!important;break-inside:avoid;page-break-inside:avoid}
  #wissen .anatomie pre{font-size:7.6pt;line-height:1.45;white-space:pre!important;overflow:visible}
  #wissen .anatomie ol,#wissen .anatomie li,#wissen .anatomie p{font-size:8.8pt}
  #wissen .zwei,#wissen .vergleich-bild{gap:3mm!important}
  #wissen table{font-size:8.8pt}
  #wissen h2,#wissen h3,#wissen h4{break-after:avoid;page-break-after:avoid;color:#000}
  #wissen #w-stateless,#wissen #w-stateful{break-before:page;page-break-before:always}
  #wissen pre,#wissen table,#wissen .kasten,#wissen .schritt-box,#wissen .station{break-inside:avoid;page-break-inside:avoid}
  #wissen pre{background:#f5f6f8!important;color:#111!important;border:1px solid #bbb;white-space:pre-wrap;font-size:8.2pt;padding:2.5mm 3mm!important}
  #wissen pre *{color:#111!important}
  #wissen a{color:#000;text-decoration:none}
  .druck-fuss{display:block;font-size:8.5pt;color:#555;text-align:center;margin-top:8px}
  html.druck-wissen .druckfuss,:root:has(#wissen:target) .druckfuss{display:none!important}
}
.spr-einfach .sprache-standard{display:none!important}
html:not(.spr-einfach) .sprache-einfach{display:none!important}
.sprach-wahl{align-items:center;padding-left:10px}
.woerter{margin-top:16px;border-top:2px solid var(--line);padding-top:6px}
.woerter dl{display:grid;grid-template-columns:minmax(0,14rem) minmax(0,1fr);gap:6px 14px;margin:8px 0}
.woerter dt{font-weight:700}.woerter dt small{display:block;font-weight:400;color:#6b7280;font-size:.82rem}
.woerter dd{margin:0}
@media (max-width:620px){.woerter dl{grid-template-columns:minmax(0,1fr)}.woerter dd{margin-bottom:8px}}
html:not(.modus-profi) .nur-profi{display:none!important}
.profi-kasten h3::before{content:"🚀 "!important}
.modus-profi .erklaert{border:1px dashed var(--line);border-radius:12px;padding:0 14px;margin:12px 0}
.modus-profi .erklaert>h3{cursor:pointer;user-select:none}
.modus-profi .erklaert>h3::after{content:" ▸ bei Bedarf einblenden";font-size:.8rem;font-weight:500;color:#6b7280}
.modus-profi .erklaert.offen>h3::after{content:" ▾ ausblenden"}
.modus-profi .erklaert:not(.offen)>:not(h3){display:none}
.pfad-wahl{display:flex;gap:4px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:4px;flex:none}
.pfad-wahl button{border:0;background:none;border-radius:999px;padding:6px 12px;font:inherit;font-weight:600;cursor:pointer;color:#fff}
.pfad-wahl button.gewaehlt{background:#fff;color:#b42318}
.pfad-karten{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:12px}
.pfad-karte{text-align:left;font:inherit;color:inherit;background:var(--card2);border:2px solid var(--line);border-radius:16px;padding:14px 16px;cursor:pointer;display:flex;flex-direction:column;gap:6px}
.pfad-karte.gewaehlt{border-color:#d9534f;background:#fdecec}
.pk-titel{font-weight:800;font-size:1.15rem}.pk-unter{font-weight:600;color:#b42318}
.pk-liste{font-size:.92rem;line-height:1.6}.pk-fuer{font-size:.85rem;color:#6b7280}
@media (max-width:620px){.pfad-karten{grid-template-columns:minmax(0,1fr)}}
pre.rahmen-code .z{display:block;padding:0 14px 0 0;white-space:pre}
pre.rahmen-code .z i{display:inline-block;width:26px;text-align:center;font-style:normal;font-weight:700}
pre.rahmen-code .z.rahmen{color:#7f8aa0}
pre.rahmen-code .z.neu{background:rgba(34,197,94,.22);color:#eafff1}
pre.rahmen-code .z.neu i{color:#4ade80}
pre.rahmen-code .z.weg{background:rgba(239,68,68,.22);color:#ffd9d9;text-decoration:line-through;text-decoration-color:rgba(255,160,160,.8)}
pre.rahmen-code .z.weg i{color:#f87171;text-decoration:none}
.rahmen-legende{font-size:.88rem;background:#fff;border:1px solid #f3b4b4;border-radius:10px;padding:8px 12px;line-height:1.9}
.rahmen-legende .lg{display:inline-block;font-family:ui-monospace,Consolas,monospace;font-size:.82rem;border-radius:5px;padding:0 6px;background:#1a2130}
.rahmen-legende .lg.rahmen{color:#9aa4b8}.rahmen-legende .lg.neu{color:#4ade80;background:#173a2a}.rahmen-legende .lg.weg{color:#f87171;background:#3d1c22;text-decoration:line-through}
.ausschnitt{margin-top:8px;text-align:left}
.ausschnitt-titel{display:block;font-size:.78rem;font-weight:700;color:var(--ink-soft);margin-bottom:3px}
.ausschnitt-bild{display:block;width:100%;background-repeat:no-repeat;border:2px solid #f59e0b;border-radius:10px;background-color:#fef7ff}
.marken-legende{list-style:none;margin:6px 0 0;padding:0;text-align:left;font-size:.8rem;line-height:1.3}
.marken-legende li{display:flex;gap:6px;padding:3px 4px;border-radius:6px;cursor:default}
.marken-legende li span{color:#b45309;font-weight:800}
.marken-legende li.marke-hl{background:rgba(245,158,11,.2)}
#gross{border:0;border-radius:18px;padding:16px;max-width:min(860px,94vw);box-shadow:var(--shadow)}
#gross::backdrop{background:rgba(15,20,35,.6)}
.gross-inhalt{display:grid;grid-template-columns:minmax(0,360px) minmax(0,1fr);gap:18px;align-items:start}
.gross-inhalt .bild{border:8px solid #1a2130;border-radius:22px}
.gross-inhalt .marken-legende{font-size:.95rem}
.gross-inhalt h3{margin-top:0}
#gross form{text-align:right;margin-top:10px}
@media (max-width:600px){.gross-inhalt{grid-template-columns:1fr}}
.handy figcaption{font-size:.82rem;color:var(--ink-soft);margin-top:6px;line-height:1.3}
/* Widget-Baum */
.baum,.baum ul{list-style:none;margin:0;padding:0}
.baum ul{margin-left:14px;padding-left:12px;border-left:2px solid var(--line)}
.baum li{position:relative;padding:3px 0}
.baum ul>li::before{content:"";position:absolute;left:-12px;top:16px;width:10px;border-top:2px solid var(--line)}
.knoten{display:inline-flex;flex-wrap:wrap;align-items:baseline;gap:6px;padding:3px 9px;border-radius:9px;
  border:1px solid var(--line);background:var(--card2);font-size:.86rem}
.knoten small{color:var(--muted);font-size:.78rem}
.knoten.stateless{background:#e3eefc;border-color:#9fc0ef}
.knoten.stateful{background:#fde7dc;border-color:#f0a98a}
.knoten.state{background:#fff3d6;border-color:#e6c46e}
.knoten.neu{box-shadow:0 0 0 2px var(--accent)}
.neu-marke{font-style:normal;font-size:.68rem;font-weight:700;color:#fff;background:var(--accent);border-radius:6px;padding:0 5px}
.legende{display:flex;gap:6px;flex-wrap:wrap;margin:.8rem 0 0}
/* Grafiken */
.kette{display:flex;flex-wrap:wrap;align-items:stretch;gap:8px}
.schritt-box{flex:1 1 120px;display:flex;flex-direction:column;gap:2px;padding:10px 12px;border-radius:12px;
  background:var(--accent-soft);border:1px solid var(--line)}
.schritt-box b{font-family:ui-monospace,Consolas,monospace;font-size:.92rem}
.schritt-box span{font-size:.84rem;color:var(--ink-soft)}
.pfeil{align-self:center;font-size:1.4rem;color:var(--accent);font-weight:800}
.pfeil.kreis{font-size:.95rem}
.schachtel{border-radius:12px;padding:30px 14px 14px;position:relative;border:2px dashed var(--ink-soft)}
.schachtel .etikett{position:absolute;top:6px;left:10px;font-size:.8rem;font-weight:700;font-family:ui-monospace,monospace}
.s1{background:#fff;max-width:520px}.s2{background:#bdbdbd;border-style:solid}.s3{background:#d6d6d6}
.s4{background:#fff;border:2px solid var(--ink);padding:8px;text-align:center;font-weight:700;max-width:140px;margin:auto}
.zwei{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.kasten{flex:1 1 220px;padding:12px 14px;border-radius:14px;border:2px solid var(--line);background:var(--card2)}
.kasten b{display:block;font-family:ui-monospace,monospace}
.kasten small{color:var(--ink-soft)}
.kasten ul{margin:.4rem 0 0;padding-left:1.1rem;font-size:.9rem}
.kasten.stateful{background:#fde7dc;border-color:#f0a98a}
.kasten.state{background:#fff3d6;border-color:#e6c46e}
.kasten.stateless{background:#e3eefc;border-color:#9fc0ef}
.kasten table{margin-top:6px;font-size:.88rem}
.verbindung{display:flex;flex-direction:column;align-items:center;font-size:1.6rem;color:var(--accent);font-weight:800}
.verbindung code{font-size:.8rem}
.ebenen{display:flex;flex-direction:column;gap:8px;max-width:640px}
.ebenen .kasten{flex:none}
.runter{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:.88rem;padding:4px 18px}
.runter span{color:var(--accent);font-weight:700}
.runter .hoch{color:var(--ok)}
.reihe-demo{display:flex;gap:6px;max-width:560px;border:2px dashed var(--ink-soft);border-radius:12px;padding:8px}
.zelle{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:8px 10px;
  border-radius:10px;background:var(--card2);border:1px solid var(--line);font-size:1.1rem}
.zelle.breit{flex:1;align-items:flex-start;background:var(--accent-soft)}
.zelle small{font-size:.74rem;color:var(--ink-soft)}
.cb{width:18px;height:18px;border:2px solid var(--ink);border-radius:3px}
.liste-demo{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:12px}
.idx{border:1px solid var(--line);background:var(--card2);border-radius:8px;padding:4px 8px;font-family:ui-monospace,monospace;font-size:.86rem}
.idx i{color:var(--muted);font-style:normal;margin-right:4px}
.kl{background:#e3eefc;border:1px solid #9fc0ef;border-radius:8px;padding:4px 8px;font-size:.86rem}
.lp-fuss{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.pruefen{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.level.fertig button.erledigt{background:var(--ok);border-color:var(--ok);color:#fff}
pre{background:#1a2130;color:#e8ebf0;border-radius:12px;padding:12px 14px;overflow-x:auto;font-size:.86rem}
pre code{background:none;border:0;color:inherit;padding:0}
blockquote{margin:.8rem 0;padding:10px 14px;border-left:4px solid var(--deko);background:var(--accent-soft);border-radius:0 12px 12px 0}
blockquote p{margin:0}
table{border-collapse:collapse;width:100%}
td,th{border:1px solid var(--line);padding:5px 9px;text-align:left;vertical-align:top}
th{background:var(--card2)}
summary{cursor:pointer;font-weight:700}
details.loesung{margin-top:14px;border-color:var(--ok)}
/* Code-Kästen im Auftrag: zum Aufklappen */
details.code-klapp{border:0;padding:0;margin:.5rem 0;background:none}
details.code-klapp>summary{display:inline-flex;align-items:center;gap:8px;list-style:none;padding:6px 12px;border-radius:10px;
  background:#1a2130;color:#e8ebf0;font-weight:600;font-size:.9rem;user-select:none}
details.code-klapp>summary::-webkit-details-marker{display:none}
details.code-klapp>summary small{color:#9aa4b8;font-weight:500}
details.code-klapp>summary:hover{background:#2a3350}
details.code-klapp>summary:focus-visible{outline:2px solid #f59e0b;outline-offset:2px}
details.code-klapp[open]>summary{border-radius:10px 10px 0 0}
details.code-klapp[open]>pre{margin-top:0;border-top-left-radius:0}
details.code-klapp:not([open]) .ck-auf,details.code-klapp[open] .ck-zu{display:none}
.start-raster{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.start-raster h3{margin-top:0}
.uebersicht{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.uebersicht a{display:flex;flex-direction:column;gap:6px;text-decoration:none;color:var(--ink);background:var(--card);
  border:1px solid var(--line);border-radius:14px;padding:10px;box-shadow:var(--shadow)}
.uebersicht img{width:100%;height:150px;object-fit:cover;object-position:top;border-radius:10px;border:1px solid var(--line)}
.uebersicht b{font-family:var(--titel)}
.uebersicht .fertig-marke{display:none;color:var(--ok);font-weight:700;font-size:.85rem}
.uebersicht a.ok .fertig-marke{display:inline}
.echt{display:flex;gap:12px;align-items:flex-start;background:var(--warn-soft);border:1px solid #e6c46e;border-radius:14px;padding:12px 14px}
.echt span{font-size:1.6rem}
/* ---------- Wissensseite ---------- */
.inhalt-navi{display:flex;flex-wrap:wrap;gap:6px}
.inhalt-navi a{text-decoration:none;border:1px solid var(--line);background:var(--card2);border-radius:999px;padding:4px 12px;font-size:.88rem}
.anatomie{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:14px;align-items:start}
.anatomie pre{margin:0}
.zwei-code>div pre+.code-titel{margin-top:12px}
.code-titel{margin:0 0 4px;font-weight:700;font-size:.85rem;display:inline-block;padding:2px 10px;border-radius:8px}
.code-titel.stateful{background:#fde7dc}.code-titel.state{background:#fff3d6}
.m{display:inline-block;width:1.4em;color:#fbbf24;font-weight:700}
.marken{margin:0;padding-left:0;list-style:none;counter-reset:m}
.marken li{counter-increment:m;position:relative;padding:6px 0 6px 34px;border-bottom:1px solid var(--line);font-size:.93rem}
.marken li::before{content:counter(m);position:absolute;left:0;top:6px;width:24px;height:24px;border-radius:50%;
  background:#fbbf24;color:#1a2130;font-weight:800;display:grid;place-items:center;font-size:.8rem}
.vergleich th.stateless{background:#e3eefc}.vergleich th.stateful{background:#fde7dc}
.vergleich-bild{margin-top:10px}
.leben{display:flex;flex-direction:column;gap:6px;max-width:620px;margin:10px 0}
.station{display:flex;flex-direction:column;padding:10px 14px;border-radius:12px;background:var(--card2);border:1px solid var(--line);position:relative}
.station b{font-family:ui-monospace,monospace}
.station span{font-size:.88rem;color:var(--ink-soft)}
.station+.station::before{content:"↓";position:absolute;top:-17px;left:22px;color:var(--accent);font-weight:800}
.station.schleife{background:var(--accent-soft);border-color:var(--accent)}
.zurueck{margin-top:6px;font-size:.88rem;color:var(--accent);font-weight:700}
.entscheidung .frage{padding:12px 14px;border-radius:12px;background:var(--warn-soft);border:1px solid #e6c46e;margin-bottom:8px}
.antworten{display:flex;gap:10px;flex-wrap:wrap}
.wissen-link{margin:14px 0 0}
/* ---------- Baukästen ---------- */
.baukasten{display:grid;grid-template-columns:200px 230px minmax(0,1fr);gap:16px;align-items:start}
.bk-steuer{display:flex;flex-direction:column;gap:8px}
.bk-titel{margin:0;font-weight:700}
.bk-schalter{display:flex;gap:8px;align-items:center;cursor:pointer;font-size:.9rem}
.bk-schalter input{width:18px;height:18px;accent-color:var(--accent)}
.bk-feld{display:flex;flex-direction:column;gap:3px;font-size:.85rem;color:var(--ink-soft)}
.bk-feld input[type=text],.bk-feld select{font:inherit;color:var(--ink);padding:6px 8px;border-radius:8px;border:1px solid var(--line);background:var(--card)}
.bk-feld[hidden]{display:none}
.bk-handy{background:#1a2130;border-radius:26px;padding:9px;box-shadow:var(--shadow)}
.bk-schirm{position:relative;height:400px;border-radius:17px;overflow:hidden;background:#fef7ff;display:flex;flex-direction:column;
  font-family:Roboto,system-ui,sans-serif;color:#1d1b20;outline:3px solid transparent;outline-offset:-3px}
.bk-schirm.hl,.bk-schirm .hl{outline:3px solid #f59e0b!important;outline-offset:-3px;box-shadow:0 0 0 4px rgba(245,158,11,.25)}
.bk-schirm [data-teil]{cursor:pointer}
.m-appbar{flex:0 0 auto;display:flex;align-items:center;gap:8px;padding:14px 12px;font-size:1.05rem;background:#fef7ff}
.m-menu{border:0;background:none;font-size:1.1rem;padding:0 4px;min-height:0;color:inherit}
.m-body{flex:1;display:grid;place-items:center;padding:8px;font-size:.88rem;text-align:center}
.m-body.leer{color:#999}
.m-fab{position:absolute;right:14px;bottom:14px;width:46px;height:46px;min-height:0;border-radius:14px;border:0;background:#eaddff;
  color:#21005d;font-size:1.5rem;box-shadow:0 3px 6px rgba(0,0,0,.25);padding:0}
.m-bottom{flex:0 0 auto;display:flex;justify-content:space-around;padding:8px 0 10px;background:#f3edf7;font-size:.72rem}
.m-bottom~.m-fab{bottom:76px}
.m-ziel{display:flex;flex-direction:column;align-items:center;gap:2px}
.m-ziel i{font-style:normal;font-size:1rem;padding:2px 16px;border-radius:12px}
.m-ziel.aktiv i{background:#e8def8}
.m-schleier{position:absolute;inset:0;background:rgba(0,0,0,.35)}
.m-drawer{position:absolute;top:0;bottom:0;left:0;width:72%;background:#f7f2fa;padding:22px 16px;display:flex;flex-direction:column;gap:14px;
  border-radius:0 16px 16px 0;font-size:.9rem}
.l-body{flex:1;display:flex;flex-direction:column;min-height:0}
.l-padding,.l-farbe,.l-center{flex:1;display:flex;flex-direction:column;min-height:0}
.l-padding{background:repeating-linear-gradient(45deg,#fef7ff,#fef7ff 6px,#f1e6f5 6px,#f1e6f5 12px)}
.l-center{align-items:center;justify-content:center}
.l-text{align-self:flex-start;font-size:.85rem}
.l-center>.l-text{align-self:center}
.l-liste{display:flex;gap:4px}
.l-column{flex-direction:column;flex:1;align-self:flex-start}
.l-center>.l-column{align-self:center}
.l-row{flex-direction:row;align-self:stretch}
.l-kind{background:#fff;border:1px solid #79747e;border-radius:6px;padding:4px 10px;font-size:.8rem}
.bk-rechts{display:flex;flex-direction:column;gap:10px;min-width:0}
.bk-codeleiste{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
.bk-kopieren{min-height:34px;padding:4px 12px;font-size:.85rem}
.bk-zeile.rahmen-zeile{color:#9aa4b8}
.bk-zeile.rahmen-zeile.hl{color:#fff}
.bk-spielwiese{margin:0}
.bk-code{margin:0;font-size:.8rem;line-height:1.5}
.bk-zeile{display:inline-block;width:100%;border-radius:4px;cursor:pointer}
.bk-zeile.hl{background:rgba(245,158,11,.35)}
.bk-info{padding:10px 12px;border-radius:12px;background:var(--accent-soft);font-size:.9rem;min-height:3.2em}
@media (max-width:1100px){.baukasten{grid-template-columns:200px minmax(0,1fr)}.bk-rechts{grid-column:1/-1}}
@media (max-width:620px){.baukasten{grid-template-columns:minmax(0,1fr)}.bk-handy{width:100%;max-width:250px;margin:auto}.anatomie{grid-template-columns:minmax(0,1fr)}}
@media (max-width:980px){.ziel-raster{grid-template-columns:1fr}}
@media (max-width:540px){.schritt-reiter button{flex-basis:calc(50% - 3px)}.schritt-reiter.viele button{white-space:normal}}
@media (max-width:700px){.uebersicht{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:600px){table{display:block;overflow-x:auto;max-width:100%}p code,li code,td code{overflow-wrap:anywhere}.app{padding:10px}.kopf{padding:16px}}
"""

JS = r"""
document.documentElement.classList.add("js");
(function(){
  var MKEY = "flutter-lernpfad-lf11-modus", wurzel = document.documentElement;
  function setze(m){
    wurzel.classList.toggle("modus-profi", m === "profi");
    document.querySelectorAll(".pfad-wahl button, .pfad-karte").forEach(function(b){
      var an = b.getAttribute("data-modus") === m;
      b.setAttribute("aria-pressed", an ? "true" : "false"); b.classList.toggle("gewaehlt", an);
    });
  }
  var m = "begleitet"; try { m = localStorage.getItem(MKEY) || m; } catch (e) {}
  setze(m);
  window.addEventListener("afterprint", function(){ wurzel.classList.remove("druck-wissen"); });
  var SKEY = "flutter-lernpfad-lf11-sprache";
  function sprache(s){
    wurzel.classList.toggle("spr-einfach", s === "einfach");
    document.querySelectorAll("[data-sprache]").forEach(function(b){
      var an = b.getAttribute("data-sprache") === s;
      b.setAttribute("aria-pressed", an ? "true" : "false"); b.classList.toggle("gewaehlt", an);
    });
  }
  var sp = "standard"; try { sp = localStorage.getItem(SKEY) || sp; } catch (e) {}
  sprache(sp);
  document.addEventListener("click", function(ev){
    if (ev.target.closest("[data-drucken]")) { wurzel.classList.add("druck-wissen"); window.print(); return; }
    var sb = ev.target.closest("[data-sprache]");
    if (sb) { var ns = sb.getAttribute("data-sprache"); sprache(ns); try { localStorage.setItem(SKEY, ns); } catch (e) {} return; }
    var b = ev.target.closest("[data-modus]");
    if (b) { var neu = b.getAttribute("data-modus"); setze(neu); try { localStorage.setItem(MKEY, neu); } catch (e) {} return; }
    var h = ev.target.closest(".erklaert > h3");
    if (h && wurzel.classList.contains("modus-profi")) h.parentNode.classList.toggle("offen");
  });
})();
(function(){
  var KEY = "flutter-lernpfad-lf11", stand = {};
  try { stand = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
  var ansichten = document.querySelectorAll(".ansicht");
  function route(){
    var ziel = document.getElementById((location.hash || "#start").slice(1));
    var ansicht = ziel && ziel.closest(".ansicht");
    if (!ansicht) { ansicht = document.getElementById("start"); ziel = null; }
    var id = ansicht.id;
    ansichten.forEach(function(a){ a.hidden = a.id !== id; });
    document.querySelectorAll("[data-ziel]").forEach(function(c){ c.classList.toggle("aktiv", c.dataset.ziel === id); });
    if (ansicht.querySelector(".schritt")) {
      var s = ziel && ziel !== ansicht && ziel.closest(".schritt");
      var gemerkt; try { gemerkt = sessionStorage.getItem(KEY + "-schritt-" + id); } catch (e) {}
      schritt(ansicht, s ? s.dataset.schritt : (gemerkt || ansicht.querySelector(".schritt").dataset.schritt));
    }
    if (ziel && ziel !== ansicht) ziel.scrollIntoView(); else window.scrollTo(0, 0);
  }
  function schritt(ansicht, name){
    ansicht.querySelectorAll(".schritt").forEach(function(p){ p.hidden = p.dataset.schritt !== name; });
    ansicht.querySelectorAll(".schritt-reiter button").forEach(function(b){ b.setAttribute("aria-selected", b.dataset.schritt === name); });
    try { sessionStorage.setItem(KEY + "-schritt-" + ansicht.id, name); } catch (e) {}
  }
  document.addEventListener("click", function(ev){
    var b = ev.target.closest(".schritt-reiter button, [data-geh]");
    if (!b) return;
    var ansicht = b.closest(".ansicht");
    schritt(ansicht, b.dataset.schritt || b.dataset.geh);
    var r = ansicht.querySelector(".schritt-reiter");
    if (r.getBoundingClientRect().top < 0 || b.dataset.geh) ansicht.querySelector(".level-kopf").scrollIntoView();
  });
  function zeigen(){
    var n = 0;
    document.querySelectorAll(".level").forEach(function(s){
      var nr = s.dataset.level, ok = !!stand[nr];
      if (ok) n++;
      s.classList.toggle("fertig", ok);
      var b = s.querySelector("button.erledigt");
      b.textContent = ok ? "✓ Geschafft (zurücksetzen)" : "Level geschafft";
      b.setAttribute("aria-pressed", ok);
      document.querySelectorAll('[data-ziel="level-' + nr + '"]').forEach(function(c){ c.classList.toggle("ok", ok); });
    });
    document.getElementById("zaehler").textContent = n + " / 9";
  }
  document.querySelectorAll("button.erledigt").forEach(function(b){
    b.addEventListener("click", function(){
      stand[b.dataset.level] = !stand[b.dataset.level];
      try { localStorage.setItem(KEY, JSON.stringify(stand)); } catch (e) {}
      zeigen();
    });
  });
  // Zielbilder: Markierung ↔ Legende, Großansicht
  document.addEventListener("mouseover", function(ev){
    var t = ev.target.closest("[data-marke]"), fig = t && t.closest(".handy, .gross-inhalt");
    document.querySelectorAll(".marke-hl").forEach(function(el){ el.classList.remove("marke-hl"); });
    if (fig) fig.querySelectorAll('[data-marke="' + t.dataset.marke + '"]').forEach(function(el){ el.classList.add("marke-hl"); });
  });
  var dlg = document.getElementById("gross");
  document.querySelectorAll(".handy .rahmen").forEach(function(b){
    b.addEventListener("click", function(){
      var fig = b.closest(".handy"), ziel = dlg.querySelector(".gross-inhalt");
      ziel.innerHTML = "";
      ziel.appendChild(fig.querySelector(".bild").cloneNode(true));
      var leg = fig.querySelector(".marken-legende"), cap = fig.querySelector("figcaption");
      var rechts = document.createElement("div");
      if (cap) { var h = document.createElement("h3"); h.textContent = cap.textContent; rechts.appendChild(h); }
      if (leg) rechts.appendChild(leg.cloneNode(true));
      ziel.appendChild(rechts);
      if (dlg.showModal) dlg.showModal();
    });
  });
  dlg.addEventListener("click", function(ev){ if (ev.target === dlg) dlg.close(); });
  // Code-Kästen in den Aufträgen ausklappbar machen (zu Beginn zu – erst lesen, dann aufklappen und tippen)
  document.querySelectorAll(".auftrags-kasten pre").forEach(function(pre){
    if (pre.closest("details")) return;
    var rahmen = pre.classList.contains("rahmen-code"), art = rahmen ? "Code" : "Befehle";
    var n = rahmen ? pre.querySelectorAll(".z").length : pre.textContent.replace(/\n+$/, "").split("\n").length;
    var d = document.createElement("details"); d.className = "code-klapp";
    var su = document.createElement("summary");
    su.innerHTML = '<span class="ck-zu">▶ ' + art + ' anzeigen</span><span class="ck-auf">▼ ' + art + ' ausblenden</span>'
      + '<small>' + n + (n === 1 ? " Zeile" : " Zeilen") + '</small>';
    pre.parentNode.insertBefore(d, pre); d.appendChild(su); d.appendChild(pre);
  });
  window.addEventListener("hashchange", route);
  route(); zeigen();
})();
"""

JS_LOESUNG = r"""
(function(){
  if (typeof GEHEIM === "undefined" || !GEHEIM) return;
  var b = function(s){ return Uint8Array.from(atob(s), function(c){ return c.charCodeAt(0); }); };
  var status = document.getElementById("pw-status");
  async function entschluesseln(pw){
    var basis = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveKey"]);
    var key = await crypto.subtle.deriveKey(
      {name: "PBKDF2", salt: b(GEHEIM.salt), iterations: GEHEIM.iter, hash: "SHA-256"},
      basis, {name: "AES-CBC", length: 256}, false, ["decrypt"]);
    var klar = await crypto.subtle.decrypt({name: "AES-CBC", iv: b(GEHEIM.iv)}, key, b(GEHEIM.daten));
    var text = new TextDecoder().decode(klar);
    if (text.indexOf(MARKER) !== 0) throw new Error("falsch");
    return JSON.parse(text.slice(MARKER.length));
  }
  function einfuegen(daten){
    Object.keys(daten).forEach(function(nr){
      var box = document.querySelector('[data-loesung="' + nr + '"]');
      if (!box) return;
      box.querySelectorAll("div").forEach(function(d){ d.remove(); });
      daten[nr].forEach(function(f){
        var div = document.createElement("div");
        var h = document.createElement("h3"); h.textContent = f.datei;
        var pre = document.createElement("pre"), code = document.createElement("code");
        code.textContent = f.code; pre.appendChild(code);
        div.appendChild(h); div.appendChild(pre); box.appendChild(div);
      });
      box.hidden = false;
    });
  }
  document.getElementById("entsperren").addEventListener("submit", async function(ev){
    ev.preventDefault();
    status.textContent = "Prüfe …";
    try {
      einfuegen(await entschluesseln(document.getElementById("pw").value));
      status.textContent = "✓ Freigeschaltet – die Lösungen stehen jetzt in jedem Level unten im Auftrag.";
    } catch (err) { status.textContent = "✗ Passwort falsch."; }
  });
})();
"""


def main() -> None:
    ohne = "--ohne-loesungen" in sys.argv
    geheim = "null" if ohne else loesungen_verschluesseln(passwort_holen())
    navi = ('<a class="chip" href="#start" data-ziel="start">Start</a>'
            + "".join(f'<a class="chip" href="#level-{n}" data-ziel="level-{n}">{n}</a>' for n in LEVEL)
            + '<a class="chip" href="#wissen" data-ziel="wissen" title="Wissen: Stateless &amp; Stateful">📘 Wissen</a>'
            + '<a class="chip" href="#bonus" data-ziel="bonus">★</a>'
            + '<a class="chip" href="#loesungen" data-ziel="loesungen" title="Musterlösungen">🔒</a>'
            + '<span class="chip zaehler" id="zaehler">0 / 9</span>')
    uebersicht = "".join(
        f'<a href="#level-{n}" data-ziel="level-{n}"><img src="bilder/{d["bilder"][-1][0]}.png" alt="" loading="lazy">'
        f'<b>{n} · {e(d["titel"])}</b><span class="klein">{e(d["stich"])}</span>'
        f'<span class="fertig-marke">✓ geschafft</span></a>' for n, d in LEVEL.items())
    ansichten = "".join(level_ansicht(n, d) for n, d in LEVEL.items())
    seite = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Flutter-Einführung LF11</title>
<meta name="version" content="{VERSION}">
<meta name="description" content="In 9 Leveln zur eigenen Flutter-App mit Login und ToDo-Liste – alles selbst getippt, mit Selbstkontrolle.">
<link rel="stylesheet" href="css/stil.css">
<style>{CSS}{bausteine.CSS}</style>
</head>
<body data-thema="technik">
<div class="app">
  <header class="card kopf">
    <figure class="kopf-handy" aria-hidden="true"><span class="kh-kerbe"></span><span class="kh-app"><span class="kh-leiste">ToDo Liste</span><span class="kh-zeile an"><i></i><b style="width:62%"></b><u></u></span><span class="kh-zeile"><i></i><b style="width:48%"></b><u></u></span><span class="kh-zeile an"><i></i><b style="width:70%"></b><u></u></span><span class="kh-zeile"><i></i><b style="width:40%"></b><u></u></span><span class="kh-plus">+</span></span></figure>
    {LOGO}
    <div class="titel">
      <h1>Flutter-Einführung <span class="version">LF11 · Version {VERSION}</span></h1>
      <div class="unter">In 9 Leveln zur eigenen App: Login-Maske, danach ToDo-Liste – jede Zeile selbst getippt.</div>
    </div>
    <nav class="fortschritt" aria-label="Level">{navi}</nav>
    <div class="schalter-zeile">
    <div class="pfad-wahl" role="group" aria-label="Lernpfad wählen">
      <button type="button" data-modus="begleitet" aria-pressed="true">🧭 Begleitet</button>
      <button type="button" data-modus="profi" aria-pressed="false">🚀 Profi</button>
    </div>
    <div class="pfad-wahl sprach-wahl" role="group" aria-label="Sprache wählen">
      <button type="button" data-sprache="standard" aria-pressed="true">Standard</button>
      <button type="button" data-sprache="einfach" aria-pressed="false">Sprache einfach</button>
    </div>
    <button type="button" class="druck-kopf" data-drucken title="Druckt nur die Wissen-Seite – auch als PDF speichern">🖨️ Drucken</button>
    </div>
  </header>

  <section class="ansicht" id="start">
    <div class="card echt"><span aria-hidden="true">💻</span><div>
      <b>Programmiert wird nicht im Browser, sondern in Ihrer echten Entwicklungsumgebung</b>
      (Android Studio oder VS Code) – mit eigenem Flutter-Projekt und Emulator, genau wie im Betrieb.
      Es gibt <b>keine Vorlagen zum Herunterladen</b>: Sie legen das Projekt selbst an und tippen jede Zeile.
      Diese Seite ist Ihr Wegweiser: Auftrag, Zielbild, Widget-Baum, Hilfen und Selbstkontrolle.</div></div>
    <div class="card"><h2>Wählen Sie Ihren Pfad</h2>
      <p>Beide Pfade bauen <b>dieselbe App</b> mit denselben Leveln und derselben Selbstkontrolle. Sie können jederzeit
      oben im Seitenkopf umschalten – auch mitten in einem Level.</p>
      <div class="pfad-karten">
        <button type="button" class="pfad-karte" data-modus="begleitet">
          <span class="pk-titel">🧭 Begleiteter Pfad</span>
          <span class="pk-unter">mit sehr viel Unterstützung</span>
          <span class="pk-liste">✔ jeder Schritt einzeln: neue Datei, ändern oder löschen<br>
          ✔ Code-Rahmen zeigen genau die Stelle in der Datei<br>✔ Erklärungen, Tipps und interaktive Baukästen</span>
          <span class="pk-fuer">Für alle, die Flutter zum ersten Mal sehen.</span>
        </button>
        <button type="button" class="pfad-karte" data-modus="profi">
          <span class="pk-titel">🚀 Profipfad</span>
          <span class="pk-unter">nur Anforderungen – den Weg finden Sie selbst</span>
          <span class="pk-liste">✔ je Level eine knappe Liste: Was muss die App können?<br>
          ✔ kein Code vorgegeben, Erklärungen nur auf Klick<br>✔ Zielbild und Widget-Baum als Spezifikation</span>
          <span class="pk-fuer">Für alle, die schon programmieren und selbstständig arbeiten wollen.</span>
        </button>
      </div>
    </div>
    <div class="card"><h2>So geht's</h2>
      <div class="start-raster">
        <div><h3>1 · Projekt anlegen</h3>
          <p>In Level 1 legen Sie mit <code>flutter create meine_app</code> Ihr eigenes Projekt an.
          Diese eine App bauen Sie in allen Leveln weiter aus.</p></div>
        <div><h3>2 · Auftrag lesen</h3>
          <p>Der rote Kasten sagt, was zu tun ist – im begleiteten Pfad Schritt für Schritt, im Profipfad als Anforderungsliste. <i>Erklärt</i> sagt, warum. Zielbild und Widget-Baum zeigen, wo Sie hinwollen.</p></div>
        <div><h3>3 · Abtippen</h3>
          <p>Code wird <b>abgetippt</b> – Kopieren ist auf dieser Seite gesperrt. Wer tippt, liest jede Zeile und lernt die
          Fehlermeldungen der IDE kennen. Nach Änderungen: <b>Hot Reload</b>.</p></div>
        <div><h3>4 · Selbstkontrolle</h3>
          <p>Unter jedem Level: Haken setzen, was in Ihrer App wirklich funktioniert, Kontrollfragen beantworten –
          dann ist das Level geschafft.</p></div>
      </div>
    </div>
    <div class="card"><h2>Grundlagen zum Nachschlagen</h2>
      <p><a href="#wissen">📘 Wissen: Stateless &amp; Stateful</a> – Aufbau beider Widget-Arten Zeile für Zeile, Vergleich,
      setState, Lebenszyklus und typische Fehler. In Level 1–3 finden Sie außerdem interaktive Baukästen zu Scaffold und Layout.</p></div>
    <div class="card"><h2>Ihr Weg in 9 Leveln</h2><div class="uebersicht">{uebersicht}</div>
      <p style="margin-top:14px"><a class="knopf primaer" href="#level-1">Los geht's mit Level 1 ▶</a></p></div>
  </section>
{ansichten}
  <section class="ansicht" id="wissen">
{wissen_reiter((ROOT / "tool" / "wissen.html").read_text(encoding="utf-8"))}
    <p class="druck-fuss">Flutter-Einführung LF11 · Version {VERSION} · Stand {STAND} · bnbsinfo.github.io/lf11_lernpfade/flutter/</p>
    <div class="card lp-fuss"><a class="knopf" href="#start">◀ Start</a><button type="button" class="knopf druck-knopf" data-drucken>🖨️ Wissen drucken</button><a class="knopf primaer" href="#level-1">Zu Level 1 ▶</a></div>
  </section>

  <section class="ansicht" id="bonus">
    <div class="card level-kopf"><span class="nummer" aria-hidden="true">★</span>
      <div><h2>Bonus – Die App weiterentwickeln</h2><p class="stich">für alle, die fertig sind</p></div></div>
    <div class="card">{md_zu_html(DOCS / "bonus.md")}</div>
    <div class="card lp-fuss"><a class="knopf" href="#level-9">◀ Level 9</a><a class="knopf" href="#start">Zum Start</a></div>
  </section>

  <section class="ansicht" id="loesungen">
    <div class="card"><h2>🔒 Musterlösungen</h2>
      <p>Die Lösungen sind verschlüsselt. Mit dem Passwort Ihrer Lehrkraft erscheinen sie in jedem Level
      unten im Auftrag unter <i>Musterlösung</i>. Erst selbst probieren – Fehlermeldungen lesen und die Tipps nutzen bringt mehr als jede Lösung!</p>
      <form id="entsperren" class="pruefen">
        <label for="pw" class="sr">Passwort</label>
        <input id="pw" type="password" autocomplete="off" placeholder="Passwort"
          style="font:inherit;padding:8px 12px;border-radius:12px;border:1px solid var(--line);min-height:42px">
        <button class="primaer" type="submit">Lösungen anzeigen</button>
        <span id="pw-status" role="status"></span>
      </form></div>
  </section>

  <footer class="druckfuss"><small>Flutter-Einführung LF11 · Version {VERSION} vom {STAND} · BS Info · Ihr Fortschritt auf dieser Seite wird nur in Ihrem Browser gespeichert.</small></footer>
</div>
<dialog id="gross" aria-label="Großansicht"><div class="gross-inhalt"></div>
  <form method="dialog"><button class="primaer">Schließen</button></form></dialog>
<script>var LP_KEY = "flutter-lernpfad-lf11";{JS}</script>
<script>{bausteine.JS}</script>
<script>{(ROOT / "tool" / "baukasten.js").read_text(encoding="utf-8")}</script>
<script>var BEGRIFFE = {json.dumps({w: v[1] for w, v in WOERTER.items()}, ensure_ascii=False)};{(ROOT / "tool" / "begriffe.js").read_text(encoding="utf-8")}</script>
<script>var GEHEIM = {geheim}; var MARKER = {json.dumps(MARKER)};{JS_LOESUNG}</script>
</body>
</html>
"""
    (DOCS / "index.html").write_text(bausteine.einbetten(seite, DOCS), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print("Erstellt:", DOCS / "index.html")


if __name__ == "__main__":
    main()
