# Dag 2: Hvordan et system hænger sammen

*Ca. 3½ time for kernen. **Kerne:** del A–D og F. **Fordybelse:** del E og øvelse 12.*

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

## Del E: Kig under motorhjelmen på rigtige hjemmesider (ca. 15 min, fordybelse)

1. Åbn en hjemmeside, du bruger, f.eks. en nyhedsside, i Chrome eller Safari. I Safari skal du først slå *Udvikler*-menuen til under *Indstillinger → Avanceret*.
2. Åbn **Developer Tools** med `Cmd-Option-I`, og vælg fanen **Network**.
3. Genindlæs siden. Hver linje er en HTTP-request. Klik på nogle af dem, og find metode, statuskode, headers og response.
4. Filtrér på **Fetch/XHR**. Det er de kald, frontenden laver til et API. Kan du finde ét, der returnerer JSON?

Testere og analytikere bruger Network-fanen dagligt til at se, hvad der faktisk bliver sendt.

---

## Del F: Netværk og porte (ca. 45 min)

Du skal ikke designe netværk, men du skal kunne følge med, når nogen siger "porten er ikke åbnet i firewallen" eller "er du på VPN?". Du skal også kunne lave den første fejlfinding selv.

### IP-adresser og porte

En **IP-adresse** identificerer en maskine på netværket. En **port** er et nummer fra 0 til 65535, som identificerer et bestemt program *på* maskinen. Tænk på et kontorhus: IP-adressen er gadeadressen, og porten er lokalenummeret.

Når et serverprogram starter, beder det styresystemet om at **lytte** (*listen*) på en port. Kun ét program ad gangen kan lytte på samme port og adresse.

Prøv det. Start `server.py` i ét faneblad, og start den igen i et andet:

```
OSError: [Errno 48] Address already in use
```

Den fejl møder du igen og igen. Find ud af, hvem der optager porten:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

Svaret viser programnavnet og dets **PID** (*process ID*). Stop det med Ctrl-C i dets faneblad, eller med `kill <PID>`.

> `-nP` betyder "vis tal". Uden det oversætter `lsof` port 8000 til et gammelt servicenavn (`irdmi`), som ikke giver mening for nogen.

### Porte du vil møde

| Port | Hvad |
|------|------|
| 22 | SSH: log ind på en server via terminalen |
| 80 / 443 | HTTP / HTTPS |
| 1433 | Microsoft SQL Server |
| 1521 | Oracle-database |
| 5432 | PostgreSQL |
| 3000, 5173, 8000, 8080 | Typiske udviklingsservere på din egen maskine |

Porte under 1024 kræver administratorrettigheder. Derfor kører udviklingsservere på høje porte.

### TCP og UDP

Data bliver sendt i små **pakker**. To protokoller bestemmer, hvordan det sker:

| | **TCP** | **UDP** |
|---|---------|---------|
| Pålidelighed | Alt kommer frem, i rigtig rækkefølge, og tabte pakker bliver sendt igen | Ingen garanti |
| Hastighed | Lidt langsommere: forbindelsen bliver etableret først (*handshake*) | Hurtig |
| Bruges af | HTTP, databaser, SSH, mail | DNS, video, telefoni, spil |

Når nogen siger "port 443", mener de næsten altid TCP-port 443.

### Hvem kan nå din server? `127.0.0.1` og `0.0.0.0`

Kig i bunden af `server.py`:

```python
adresse = ("127.0.0.1", 8000)
```

- `127.0.0.1` (**localhost**): serveren kan **kun** nås fra din egen maskine.
- `0.0.0.0`: serveren lytter på **alle** netværkskort og kan nås fra andre maskiner på netværket.

Udviklingsservere kører på `127.0.0.1` som standard. Det er en sikkerhedsbeslutning.

### Privat og offentlig IP

```bash
ipconfig getifaddr en0             # din IP på det lokale netværk (wifi)
curl https://api.ipify.org         # den IP, internettet ser dig med
```

