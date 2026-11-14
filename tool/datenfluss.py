"""Datenfluss-Grafik (SVG): PC/Handy ⇄ Netz ⇄ Raspberry Pi (SSH, Apache, PHP, MySQL).

datenfluss_svg(nr)   – Teile bis Level nr sichtbar, Teile von Level nr hervorgehoben
datenfluss_svg(None) – alles sichtbar (Wissen-Seite)
"""
from html import escape as e

# Welche Teile kommen in welchem Level dazu?
NEU = {
    1: ["pi", "lan"],
    2: ["terminal", "ssh", "sshd", "sshd-shell", "shell"],
    3: ["browser", "http-browser", "apache", "antwort"],
    4: ["php", "apache-php"],
    5: ["pma", "mysql", "mysqli"],
    6: ["db", "tb1", "tb2", "shell-mysql"],
    7: ["benutzer"],
    8: ["crud"],
    9: ["dart", "http-dart"],
}
IMMER = {"pc"}
# Weg der Anfrage, der in einem Level zusätzlich aufleuchtet (schon vorhandene Teile)
WEG = {
    4: ["http-browser", "antwort", "apache"],
    5: ["http-browser", "antwort", "apache", "apache-php", "php"],
    6: ["terminal", "ssh", "sshd", "sshd-shell", "shell", "mysql"],
    7: ["http-browser", "antwort", "apache", "apache-php", "mysqli", "tb1"],
    8: ["http-browser", "antwort", "apache", "apache-php", "mysqli", "tb1", "tb2"],
    9: ["antwort", "apache", "apache-php", "mysqli", "crud", "tb2"],
}


def _klasse(teil, nr):
    if nr is None or teil in IMMER:
        return "da"
    if teil in WEG.get(nr, []):
        return "neu"
    for lv, teile in NEU.items():
        if teil in teile:
            return "neu" if lv == nr else ("da" if lv < nr else "spaeter")
    return "da"


