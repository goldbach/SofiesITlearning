# Dag 7: Sikkerhed og konsulentlivet

*Ca. 3½ time. Det hele er kerne. Del A–D handler om sikkerhed, del E–F om at være konsulent.*

## Hvorfor?

Offentlige systemer indeholder nogle af de mest følsomme data, der findes: CPR-numre, helbred, økonomi, børnesager. Et brud kan ramme tusindvis af borgere og ender i avisen. Sikkerhed er derfor ikke noget, "sikkerhedsfolkene" klarer. Det er en del af alle krav, al kode og al test.

Samtidig er du konsulent. Det betyder, at du arbejder i *kundens* systemer, med *kundens* data, efter *kontrakten*. Det giver nogle spilleregler, som ingen skriver ned, men som alle forventer, at du kender.

## Videoer og interaktivt materiale

| Hvornår | Hvad | Længde |
|---------|------|--------|
| **Før del B** | [Session vs Token Authentication in 100 Seconds](https://www.youtube.com/watch?v=UBUNrFtufWo) (Fireship) | 2 min |
| **Før del C** | [OAuth 2.0 and OpenID Connect (in plain English)](https://www.youtube.com/watch?v=996OiexHze0) (OktaDev): den bedste forklaring på emnet. Den er lang, men værd at se | 60 min |
| **Opslag** | [OWASP Top 10](https://owasp.org/www-project-top-ten/): de ti mest kritiske sikkerhedsrisici i webapplikationer | – |
| **Opslag** | [Datatilsynet](https://www.datatilsynet.dk/): vejledninger om GDPR på dansk | – |
| **Opslag** | [NemLog-in](https://www.nemlog-in.dk/) og [MitID](https://www.mitid.dk/) | – |

---

## Del A: Hvem er du, og hvad må du? (ca. 20 min)

To ord, der lyder ens, men er forskellige:

| | **Authentication** (autentifikation) | **Authorization** (autorisation) |
|---|---|---|
| Spørgsmål | *Hvem er du?* | *Hvad må du?* |
| Eksempel | Login med MitID | Må sagsbehandleren se *denne* ansøgning? |
| HTTP-fejl (dag 2) | `401 Unauthorized`: "Jeg ved ikke, hvem du er" | `403 Forbidden`: "Jeg ved, hvem du er, og svaret er nej" |
| Forkortelse | **AuthN** | **AuthZ** |

(Ja, `401` hedder "Unauthorized", selvom det handler om authentication. Det er en historisk fejl i HTTP-standarden, som alle lever med.)

### Godkendelse af identitet

Man kan bevise sin identitet med noget, man **ved** (password), noget, man **har** (telefon, nøglekort) eller noget, man **er** (fingeraftryk). **MFA** (*multi-factor authentication*) kombinerer to eller flere. MitID er MFA: brugernavn plus app eller kodeviser.

### Passwords gemmes aldrig

Et system må **aldrig** gemme passwords, heller ikke krypteret. Det gemmer en **hash** (dag 6b, del A): et fingeraftryk, som ikke kan regnes tilbage. Ved login hasher man det indtastede password og sammenligner fingeraftrykkene.

```python
import hashlib, os
salt = os.urandom(16)                       # tilfældigt pr. bruger, gemmes sammen med hashen
h = hashlib.scrypt(b"Sommer2026!", salt=salt, n=2**14, r=8, p=1)
print(h.hex())
```

Et **salt** sørger for, at to brugere med samme password får forskellige hashes. Algoritmen skal være *langsom med vilje* (scrypt, bcrypt, Argon2), så en angriber, der stjæler databasen, ikke kan prøve milliarder af gæt i sekundet. Almindelig SHA-256 er for hurtig til passwords.

I praksis bygger man sjældent login selv. Man bruger en **identity provider** (del C).

### Autorisation: roller og mindst mulig adgang

- **RBAC** (*role-based access control*): Brugere får roller (*sagsbehandler*, *teamleder*, *administrator*), og roller giver rettigheder.
- **Least privilege**: Alle skal have præcis den adgang, de har brug for, og ikke mere. Det gælder også dig som konsulent og systemer, der taler med hinanden.
- **Audit log**: I offentlige systemer skal det ofte logges, *hvem* der har *set* hvad, og ikke kun hvem der har ændret noget. "Hvem har slået mit CPR-nummer op?" skal kunne besvares.

Som analytiker skriver du autorisationsreglerne. De er tit de mest komplicerede krav i hele systemet: *"En sagsbehandler må se ansøgninger i sin egen afdeling, undtagen ansøgninger fra kolleger, medmindre vedkommende er teamleder."*

---

## Del B: Sessions og tokens (ca. 45 min)

På dag 2 lærte du, at HTTP er **stateless**. Serveren husker intet mellem to requests. Hvordan ved en hjemmeside så, at du er logget ind? Der er to hovedmåder.

### Session og cookie

1. Du logger ind. Serveren gemmer en **session** i sin hukommelse eller database: `abc123 → sofie`.
2. Serveren sender en **cookie** med `abc123` tilbage til browseren.
3. Browseren sender automatisk cookien med i hver request, og serveren slår den op.

Det er simpelt og sikkert, men serveren skal huske alle sessions. Det er besværligt, når der er mange servere (dag 6) og mange systemer.

### Token: JWT

1. Du logger ind. Serveren laver et **token**, der *selv indeholder* oplysningerne ("dette er sofie, hun er laborant, det udløber kl. 14:15"), og **signerer** det.
2. Klienten sender tokenet med i hver request: `Authorization: Bearer <token>`.
3. Serveren tjekker signaturen. Er den ægte, kan den stole på indholdet uden at slå noget op.

Det mest udbredte format er **JWT** (*JSON Web Token*, udtales "jot"). Kør laboratoriet:

```bash
cd ~/kursus/SofiesITlearning/07-sikkerhed-og-konsulentlivet
python3 jwt_lab.py
```

Et JWT er tre dele adskilt af punktum: `header.payload.signatur`.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2xvZ2lu....FkWqpVxzyTi4nD2UfMqe5Gtx0tkcFKpl4Zl4Jl0nhUk
└──────────── header ──────────────┘ └──────── payload ──────────┘ └──────────── signatur ─────────────┘
```

Header og payload er bare JSON, kodet med **base64url**. Det er *ikke* kryptering. Prøv selv:

```bash
echo -n "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" | base64 -d
```

Felterne i payloaden hedder **claims**. Standardfelterne er:

| Claim | Betydning |
|-------|-----------|
| `iss` | *issuer*: hvem har udstedt tokenet |
| `sub` | *subject*: hvem handler det om (brugerens id) |
| `aud` | *audience*: hvilket system er tokenet beregnet til |
| `exp` | *expiration*: hvornår udløber det (sekunder siden 1/1-1970) |
| `iat` | *issued at*: hvornår blev det udstedt |

Dertil kommer egne claims, f.eks. `roller`.

**Signaturen** er det, der gør tokenet til at stole på. Den er beregnet ud fra header, payload og en hemmelig nøgle. Ændrer man ét tegn i payloaden, f.eks. sin rolle fra `laborant` til `admin`, passer signaturen ikke længere. Det viser sidste linje i `jwt_lab.py`.

> **Tre ting du skal huske om JWT:**
> 1. **Alle kan læse indholdet.** Læg aldrig hemmeligheder eller unødvendige persondata i et token.
> 2. **Et token er som en nøgle.** Den, der har det, *er* dig, indtil det udløber. Derfor er levetiden kort (minutter), og derfor må tokens ikke stå i logs, i Jira-sager eller i chatbeskeder.
> 3. **Sæt aldrig et rigtigt token ind på en hjemmeside** for at "se, hvad der står i det", heller ikke på jwt.io. Brug `jwt_lab.afkod` eller tilsvarende lokalt.

`jwt_lab.py` bruger **HS256**, som er en HMAC (dag 6b, del A): én fælles hemmelig nøgle til både at signere og verificere. I praksis bruger identity providere oftest **RS256**, som er en digital signatur (dag 6b, del D): Den signerer med en *privat* nøgle, og alle systemer kan verificere med den tilsvarende *offentlige* nøgle. Så er det kun udstederen, der kan lave tokens.

### Øvelser B

1. Læs `jwt_lab.py`. Find de tre dele, og forklar med dine egne ord, hvad `signer` og `verificer` gør.
2. Afkod payloaden fra tokenet i dit eget output med `base64 -d`. Hvornår udløber tokenet? *Hint:* `date -r <exp>` på Mac.
3. `verificer` tjekker signatur og udløb, men ikke `aud`. Hvorfor er det et problem? Forestil dig, at det samme login-system udsteder tokens til både en kantine-app og tilskudssystemet. Tilføj et tjek af `aud`.
4. **Beskyt API'et.** Kopiér `server.py` fra dag 2 hertil, og få `POST /maalinger` til at kræve et gyldigt token med rollen `laborant`:
   - Intet eller ugyldigt token: `401`
   - Gyldigt token, men uden rollen: `403`
   - `GET` må stadig være åben

   Lav et token og test sådan:
   ```bash
   TOKEN=$(python3 -c 'import time, jwt_lab; print(jwt_lab.lav_token({"sub": "sofie", "aud": "maalinger-api", "roller": ["laborant"], "exp": int(time.time()) + 900}, "kun-til-laering-aldrig-i-git-i-virkeligheden"))')
   curl -i -X POST http://127.0.0.1:8000/maalinger -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" -d '{"temperatur": 22, "tryk": 1010}'
   ```
   *Hints:* `self.headers.get("Authorization")`, `str.removeprefix("Bearer ")`, `from jwt_lab import verificer`.

---

## Del C: OAuth 2.0, OpenID Connect og MitID (ca. 45 min)

### Problemet

Kommunen har 50 systemer. Skal hvert system have sit eget login, sine egne passwords og sin egen MFA? Nej. Login bliver samlet ét sted, hos en **identity provider** (IdP), og systemerne stoler på IdP'en. Det giver også **single sign-on** (SSO): Log ind én gang, og få adgang til mange systemer.

### OAuth 2.0 og OpenID Connect

- **OAuth 2.0** er en standard for at give et system *adgang* til noget på vegne af en bruger. Det handler om authorization. Resultatet er et **access token**.
- **OpenID Connect** (OIDC) er et lag oven på OAuth 2.0, der også fortæller, *hvem* brugeren er. Det handler om authentication. Resultatet er et **ID token**, som er et JWT.

Det mest brugte flow for webapplikationer hedder **authorization code flow** (med **PKCE**):

```
  Bruger           Webapp (klient)            Identity provider           API
    │  klik "Log ind"  │                              │                     │
    │─────────────────►│                              │                     │
    │  redirect til IdP│                              │                     │
    │◄─────────────────│                              │                     │
    │           log ind med MitID                     │                     │
    │────────────────────────────────────────────────►│                     │
    │  redirect tilbage med en engangs-"code"         │                     │
    │◄────────────────────────────────────────────────│                     │
    │─────────────────►│  byt code til tokens         │                     │
    │                  │─────────────────────────────►│                     │
    │                  │  ID token + access token     │                     │
    │                  │◄─────────────────────────────│                     │
    │                  │  GET /ansoegninger, Authorization: Bearer <access token>
    │                  │───────────────────────────────────────────────────►│
    │                  │                              │   verificér token,  │
    │                  │◄───────────────────────────────────────────────────│   tjek roller
```

Vigtige pointer:
- **Webappen ser aldrig brugerens password.** Det bliver kun indtastet hos IdP'en.
- **API'et kontakter ikke IdP'en ved hver request.** Det verificerer tokenets signatur med IdP'ens offentlige nøgle. Det er det, du byggede i del B.
- Access tokens udløber hurtigt. Et **refresh token** bruges til at hente et nyt uden at logge ind igen.
- **Scopes** beskriver, hvad klienten beder om adgang til, f.eks. `openid profile ansoegninger:laes`.

Du vil også møde **SAML**, en ældre standard med samme formål, baseret på XML. Den er stadig udbredt i det offentlige.

### Danmark: MitID og NemLog-in

- **MitID** er den nationale digitale identitet for borgere. **MitID Erhverv** er til medarbejdere, der handler på vegne af en virksomhed.
- **NemLog-in** er det fælles offentlige login, som Digitaliseringsstyrelsen står bag. Offentlige selvbetjeningsløsninger kobler sig på NemLog-in i stedet for at integrere direkte med MitID. NemLog-in har historisk brugt en dansk SAML-profil, **OIOSAML**.
- Private virksomheder (banker, forsikring) bruger typisk en certificeret **MitID-broker**.
- Medarbejdere hos kunden logger tit ind via organisationens egen IdP, f.eks. **Microsoft Entra ID** (tidligere *Azure AD*).

Så når nogen siger *"vi skal integrere med NemLog-in"*, betyder det: Systemet skal sende brugeren til NemLog-in, modtage et signeret svar og stole på det. Det er præcis flowet ovenfor.

### Øvelse C

5. Tilskudssystemet fra dag 3: Hvilke brugertyper er der, og hvordan logger hver af dem ind? Hvilke roller skal systemet kende, og hvad må hver rolle? Lav en tabel med rolle, login-metode og rettigheder. Det er en rigtig analyseopgave.

---

## Del D: Sikker software og GDPR (ca. 45 min)

### OWASP Top 10

**OWASP** udgiver en liste over de mest kritiske sikkerhedsrisici i webapplikationer. Den nuværende udgave er fra 2025:

| # | Risiko | Kender du den? |
|---|--------|----------------|
| A01 | Broken Access Control | Brugere kan se eller gøre noget, de ikke må. Typisk mangler et tjek som det i øvelse 4 |
| A02 | Security Misconfiguration | Standardpasswords, åbne porte, debug slået til i produktion |
| A03 | Software Supply Chain Failures | Sårbare eller ondsindede dependencies (dag 2: `requirements.txt`, dag 4: `pom.xml`) |
| A04 | Cryptographic Failures | Manglende HTTPS, passwords gemt uden hash |
| A05 | Injection | SQL injection fra dag 3 |
| A06 | Insecure Design | Sikkerhed, der ikke er tænkt ind fra starten |
| A07 | Authentication Failures | Svagt login, ingen MFA, sessions der aldrig udløber |
| A08 | Software or Data Integrity Failures | Kode eller data, der ikke er tjekket for manipulation |
| A09 | Security Logging and Alerting Failures | Ingen opdager angrebet, fordi intet bliver logget eller overvåget (dag 6) |
| A10 | Mishandling of Exceptional Conditions | Fejl, der ikke bliver håndteret ordentligt, som `TypeError`-fejlen fra dag 5 |

Læg mærke til, hvor mange af dem du allerede har mødt. Sikkerhed er ikke et særskilt emne. Det er god praksis i alt det, du har lært.

### Andre trusler, du selv skal passe på

- **Phishing**: e-mails og beskeder, der prøver at få dig til at klikke, logge ind eller godkende noget. Som ny medarbejder er du et yndet mål ("Hej, det er din chef, kan du lige ...?"). Er du i tvivl, så ring til afsenderen på et nummer, du selv har fundet.
- **MFA-træthed**: Godkend *aldrig* en login-anmodning, du ikke selv har startet.
- **Secrets**: passwords, nøgler og tokens hører hjemme i et vault, ikke i Git, Jira, Teams eller e-mails (dag 1 og 6).
- **Den fysiske verden**: Lås skærmen (`Ctrl-Cmd-Q`), når du går fra den. Tal ikke om kundens sager i toget. Pas på med skærmen på caféen.

### GDPR i én side

**GDPR** (databeskyttelsesforordningen) gælder for alle **personoplysninger**: alt, der kan knyttes til en person. Det gælder navn, e-mail, IP-adresse og CPR-nummer, men også kombinationer, der tilsammen kan identificere en person.

- **Følsomme oplysninger** (helbred, etnicitet, religion, fagforening, seksualitet m.fl.) er særligt beskyttede. CPR-numre har også særlige regler i den danske databeskyttelseslov.
- **Dataansvarlig**: den, der bestemmer, *hvorfor* og *hvordan* data bliver behandlet. Det er typisk kunden.
- **Databehandler**: den, der behandler data på den dataansvarliges vegne. Det er typisk leverandøren, altså Netcompany. Forholdet er reguleret i en **databehandleraftale**.

Principperne, du skal kunne genkende i krav:

| Princip | Betyder | Eksempel på krav |
|---------|---------|------------------|
| **Formålsbegrænsning** | Data må kun bruges til det formål, de er indsamlet til | Data fra tilskudsansøgninger må ikke bruges til markedsføring |
| **Dataminimering** | Indsaml kun det nødvendige | Skal vi virkelig have borgerens telefonnummer? |
| **Opbevaringsbegrænsning** | Slet data, når de ikke skal bruges mere | Ansøgninger slettes 5 år efter afgørelse |
| **Integritet og fortrolighed** | Beskyt data | Kryptering, adgangskontrol, audit log |
| **Privacy by design** | Tænk databeskyttelse ind fra starten | Testmiljøer bruger kun anonymiserede data (dag 3) |

Et **brud på persondatasikkerheden** (f.eks. data sendt til forkert modtager, en stjålet computer eller et hack) skal som udgangspunkt anmeldes til **Datatilsynet inden 72 timer**. Derfor: Opdager du noget, så sig det **med det samme** til din projektleder. Det er aldrig for småt, og ingen bliver skældt ud for at sige det. Problemet opstår, når det bliver skjult.

Ved behandlinger med høj risiko skal man lave en **konsekvensanalyse** (DPIA). Det er tit analytikere, der hjælper med den.

### Øvelse D

6. Gå tilbage til din datamodel for tilskudssystemet (dag 3). Markér alle personoplysninger, og markér de følsomme. Skriv tre GDPR-krav til systemet som testbare krav (dag 5).

---

## Del E: At være konsulent (ca. 45 min)

### Kunden, kontrakten og dig

- **Du repræsenterer Netcompany** over for kunden, også i det små. Vær forberedt, kom til tiden, og gør det, du siger, du vil gøre.
- **Lov aldrig kunden noget, der ikke er aftalt.** *"Det kan vi sagtens lave"* kan blive en ændring på 200 timer, som ingen har budgetteret med (dag 5: change requests). Sig i stedet: *"Godt spørgsmål. Jeg tager det med til teamet, og så vender vi tilbage."*
- **Kunden er ikke altid én person.** Der er en projektleder, en product owner, fagfolk, it-afdelingen, jurister og en driftsleverandør, og de vil ikke altid det samme. Find ud af, hvem der *beslutter* hvad.
- **Fortrolighed**: Det, du ser hos kunden, bliver hos kunden. Du har sikkert skrevet under på en fortrolighedserklæring. Nogle projekter, f.eks. inden for forsvar og politi, kræver også en særlig **sikkerhedsgodkendelse**.

### Tid og timer

Konsulenthuse lever af timer. Det betyder for dig:

- **Timeregistrering hver dag**, på den rigtige sag eller det rigtige projektnummer. Det, du registrerer, bliver ofte faktureret til kunden og skal kunne forsvares.
- **Fakturerbar og intern tid**: Tid på kundens opgaver kan faktureres. Kurser og interne møder kan ikke. **Udnyttelsesgrad** (*utilization*) er andelen af din tid, der kan faktureres. Det er et nøgletal, du vil høre om.
- **At være "allokeret"** til et projekt betyder, at du er sat på det med en vis procentdel af din tid.

Spørg din leder, hvordan det konkret foregår hos Netcompany. Det her er det generelle billede.

### Roller på et projekt

| Rolle | Hvad de gør |
|-------|-------------|
| **Projektleder** | Plan, økonomi, risici og kunderelation. Den, du eskalerer til |
| **Arkitekt** | De store tekniske beslutninger: hvordan systemet er skruet sammen |
| **Lead developer / tech lead** | Leder udviklerne og står for den tekniske kvalitet |
| **Udvikler** | Skriver koden |
| **Tester / test manager** | Planlægger og udfører test, og styrer testmiljøer og testdata |
| **Business analyst / funktionel konsulent** | Krav, user stories, datamodeller og workshops. Måske dig |
| **Scrum master** | Processen (dag 5) |
| **Kundens PO / fagansvarlige** | Ved, hvad forretningen har brug for |
| **Driftsleverandør** | Kører systemet i produktion (dag 6) |

### Kommunikation, der virker

- **Konklusionen først.** *"Vi kan ikke nå release 2.4 til 1. december. Årsagen er ... Mit forslag er ..."* Ikke ti linjers baggrund før pointen.
- **Skriv beslutninger ned.** Efter et møde: et kort referat med *beslutninger*, *handlinger* (hvem gør hvad og hvornår) og *åbne spørgsmål*. Det, der ikke er skrevet ned, er ikke besluttet.
- **Eskalér tidligt.** Et problem, der bliver nævnt på dag 2, er et problem. Et problem, der bliver nævnt dagen før deadline, er en krise. At eskalere er ikke at sladre. Det er at give folk mulighed for at hjælpe.
- **Spørg, også de "dumme" spørgsmål.** Som ny forventer alle, at du spørger. Spørgsmål som *"hvad betyder STATUS_KD = 7?"* eller *"hvorfor gør vi det sådan?"* finder ofte fejl, som de erfarne er blevet blinde for.
- **Lav din egen ordliste over domænet.** Hvert projekt har sine forkortelser og fagudtryk (*"partshøring"*, *"bevillingsramme"*, *"KLE-nummer"*). Skriv dem ned, efterhånden som du hører dem, ligesom ordlisterne i det her forløb.

### Det er normalt at føle sig på dybt vand

Alle nye konsulenter føler, at de andre ved meget mere, og at de selv snart bliver "afsløret". Det hedder *imposter syndrome*, og det går over. Du er ikke ansat, fordi du kan alt i forvejen. Du er ansat, fordi du kan lære hurtigt og tænke klart. Det har du bevist med en kandidat i nanoscience og med det her forløb.

---

## Del F: Din første uge (ca. 15 min)

### Tjekliste

- [ ] **Adgang**: computer, e-mail, VPN, Jira/Azure DevOps, Git, Confluence/wiki, timeregistrering. Noget plejer at mangle. Sig til med det samme.
- [ ] **Mennesker**: Hvem er din leder, din buddy/mentor, din projektleder og dine nærmeste kolleger? Book en kop kaffe med dem.
- [ ] **Projektet**: Hvad er formålet? Hvem er kunden? Hvilken fase er I i (dag 5)? Hvornår er næste release eller milepæl?
- [ ] **Systemet**: Find arkitekturtegningen. Hvilke systemer integrerer I med (dag 2)? Hvor ligger koden? Hvilke miljøer er der (dag 5 og 6)?
- [ ] **Arbejdsgangene**: Hvornår er standup, refinement og demo? Hvordan ser jeres Definition of Done ud?
- [ ] **Regler**: Hvilke AI-værktøjer er godkendt (dag 1b)? Hvordan håndterer I persondata og testdata? Hvem kontakter du ved et sikkerhedsbrud?
- [ ] **Din ordliste**: Begynd på din ordliste over domænet allerede første dag.

### Efter forløbet

Det her repo er dit. Brug det:
- Kom tilbage til ordlisterne, når du hører et ord på jobbet, du har glemt. [ORDLISTE.md](../ORDLISTE.md) samler dem.
- Brug Claude som tutor, når der kommer et nyt emne: *"Jeg skal i morgen til en workshop om integration med CPR-registret. Hvad skal jeg vide?"* Men husk reglerne fra dag 1b. Kundens data og kode hører ikke hjemme her.
- Lav nye øvelser til dig selv i `noter/`. Det bedste bevis på, at man har forstået noget, er at kunne forklare det.

**Held og lykke. Du bliver god til det her.**

---

## Aflevering

Lav en branch `opgaver/dag-7`, og aflevér via PR:
- `noter/dag-7.md` med svar på øvelse 1, 2, 3, 5 og 6
- `jwt_lab.py` med `aud`-tjek (øvelse 3) og `server.py` med beskyttet `POST` (øvelse 4)

## Spørg Claude

- *"Forklar forskellen på et ID token og et access token, som om jeg skal forklare det for en sagsbehandler."*
- *"Hvorfor er det et problem, hvis et JWT aldrig udløber?"*
- *"Gennemgå min `server.py` med token-tjek. Kan du finde en måde at omgå det? Giv mig kun et hint."*
- *"Spil en kunde, der beder mig om en 'lille ekstra ting' i et møde. Hjælp mig med at øve at svare uden at love noget."*
- *"Hvad er forskellen på dataansvarlig og databehandler? Giv et eksempel med en kommune og en leverandør."*
- *"Jeg har opdaget, at et testmiljø indeholder rigtige CPR-numre. Hvad gør jeg?"*

## Tjekliste: kan du...

- [ ] forklare forskellen på authentication og authorization, og på 401 og 403?
- [ ] forklare, hvorfor passwords bliver hashet og ikke krypteret?
- [ ] forklare forskellen på session/cookie og token?
- [ ] afkode et JWT og forklare, hvad signaturen beskytter mod?
- [ ] forklare, hvad en identity provider gør, og tegne authorization code flow i grove træk?
- [ ] forklare, hvad MitID og NemLog-in er, og hvordan de hænger sammen?
- [ ] nævne fem punkter fra OWASP Top 10, og hvor du har mødt dem i forløbet?
- [ ] forklare dataansvarlig, databehandler, og hvad du gør ved et brud?
- [ ] svare en kunde, der beder om noget, der ikke er aftalt?

## Ordliste

| Ord | Betydning |
|-----|-----------|
| **authentication (AuthN)** | Hvem er du? |
| **authorization (AuthZ)** | Hvad må du? |
| **MFA** | Login med flere faktorer (ved, har, er) |
| **hash / salt** | Envejs-fingeraftryk / tilfældig værdi, der gør hashen unik pr. bruger |
| **scrypt / bcrypt / Argon2** | Bevidst langsomme hash-algoritmer til passwords |
| **RBAC** | Adgang styret af roller |
| **least privilege** | Kun den adgang, man har brug for |
| **audit log** | Log over, hvem der har set og ændret hvad |
| **session / cookie** | Login husket af serveren / lille værdi, som browseren sender med automatisk |
| **token / bearer token** | Et bevis på login, der bliver sendt i `Authorization: Bearer ...` |
| **JWT** | JSON Web Token: header.payload.signatur |
| **base64url** | Tegnkodning, der gør binære data til tekst. Ikke kryptering |
| **claim** | Et felt i et JWT (`sub`, `exp`, `roller` …) |
| **signatur / HS256 / RS256** | Bevis for ægthed / fælles hemmelig nøgle / privat og offentlig nøgle |
| **identity provider (IdP)** | Systemet, der står for login |
| **SSO** | Single sign-on: ét login til mange systemer |
| **OAuth 2.0** | Standard for at give adgang på en brugers vegne |
| **OpenID Connect (OIDC)** | Login-lag oven på OAuth 2.0 |
| **ID token / access token / refresh token** | Hvem brugeren er / adgang til et API / til at hente nye tokens |
| **authorization code flow / PKCE** | Det almindelige login-flow for webapps / en sikring af det |
| **scope** | Hvad en klient beder om adgang til |
| **SAML / OIOSAML** | Ældre XML-baseret login-standard / dansk profil af den |
| **MitID / MitID Erhverv** | National digital identitet for borgere / for medarbejdere i virksomheder |
| **NemLog-in** | Det fælles offentlige login |
| **MitID-broker** | Certificeret mellemled mellem MitID og private tjenester |
| **Entra ID (Azure AD)** | Microsofts identity provider, som mange organisationer bruger |
| **OWASP Top 10** | Listen over de mest kritiske sikkerhedsrisici i webapplikationer |
| **phishing** | Svindelbeskeder, der prøver at narre dig |
| **supply chain** | Risikoen i de dependencies og værktøjer, man bygger på |
| **GDPR / personoplysning** | Databeskyttelsesforordningen / alt, der kan knyttes til en person |
| **følsomme oplysninger** | Helbred, religion, etnicitet m.fl. Særligt beskyttet |
| **dataansvarlig / databehandler** | Bestemmer over data (kunden) / behandler på dens vegne (leverandøren) |
| **databehandleraftale** | Kontrakten om, hvordan databehandleren må behandle data |
| **formålsbegrænsning / dataminimering** | Kun til formålet / kun det nødvendige |
| **privacy by design** | Databeskyttelse tænkt ind fra starten |
| **brud på persondatasikkerheden** | Data er kommet i forkerte hænder eller tabt. Anmeldes inden 72 timer |
| **Datatilsynet** | Den danske myndighed for databeskyttelse |
| **DPIA / konsekvensanalyse** | Analyse af risici ved en behandling af persondata |
| **fortrolighedserklæring / NDA** | Aftale om tavshed om kundens forhold |
| **sikkerhedsgodkendelse** | Godkendelse, som nogle følsomme projekter kræver |
| **timeregistrering** | Registrering af arbejdstid på sager |
| **fakturerbar tid / udnyttelsesgrad** | Tid, kunden betaler for / andelen af tiden, der kan faktureres |
| **allokeret** | Sat på et projekt |
| **eskalere** | Bringe et problem videre til dem, der kan løse det |
| **referat** | Beslutninger, handlinger og åbne spørgsmål efter et møde |
| **imposter syndrome** | Følelsen af ikke at være god nok. Den er normal, og den går over |