De er forskellige. Hjemme og på kontoret har du en **privat IP**, typisk `192.168.x.x`, `10.x.x.x` eller `172.16–31.x.x`. Den kan kun bruges på det lokale netværk. Routeren deler én **offentlig IP** mellem alle enhederne. Det kaldes **NAT** (*network address translation*). Derfor kan internettet ikke bare kontakte din bærbare, men din bærbare kan godt kontakte internettet.

### Fejlfinding: fire kommandoer

```bash
nslookup api.github.com          # DNS: hvilken IP har navnet? (eller: dig +short api.github.com)
ping -c 4 api.github.com         # kan jeg nå maskinen, og hvor lang tid tager det (ms)?
nc -vz api.github.com 443        # er der hul igennem til netop den port?
traceroute api.github.com        # hvilken vej går pakkerne? (stop med Ctrl-C)
```

`nc -vz` (*netcat*) er den mest brugbare til fejlfinding. Den svarer på spørgsmålet: kan jeg få forbindelse til *den* port på *den* maskine? Læg mærke til de tre mulige svar:

| Svar | Betydning |
|------|-----------|
| `succeeded!` | Der er hul igennem, og noget lytter |
| `Connection refused` | Maskinen kan nås, men intet lytter på porten. Serveren kører måske ikke |
| `Operation timed out` | Intet svar. Typisk blokerer en **firewall**, eller du er ikke på det rigtige netværk |

Prøv selv:

```bash
nc -vz 127.0.0.1 8000                  # med server.py kørende, og uden
nc -vz -G 3 api.github.com 8443        # en port, GitHub ikke har åben
```

> `ping` er ikke altid til at stole på. Mange servere og firewalls ignorerer ping med vilje. Hvis ping ikke svarer, er det ikke et bevis på, at maskinen er nede.

### Konsulent-hverdagen: VPN, firewall, proxy og certifikater

Kundens systemer ligger sjældent åbent på internettet. Du kommer til at høre disse sætninger:

- **"Er du på VPN?"** Et **VPN** (*virtual private network*) er en krypteret tunnel ind på kundens netværk. Uden det kan du ikke nå test- og udviklingsmiljøerne. Typisk symptom: `Operation timed out` eller "siden kan ikke findes".
- **"Porten er ikke åbnet i firewallen."** En **firewall** bestemmer, hvilken trafik der må komme igennem, fra hvor og til hvilke porte. Når to systemer skal integreres, skal der ofte bestilles en **firewall-åbning** hos kundens driftsleverandør. Det kan tage uger, så analytikeren gør klogt i at få det med i planen tidligt.
- **"Du skal igennem proxyen."** En **proxy** er en mellemstation, som trafikken skal igennem, typisk ud mod internettet i store organisationer. `pip install` og `curl` virker ikke, før proxyen er sat op.
- **"Certifikatet er udløbet."** HTTPS bruger **TLS-certifikater** til at bevise, at serveren er den, den udgiver sig for at være. Et certifikat har en udløbsdato. Når den passerer, holder integrationerne op med at virke. Det er en klassisk produktionsfejl. Se GitHubs certifikat:
  ```bash
  curl -svI https://api.github.com 2>&1 | grep -iE "subject:|issuer:|expire"
  ```

### Øvelser F

10. **Optaget port.** Fremprovokér `Address already in use`, find PID'en med `lsof`, og stop den rigtige proces.
11. **Refused eller timeout?** Kør `nc -vz 127.0.0.1 8000` med og uden server. Kør også `nc -vz -G 3 api.github.com 8443`. Skriv ned, hvad de tre svar betyder.
12. **Kald din server fra telefonen** (fordybelse).
    1. Ret `adresse` i `server.py` til `("0.0.0.0", 8000)`, og start serveren.
    2. Hvis macOS spørger, om Python må modtage indgående forbindelser, så tillad det.
    3. Find din private IP med `ipconfig getifaddr en0`.
    4. Åbn `http://<din-ip>:8000/maalinger` i telefonens browser. Telefonen skal være på samme wifi.
    5. Kig i serverens log. Hvilken IP kommer requesten fra?
    6. **Ret den tilbage til `127.0.0.1` bagefter.** En udviklingsserver skal ikke stå åben på en café-wifi.

    Virker det ikke? Gæste- og firmanetværk blokerer ofte for, at enheder taler direkte sammen. Det er i sig selv en lektion i firewalls.
