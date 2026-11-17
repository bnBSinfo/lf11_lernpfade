/* Begriffe (wie LF3): In „Sprache einfach“ sind Fachwörter gepunktet unterstrichen.
   Die Erklärung erscheint beim Darüberfahren, beim Antippen (Tablet) und mit der Tab-Taste.
   Die Erklärungen kommen aus tool/woerter.py (BEGRIFFE). In „Standard“ ist nichts markiert. */
(function () {
  "use strict";
  var NICHT = "pre,a,button,input,select,textarea,label,script,style,svg,h1,h2,h3,h4,dt,dd,.woerter,.rahmen-legende,.begriff,#begriff-tipp,.kopf";
  var BUCHST = "A-Za-zÄÖÜäöüß0-9_";
  var liste = Object.keys(BEGRIFFE).sort(function (a, b) { return b.length - a.length; }).map(function (w) {
    var q = w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return { wort: w, erkl: BEGRIFFE[w], re: new RegExp("(^|[^" + BUCHST + "-])(" + q + "(?:e|en|n|s|es)?)(?![" + BUCHST + "-])") };
  });
  function setze(el, wort) {
    el.classList.add("begriff"); el.tabIndex = 0;
    el.setAttribute("data-wort", wort); el.setAttribute("aria-label", el.textContent + ": " + BEGRIFFE[wort]);
  }
  function markiere(wurzel) {
    /* Inline-Code, der genau ein Fachwort ist (z. B. setState oder setState()) */
    wurzel.querySelectorAll("code").forEach(function (c) {
      if (c.closest(NICHT)) return;
      var t = c.textContent.replace(/\(\)$/, "");
      if (BEGRIFFE[t]) setze(c, t);
    });
    var w = document.createTreeWalker(wurzel, NodeFilter.SHOW_TEXT, { acceptNode: function (n) {
      var p = n.parentElement;
      return n.nodeValue.length > 2 && p && !p.closest(NICHT + ",code") ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    } });
    var knoten = []; while (w.nextNode()) knoten.push(w.currentNode);
    knoten.forEach(function (n) {
      var block = n.parentElement.closest("p,li,td,th,summary,div") || n.parentElement;
      for (var i = 0; i < liste.length; i++) {
        var e = liste[i], m = e.re.exec(n.nodeValue);
        if (!m) continue;
        if (block.querySelector('.begriff[data-wort="' + e.wort + '"]')) continue; /* je Absatz nur einmal */
        var rest = n.splitText(m.index + m[1].length);
        rest.nodeValue = rest.nodeValue.slice(m[2].length);
        var s = document.createElement("span"); s.textContent = m[2]; setze(s, e.wort);
        rest.parentNode.insertBefore(s, rest);
        n = rest; i = -1;
        if (!n.nodeValue) break;
      }
    });
  }
  document.querySelectorAll(".sprache-einfach").forEach(markiere);

  var tipp = document.createElement("div"); tipp.id = "begriff-tipp"; tipp.setAttribute("role", "tooltip"); tipp.hidden = true;
  document.body.appendChild(tipp);
  var aktiv = null;
  function zeige(s) {
    aktiv = s; tipp.innerHTML = "";
    var b = document.createElement("b"); b.textContent = s.dataset.wort; tipp.appendChild(b);
    tipp.appendChild(document.createTextNode(BEGRIFFE[s.dataset.wort]));
    tipp.hidden = false;
    var r = s.getBoundingClientRect(), tw = tipp.offsetWidth, th = tipp.offsetHeight;
    var x = Math.max(8, Math.min(r.left + window.scrollX, window.scrollX + document.documentElement.clientWidth - tw - 8));
    var y = r.top + window.scrollY - th - 8;
    if (r.top < th + 16) y = r.bottom + window.scrollY + 8;
    tipp.style.left = x + "px"; tipp.style.top = y + "px";
  }
  function weg() { aktiv = null; tipp.hidden = true; }
  document.addEventListener("mouseover", function (ev) { var s = ev.target.closest(".begriff"); if (s) zeige(s); else if (aktiv) weg(); });
  document.addEventListener("focusin", function (ev) { var s = ev.target.closest(".begriff"); if (s) zeige(s); });
  document.addEventListener("focusout", function (ev) { if (ev.target.closest(".begriff")) weg(); });
  document.addEventListener("click", function (ev) { var s = ev.target.closest(".begriff"); if (s) { if (aktiv === s) weg(); else zeige(s); } else if (aktiv) weg(); });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") weg(); });
  window.addEventListener("scroll", function () { if (aktiv && document.activeElement !== aktiv) weg(); }, { passive: true });
})();