def datenfluss_svg(nr=None) -> str:
    k = lambda teil: f'class="df {_klasse(teil, nr)}"'

    def box(teil, x, y, w, h, titel, unter="", unter2="", gross=False, titel_oben=False):
        ty = y + 22 if titel_oben else y + h / 2 - (6 if unter else -5) - (7 if unter2 else 0)
        t = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
             f'<text x="{x + w / 2}" y="{ty}" class="{"t-gross" if gross else "t"}">{e(titel)}</text>']
        if unter:
            t.append(f'<text x="{x + w / 2}" y="{ty + 17}" class="t-klein">{e(unter)}</text>')
        if unter2:
            t.append(f'<text x="{x + w / 2}" y="{ty + 32}" class="t-klein">{e(unter2)}</text>')
        return f'<g {k(teil)}>{"".join(t)}</g>'

    def pfeil(teil, d, text="", tx=0, ty=0, gestrichelt=False):
        strich = ' stroke-dasharray="7 5"' if gestrichelt else ""
        lbl = f'<text x="{tx}" y="{ty}" class="t-pfeil">{e(text)}</text>' if text else ""
        spitze = ("df-spitze-neu" if _klasse(teil, nr) == "neu" else "df-spitze") + f"-{nr or 0}"
        return f'<g {k(teil)}><path d="{d}" class="linie" marker-end="url(#{spitze})"{strich}/>{lbl}</g>'

    teile = [
        # Behälter
        f'<g {k("pc")}><rect x="10" y="30" width="210" height="380" rx="16" class="behaelter"/>'
        f'<text x="115" y="56" class="t-gross">PC / Handy</text></g>',
        f'<g {k("lan")}><rect x="226" y="30" width="98" height="380" rx="12" class="netz"/>'
        f'<text x="275" y="398" class="t-klein">LAN</text><text x="275" y="384" class="t-klein">Netz</text></g>',
        f'<g {k("pi")}><rect x="330" y="10" width="600" height="410" rx="16" class="behaelter"/>'
        f'<text x="630" y="36" class="t-gross">Raspberry Pi · Ubuntu</text></g>',
        box("php", 520, 145, 180, 205, "PHP", titel_oben=True, gross=True),
        box("mysql", 735, 145, 180, 205, "MySQL", "nur localhost:3306", titel_oben=True, gross=True),
        box("db", 750, 200, 150, 138, "flutterDB", titel_oben=True),
        # PC
        box("terminal", 30, 75, 170, 50, "Terminal", "ssh administrator@IP"),
        box("browser", 30, 165, 170, 50, "Browser", "Firefox"),
        box("dart", 30, 285, 170, 50, "Flutter-App / Dart", "TodoApi"),
        # Pi
        box("sshd", 350, 75, 140, 50, "SSH-Server", "Port 22"),
        box("shell", 520, 75, 180, 50, "Shell (root)", "apt · nano · mysql"),
        box("apache", 350, 165, 140, 170, "Apache", "Port 80", "/var/www/html"),
        box("pma", 535, 180, 150, 40, "phpMyAdmin"),
        box("benutzer", 535, 230, 150, 40, "benutzer.php"),
        box("crud", 535, 280, 150, 40, "php-crud-api"),
        box("tb1", 765, 235, 120, 38, "flutterTB"),
        box("tb2", 765, 285, 120, 38, "ToDoTB"),
        # Pfeile
        pfeil("ssh", "M200 100 H344", "SSH :22", 275, 92),
        pfeil("sshd-shell", "M490 100 H514"),
        pfeil("shell-mysql", "M700 100 H825 V139", "SQL ausführen", 765, 92),
        pfeil("http-browser", "M200 190 H344", "HTTP GET", 275, 182),
        pfeil("http-dart", "M200 310 H344", "GET · POST", 275, 296),
        pfeil("antwort", "M350 250 H226", "JSON / HTML", 275, 242, gestrichelt=True),
        pfeil("apache-php", "M490 250 H514"),
        pfeil("mysqli", "M700 265 H729", "SQL", 717, 257),
    ]
    # zweite Zeile für den Dart-Pfeil
    teile.append(f'<g {k("http-dart")}><text x="275" y="326" class="t-pfeil">PUT · DELETE</text></g>')
    titel = "Datenfluss" + (f" – Stand Level {nr}" if nr else "")
    return (f'<svg class="datenfluss" viewBox="0 0 940 430" role="img" aria-label="{e(titel)}: '
            'PC oder Handy schicken über das Netz HTTP-Anfragen an Apache auf dem Raspberry Pi, '
            'PHP fragt MySQL ab und die Antwort geht als JSON zurück; per SSH wird der Pi verwaltet.">'
            f'<defs><marker id="df-spitze-{nr or 0}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" '
            'orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#485263"/></marker>'
            f'<marker id="df-spitze-neu-{nr or 0}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" '
            'orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#4338ca"/></marker></defs>'
            + "".join(teile) + "</svg>")


CSS = """
.datenfluss{width:100%;height:auto;display:block;margin:4px 0 12px;font-family:inherit}
.datenfluss rect{fill:#fff;stroke:#b9bfcc;stroke-width:1.5}
.datenfluss rect.behaelter{fill:#f5f6f8;stroke:#c9ced8}
.datenfluss rect.netz{fill:#eef6ff;stroke:#a9c8ee;stroke-dasharray:6 5}
.datenfluss text{text-anchor:middle;fill:#1a2130;font-size:14px;font-weight:600}
.datenfluss .t-gross{font-size:16px;font-weight:700}
.datenfluss .t-klein{font-size:11.5px;font-weight:400;fill:#485263}
.datenfluss .t-pfeil{font-size:11.5px;font-weight:600;fill:#485263}
.datenfluss .linie{fill:none;stroke:#485263;stroke-width:2}
.datenfluss .df.neu rect{stroke:var(--accent);stroke-width:3;fill:var(--accent-soft)}
.datenfluss .df.neu .linie{stroke:var(--accent);stroke-width:3}
.datenfluss .df.neu .t-pfeil{fill:var(--accent)}
.datenfluss .df.spaeter{opacity:.18}
"""