13. **Hvor bor GitHub?** Find IP-adressen på `api.github.com` med `nslookup`, og hvornår certifikatet udløber.

---

## Aflevering

Lav en branch `opgaver/dag-2`, og aflevér via PR:
- dine ændringer i `server.py` (øvelse 3–5) og `app.py` (øvelse 8)
- `requirements.txt`
- `noter/dag-2.md` med dine svar på øvelse 1, 2, 6, 9, 11 og 13

## Spørg Claude

- *"Forklar forskellen på 401 og 403 med et eksempel fra et offentligt system."*
- *"Hvorfor er HTTP stateless? Hvordan ved en hjemmeside så, at jeg er logget ind?"* (Det kommer vi til på dag 7.)
- *"Gennemgå min `do_DELETE`. Er der fejl? Giv mig hints, ikke en rettet version."*
- *"Hvad er forskellen på REST og SOAP, og hvorfor findes SOAP stadig?"*
- *"Quiz mig i statuskoderne."*
- *"Jeg kan ikke nå kundens testmiljø, og `nc` giver timeout. Hvilke spørgsmål skal jeg stille, og til hvem?"*
- *"Forklar NAT med en analogi."*

## Tjekliste: kan du...

- [ ] tegne frontend, backend, database og integrationer og forklare, hvad hver del gør?
- [ ] pege på scheme, host, port, path og query i en URL?
- [ ] forklare, hvad der står i en HTTP-request og -response?
- [ ] forklare forskellen på 2xx, 4xx og 5xx og nævne et par af hver?
- [ ] lave `GET` og `POST` med `curl`?
- [ ] forklare, hvad REST er, og hvad et endpoint er?
- [ ] lave et venv og installere en pakke?
- [ ] forklare, hvad en OpenAPI-specifikation er, og hvorfor den er vigtig?
- [ ] forklare forskellen på en IP-adresse og en port, og finde ud af, hvem der optager en port?
- [ ] forklare forskellen på `127.0.0.1` og `0.0.0.0`, og på en privat og en offentlig IP?
- [ ] bruge `nc -vz` og forklare forskellen på "refused" og "timed out"?
- [ ] forklare, hvad VPN, firewall, proxy og TLS-certifikat er, med én sætning hver?

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
| **port** | Nummeret på et bestemt program på en maskine, f.eks. 443 eller 8000 |
| **listen / lytte** | En server, der venter på forbindelser på en port |
| **PID** | *Process ID*: nummeret på et kørende program |
| **TCP / UDP** | Pålidelig transport (HTTP, databaser) / hurtig, upålidelig transport (DNS, video) |
| **`0.0.0.0`** | "Lyt på alle netværkskort", så serveren kan nås udefra |
| **privat / offentlig IP** | Adresse på det lokale netværk (`192.168.x.x`) / den adresse, internettet ser |
| **NAT** | Routeren deler én offentlig IP mellem mange enheder |
| **firewall** | Regler for, hvilken trafik der må komme igennem |
| **firewall-åbning** | En bestilling på at åbne for trafik mellem to systemer. Kan tage lang tid |
| **VPN** | En krypteret tunnel ind på et andet netværk, f.eks. kundens |
| **proxy** | En mellemstation, trafikken skal igennem |
| **TLS / certifikat** | Kryptering i HTTPS / et digitalt bevis for serverens identitet, med udløbsdato |
| **SSH** | Krypteret login på en server via terminalen (port 22) |
| **ping / traceroute / nslookup / nc** | Kan jeg nå den? / Hvilken vej? / Hvilken IP? / Er porten åben? |
| **timeout / connection refused** | Intet svar, ofte en firewall / intet lytter på porten |
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
