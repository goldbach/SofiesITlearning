# Dag 5: Fra behov til løsning

*Ca. 4 timer. Det hele er kerne. Det er det modul, der ligger tættest på dit kommende job. I dag er der mindre kode og mere af det, du kommer til at lave hver dag.*

## Hvorfor?

De fleste IT-projekter, der går galt, går ikke galt på grund af dårlig kode. De går galt, fordi man har bygget det forkerte: Kravene var uklare, kunden og leverandøren forstod dem forskelligt, eller ingen spurgte "hvad sker der, hvis ...?".

Analytikerens opgave er at bygge bro mellem **forretningen** (kunden, brugerne, lovgivningen) og **udviklerne**. Det gør man med krav, user stories og acceptkriterier, og man følger dem hele vejen gennem test til produktion.

I dag lærer du sproget og arbejdsgangene: hvordan et behov bliver til en Jira-sag, til kode, til test og til en release.

## Videoer og interaktivt materiale

| Hvornår | Hvad | Længde |
|---------|------|--------|
| **Før du starter** | [Agile Product Ownership in a Nutshell](https://www.youtube.com/watch?v=502ILHjX9EE) (Henrik Kniberg): en klassiker. Den forklarer backlog, prioritering og værdi bedre end nogen bog | 15 min |
| **Før del D** | [Introduction to Scrum – 7 Minutes](https://www.youtube.com/watch?v=9TycLR0TqFA) (Uzility) | 7 min |
| **Opslag** | [The Scrum Guide](https://scrumguides.org/scrum-guide.html): den officielle definition. Kun 13 sider | 30 min |
| **Opslag** | [Atlassian: User stories](https://www.atlassian.com/agile/project-management/user-stories) og [Scrum](https://www.atlassian.com/agile/scrum) | – |
| **Til fordybelse** | [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) (Martin Fowler): standardteksten om teststrategi | 45 min |

---

## Del A: Et projekts liv (ca. 30 min)

Et typisk offentligt IT-projekt gennemløber nogenlunde disse faser:

```
 Udbud ──► Kontrakt ──► Analyse ──► Udvikling & test ──► Overtagelse ──► Drift & vedligehold
   │                     ▲    │         ▲        │                            │
   │                     │    └─────────┘        │                            │
   │                     └────── ændringer (change requests) ◄────────────────┘
```

- **Udbud**: Offentlige myndigheder skal som regel sende større opgaver i **udbud** efter udbudsloven. Kunden beskriver behovet, ofte i en **kravspecifikation** med nummererede krav. Leverandører som Netcompany afgiver **tilbud** med løsning og pris.
- **Kontrakt**: Den vindende leverandør skriver kontrakt. Staten har standardkontrakter, og kravspecifikationen bliver typisk et bilag til kontrakten. Det betyder, at **kravene er juridisk bindende**. Derfor betyder præcise formuleringer meget.
- **Analyse/design**: Kravene bliver detaljeret, ofte i workshops med kunden. Her bliver user stories, datamodeller (dag 3) og integrationsbeskrivelser (dag 2) skrevet.
- **Udvikling og test**: Ofte i **sprints** (del D).
- **Overtagelse**: Kunden tester, om leverancen opfylder kontrakten. Det kaldes f.eks. en **overtagelsesprøve** eller **UAT**. Først derefter betaler kunden typisk det fulde beløb.
- **Drift og vedligehold**: Systemet kører i produktion. Fejl bliver rettet, og nye ønsker kommer som **change requests** (CR, *ændringsanmodninger*), som skal estimeres og godkendes.

### Vandfald og agilt

- **Vandfald**: Faserne kommer efter hinanden: først alle krav, så al udvikling, så al test. Det er forudsigeligt på papiret, men man opdager misforståelser sent.
- **Agilt**: Man leverer i små bidder, typisk hver 2. uge. Man viser dem til kunden og retter kursen undervejs. Misforståelser bliver opdaget tidligt.

I virkeligheden er de fleste store projekter **hybride**: en fast kontrakt med en kravspecifikation, men leveret agilt indenfor den. Det giver spændinger, som du vil mærke: *"Står det i kontrakten?"*, *"Er det en fejl eller en ændring?"*

---

## Del B: Krav (ca. 45 min)

### Funktionelle og ikke-funktionelle krav

- **Funktionelle krav** beskriver, *hvad* systemet skal gøre: *"Sagsbehandleren skal kunne bevilge eller afslå en ansøgning."*
- **Ikke-funktionelle krav** beskriver, *hvor godt* det skal gøres. De bliver ofte glemt, og så bliver de dyre:

| Område | Eksempel |
|--------|----------|
| **Performance** | 95 % af sidevisninger skal svare på under 2 sekunder ved 500 samtidige brugere |
| **Tilgængelighed** (*availability*) | Systemet skal være oppe 99,5 % af tiden i åbningstiden |
| **Sikkerhed** | Kun sagsbehandlere i den rette afdeling må se en ansøgning |
| **Webtilgængelighed** (*accessibility*) | Offentlige løsninger skal efter loven overholde **WCAG**, så f.eks. blinde kan bruge dem med skærmlæser |
| **Persondata/GDPR** | Ansøgninger slettes 5 år efter afgørelsen |
| **Logning og sporbarhed** | Det skal logges, hvem der har set et CPR-nummer |
| **Drift** | Systemet skal kunne overvåges, og backup skal kunne genskabes inden for 4 timer |

### Et godt krav kan testes

Som eksperimentalist ved du det allerede: En hypotese, man ikke kan teste, er ikke meget værd. Det samme gælder krav.

| Dårligt | Bedre |
|---------|-------|
| Systemet skal være hurtigt | Søgning returnerer resultater på under 1 sekund for 95 % af søgningerne |
| Det skal være brugervenligt | En ny sagsbehandler kan oprette en sag uden hjælp efter en introduktion på 30 minutter |
| Ansøgninger skal valideres | En ansøgning kan ikke indsendes, hvis ansøgt beløb er 0 eller over 200.000 kr. |
| Systemet skal håndtere fejl | Hvis CPR-registret ikke svarer inden 5 sekunder, får brugeren en besked om at prøve igen senere, og hændelsen logges |

Gode krav er **entydige** (kun én fortolkning), **testbare**, **nødvendige** og **sporbare** (man kan følge kravet til de stories og tests, der opfylder det).

### Øvelser B

1. Omskriv disse krav, så de bliver testbare. Skriv, hvilke spørgsmål du ville stille kunden for at kunne gøre det:
   - *"Systemet skal kunne håndtere mange ansøgninger."*
   - *"Borgeren skal have svar hurtigt."*
   - *"Data skal være sikre."*
   - *"Det skal være nemt at vedhæfte dokumenter."*
2. Find mindst fem ikke-funktionelle krav til tilskudssystemet fra dag 3.

---

## Del C: User stories og acceptkriterier (ca. 60 min)

### User stories

En **user story** beskriver et behov fra brugerens synsvinkel i én sætning:

> **Som** sagsbehandler
> **vil jeg** kunne se alle ansøgninger, der er tildelt mig, sorteret efter indsendelsesdato,
> **så** jeg behandler de ældste først og overholder fristerne.

Det vigtigste er **så**-delen. Den fortæller *hvorfor*, og det giver udviklerne mulighed for at foreslå en bedre løsning.

En user story er ikke en komplet specifikation. Den er *et løfte om en samtale*. Detaljerne bliver aftalt, når teamet **refiner** den, og de bliver skrevet ned som **acceptkriterier**.

### Acceptkriterier og Gherkin

Acceptkriterier beskriver præcist, hvornår historien er færdig. Et udbredt format er **Gherkin** (*Given/When/Then*), som mange teams også bruger på dansk som *Givet/Når/Så*:

```gherkin
Feature: Indsendelse af ansøgning om tilskud

  Scenario: Gyldig ansøgning bliver modtaget
    Given borgeren er logget ind og ejer boligen "Solvej 12"
    When borgeren indsender en ansøgning på 45.000 kr. med et tilbud vedhæftet
    Then får ansøgningen status "modtaget"
    And borgeren modtager en kvittering på e-mail

  Scenario: Ansøgning over maksimumbeløbet bliver afvist
    Given borgeren er logget ind og ejer boligen "Solvej 12"
    When borgeren indsender en ansøgning på 250.000 kr.
    Then bliver ansøgningen ikke indsendt
    And borgeren får beskeden "Du kan højst søge 200.000 kr."

  Scenario: Borgeren ejer ikke boligen
    Given borgeren er logget ind, men ejer ikke boligen "Solvej 12"
    When borgeren forsøger at søge til "Solvej 12"
    Then kan boligen ikke vælges
```

Hvert scenarie kan blive til en automatisk test, ligesom testene i `lab-java` på dag 4. Kig i `MaalingServiceTest`. Hver test har en *given*-del (opsætning), en *when*-del (kaldet) og en *then*-del (`assertEquals`). Der findes værktøjer (f.eks. *Cucumber*), der kører Gherkin-tekst direkte som tests.

Tænk som en tester, når du skriver acceptkriterier: **Hvad sker der på grænsen? Hvad hvis data mangler? Hvad hvis brugeren ikke har adgang?** Det er de scenarier, der bliver glemt.

### INVEST: en god story er ...

| | |
|---|---|
| **I**ndependent | kan laves uafhængigt af andre stories |
| **N**egotiable | detaljerne kan forhandles |
| **V**aluable | giver værdi for nogen |
| **E**stimable | teamet kan vurdere størrelsen |
| **S**mall | kan blive færdig inden for et sprint |
| **T**estable | har klare acceptkriterier |

### Hierarkiet

```
Epic        "Ansøgning om tilskud"                         (stort, flere sprints)
 └ Story    "Som borger vil jeg indsende en ansøgning ..."  (et sprint eller mindre)
    └ Task  "Lav endpoint POST /ansoegninger"               (teknisk delopgave)
Bug         "Kvittering sendes to gange ved dobbeltklik"    (fejl)
```

Er en story for stor, bliver den **splittet**. Det gøres helst efter brugerværdi (f.eks. "indsend uden dokumenter" og "vedhæft dokumenter"), ikke efter teknik ("frontend" og "backend").

### Estimering

Teams estimerer ofte i **story points**: en relativ størrelse (1, 2, 3, 5, 8, 13 …, Fibonacci-agtigt) og ikke i timer. *"Den her er cirka dobbelt så stor som den der."* Det foregår tit som **planning poker**, hvor alle viser deres bud på samme tid. Hvis buddene er langt fra hinanden, betyder det, at folk har forstået opgaven forskelligt, og det er værdifuld viden.

### Definition of Ready og Definition of Done

- **Definition of Ready (DoR)**: Hvornår er en story klar til at blive taget ind i et sprint? F.eks.: Den har acceptkriterier, afhængigheder er afklaret, og den er estimeret.
- **Definition of Done (DoD)**: Hvornår er den *færdig*? F.eks.: Koden er reviewet og merget, testene er grønne, den er deployet til testmiljøet, og PO har godkendt den.

"Færdig" uden en DoD betyder noget forskelligt for alle. Det er en klassisk kilde til konflikter.

### Øvelser C

3. Skriv 4–6 user stories til tilskudssystemet fra dag 3. Lav mindst én for borgeren, én for sagsbehandleren og én for en tredje rolle, som du selv finder på. Hvem har ellers interesse i systemet?
4. Skriv acceptkriterier i Gherkin til to af dem. Lav mindst ét scenarie for en fejl eller en grænseværdi til hver.
5. Skriv kravændringen fra dag 4, øvelse 7 (*"Tryk skal ligge mellem 870 og 1100 hPa"*), som Gherkin-scenarier. Sammenlign med de tests, du rettede. Dækker de det samme?
6. Epic'en *"Sagsbehandling"* er for stor. Split den i 4–6 stories efter brugerværdi.

---

## Del D: Scrum og Jira (ca. 45 min)

### Scrum

**Scrum** er den mest udbredte agile metode. Den har tre roller, fem begivenheder og tre artefakter:

**Roller**
- **Product Owner (PO)**: ejer backloggen og prioriterer. Bestemmer *hvad* og *i hvilken rækkefølge*. Det er ofte en person hos kunden, eller en analytiker hos leverandøren, der arbejder tæt sammen med kunden.
- **Scrum Master**: hjælper teamet med processen og fjerner forhindringer.
- **Developers**: alle, der laver arbejdet: udviklere, testere og analytikere.

**Begivenheder**
| | Hvad | Hvor tit |
|---|------|----------|
| **Sprint** | En fast periode (typisk 2 uger), hvor teamet laver det, det har lovet | Løbende |
| **Sprint planning** | Teamet vælger stories til sprintet og planlægger | Starten af sprintet |
| **Daily standup** (*daily scrum*) | 15 minutter: Hvad har jeg lavet, hvad laver jeg nu, og er jeg **blokeret**? | Hver dag |
| **Sprint review / demo** | Teamet viser kunden, hvad der er lavet | Slutningen af sprintet |
| **Retrospektiv** (*retro*) | Teamet ser på sit eget samarbejde: Hvad gik godt, og hvad skal vi gøre anderledes? | Slutningen af sprintet |

Dertil kommer **refinement** (*backlog grooming*): løbende møder, hvor kommende stories bliver gennemgået, afklaret og estimeret. Her har analytikeren en hovedrolle.

**Artefakter**
- **Product backlog**: en prioriteret liste over alt, der skal laves.
- **Sprint backlog**: det, teamet har valgt til det aktuelle sprint.
- **Increment**: det, der er færdigt (efter DoD) ved slutningen af sprintet.

**Andre ord du vil høre:**
- **Velocity**: hvor mange story points teamet typisk når pr. sprint.
- **Kanban**: en anden metode uden sprints, hvor man trækker opgaver ind løbende og begrænser antallet af igangværende opgaver (*WIP limit*). Den bruges ofte i drift og support.
- **SAFe**: en ramme for at koordinere mange teams i store organisationer, med f.eks. *PI planning* hvert kvartal.

### Sådan siger du noget til standup

Kort og konkret:

> *"I går blev jeg færdig med acceptkriterierne til TILSKUD-142 og fik dem reviewet af Mads. I dag tager jeg TILSKUD-150 om dokumentupload. Jeg er blokeret på 147, fordi vi mangler svar fra kunden om, hvilke filtyper der er tilladt. Jeg har skrevet til Ida."*

Det er helt i orden at sige *"jeg sidder fast og har brug for en halv time med en af jer bagefter"*. Problemer løser man efter standup, ikke under.

### Jira

**Jira** (fra Atlassian) er det mest udbredte værktøj til at styre opgaver. Andre er **Azure DevOps Boards** og **GitHub Projects**. Begreberne er de samme:

- **Issue** (sag): en story, task, bug eller epic med et **nøglenummer** som `TILSKUD-142`. Nummeret skriver man i branch-navne og commit-beskeder (dag 1), så kode og sag hænger sammen.
- **Workflow / statusser**: f.eks. *To Do → In Progress → In Review → In Test → Done*.
- **Board**: en tavle med en kolonne pr. status.
- **Assignee / reporter**: hvem sagen er tildelt / hvem der har oprettet den.
- **Components, labels, fix version**: kategorier og hvilken release sagen kommer med i.
- **Links**: *blocks / is blocked by*, *relates to*, *duplicates*.

Jira har et søgesprog, **JQL**, som minder om `WHERE` i SQL fra dag 3:

```
project = TILSKUD AND status = "In Progress" AND assignee = currentUser()
project = TILSKUD AND type = Bug AND priority in (High, Highest) ORDER BY created DESC
project = TILSKUD AND sprint in openSprints() AND status != Done
```

Dokumentation ligger typisk i **Confluence** (Atlassians wiki) ved siden af Jira.

### Øvelser D

7. **Lav en backlog på GitHub.** Opret dine user stories fra øvelse 3 som **Issues** i repoet SofiesITlearning, med acceptkriterierne i beskrivelsen. Lav et **GitHub Project** (skabelonen *Board*) under din egen konto, og læg dine issues på det. Flyt dem rundt mellem *Todo*, *In Progress* og *Done*. Begreberne er de samme som i Jira.
8. **Skriv JQL** (på papir) til: alle bugs i projektet TILSKUD, der ikke er lukket. Alle sager i det aktuelle sprint, der er tildelt dig. Alle stories uden story points.
9. **Standup.** Skriv, hvad du ville sige til standup i morgen om dit arbejde med det her forløb. Højst 4 sætninger.

---

## Del E: Test (ca. 45 min)

### Testniveauer

| Niveau | Hvad testes | Hvem | Eksempel |
|--------|-------------|------|----------|
| **Unit test** | Én klasse eller funktion isoleret | Udvikler, automatisk | `MaalingServiceTest` fra dag 4 |
| **Integrationstest** | Flere dele sammen, f.eks. kode + database eller to systemer | Udvikler/tester, ofte automatisk | API'et fra dag 3 med rigtig SQLite |
| **Systemtest / end-to-end** | Hele systemet, som en bruger oplever det | Tester, manuelt eller automatisk (f.eks. *Playwright*, *Selenium*) | "Borger logger ind, søger og får kvittering" |
| **Accepttest / UAT** | Opfylder det kundens behov og kontrakten? | Kunden og forretningen | Overtagelsesprøven |
| **Regressionstest** | Virker det gamle stadig efter en ændring? | Alle, så automatisk som muligt | Hele testsuiten ved hver PR |

### Testpyramiden

```
        /\          få:   end-to-end   (langsomme, skrøbelige, dyre)
       /  \
      /----\        nogle: integration
     /      \
    /--------\      mange: unit tests  (hurtige, stabile, billige)
```

Man vil have mange hurtige unit tests og få langsomme end-to-end-tests. Et projekt med det omvendte (manuel klik-test af alt før hver release) er langsomt og dyrt at ændre.

### En god fejlrapport

Når du finder en fejl, er en god fejlrapport guld værd for udvikleren. En dårlig koster en halv dags gætteri.

```
Titel:        POST /maalinger med en JSON-værdi, der ikke er et objekt, giver tomt svar
Miljø:        Lokalt, server.py fra dag 2 (commit abc1234), Python 3.12, macOS
Trin:         1. Start server.py
              2. curl -i -X POST http://127.0.0.1:8000/maalinger -H "Content-Type: application/json" -d '5'
Forventet:    400 Bad Request med en fejlbesked i JSON, som ved ugyldig JSON
Faktisk:      curl: (52) Empty reply from server. Ingen statuskode.
Log:          TypeError: argument of type 'int' is not iterable  (server.py, linje 61, do_POST)
Alvor:        Mellem: serveren kører videre, men klienten får intet svar
Bilag:        Hele stack trace fra serverens log
```

Elementerne er titel, miljø/version, trin til at genskabe fejlen, **forventet** og **faktisk** resultat, log eller skærmbillede, og alvor.

Man skelner mellem **severity** (hvor alvorlig er fejlen teknisk?) og **priority** (hvor vigtigt er det at rette den nu?). En stavefejl på forsiden har lav severity, men måske høj priority.

### Øvelser E

10. Fejlen i eksemplet ovenfor findes faktisk. Genskab den på den *oprindelige* `server.py` fra dag 2, ikke din rettede version. Find den i Git-historikken:
    ```bash
    git log --oneline -- 02-system-og-api/server.py     # det nederste commit er det første
    git show <hash>:02-system-og-api/server.py > /tmp/server_original.py
    python3 /tmp/server_original.py
    ```
    Findes fejlen også i din egen version fra dag 2, øvelse 4?
11. Find selv en anden fejl i `server.py` eller `app.py` fra dag 2, og skriv en fejlrapport som et **GitHub Issue** med labelen `bug`. *Idéer:* Hvad sker der med meget store tal, negative tryk, en tom body eller forkert `Content-Type`?
12. For kravet *"En ansøgning kan ikke indsendes, hvis ansøgt beløb er 0 eller over 200.000 kr."*: Hvilke testværdier vil du bruge? Begrund hver værdi. *Hint:* grænseværdier, ækvivalensklasser og "mærkelige" input.

---

## Del F: Miljøer og vejen til produktion (ca. 20 min)

Koden går ikke direkte fra udviklerens computer til borgerne. Den passerer en række **miljøer**:

```
 Udviklerens   PR +       ┌──────┐     ┌──────┐     ┌──────────────┐     ┌──────┐
 maskine  ──► pipeline ──► │ DEV  │ ──► │ TEST │ ──► │ PREPROD /    │ ──► │ PROD │
               (CI)        └──────┘     └──────┘     │ STAGING      │     └──────┘
                           løbende      testere      │ som prod,    │     borgerne
                                        og PO         │ UAT, perf.   │
                                                      └──────────────┘
```

- **CI** (*continuous integration*): Ved hver PR bygger en **pipeline** koden og kører alle tests automatisk. Rødt betyder, at PR'en ikke kan merges. Det er det, du så med `./mvnw test` på dag 4, bare automatisk.
- **CD** (*continuous delivery/deployment*): Efter merge bliver den nye version automatisk **deployet** til DEV og evt. TEST.
- **Release**: en samlet version, der går i produktion, ofte med **release notes**, der beskriver, hvad der er nyt. I det offentlige sker det tit på aftalte tidspunkter, f.eks. hver måned, og med godkendelse fra kunden (*change management*).
- **Hotfix**: en hurtig rettelse af en kritisk fejl i produktion, uden om den normale releaseplan.
- **Feature toggle / feature flag**: Ny funktionalitet ligger i koden, men er slået fra, indtil den skal bruges.
- **Testdata**: Hvert miljø har sine egne data. Produktionsdata (med rigtige CPR-numre) må ikke kopieres til test uden videre (dag 3, anonymisering).

### Når noget går galt i produktion

- **Incident**: en hændelse, hvor systemet ikke virker som det skal.
- **Support-niveauer**: *1st line* (kundens servicedesk tager imod henvendelsen), *2nd line* (driften eller applikationsfolk undersøger), *3rd line* (udviklerne retter koden).
- **SLA** (*service level agreement*): aftalte svartider. F.eks. skal en kritisk fejl være i gang med at blive løst inden 1 time.
- **Postmortem / RCA** (*root cause analysis*): Hvad skete der, hvorfor, og hvordan undgår vi det igen? Uden at finde syndebukke.

### Sporbarhed: hele kæden

```
 Krav K-17  ──►  Story TILSKUD-142  ──►  Branch feature/TILSKUD-142  ──►  PR #87
   ──►  Tests (grønne)  ──►  Release 2.4  ──►  Overtagelsesprøve: K-17 godkendt
```

Den kæde er det, analytikeren holder styr på. Når kunden spørger *"er krav 17 opfyldt?"*, skal man kunne svare *ja, og her er beviset*.

---

## Aflevering

Lav en branch `opgaver/dag-5`, og aflevér via PR:
- `noter/dag-5.md` med øvelse 1, 2, 4, 5, 6, 8, 9, 10 og 12
- dine user stories som Issues (øvelse 3 og 7) og din fejlrapport (øvelse 11). Link til dem fra `noter/dag-5.md`

## Spørg Claude

- *"Her er min user story og mine acceptkriterier. Hvilke scenarier har jeg glemt? Stil spørgsmål, giv mig ikke svarene."*
- *"Spil kunden i en workshop om tilskudssystemet. Jeg stiller spørgsmål for at afklare kravene. Svar som en travl kontorchef, der ikke kender IT."*
- *"Er det her en fejl eller en ændring?"* (Beskriv en situation.)
- *"Forklar forskellen på severity og priority med tre eksempler."*
- *"Hvad er forskellen på integrationstest og end-to-end-test?"*

Rollespillet med kontorchefen (den anden prompt) er godt at bruge flere gange. Det er sådan, du træner workshops, før du skal holde en rigtig.

## Tjekliste: kan du...

- [ ] beskrive faserne i et offentligt IT-projekt fra udbud til drift?
- [ ] forklare forskellen på funktionelle og ikke-funktionelle krav, og give eksempler?
- [ ] omskrive et vagt krav til et testbart?
- [ ] skrive en user story med acceptkriterier i Gherkin?
- [ ] forklare Scrums roller, begivenheder og artefakter?
- [ ] forklare forskellen på Definition of Ready og Definition of Done?
- [ ] nævne testniveauerne og forklare testpyramiden?
- [ ] skrive en god fejlrapport?
- [ ] forklare vejen fra commit til produktion gennem miljøerne?

## Ordliste

| Ord | Betydning |
|-----|-----------|
| **udbud / tilbud** | Kundens offentlige indkøb / leverandørens bud |
| **kravspecifikation** | Kundens nummererede krav. Ofte et bilag til kontrakten |
| **change request (CR)** | En ændring i forhold til det aftalte, som skal estimeres og godkendes |
| **overtagelsesprøve / UAT** | Kundens test af, om leverancen kan godkendes |
| **vandfald / agilt / hybrid** | Faser efter hinanden / små leverancer med løbende feedback / en blanding |
| **funktionelt / ikke-funktionelt krav** | Hvad systemet gør / hvor godt (performance, sikkerhed, oppetid …) |
| **WCAG / webtilgængelighed** | Standarden for tilgængelige websider. Lovkrav for offentlige løsninger |
| **sporbarhed** | At kunne følge et krav til story, kode, test og release |
| **user story** | "Som … vil jeg … så …" |
| **acceptkriterier** | Præcise betingelser for, at en story er færdig |
| **Gherkin / Given-When-Then** | Formatet for acceptkriterier som scenarier |
| **INVEST** | Kendetegn ved en god story |
| **epic / story / task / bug** | Stort / brugerværdi / teknisk delopgave / fejl |
| **splitte en story** | At dele en for stor story op efter brugerværdi |
| **story points / planning poker** | Relativ estimering / estimering, hvor alle viser bud på samme tid |
| **DoR / DoD** | Definition of Ready / Definition of Done |
| **Scrum** | Agil metode med sprints, roller og faste møder |
| **Product Owner / Scrum Master** | Prioriterer backloggen / hjælper teamet med processen |
| **sprint / sprint planning / review / retro** | Periode / planlægning / demo for kunden / forbedring af samarbejdet |
| **daily standup** | Dagligt 15-minutters møde |
| **refinement / grooming** | Afklaring og estimering af kommende stories |
| **backlog** | Prioriteret liste over arbejde |
| **blokeret** | Kan ikke komme videre på grund af noget udenfor ens kontrol |
| **velocity** | Antal story points pr. sprint |
| **Kanban / WIP limit** | Flow uden sprints / et loft over igangværende opgaver |
| **SAFe / PI planning** | Agilt for mange teams / fælles planlægning hvert kvartal |
| **Jira / Confluence** | Opgavestyring / wiki (Atlassian) |
| **issue key** | Sagsnummer som `TILSKUD-142` |
| **JQL** | Jiras søgesprog |
| **unit- / integrations- / system- / accepttest** | Testniveauerne |
| **end-to-end-test (E2E)** | Test af hele systemet som en bruger |
| **regressionstest** | Test af, at det gamle stadig virker |
| **testpyramiden** | Mange unit tests, få end-to-end-tests |
| **grænseværdi / ækvivalensklasse** | Værdien på kanten / en gruppe input, der bør opføre sig ens |
| **fejlrapport / bug report** | Trin, forventet, faktisk, miljø, log |
| **severity / priority** | Teknisk alvor / hvor hurtigt den skal rettes |
| **miljø: DEV / TEST / PREPROD / PROD** | Stederne, koden kører, på vej mod borgerne |
| **CI / CD / pipeline** | Automatisk build og test / automatisk deploy / den automatiserede kæde |
| **release / release notes** | En samlet version / beskrivelse af, hvad der er nyt |
| **hotfix** | En hurtig rettelse i produktion |
| **feature toggle** | Funktionalitet, der kan slås til og fra |
| **change management** | Den formelle godkendelse af ændringer i produktion |
| **incident / postmortem / RCA** | Hændelse i produktion / efterfølgende analyse af årsagen |
| **1st / 2nd / 3rd line support** | Servicedesk / drift og applikation / udviklerne |
| **SLA** | Aftalte svartider og oppetider |
