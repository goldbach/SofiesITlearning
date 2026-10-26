# Dag 2: Hvordan et system hænger sammen

*Ca. 3–4 timer.*

## Hvorfor?

Et IT-system er næsten aldrig ét program. Det er en række dele, der taler sammen: en hjemmeside, en server med forretningslogikken, en database og ofte integrationer til andre systemer. I det offentlige kan det f.eks. være CPR-registret, NemLog-in eller e-Boks.

Som analytiker kommer du til at beskrive, hvilke data der skal sendes mellem systemerne, og hvornår. Du kommer til at læse API-specifikationer, og du skal kunne sige "endpointet svarer 404" uden at blinke. I dag bygger du dit eget lille API, så du ved, hvad der sker under motorhjelmen.

## Videoer og interaktivt materiale

| Hvornår | Hvad | Længde |
|---------|------|--------|
| **Før du starter** | [How the Internet Works in 5 Minutes](https://www.youtube.com/watch?v=7_LPdttKXPc) | 5 min |
| **Efter del A** | [The Internet: IP Addresses & DNS](https://www.youtube.com/watch?v=5o8CwafCxnU) | 6 min |
| **Efter del A** | [The Internet: HTTP & HTML](https://www.youtube.com/watch?v=kBXQZMmiA4s) | 7 min |
| **Efter del B** | [RESTful APIs in 100 Seconds](https://www.youtube.com/watch?v=-MTSQjw5DrM) (Fireship). Se de første ca. 2 minutter. Resten bygger et API i JavaScript | 2 min |
| **Opslag** | [MDN: HTTP-statuskoder](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status): referencen, alle bruger | – |
| **Opslag** | [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/): til del D og senere | – |

---

## Del A: Det store billede (ca. 30 min)

### Klient og server

En **klient** spørger, og en **server** svarer. Browseren er en klient. Det samme er en app på telefonen eller et andet system. Serveren er et program, der kører et sted og venter på spørgsmål.

Et typisk forretningssystem er bygget i lag (en *3-tier architecture*):

```
  ┌──────────────┐   HTTP    ┌──────────────┐    SQL    ┌──────────────┐
  │   Frontend   │ ────────► │   Backend    │ ────────► │   Database   │
  │ (browseren)  │ ◄──────── │ (API, logik) │ ◄──────── │              │
  └──────────────┘   JSON    └──────┬───────┘           └──────────────┘
                                    │ HTTP / SOAP / beskeder
                                    ▼
                             ┌──────────────┐
                             │ Andre systemer│  (integrationer)
                             └──────────────┘
```

- **Frontend**: det brugeren ser og klikker på. Det kører i browseren.
- **Backend**: forretningsreglerne. Hvem må se hvad? Hvad sker der, når en ansøgning bliver indsendt? Det kører på en server.
- **Database**: hvor data bliver gemt permanent. Det er emnet for dag 3.
- **Integrationer**: forbindelser til andre systemer. Her bliver meget af analytikerarbejdet lagt.

Frontend og backend taler sammen via et **API** (*application programming interface*). Det er en aftalt måde at stille spørgsmål og få svar på. Et API er en **kontrakt**: "hvis du sender det her, får du det her tilbage".

### Hvordan finder klienten serveren?

En URL som `https://api.github.com:443/repos/goldbach/SofiesITlearning?per_page=5` består af:

| Del | Eksempel | Betydning |
|-----|----------|-----------|
| **scheme** | `https` | Protokollen. `https` er krypteret `http` |
| **host** | `api.github.com` | Serverens navn |
| **port** | `443` | Hvilken "dør" på serveren. Standarden er 443 for https og 80 for http, så porten bliver oftest udeladt |
| **path** | `/repos/goldbach/SofiesITlearning` | Hvilken ressource du vil have |
| **query string** | `?per_page=5` | Ekstra parametre, `nøgle=værdi`, adskilt med `&` |

**DNS** oversætter navnet `api.github.com` til en **IP-adresse** som `140.82.121.6`, ligesom en telefonbog. `localhost` (eller `127.0.0.1`) betyder "denne computer". Det bruger du, når du kører en server på din egen maskine.

---

## Del B: HTTP, sproget mellem klient og server (ca. 45 min)

**HTTP** er en simpel tekstprotokol. Klienten sender en **request**, og serveren sender en **response**. Derefter glemmer serveren klienten igen. HTTP er **stateless**: hver request skal indeholde alt, hvad serveren behøver at vide.

### En request

```
GET /repos/goldbach/SofiesITlearning HTTP/1.1      ← metode, sti, version
Host: api.github.com                               ← headers
Accept: application/json
                                                    ← tom linje
(body, hvis der er en)
```

### En response

```
HTTP/1.1 200 OK                                    ← statuskode
Content-Type: application/json; charset=utf-8      ← headers
Content-Length: 5843

{"name": "SofiesITlearning", ...}                  ← body
```

### Prøv det: `curl`

`curl` er en HTTP-klient i terminalen. Den kommer til at blive din bedste ven.

```bash
curl https://api.github.com/repos/goldbach/SofiesITlearning
```

Svaret er **JSON**. Gør det læsbart med Python (som du har i forvejen):

```bash
curl -s https://api.github.com/repos/goldbach/SofiesITlearning | python3 -m json.tool
```

Se hele samtalen med `-v` (verbose). Linjer med `>` er det, du sender, og linjer med `<` er det, serveren svarer:

```bash
curl -v https://api.github.com/repos/goldbach/SofiesITlearning > /dev/null
```

Og et repo, der ikke findes:

```bash
curl -i https://api.github.com/repos/goldbach/findes-ikke
```

`-i` viser response-headers. Læg mærke til statuskoden.

### Metoder

| Metode | Betydning | Python-analogi |
|--------|-----------|----------------|
| `GET` | Hent | `d[key]` |
| `POST` | Opret noget nyt | `d[ny_key] = værdi` |
| `PUT` | Erstat helt | `d[key] = ny_værdi` |
| `PATCH` | Ret en del | `d[key].update(...)` |
| `DELETE` | Slet | `del d[key]` |

`GET`, `PUT` og `DELETE` er **idempotente**: Hvis du gør det samme to gange, er resultatet det samme som at gøre det én gang. Det gælder ikke `POST`, som opretter to ting. Det betyder noget, når netværket fejler, og nogen trykker "prøv igen".

### Statuskoder

Første ciffer fortæller det meste:

| Kode | Betydning | De vigtigste |
|------|-----------|--------------|
| **2xx** | Det gik godt | `200 OK`, `201 Created`, `204 No Content` |
| **3xx** | Kig et andet sted | `301 Moved Permanently`, `302 Found` |
| **4xx** | **Klienten** har lavet en fejl | `400 Bad Request`, `401 Unauthorized` (ikke logget ind), `403 Forbidden` (logget ind, men ikke adgang), `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity` |
| **5xx** | **Serveren** har lavet en fejl | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable` |

> **Tommelfingerregel i fejlfinding:** 4xx betyder, at man kigger på det, der blev sendt. 5xx betyder, at man kigger i serverens logs.

### JSON

**JSON** (*JavaScript Object Notation*) er det mest udbredte dataformat mellem systemer. Du kender det allerede: det ligner Python's `dict` og `list` næsten fuldstændigt.

```json
{
  "id": 1,
  "temperatur": 21.3,
  "aktiv": true,
  "maalere": ["A", "B"],
  "note": null
}
```

Forskellene fra Python er `true`/`false`/`null` i stedet for `True`/`False`/`None` og kun `"`, ikke `'`.

```python
import json
data = json.loads('{"temperatur": 21.3}')   # tekst -> dict
tekst = json.dumps({"temperatur": 21.3})    # dict -> tekst
# og pandas: pd.read_json(...), df.to_json(...)
```

Du vil også møde **XML**, især i ældre offentlige integrationer (**SOAP**-webservices). Det er det samme princip i et andet format.

### REST

**REST** er en stil for at designe HTTP-API'er. Den vigtigste idé er, at URL'en beskriver en **ressource** (et navneord), og metoden beskriver **handlingen** (et udsagnsord):

| Request | Betydning |
|---------|-----------|
| `GET /maalinger` | Hent alle målinger |
| `GET /maalinger/2` | Hent måling 2 |
| `POST /maalinger` | Opret en ny måling (data i body) |
| `PUT /maalinger/2` | Erstat måling 2 |
| `DELETE /maalinger/2` | Slet måling 2 |

Det er **ikke** REST at skrive `/hentMaaling?id=2` eller `/sletMaaling`. Så står udsagnsordet i URL'en.

Hver af de linjer kaldes et **endpoint**. De data, du sender eller modtager, kaldes **payload**.

---

## Del C: Byg dit eget API (ca. 60 min)

I mappen ligger [`server.py`](server.py): et mini-API, der kun bruger Pythons standardbibliotek. Du skal ikke installere noget. Læs koden igennem, før du kører den. Den er kort, og du kan genkende alt fra del B: metoder, stier, statuskoder, headers og JSON.

### Start serveren

Del Ghostty-vinduet med `Cmd-D`, så serveren kører til venstre og du skriver `curl` til højre.

**Venstre:**
```bash
cd ~/kursus/SofiesITlearning/02-system-og-api
python3 server.py
```

**Højre:**
```bash
curl -s http://127.0.0.1:8000/maalinger | python3 -m json.tool
curl -i http://127.0.0.1:8000/maalinger/2
curl -i http://127.0.0.1:8000/maalinger/99
```

Kig i venstre side: Hver request bliver skrevet i serverens **log** med metode, sti og statuskode. Det er de linjer, udviklere og driftsfolk leder i, når noget går galt.

Opret en måling:

```bash
curl -i -X POST http://127.0.0.1:8000/maalinger \
  -H "Content-Type: application/json" \
  -d '{"temperatur": 23.4, "tryk": 1011}'
```

- `-X POST`: metoden
- `-H`: en header. Her fortæller vi, at body er JSON
- `-d`: body (*data*)
- `\` i slutningen af en linje betyder, at kommandoen fortsætter på næste linje

Prøv også at åbne http://127.0.0.1:8000/maalinger i browseren. Browseren er bare endnu en klient, der laver en `GET`.

### Øvelser C

1. **Fejl med vilje.** Send ugyldig JSON (`-d 'hej'`) og en måling uden `tryk`. Hvilke statuskoder får du? Hvorfor er de 4xx og ikke 5xx?
2. **Hvad med `DELETE`?** Prøv `curl -i -X DELETE http://127.0.0.1:8000/maalinger/1`. Hvad svarer serveren? Kig efter koden i en tabel i del B eller på MDN.
3. **Implementér `DELETE /maalinger/{id}`.** Tilføj en metode `do_DELETE` i `Handler`. Den skal svare `204 No Content` uden body, hvis målingen fandtes, og `404` ellers.
   *Hint:* Ved 204 kalder du `self.send_response(204)` og `self.end_headers()`, og ikke `send_json`.
4. **Validering.** Lige nu kan man oprette en måling med `"temperatur": "varmt"`. Ret `do_POST`, så den svarer `400`, hvis temperatur eller tryk ikke er et tal.
   *Hint:* `isinstance(x, (int, float))`.
5. **Filtrering med query string.** Få `GET /maalinger?min_temperatur=20` til kun at returnere målinger med temperatur ≥ 20.
   *Hint:* `from urllib.parse import parse_qs` og `parse_qs(urlsplit(self.path).query)`.
6. **Genstart serveren** (Ctrl-C og start igen). Hvor blev de målinger af, som du oprettede? Hvorfor? Svaret fører direkte til dag 3.

Du skal genstarte serveren, hver gang du har rettet i koden.

---

## Del D: Det samme med FastAPI (ca. 45 min)

I praksis skriver man ikke HTTP-håndtering i hånden. Man bruger et **framework**, der klarer det kedelige. I Java er det typisk *Spring Boot*, i C# *ASP.NET*, og i Python bl.a. *FastAPI*. Principperne er de samme.

### Virtuelt miljø og dependencies

FastAPI er ikke en del af Python, så det skal installeres. Man installerer **ikke** pakker globalt på maskinen, for så får forskellige projekter konflikter om versioner. I stedet laver man et **virtual environment** (venv) pr. projekt:

```bash
cd ~/kursus/SofiesITlearning/02-system-og-api
python3 -m venv .venv               # lav et miljø i mappen .venv
source .venv/bin/activate           # aktivér det. Din prompt viser nu (.venv)
pip install "fastapi[standard]"     # installér FastAPI og webserveren uvicorn
pip freeze > requirements.txt       # skriv de præcise versioner ned
```

- En **dependency** er en pakke, dit projekt afhænger af.
- `requirements.txt` er listen over dependencies med versioner. En kollega kan genskabe dit miljø med `pip install -r requirements.txt`. Java og C# har det samme (Maven/Gradle og NuGet).
- `.venv` skal **ikke** i Git. Det er genereret og fylder meget. Derfor står det i repoets `.gitignore`. `requirements.txt` skal med i Git.
- `deactivate` slår miljøet fra igen.

### Kør det

Læs [`app.py`](app.py). Det er det samme API som `server.py`. Sammenlign længden.

```bash
fastapi dev app.py
```

Afprøv det med de samme `curl`-kommandoer som før. Prøv så at oprette `{"temperatur": "varmt"}`. FastAPI svarer `422` med en præcis fejlbesked, uden at du har skrevet en eneste linje validering. Det kommer fra de typer, du har angivet i `NyMaaling` (`temperatur: float`, `tryk: int`).

`dev` betyder, at serveren selv genstarter, når du gemmer filen.

### Swagger/OpenAPI: det vigtigste for en analytiker

Åbn **http://127.0.0.1:8000/docs** i browseren.

Det er **Swagger UI**: automatisk genereret dokumentation, som du kan klikke rundt i. Vælg et endpoint, tryk **Try it out** og **Execute**. Under siden ligger en maskinlæsbar beskrivelse af hele API'et, **OpenAPI-specifikationen**. Du kan se den på http://127.0.0.1:8000/openapi.json.

En OpenAPI-specifikation er *kontrakten* mellem to systemer. I mange projekter bliver den skrevet og aftalt *før* koden, og analytikere er ofte med til at skrive og reviewe den. Når nogen siger "send mig specifikationen" eller "hvad siger Swaggeren?", er det den, de mener.

### Øvelser D

7. Brug Swagger UI til at oprette en måling og hente den igen.
8. Implementér `DELETE /maalinger/{maaling_id}` i `app.py` (`@app.delete(...)`, `status_code=204`). Kig i FastAPI-tutorialen eller spørg Claude om et hint. Se, at det nye endpoint dukker op i `/docs`, uden at du gør noget.
9. Hvad gav FastAPI dig gratis, som du selv skulle skrive i `server.py`? Lav en liste.

---

## Del E: Kig under motorhjelmen på rigtige hjemmesider (ca. 15 min)

1. Åbn en hjemmeside, du bruger, f.eks. en nyhedsside, i Chrome eller Safari. I Safari skal du først slå *Udvikler*-menuen til under *Indstillinger → Avanceret*.
2. Åbn **Developer Tools** med `Cmd-Option-I`, og vælg fanen **Network**.
3. Genindlæs siden. Hver linje er en HTTP-request. Klik på nogle af dem, og find metode, statuskode, headers og response.
4. Filtrér på **Fetch/XHR**. Det er de kald, frontenden laver til et API. Kan du finde ét, der returnerer JSON?

Testere og analytikere bruger Network-fanen dagligt til at se, hvad der faktisk bliver sendt.

---

## Aflevering

Lav en branch `opgaver/dag-2`, og aflevér via PR:
- dine ændringer i `server.py` (øvelse 3–5) og `app.py` (øvelse 8)
- `requirements.txt`
- `noter/dag-2.md` med dine svar på øvelse 1, 2, 6 og 9

## Spørg Claude

- *"Forklar forskellen på 401 og 403 med et eksempel fra et offentligt system."*
- *"Hvorfor er HTTP stateless? Hvordan ved en hjemmeside så, at jeg er logget ind?"* (Det kommer vi til på dag 7.)
- *"Gennemgå min `do_DELETE`. Er der fejl? Giv mig hints, ikke en rettet version."*
- *"Hvad er forskellen på REST og SOAP, og hvorfor findes SOAP stadig?"*
- *"Quiz mig i statuskoderne."*

## Tjekliste: kan du...

- [ ] tegne frontend, backend, database og integrationer og forklare, hvad hver del gør?
- [ ] pege på scheme, host, port, path og query i en URL?
- [ ] forklare, hvad der står i en HTTP-request og -response?
- [ ] forklare forskellen på 2xx, 4xx og 5xx og nævne et par af hver?
- [ ] lave `GET` og `POST` med `curl`?
- [ ] forklare, hvad REST er, og hvad et endpoint er?
- [ ] lave et venv og installere en pakke?
- [ ] forklare, hvad en OpenAPI-specifikation er, og hvorfor den er vigtig?

## Ordliste

| Ord | Betydning |
|-----|-----------|
| **klient / server** | Den, der spørger / den, der svarer |
| **frontend / backend** | Det, brugeren ser (i browseren) / forretningslogikken (på serveren) |
| **3-tier architecture** | Frontend, backend, database |
| **API** | En aftalt grænseflade, som et program kan kalde |
| **endpoint** | Én kombination af metode og sti, f.eks. `GET /maalinger/{id}` |
| **request / response** | Spørgsmål / svar i HTTP |
| **payload / body** | De data, der bliver sendt med i en request eller response |
| **header** | Metadata om en request eller response, f.eks. `Content-Type` |
| **HTTP / HTTPS** | Protokollen for web og API'er / krypteret udgave |
| **stateless** | Serveren husker ikke tidligere requests |
| **statuskode** | Tre cifre, der fortæller, hvordan det gik (200, 404, 500 …) |
| **idempotent** | At gentage en request giver samme resultat |
| **URL** | Adressen: scheme, host, port, path, query |
| **DNS** | Oversætter navne til IP-adresser |
| **localhost / 127.0.0.1** | Din egen maskine |
| **port** | "Døren" på en server, f.eks. 443 eller 8000 |
| **JSON** | Det mest udbredte dataformat mellem systemer |
| **XML / SOAP** | Ældre dataformat / ældre webservice-standard. Findes i mange offentlige integrationer |
| **REST** | En stil for HTTP-API'er: ressourcer i URL'en, handling i metoden |
| **CRUD** | Create, Read, Update, Delete: de fire grundoperationer |
| **framework** | Et bibliotek, der giver strukturen, f.eks. FastAPI, Spring Boot, ASP.NET |
| **dependency** | En pakke, projektet afhænger af |
| **virtual environment (venv)** | Et isoleret Python-miljø til ét projekt |
| **requirements.txt** | Listen over Python-dependencies med versioner |
| **OpenAPI / Swagger** | Standarden for at beskrive et REST-API / værktøjerne, der viser og afprøver det |
| **integration** | En forbindelse mellem to systemer |
| **log** | Den tekst, et program skriver om, hvad det laver. Det første sted, man kigger ved fejl |
| **DevTools / Network-fanen** | Browserens værktøj til at se alle HTTP-requests |
| **Postman / Bruno** | Grafiske værktøjer til at afprøve API'er. De bliver brugt meget i projekter |
