// REST-Baukasten auf der Wissen-Seite: zeigt zu Methode/Tabelle/id die Adresse, curl, Dart und SQL.
(function(){
  var $ = function(id){ return document.getElementById(id); };
  if (!$("bk-methode")) return;
  var vorschlag = {
    ToDoTB: {POST: '{"titel": "Milch kaufen", "erledigt": false}', PUT: '{"erledigt": true}'},
    flutterTB: {POST: '{"name": "neu", "passwordLogin": "geheim"}', PUT: '{"name": "umbenannt"}'}
  };
  var letzte = "";
  function sqlWert(v){ return typeof v === "string" ? "'" + v.replace(/'/g, "''") + "'" : (v === true ? "TRUE" : v === false ? "FALSE" : String(v)); }
  function zeigen(){
    var m = $("bk-methode").value, t = $("bk-tabelle").value, id = $("bk-id").value.trim(), ip = $("bk-ip").value.trim() || "IP";
    var braucht = m === "POST" || m === "PUT";
    var schluessel = m + t;
    if (braucht && schluessel !== letzte) $("bk-body").value = vorschlag[t][m];
    if (!braucht) $("bk-body").value = "";
    letzte = braucht ? schluessel : "";
    $("bk-body").disabled = !braucht;
    var hinweis = "";
    if (m === "POST" && id) { hinweis = "POST geht an die Tabelle, nicht an eine id – die vergibt die Datenbank (AUTO_INCREMENT)."; id = ""; }
    if ((m === "PUT" || m === "DELETE") && !id) { hinweis = m + " braucht eine id – sonst weiß die API nicht, welchen Datensatz."; }
    var pfad = "/php-crud-api/api.php/records/" + t + (id ? "/" + id : "");
    var url = "http://" + ip + pfad, body = $("bk-body").value.trim(), daten = null;
    if (braucht) { try { daten = JSON.parse(body); } catch (e) { hinweis = "Die Daten sind kein gültiges JSON (doppelte Anführungszeichen?)."; } }
    $("bk-url").textContent = m + " " + url;
    $("bk-curl").textContent = "curl" + (m === "GET" ? "" : " -X " + m) + (braucht ? " -H \"Content-Type: application/json\" -d '" + body + "'" : "") + " " + url;
    var dartUri = "Uri.parse('" + url + "')";
    $("bk-dart").textContent = "final antwort = await http." + m.toLowerCase() + "(" + dartUri +
      (braucht ? ",\n    headers: {'Content-Type': 'application/json'},\n    body: jsonEncode(" + body.replace(/"/g, "'") + ")" : "") + ");\nprint(antwort.statusCode);\nprint(antwort.body);";
    var sql = "";
    var wo = id ? " WHERE id = " + (parseInt(id, 10) || 0) : "";
    if (m === "GET") sql = "SELECT * FROM " + t + wo + ";";
    if (m === "DELETE") sql = "DELETE FROM " + t + wo + ";";
    if (daten && m === "POST") sql = "INSERT INTO " + t + " (" + Object.keys(daten).join(", ") + ")\nVALUES (" + Object.keys(daten).map(function(k){ return sqlWert(daten[k]); }).join(", ") + ");";
    if (daten && m === "PUT") sql = "UPDATE " + t + " SET " + Object.keys(daten).map(function(k){ return k + " = " + sqlWert(daten[k]); }).join(", ") + wo + ";";
    $("bk-sql").textContent = sql;
    if (!hinweis && t === "flutterTB" && m === "GET") hinweis = "Achtung: Die Antwort enthält passwordLogin – siehe Bonus 3.";
    $("bk-hinweis").textContent = hinweis;
  }
  ["bk-methode", "bk-tabelle", "bk-id", "bk-ip", "bk-body"].forEach(function(id){ $(id).addEventListener("input", zeigen); });
  zeigen();
})();
