"""Animiertes Ablaufdiagramm der App (ersetzt den Skript-Screenshot bilder/ablauf.png).

ablauf_html(fokus, kennung) – fokus: Schritte, die in diesem Level dran sind (hervorgehoben, Start dort)
Die Animation läuft per SVG-SMIL (ohne Bibliothek), 6 Schritte à 3 s. Knöpfe darunter halten bei einem Schritt an.
"""
from html import escape as e

TAKT = 3.0
SCHRITTE = [
    ("Login öffnen", "Der Knopf <b>Login</b> öffnet den Login-Dialog."),
    ("Benutzer laden", "Die App holt die Benutzer als <b>JSON</b>: <code>GET …/records/flutterTB</code>."),
    ("Login prüfen", "Name und Passwort stimmen – die App öffnet die <b>ToDo-Liste</b>."),
    ("ToDos laden", "Die ToDo-Liste lädt die ToDos als <b>JSON</b>: <code>GET …/records/ToDoTB</code> in <code>initState()</code>."),
    ("Neues ToDo", "Der <b>+</b>-Knopf öffnet den Eingabedialog."),
    ("Speichern", "Das neue ToDo erscheint in der Liste und geht als <b>JSON</b> per <code>POST</code> an die Datenbank."),
]
N = len(SCHRITTE)
DAUER = TAKT * N

# Pfade der Pfeile (viewBox 0 0 1000 620)
PFADE = {
    1: "M196 175 H262",
    2: "M455 470 C 430 420, 400 380, 372 318",
    3: "M482 150 H580",
    4: "M545 470 C 590 440, 640 420, 672 392",
    5: "M775 352 C 800 330, 820 318, 836 300",
    6: "M905 300 C 940 400, 760 500, 600 500",
}
BADGE = {1: (229, 150), 2: (392, 400), 3: (531, 125), 4: (628, 425), 5: (842, 340), 6: (840, 455)}
JSON_SCHRITTE = {2, 4, 6}


def _fenster(i):
    a, b = (i - 1) / N, i / N
    return a, b


def _hervor(i, aus="0.22"):
    """SMIL: sichtbar nur im eigenen Zeitfenster."""
    a, b = _fenster(i)
    if a == 0:
        werte, zeiten = f"1;{aus}", f"0;{b:.4f}"
    else:
        werte, zeiten = f"{aus};1;{aus}", f"0;{a:.4f};{b:.4f}"
    return (f'<animate attributeName="opacity" dur="{DAUER}s" repeatCount="indefinite" calcMode="discrete" '
            f'values="{werte}" keyTimes="{zeiten}"/>')


def _paket(k, i):
    a, b = _fenster(i)
    start, ende = a + 0.15 / N, b - 0.2 / N
    return (f'<g class="ab-paket">{_hervor(i, "0")}'
            f'<rect x="-30" y="-15" width="60" height="30" rx="7"/><text y="6">JSON</text>'
            f'<animateMotion dur="{DAUER}s" repeatCount="indefinite" calcMode="linear" '
            f'keyPoints="0;0;1;1" keyTimes="0;{start:.4f};{ende:.4f};1"><mpath href="#{k}-p{i}"/></animateMotion></g>')


def _handy(x, y, w, h, titel, inhalt):
    return (f'<g class="ab-geraet"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" class="ab-handy"/>'
            f'<rect x="{x + 8}" y="{y + 22}" width="{w - 16}" height="40" class="ab-leiste"/>'
            f'<text x="{x + 22}" y="{y + 49}" class="ab-leiste-t">{e(titel)}</text>{inhalt}</g>')


