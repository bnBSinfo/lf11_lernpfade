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

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO = "bnBSinfo/flutter_lernpfad_schueler"
ITERATIONEN = 600_000
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
        grafik="start",
    ),
    2: dict(
        titel="Widget im Widget", stich="Padding, ColoredBox, Center",
        bilder=[("level_2", "Grauer Kasten mit 50 Pixel Rand, Text in der Mitte")],
        baum=k("MyFirstApp", "stateless", kinder=[k("MaterialApp", kinder=[k("Scaffold", kinder=[
            k("Padding", neu=True, notiz="body:", kinder=[
                k("ColoredBox", neu=True, notiz="child:", kinder=[
                    k("Center", neu=True, notiz="child:", kinder=[
                        k("Text", notiz="child:")])])])])])]),
        grafik="schachteln",
    ),
    3: dict(
        titel="Das erste Stateful Widget", stich="StatefulWidget, State, eigene Datei",
        bilder=[("level_3", "AppBar oben, Text aus dem Stateful Widget in der Mitte")],
        baum=k("MyFirstApp", "stateless", kinder=[k("MaterialApp", kinder=[k("Scaffold", kinder=[
            k("AppBar", neu=True, notiz="appBar:", kinder=[k("Text")]),
            k("MyLogin", "stateful", neu=True, notiz="body:", kinder=[
                k("_MyLoginState", "state", neu=True, notiz="createState()", kinder=[
                    k("Center", kinder=[k("Text")])])])])])]),
        grafik="stateful",
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
        grafik="setstate",
    ),
    5: dict(
        titel="Ein ToDo-Element", stich="Row, Checkbox, Expanded, IconButton",
        bilder=[("level_5", "Drei ToDoItems – Checkbox und Mülleimer noch ohne Funktion")],
        baum=k("ToDoItem", "stateless", notiz="title", kinder=[
            k("Row", neu=True, notiz="children:", kinder=[
                k("Checkbox", neu=True, notiz="value: false"),
                k("Expanded", neu=True, kinder=[k("Text", notiz="title")]),
                k("IconButton", neu=True, kinder=[k("Icon", notiz="Icons.delete")])])]),
        grafik="row",
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
        grafik="liste",
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
def md_zu_html(pfad: pathlib.Path) -> str:
    text = re.sub(r"^# .*\n", "", pfad.read_text(encoding="utf-8"), count=1)
    out = subprocess.run(["pandoc", "-f", "gfm", "-t", "html", "--no-highlight"],
                         input=text, capture_output=True, text=True, check=True).stdout
    return out.replace("<h2", "<h3").replace("</h2>", "</h3>")


def baum_html(knoten) -> str:
    name, art, neu, kinder, notiz = knoten
    klassen = f"knoten {art}" + (" neu" if neu else "")
    n = f'<small>{e(notiz)}</small>' if notiz else ""
    marke = '<em class="neu-marke">neu</em>' if neu else ""
    kinder_html = "".join(f"<li>{baum_html(c)}</li>" for c in kinder)
    sub = f"<ul>{kinder_html}</ul>" if kinder else ""
    return f'<span class="{klassen}"><b>{e(name)}</b>{n}{marke}</span>{sub}'


def handy(bild, text):
    return f"""<figure class="handy"><div class="rahmen"><img src="bilder/{bild}.png" width="360" height="640"
      alt="{e(text)}" loading="lazy"></div><figcaption>{e(text)}</figcaption></figure>"""


def level_ansicht(nr: int, d: dict) -> str:
    g_titel, g_html = GRAFIK[d["grafik"]]
    bilder = "".join(handy(b, t) for b, t in d["bilder"])
    zurueck = f'<a class="knopf" href="#level-{nr-1}">◀ Level {nr-1}</a>' if nr > 1 else '<a class="knopf" href="#start">◀ Start</a>'
    weiter = f'<a class="knopf primaer" href="#level-{nr+1}">Level {nr+1} ▶</a>' if nr < 8 else '<a class="knopf primaer" href="#bonus">Bonus ▶</a>'
    return f"""
<section class="ansicht level" id="level-{nr}" data-level="{nr}">
  <div class="card level-kopf">
    <span class="nummer" aria-hidden="true">{nr}</span>
    <div><h2>Level {nr} – {e(d['titel'])}</h2><p class="stich">{e(d['stich'])}</p></div>
  </div>
  <div class="level-raster">
    <div class="card lp-auftrag">{md_zu_html(DOCS / f"level_0{nr}.md")}
      <details class="loesung" data-loesung="{nr}" hidden><summary>🔓 Musterlösung Level {nr}</summary></details>
    </div>
    <aside class="lp-seite">
      <div class="card ziel"><h3>So soll es aussehen</h3><div class="handys">{bilder}</div></div>
      <div class="card"><h3>Widget-Baum</h3>
        <ul class="baum"><li>{baum_html(d['baum'])}</li></ul>
        <p class="legende"><span class="knoten stateless"><b>Stateless</b></span>
        <span class="knoten stateful"><b>Stateful</b></span><span class="knoten state"><b>State</b></span>
        <span class="knoten neu"><b>neu</b></span></p>
      </div>
    </aside>
  </div>
  <div class="card grafik"><h3>{e(g_titel)}</h3>{g_html}</div>
  <div class="card lp-fuss">
    {zurueck}
    <div class="pruefen"><code>flutter test test/level_0{nr}_test.dart</code>
      <button class="erledigt" data-level="{nr}">Test ist grün – geschafft</button></div>
    {weiter}
  </div>
</section>"""


def loesungen_verschluesseln(passwort: str) -> str:
    """Musterlösungen als JSON, AES-256-CBC, Schlüssel per PBKDF2-SHA256 aus dem Passwort."""
    daten = {}
    for ordner in sorted((ROOT / "loesungen" / "lib").glob("level_0*")):
        daten[ordner.name[-1]] = [
            {"datei": f"lib/{ordner.name}/{f.name}", "code": f.read_text(encoding="utf-8")}
            for f in sorted(ordner.glob("*.dart"))]
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
.kopf{padding:20px 22px}
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
.level-raster{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:12px;align-items:start}
.lp-seite{display:flex;flex-direction:column;gap:12px;position:sticky;top:12px}
.lp-seite h3,.grafik h3{margin-top:0}
.lp-auftrag{min-width:0}
.handys{display:flex;gap:10px;justify-content:center}
.handy{margin:0;flex:1;max-width:220px;min-width:0;text-align:center}
.handy .rahmen{background:#1a2130;border-radius:22px;padding:8px;box-shadow:var(--shadow)}
.handy img{display:block;width:100%;height:auto;border-radius:14px;background:#fff}
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
@media (max-width:980px){.level-raster{grid-template-columns:1fr}.lp-seite{position:static;order:-1}}
@media (max-width:700px){.uebersicht{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:600px){.app{padding:10px}.kopf{padding:16px}}
"""

JS = r"""
document.documentElement.classList.add("js");
(function(){
  var KEY = "flutter-lernpfad-lf11", stand = {};
  try { stand = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
  var ansichten = document.querySelectorAll(".ansicht");
  function route(){
    var id = (location.hash || "#start").slice(1);
    if (!document.getElementById(id) || !document.getElementById(id).classList.contains("ansicht")) id = "start";
    ansichten.forEach(function(a){ a.hidden = a.id !== id; });
    document.querySelectorAll("[data-ziel]").forEach(function(c){ c.classList.toggle("aktiv", c.dataset.ziel === id); });
    window.scrollTo(0, 0);
  }
  function zeigen(){
    var n = 0;
    document.querySelectorAll(".level").forEach(function(s){
      var nr = s.dataset.level, ok = !!stand[nr];
      if (ok) n++;
      s.classList.toggle("fertig", ok);
      var b = s.querySelector("button.erledigt");
      b.textContent = ok ? "✓ Geschafft (zurücksetzen)" : "Test ist grün – geschafft";
      b.setAttribute("aria-pressed", ok);
      document.querySelectorAll('[data-ziel="level-' + nr + '"]').forEach(function(c){ c.classList.toggle("ok", ok); });
    });
    document.getElementById("zaehler").textContent = n + " / 8";
  }
  document.querySelectorAll("button.erledigt").forEach(function(b){
    b.addEventListener("click", function(){
      stand[b.dataset.level] = !stand[b.dataset.level];
      try { localStorage.setItem(KEY, JSON.stringify(stand)); } catch (e) {}
      zeigen();
    });
  });
  window.addEventListener("hashchange", route);
  route(); zeigen();
})();
"""

JS_LOESUNG = r"""
(function(){
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
    geheim = loesungen_verschluesseln(passwort_holen())
    navi = ('<a class="chip" href="#start" data-ziel="start">Start</a>'
            + "".join(f'<a class="chip" href="#level-{n}" data-ziel="level-{n}">{n}</a>' for n in LEVEL)
            + '<a class="chip" href="#bonus" data-ziel="bonus">★</a>'
            + '<a class="chip" href="#loesungen" data-ziel="loesungen" title="Musterlösungen">🔒</a>'
            + '<span class="chip zaehler" id="zaehler">0 / 8</span>')
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
<title>Flutter-Lernpfad LF11</title>
<meta name="description" content="In 8 Leveln zur ersten eigenen Flutter-App – mit automatischen Tests.">
<link rel="stylesheet" href="css/stil.css">
<style>{CSS}</style>
</head>
<body data-thema="technik">
<div class="app">
  <header class="card kopf">
    <div class="titel">
      <h1>Flutter-Lernpfad <span class="version">LF11</span></h1>
      <div class="unter">In 8 Leveln zur ersten eigenen App – Sie programmieren echt, die Tests prüfen mit.</div>
    </div>
    <nav class="fortschritt" aria-label="Level">{navi}</nav>
  </header>

  <section class="ansicht" id="start">
    <div class="card echt"><span aria-hidden="true">💻</span><div>
      <b>Programmiert wird nicht im Browser, sondern in Ihrer echten Entwicklungsumgebung</b>
      (Android Studio oder VS Code) – mit echtem Flutter-Projekt, Emulator und automatischen Tests, genau wie im Betrieb.
      Diese Seite ist Ihr Wegweiser: Auftrag, Zielbild, Widget-Baum und Hilfen.</div></div>
    <div class="card"><h2>So geht's</h2>
      <div class="start-raster">
        <div><h3>1 · Projekt holen</h3>
          <p><a href="https://github.com/{REPO}/archive/refs/heads/main.zip">ZIP herunterladen</a> und entpacken – oder:</p>
          <pre><code>git clone https://github.com/{REPO}.git</code></pre></div>
        <div><h3>2 · Öffnen</h3>
          <p>Ordner in Android Studio oder VS Code öffnen, einmalig im Terminal:</p>
          <pre><code>flutter pub get</code></pre></div>
        <div><h3>3 · Programmieren</h3>
          <p>Auftrag lesen, <code>TODO</code>s in <code>lib/level_0X/</code> lösen. Ansehen: in <code>lib/main.dart</code>
          <code>aktivesLevel</code> setzen, App starten, nach Änderungen Hot Reload.</p></div>
        <div><h3>4 · Prüfen</h3>
          <p>Test starten – bei Rot steht ein <b>Hinweis</b> in der Ausgabe. Gesamtstand:</p>
          <pre><code>dart run tool/fortschritt.dart</code></pre></div>
      </div>
      <details><summary>Tests in der IDE starten</summary>
        <p><b>Android Studio:</b> Rechtsklick auf die Testdatei → <i>Run 'tests in …'</i><br>
        <b>VS Code:</b> Seitenleiste <i>Testing</i> (Reagenzglas) oder ▶ über <code>main()</code></p></details>
    </div>
    <div class="card"><h2>Ihr Weg in 8 Leveln</h2><div class="uebersicht">{uebersicht}</div>
      <p style="margin-top:14px"><a class="knopf primaer" href="#level-1">Los geht's mit Level 1 ▶</a></p></div>
  </section>
{ansichten}
  <section class="ansicht" id="bonus">
    <div class="card level-kopf"><span class="nummer" aria-hidden="true">★</span>
      <div><h2>Bonus – Die App weiterentwickeln</h2><p class="stich">für alle, die fertig sind</p></div></div>
    <div class="card">{md_zu_html(DOCS / "bonus.md")}</div>
    <div class="card lp-fuss"><a class="knopf" href="#level-8">◀ Level 8</a><a class="knopf" href="#start">Zum Start</a></div>
  </section>

  <section class="ansicht" id="loesungen">
    <div class="card"><h2>🔒 Musterlösungen</h2>
      <p>Die Lösungen sind verschlüsselt. Mit dem Passwort Ihrer Lehrkraft erscheinen sie in jedem Level
      unten im Auftrag unter <i>Musterlösung</i>. Erst selbst probieren – die Tests verraten Ihnen mehr als jede Lösung!</p>
      <form id="entsperren" class="pruefen">
        <label for="pw" class="sr">Passwort</label>
        <input id="pw" type="password" autocomplete="off" placeholder="Passwort"
          style="font:inherit;padding:8px 12px;border-radius:12px;border:1px solid var(--line);min-height:42px">
        <button class="primaer" type="submit">Lösungen anzeigen</button>
        <span id="pw-status" role="status"></span>
      </form></div>
  </section>

  <footer class="druckfuss"><small>Flutter-Lernpfad LF11 · BS Info · Ihr Fortschritt auf dieser Seite wird nur in Ihrem Browser gespeichert.</small></footer>
</div>
<script>{JS}</script>
<script>var GEHEIM = {geheim}; var MARKER = {json.dumps(MARKER)};{JS_LOESUNG}</script>
</body>
</html>
"""
    (DOCS / "index.html").write_text(seite, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print("Erstellt:", DOCS / "index.html")


if __name__ == "__main__":
    main()