def _svg(k, fokus):
    t = []
    # Datenbank und REST-API
    t.append('<g class="ab-geraet"><path class="ab-db" d="M110 470 v86 a90 22 0 0 0 180 0 v-86"/>'
             '<ellipse class="ab-db" cx="200" cy="470" rx="90" ry="22"/>'
             '<text x="200" y="525" class="ab-t">MySQL</text><text x="200" y="548" class="ab-k">flutterTB · ToDoTB</text></g>')
    t.append('<g class="ab-geraet"><rect x="400" y="470" width="200" height="90" rx="14" class="ab-api"/>'
             '<text x="500" y="508" class="ab-t ab-hell">REST-API</text><text x="500" y="535" class="ab-k ab-hell">php-crud-api auf dem Pi</text></g>')
    t.append('<g class="ab-sql"><path d="M296 512 H394" class="ab-linie" marker-start="url(#' + k + '-s)" marker-end="url(#' + k + '-s)"/>'
             '<text x="345" y="502" class="ab-k">SQL</text></g>')
    # 1: Start-Screen mit Login-Knopf
    t.append(_handy(20, 20, 176, 320, "Start",
                    '<rect x="58" y="160" width="100" height="36" rx="18" class="ab-knopf"/><text x="108" y="184" class="ab-knopf-t">Login</text>'))
    # Login-Dialog
    t.append('<g class="ab-geraet"><rect x="268" y="70" width="210" height="246" rx="14" class="ab-dialog"/>'
             '<text x="290" y="108" class="ab-t ab-links">Login</text>'
             '<text x="290" y="148" class="ab-k ab-links">Benutzername</text><path d="M290 160 H456" class="ab-feld"/>'
             '<text x="290" y="198" class="ab-k ab-links">Passwort</text><path d="M290 210 H456" class="ab-feld"/>'
             '<rect x="370" y="240" width="86" height="34" rx="17" class="ab-knopf"/><text x="413" y="263" class="ab-knopf-t">Login</text></g>')
    # ToDo-Liste
    items = [("Projektplan", False), ("Gruppeneinteilung", True), ("Meilensteine", False), ("Swot", False)]
    liste = "".join(
        f'<rect x="604" y="{94 + j * 52}" width="20" height="20" rx="4" class="ab-check{" an" if fertig else ""}"/>'
        + (f'<path d="M608 {104 + j * 52} l5 5 l8 -10" class="ab-haken"/>' if fertig else "")
        + f'<text x="634" y="{110 + j * 52}" class="ab-item">{e(name)}</text>'
        for j, (name, fertig) in enumerate(items))
    t.append(_handy(586, 20, 210, 370, "ToDo Liste", liste +
                    '<circle cx="752" cy="340" r="24" class="ab-fab"/><text x="752" y="349" class="ab-fab-t">+</text>'))
    # Eingabedialog
    t.append('<g class="ab-geraet"><rect x="818" y="200" width="168" height="100" rx="14" class="ab-dialog"/>'
             '<text x="834" y="232" class="ab-k ab-links">Neues ToDo</text>'
             '<text x="834" y="268" class="ab-item">Netzplan</text><path d="M834 278 H970" class="ab-feld an"/></g>')
    # Schritte: Pfeil + Nummer (+ Paket)
    for i in range(1, N + 1):
        bx, by = BADGE[i]
        cls = "ab-schritt fokus" if i in fokus else "ab-schritt"
        gestr = ' stroke-dasharray="9 7"' if i == 6 else ""
        t.append(f'<g class="{cls}">{_hervor(i)}<path id="{k}-p{i}" d="{PFADE[i]}" class="ab-linie"{gestr} marker-end="url(#{k}-m)"/>'
                 f'<circle cx="{bx}" cy="{by}" r="19" class="ab-nr"/><text x="{bx}" y="{by + 7}" class="ab-nr-t">{i}</text></g>')
        if i == 6:  # zweiter Pfeil: neues ToDo erscheint in der Liste
            t.append(f'<g class="{cls}">{_hervor(i)}<path d="M818 230 H800" class="ab-linie" marker-end="url(#{k}-m)"/></g>')
    for i in sorted(JSON_SCHRITTE):
        t.append(_paket(k, i))
    defs = (f'<defs><marker id="{k}-m" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="#2f6fd6"/></marker>'
            f'<marker id="{k}-s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="#485263"/></marker></defs>')
    return (f'<svg class="ab-svg" id="{k}" viewBox="0 0 1000 620" role="img" '
            f'aria-label="Ablauf der App in 6 Schritten: Login öffnen, Benutzer als JSON laden, Login prüfen, '
            f'ToDos als JSON laden, neues ToDo eingeben, neues ToDo per POST speichern.">{defs}{"".join(t)}</svg>')


def ablauf_html(fokus, kennung):
    k = f"ab-{kennung}"
    knoepfe = "".join(
        f'<li><button type="button" data-schritt="{i}" class="{"fokus" if i in fokus else ""}">'
        f'<span class="ab-num">{i}</span><span><b>{e(titel)}</b><br>{text}</span></button></li>'
        for i, (titel, text) in enumerate(SCHRITTE, 1))
    return (f'<figure class="ab-ablauf" data-ab="{k}" data-start="{min(fokus)}">{_svg(k, set(fokus))}'
            f'<div class="ab-steuer"><button type="button" class="ab-play" aria-label="Animation anhalten">⏸ Anhalten</button>'
            f'<span class="klein">Klicken Sie auf einen Schritt, um dort anzuhalten.</span></div>'
            f'<ol class="ab-liste">{knoepfe}</ol></figure>')


CSS = """
.ab-ablauf{margin:0;width:100%}
.ab-svg{width:100%;height:auto;display:block;font-family:inherit}
.ab-svg text{text-anchor:middle;fill:#1a2130}
.ab-svg .ab-links{text-anchor:start}
.ab-svg .ab-t{font-size:22px;font-weight:700}
.ab-svg .ab-k{font-size:16px;fill:#485263}
.ab-svg .ab-hell{fill:#fff}
.ab-svg .ab-handy{fill:#fff;stroke:#1a2130;stroke-width:6}
.ab-svg .ab-leiste{fill:#2f6fd6}
.ab-svg .ab-leiste-t{fill:#fff;font-size:18px;font-weight:700;text-anchor:start}
.ab-svg .ab-dialog{fill:#fff;stroke:#9aa3b2;stroke-width:2;filter:drop-shadow(0 4px 8px rgba(0,0,0,.18))}
.ab-svg .ab-feld{stroke:#9aa3b2;stroke-width:2}
.ab-svg .ab-feld.an{stroke:#2f6fd6;stroke-width:3}
.ab-svg .ab-knopf{fill:#e8f0fd;stroke:#2f6fd6;stroke-width:2}
.ab-svg .ab-knopf-t{font-size:16px;font-weight:700;fill:#2f6fd6}
.ab-svg .ab-item{font-size:16px;text-anchor:start}
.ab-svg .ab-check{fill:#fff;stroke:#485263;stroke-width:2}
.ab-svg .ab-check.an{fill:#2f6fd6;stroke:#2f6fd6}
.ab-svg .ab-haken{fill:none;stroke:#fff;stroke-width:3}
.ab-svg .ab-fab{fill:#2f6fd6}
.ab-svg .ab-fab-t{fill:#fff;font-size:28px;font-weight:700}
.ab-svg .ab-db{fill:#e8f0fd;stroke:#2f6fd6;stroke-width:4}
.ab-svg .ab-api{fill:#2f6fd6}
.ab-svg .ab-linie{fill:none;stroke:#2f6fd6;stroke-width:5;stroke-linecap:round}
.ab-svg .ab-sql .ab-linie{stroke:#485263;stroke-width:3}
.ab-svg .ab-nr{fill:#fff;stroke:#1a2130;stroke-width:2.5}
.ab-svg .ab-nr-t{font-size:20px;font-weight:700}
.ab-svg .fokus .ab-nr{fill:#fde68a;stroke:#b45309}
.ab-svg .ab-paket rect{fill:#6d4aa6}
.ab-svg .ab-paket text{fill:#fff;font-size:15px;font-weight:700}
.ab-steuer{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:8px 0}
.ab-play{border:1px solid var(--line,#d9dde5);background:#fff;border-radius:999px;padding:6px 14px;cursor:pointer;font:inherit}
.ab-liste{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:8px}
.ab-liste button{display:flex;gap:10px;align-items:flex-start;width:100%;text-align:left;font:inherit;line-height:1.35;
  background:#fff;border:1px solid var(--line,#d9dde5);border-radius:12px;padding:8px 10px;cursor:pointer;color:inherit}
.ab-liste button.fokus{border-color:#e0b85a}
.ab-liste button.aktiv{background:#e8f0fd;border-color:#2f6fd6;box-shadow:0 0 0 2px #2f6fd6 inset}
.ab-num{flex:none;width:28px;height:28px;border-radius:50%;border:2px solid #1a2130;display:grid;place-items:center;font-weight:700}
.ab-liste button.fokus .ab-num{background:#fde68a;border-color:#b45309}
"""

JS = r"""
(function(){
  var TAKT = %TAKT%, N = %N%;
  document.querySelectorAll(".ab-ablauf").forEach(function(fig){
    var svg = fig.querySelector("svg"), play = fig.querySelector(".ab-play");
    var knoepfe = fig.querySelectorAll(".ab-liste button");
    if (!svg || !svg.setCurrentTime) return;
    var start = (parseInt(fig.dataset.start, 10) - 1) * TAKT, gestartet = false;
    function anzeigen(){
      var t = svg.getCurrentTime() % (TAKT * N), s = Math.floor(t / TAKT) + 1;
      knoepfe.forEach(function(b){ b.classList.toggle("aktiv", +b.dataset.schritt === s); });
    }
    function halten(an){
      if (an) svg.pauseAnimations(); else svg.unpauseAnimations();
      play.textContent = an ? "▶ Abspielen" : "⏸ Anhalten";
      play.setAttribute("aria-label", an ? "Animation abspielen" : "Animation anhalten");
    }
    function vorbereiten(){
      if (gestartet) return; gestartet = true;
      svg.setCurrentTime(start + 0.01);
      if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) {
        svg.setCurrentTime(start + TAKT * 0.55); halten(true);
      }
      anzeigen();
    }
    svg.addEventListener("load", vorbereiten); setTimeout(vorbereiten, 50);
    setInterval(anzeigen, 200);
    play.addEventListener("click", function(){ halten(!svg.animationsPaused()); });
    knoepfe.forEach(function(b){
      b.addEventListener("click", function(){
        svg.setCurrentTime((+b.dataset.schritt - 1) * TAKT + TAKT * 0.55); halten(true); anzeigen();
      });
    });
  });
})();
""".replace("%TAKT%", str(TAKT)).replace("%N%", str(N))
