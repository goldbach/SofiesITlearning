# Dag 4: At læse kode i Java og C#

*Ca. 3 timer for kernen. **Kerne:** del A–C. **Fordybelse:** del D–F. Læs dem gerne, hvis du har tid. D og F får du brug for, når du skal finde forretningsregler i et rigtigt system, og E, hvis dit projekt bruger C#.*

## Hvorfor?

De store forretningssystemer, Netcompany bygger, er typisk skrevet i **Java** eller **C#**. Som analytiker skal du ikke skrive dem, men du skal kunne:

- **læse** koden for at finde ud af, hvad systemet *faktisk* gør, når dokumentationen er forældet. Den er næsten altid forældet.
- **finde forretningsreglerne** i koden og sammenligne dem med kravene
- **forstå udviklerne**, når de siger "det fejler i servicelaget", "testen er rød" eller "den skal lige igennem buildet"

I dag ser du først, hvordan kode bliver til et kørende program, og hvorfor Java er så anderledes end Python. Derefter læser du, bygger og retter et lille Java-projekt.

## Videoer og interaktivt materiale

| Hvornår | Hvad | Længde |
|---------|------|--------|
| **Før du starter** | [Java in 100 Seconds](https://www.youtube.com/watch?v=l9AzO1FMgM8) (Fireship) | 2 min |
| **Før del E** | [C# in 100 Seconds](https://www.youtube.com/watch?v=ravLFzIguCM) (Fireship) | 2 min |
| **Opslag** | [dev.java/learn](https://dev.java/learn/): den officielle Java-tutorial | – |
| **Opslag** | [A tour of C#](https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/) (Microsoft Learn) | – |
| **Til fordybelse** | [Spring Guide: Building a RESTful Web Service](https://spring.io/guides/gs/rest-service): et rigtigt Spring Boot-API på 15 minutter | 15–30 min |

## Installation

Du skal bruge en **JDK** (*Java Development Kit*), som indeholder compileren og JVM'en. Vi bruger Temurin 25, som er en gratis og udbredt udgave af den seneste **LTS**-version (*long-term support*):

```bash
brew install --cask temurin@25    # beder om dit Mac-password
java -version
javac -version
```

Siger terminalen `command not found: brew`, har du sprunget Homebrew over. Se [dag 0, afsnit 4](../00-opsaetning/README.md#4-homebrew-og-github-cli). Du kan også hente installationsprogrammet direkte fra [adoptium.net](https://adoptium.net/temurin/releases/?version=25&os=mac). Vælg **macOS**, **aarch64** og **.pkg**, og dobbeltklik på filen.

`clang` (C-compileren) har du allerede. Den kom med *Command Line Developer Tools* på dag 0. Tjek med `clang --version`.

**Valgfrit:** `brew install go`, hvis du vil prøve Go i del A.

---

## Del A: Fra kildekode til kørende program (ca. 60 min)

En computers processor forstår kun **maskinkode**: binære instruktioner, der er specifikke for netop den type processor. Din Mac har en ARM-processor (Apple Silicon), og de fleste servere har Intel/AMD (x86). Kode skrevet af mennesker skal oversættes til maskinkode. Der er tre måder at gøre det på:

```
 Fortolket (Python)
   kildekode ──► fortolker læser og udfører linje for linje, hver gang programmet kører

 Kompileret til maskinkode (C, Go, Rust)
   kildekode ──► compiler ──► maskinkode (.exe / binær fil) ──► kører direkte på processoren
                 (én gang)     (kun til én processortype + OS)

 Kompileret til bytecode + JIT (Java, C#)
   kildekode ──► compiler ──► bytecode (.class / .dll) ──► virtuel maskine (JVM / .NET CLR)
                 (én gang)     (kører alle steder)          fortolker først, og JIT-kompilerer
                                                            de "varme" dele til maskinkode
                                                            mens programmet kører
```

### Eksperiment 1: Hvor hurtigt?

I mappen [`sammenligning/`](sammenligning/) ligger det samme program i fire sprog. Det lægger `i % 7` sammen for 100 millioner tal og måler tiden. Læs dem først, så du kan se, at de gør det samme.

```bash
cd ~/kursus/SofiesITlearning/04-kode-java-csharp/sammenligning

python3 sum.py                          # fortolket

clang -O2 sum.c -o sum_c                # kompilér C til maskinkode
./sum_c                                 # kør maskinkoden direkte

javac Sum.java                          # kompilér Java til bytecode -> Sum.class
java Sum                                # JVM'en kører bytecoden

go build -o sum_go sum.go && ./sum_go   # valgfrit: Go
```

Skriv tiderne ned. Som fysiker ved du, at én måling ikke er nok, så kør hver af dem 3 gange. Du vil se noget i retning af:

| Sprog | Model | Tid (ca.) |
|-------|-------|-----------|
| Python | fortolket | ~5 s |
| C | maskinkode | ~0,05–0,1 s |
| Go | maskinkode | ~0,1 s |
| Java | bytecode + JIT | ~0,05 s |

Python er **50–100 gange langsommere** i en løkke. Derfor er `numpy` og `pandas` skrevet i C bagved: Når du skriver `df.sum()`, kører løkken i C og ikke i Python.

Java er på niveau med C. JIT-compileren opdager, at løkken er "varm", og oversætter den til optimeret maskinkode, mens programmet kører.

### Eksperiment 2: Kig på mellemformen

Python og Java oversætter begge til **bytecode**, altså instruktioner til en virtuel maskine i stedet for til processoren:

```bash
python3 -c "import dis; dis.dis('total += i % 7')"    # Pythons bytecode
javap -c Sum                                          # Javas bytecode i Sum.class
file sum_c                                            # maskinkode til én processortype
```

Forskellen er, at Python gør det skjult, hver gang du kører, og fortolker bytecoden. Java gør det én gang i forvejen (`javac`), og JVM'en JIT-kompilerer den. Den mappe `__pycache__`, du har set, indeholder Pythons gemte bytecode.

`file sum_c` viser `Mach-O 64-bit executable arm64`. Den fil kan **kun** køre på en Mac med ARM-processor. `Sum.class` kan køre på enhver maskine med en JVM, uanset om det er Windows, Linux, ARM eller x86: *"write once, run anywhere"*.

> **Go (valgfrit):** Go kan kompilere til andre platforme med én kommando:
> `GOOS=windows GOARCH=amd64 go build -o sum.exe sum.go && file sum.exe`

### Eksperiment 3: Hvornår bliver fejlen fundet?

Kør begge programmer:

```bash
python3 typefejl.py
javac Typefejl.java
```

- **Python** starter, regner det første gennemsnit og fejler *først, når den kommer til linjen med fejlen*. I et stort system kan det være en linje, der kun køres den sidste dag i måneden, i produktion.
- **Java** nægter at oversætte programmet: `incompatible types: String cannot be converted to List<Double>`. Fejlen bliver fundet, *før* programmet overhovedet kører.

Det er forskellen på **dynamisk typning** (Python: typer bliver tjekket, mens programmet kører) og **statisk typning** (Java, C#, Go, C: typer bliver tjekket af compileren). I store systemer med mange udviklere, som lever i 20 år, er statisk typning en kæmpe fordel. Det er en af hovedgrundene til, at enterprise-systemer er skrevet i Java og C#.

### Sammenfatning

| | Python | C / Go | Java / C# |
|---|--------|--------|-----------|
| Oversættelse | Fortolket (skjult bytecode) | Compiler → maskinkode | Compiler → bytecode, JIT ved kørsel |
| Typer | Dynamiske | Statiske | Statiske |
| Hastighed | Langsom (men numpy er C) | Meget hurtig | Meget hurtig, efter opvarmning |
| Opstart | Hurtig | Øjeblikkelig | Langsommere: JVM'en skal starte og "varme op" |
| Kører på | Hvor Python er installeret | Kun den platform, der er kompileret til | Hvor der er en JVM / .NET |
| Hukommelse | Automatisk | C: manuel. Go: automatisk | Automatisk (*garbage collector*) |
| Typisk brug | Data, scripts, ML, automatisering | Styresystemer, værktøjer, cloud-infrastruktur (Docker og Kubernetes er skrevet i Go) | Store forretningssystemer, backend |

> **Garbage collection:** I C skal programmøren selv frigive hukommelse. Glemmer man det, *lækker* programmet. I Java, C#, Go og Python rydder en **garbage collector** automatisk op efter objekter, der ikke længere bruges.

---

## Del B: Læs Java (ca. 60 min)

Åbn projektet i VS Code:

```bash
cd ~/kursus/SofiesITlearning/04-kode-java-csharp/lab-java
code .
```

VS Code tilbyder at installere *Extension Pack for Java*. Sig ja. Så får du farver, fejlmarkering og **Go to Definition** (`F12` eller `Cmd`-klik), som er det vigtigste værktøj, når man læser kode.

Start med [`MaalingService.java`](lab-java/src/main/java/dk/eksempel/lab/MaalingService.java). Her er dens dele:

```java
package dk.eksempel.lab;                      // hvilken "mappe" klassen hører til

import java.util.List;                         // ligesom Pythons import

public class MaalingService {                  // en klasse: data + funktioner, der hører sammen

    static final double MAX_TEMPERATUR = 150;  // konstant: static = hører til klassen, final = kan ikke ændres

    private final MaalingRepository repository;    // felt: type først, så navn. private = kun synlig i klassen

    public MaalingService(MaalingRepository repository) {   // constructor, svarer til __init__
        this.repository = repository;                       // this svarer til self
    }

    public Maaling registrer(long forsoegId, double temperatur, double tryk) {
    //     ^ returtype       ^ hver parameter har en type
        if (temperatur < MIN_TEMPERATUR || temperatur > MAX_TEMPERATUR) {   // || = or, && = and
            throw new UgyldigMaalingException("...");       // throw = raise
        }
        ...
    }
}
```

### Python → Java

| Python | Java |
|--------|------|
| `x = 5` | `int x = 5;` eller `var x = 5;` |
| `def f(a, b):` | `int f(int a, int b) {` |
| indrykning bestemmer blokke | `{ }` bestemmer blokke, og `;` afslutter sætninger |
| `self` | `this` |
| `__init__` | constructor med klassens navn |
| `None` | `null` |
| `True` / `and` / `or` / `not` | `true` / `&&` / `\|\|` / `!` |
| `list`, `dict` | `List<Maaling>`, `Map<Long, Maaling>` (typen i `< >` kaldes *generics*) |
| `raise` / `try: ... except:` | `throw` / `try { } catch (...) { }` |
| `@dataclass(frozen=True)` | `record` |
| `_privat` (konvention) | `private` (håndhæves af compileren) |
| `# kommentar` / `"""docstring"""` | `// kommentar` / `/** Javadoc */` |
| `[m for m in liste if m.t > 25]` | `liste.stream().filter(m -> m.t() > 25).toList()` |
| `lambda m: m.t` | `m -> m.t()` eller `Maaling::temperatur` |

### Interfaces: kontrakter i koden

Åbn [`MaalingRepository.java`](lab-java/src/main/java/dk/eksempel/lab/MaalingRepository.java). Et **interface** siger *hvad* der kan gøres (`gem`, `findForForsoeg`), men ikke *hvordan*. [`InMemMaalingRepository`](lab-java/src/main/java/dk/eksempel/lab/InMemMaalingRepository.java) er én **implementering**, der gemmer i hukommelsen. I et rigtigt system ville der også være en, der gemmer i en database.

`MaalingService` kender kun interfacet. Derfor kan man skifte databasen ud, eller bruge den hurtige udgave i hukommelsen i tests, uden at ændre en linje i forretningsreglerne. Det er samme idé som API-kontrakten fra dag 2, bare inde i koden.

### Streams: pandas-agtig databehandling

```java
return repository.findForForsoeg(forsoegId).stream()
        .filter(m -> m.temperatur() > graense)
        .toList();
```

Læs det som en pandas-kæde: Tag målingerne, filtrér dem, hvor temperaturen er over grænsen, og lav en liste. `m -> ...` er en **lambda**, altså en lille funktion uden navn.

### Øvelser B

1. Læs alle filerne i `src/main/java`. Hvilken fil indeholder forretningsreglerne? Hvilke regler står der i Javadoc-kommentaren?
2. Hvad sker der, hvis man kalder `registrer(1, 200, 1000)`? Følg koden linje for linje.
3. Hvad betyder `OptionalDouble` i `gennemsnitTemperatur`? Hvorfor returnerer metoden ikke bare `double`? *Hint:* Hvad er gennemsnittet af nul målinger?
4. Se på `naesteId()` i `InMemMaalingRepository`. Den virker i dag. Hvad ville gå galt, hvis man senere tilføjede sletning af målinger? Det er den slags spørgsmål, man stiller i et **code review**.

---

## Del C: Byg, test og ret (ca. 60 min)

### Projektstruktur

```
lab-java/
├── pom.xml                  ← projektbeskrivelse og dependencies (svarer til requirements.txt)
├── mvnw                     ← Maven Wrapper: henter selv den rigtige Maven-version
├── src/main/java/dk/eksempel/lab/   ← koden. Mapperne følger package-navnet
└── src/test/java/dk/eksempel/lab/   ← testene, i samme package
```

Det er **Maven**-standarden, som næsten alle Java-projekter følger. Det andet store byggeværktøj er **Gradle** (`build.gradle`). Kig i `pom.xml`: `junit-jupiter` er en dependency med `<scope>test</scope>`. Den bliver kun brugt til tests og kommer ikke med i det færdige program.

### Byg og kør testene

```bash
./mvnw test
```

Første gang henter Maven sig selv og alle dependencies fra internettet (*Maven Central*). Det tager et minut. Til sidst:

```
[ERROR] Tests run: 12, Failures: 0, Errors: 1, Skipped: 0
[ERROR]   MaalingServiceTest.graensevaerdierErGyldige:37 » UgyldigMaaling Tryk uden for gyldigt interval: 1100.0
[INFO] BUILD FAILURE
```

Testen er **rød**. Det er med vilje.

### Øvelser C

5. **Læs fejlen.** Hvilken test fejler, med hvilke værdier, og hvad siger fejlbeskeden? Åbn [`MaalingServiceTest.java`](lab-java/src/test/java/dk/eksempel/lab/MaalingServiceTest.java), og find testen. Hvad forventer den?
6. **Find fejlen.** Sammenlign koden i `MaalingService.registrer` med reglerne i Javadoc-kommentaren øverst i filen. Hvem har ret, testen eller koden? Ret fejlen, og kør `./mvnw test` igen, indtil du ser `BUILD SUCCESS`.

   Det er en klassisk **grænseværdifejl** (*off-by-one*): `>=` i stedet for `>`. Den slags fejl finder testere og analytikere, fordi de spørger: *"Hvad sker der præcis på grænsen?"*
7. **Kravændring, test først.** Laboratoriet har fået et nyt barometer og ændrer kravet: *"Tryk skal ligge mellem 870 og 1100 hPa."*
   1. Ret **først** testene i `MaalingServiceTest`, så de beskriver det nye krav. Kør dem, og se dem fejle.
   2. Ret derefter koden, så testene bliver grønne.

   Det hedder **TDD** (*test-driven development*). Testen er en kørbar udgave af kravet. Som analytiker vil du ofte skrive acceptkriterierne, som testene bliver bygget på. Mere om det på dag 5.
8. **Byg og kør programmet.**
   ```bash
   ./mvnw package          # kompilér, test og pak i en .jar-fil
   ls target/
   java -jar target/lab-java-1.0.jar
   ```
   En **jar**-fil er en zip-fil med alle `.class`-filerne. Det er den, man **deployer** til en server. Se indholdet med `unzip -l target/lab-java-1.0.jar`.

Maven-livscyklussen kører altid i rækkefølge: `compile` → `test` → `package`. Fejler testene, bliver der ikke lavet nogen jar. Sådan forhindrer man, at fejl kommer i produktion. På dag 5 og 6 ser du, hvordan en **pipeline** gør det samme automatisk ved hver pull request.

---

## Del D: Sådan ser et rigtigt system ud (ca. 30 min, fordybelse)

### Lagdeling

Næsten alle Java- og C#-backends er bygget i lag:

```
  HTTP-request
       │
  ┌────▼─────────┐
  │  Controller  │  modtager HTTP, oversætter til/fra JSON   (dag 2)
  └────┬─────────┘
  ┌────▼─────────┐
  │   Service    │  forretningsreglerne                       ← her skal analytikeren kigge
  └────┬─────────┘
  ┌────▼─────────┐
  │  Repository  │  henter og gemmer data                     (dag 3)
  └────┬─────────┘
       ▼
   Database
```

`lab-java` har service- og repository-laget. `Main` spiller controllerens rolle.

### Spring Boot

**Spring Boot** er det mest udbredte Java-framework. En controller ser sådan ud. Sammenlign med `app.py` fra dag 2:

```java
@RestController
@RequestMapping("/maalinger")
public class MaalingController {

    private final MaalingService service;

    public MaalingController(MaalingService service) {    // Spring sætter servicen ind automatisk
        this.service = service;
    }

    @GetMapping("/{id}")                                  // FastAPI: @app.get("/maalinger/{id}")
    public Maaling hentEn(@PathVariable long id) {
        return service.hent(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    }

    @PostMapping                                          // FastAPI: @app.post("/maalinger", status_code=201)
    @ResponseStatus(HttpStatus.CREATED)
    public Maaling opret(@RequestBody @Valid NyMaaling ny) {
        return service.registrer(ny.forsoegId(), ny.temperatur(), ny.tryk());
    }
}
```

Og en database-tabel fra dag 3, som den ser ud med **JPA/Hibernate** (Javas ORM):

```java
@Entity
@Table(name = "maaling")
public class MaalingEntity {

    @Id
    @GeneratedValue
    private Long id;                       // PRIMARY KEY

    @ManyToOne                             // mange målinger -> ét forsøg (1:N)
    @JoinColumn(name = "forsoeg_id")       // FOREIGN KEY
    private ForsoegEntity forsoeg;

    private Double temperatur;             // Double (ikke double) kan være null
    private Double tryk;
}
```

Det er kun eksempler til at læse. De er ikke en del af `lab-java`.

Ordene med `@` hedder **annotationer**. De er metadata, som frameworket læser og handler på. `@GetMapping` får Spring til at koble en URL til metoden, og `@Entity` får Hibernate til at koble klassen til en tabel. Når du læser enterprise-kode, fortæller annotationerne dig, hvad en klasse *er*.

### Dependency injection

Læg mærke til, at `MaalingService` ikke selv laver sit repository. Det får det med i constructoren. Det hedder **dependency injection** (DI). I Spring sørger frameworket for at "sprøjte" de rigtige objekter ind. Det er derfor, testene kan give servicen et `InMemMaalingRepository`, mens produktionen giver den et, der taler med databasen.

---

## Del E: C# for Java-læsere (ca. 20 min, fordybelse)

C# og Java ligner hinanden så meget, at kan du læse det ene, kan du næsten læse det andet:

| Java | C# |
|------|-----|
| `package dk.eksempel.lab;` | `namespace Dk.Eksempel.Lab;` |
| `import java.util.List;` | `using System.Collections.Generic;` |
| `metodeNavn()` (camelCase) | `MetodeNavn()` (PascalCase) |
| `interface MaalingRepository` | `interface IMaalingRepository` (konvention: `I` foran) |
| `class X implements Y` / `extends Z` | `class X : Y` |
| `stream().filter(...).toList()` | LINQ: `.Where(...).ToList()` |
| getters/setters | properties: `public double Tryk { get; set; }` |
| `@GetMapping` (annotation) | `[HttpGet]` (attribute) |
| JVM, bytecode i `.class` / `.jar` | .NET CLR, IL i `.dll` |
| Maven/Gradle, `pom.xml` | NuGet, `.csproj`, `dotnet build` |
| Spring Boot | ASP.NET Core |
| JPA/Hibernate | Entity Framework |
| JUnit | xUnit / NUnit / MSTest |

`MaalingService` i C#:

```csharp
public record Maaling(long Id, long ForsoegId, double Temperatur, double Tryk);

public class MaalingService
{
    private readonly IMaalingRepository _repository;

    public MaalingService(IMaalingRepository repository)
    {
        _repository = repository;
    }

    public Maaling Registrer(long forsoegId, double temperatur, double tryk)
    {
        if (temperatur < -50 || temperatur > 150)
            throw new ArgumentOutOfRangeException(nameof(temperatur));
        var maaling = new Maaling(_repository.NaesteId(), forsoegId, temperatur, tryk);
        return _repository.Gem(maaling);
    }

    public List<Maaling> VarmeMaalinger(long forsoegId, double graense) =>
        _repository.FindForForsoeg(forsoegId)
            .Where(m => m.Temperatur > graense)
            .ToList();
}
```

---

## Del F: Sådan læser du en ukendt kodebase (ca. 15 min, fordybelse)

På dit første projekt vil der være hundredtusindvis af linjer kode. Du skal ikke læse dem alle. Sådan finder du rundt:

1. **Start med `README.md`** og byggefilen (`pom.xml` / `.csproj`). Hvilke frameworks og dependencies er der?
2. **Find indgangene:** controllere (`@RestController`, `[ApiController]`), beskedmodtagere og planlagte jobs. Hvad kan systemet blive bedt om?
3. **Følg ét flow fra ende til anden:** controller → service → repository. Brug *Go to Definition* (`F12`).
4. **Søg** efter domæneord fra kravene, f.eks. "bevilling" eller "frist", med `Cmd-Shift-F` i VS Code.
5. **Læs testene.** De er ofte den bedste dokumentation af, hvad koden *skal* gøre.
6. **Brug Git-historikken:** `git log -p <fil>` og `git blame <fil>` viser, hvem der har ændret hvad og hvorfor. Commit-beskeden nævner ofte Jira-sagen.
7. **Spørg.** Udviklerne forklarer gerne. Og hvis projektet har godkendt et AI-værktøj, så bed det forklare koden (se dag 1b).

---

## Aflevering

Lav en branch `opgaver/dag-4`, og aflevér via PR:
- `noter/dag-4.md` med tiderne fra eksperiment 1, dine observationer fra eksperiment 2 og 3, og svar på øvelse 1–5
- dine rettelser i `MaalingService.java` og `MaalingServiceTest.java` (øvelse 6 og 7)

Kompilerede filer (`sum_c`, `*.class`, `target/`) skal ikke med. De står i `.gitignore`.

## Spørg Claude

- *"Forklar JIT-kompilering med en analogi fra laboratoriet."*
- *"Hvorfor er Java hurtigere end Python, når begge bruger bytecode?"*
- *"Forklar linje for linje, hvad `gennemsnitTemperatur` gør."*
- *"Hvad er forskellen på `double` og `Double` i Java?"*
- *"Jeg har rettet testene til det nye trykkrav. Er de dækkende? Hvilke grænseværdier mangler jeg?"*
- *"Hvad er forskellen på et interface og en abstrakt klasse?"*

## Tjekliste: kan du...

- [ ] forklare forskellen på et fortolket sprog, et sprog kompileret til maskinkode, og bytecode med JIT?
- [ ] forklare, hvorfor en `.class`-fil kan køre overalt, men en C-binær fil ikke kan?
- [ ] forklare forskellen på statisk og dynamisk typning, og hvorfor enterprise-systemer foretrækker statisk?
- [ ] læse en Java-klasse og pege på package, felter, constructor og metoder?
- [ ] forklare, hvad et interface er, og hvorfor `MaalingService` bruger et?
- [ ] køre `./mvnw test`, læse en fejlende test og rette koden?
- [ ] forklare lagene controller, service og repository, og hvor forretningsreglerne bor?
- [ ] genkende de samme begreber i C#?

## Ordliste

| Ord | Betydning |
|-----|-----------|
| **kildekode** | Den kode, mennesker skriver |
| **maskinkode** | Binære instruktioner til en bestemt processor |
| **compiler / kompilere** | Oversætter kildekode før kørsel (`javac`, `clang`, `go build`) |
| **fortolker / interpreter** | Udfører kode, mens programmet kører (`python3`) |
| **bytecode** | Instruktioner til en virtuel maskine (`.class`, `.pyc`, .NET IL) |
| **JVM / .NET CLR** | De virtuelle maskiner, der kører Java- og C#-bytecode |
| **JIT** | *Just-in-time*: kompilerer bytecode til maskinkode, mens programmet kører |
| **JDK / JRE** | Udviklingskit med compiler / kun det, der skal til for at køre Java |
| **LTS** | *Long-term support*: en version, der bliver vedligeholdt i mange år. Enterprise bruger dem |
| **statisk / dynamisk typning** | Typer tjekkes af compileren / mens programmet kører |
| **compile-time / runtime** | Når koden bliver oversat / når den kører |
| **garbage collector** | Rydder automatisk op i hukommelse, der ikke bruges |
| **binær / executable** | En kørbar fil med maskinkode |
| **klasse / objekt** | Skabelon / en konkret instans af den |
| **felt / metode / constructor** | Data i en klasse / en funktion i en klasse / den, der laver objektet |
| **`public` / `private`** | Synlig for alle / kun inde i klassen |
| **`static`** | Hører til klassen, ikke til et objekt |
| **record** | En uforanderlig dataklasse |
| **interface / implementering** | En kontrakt / en klasse, der opfylder den |
| **generics** | Typer med parametre: `List<Maaling>` |
| **exception** | En fejl, der bliver kastet (`throw`) og grebet (`catch`) |
| **lambda / stream** | En lille funktion uden navn / en kæde af operationer på en samling |
| **LINQ** | C#'s udgave af streams |
| **annotation / attribute** | Metadata med `@` i Java / `[...]` i C#, som frameworks læser |
| **Maven / Gradle / NuGet** | Byggeværktøjer og pakkesystemer |
| **`pom.xml` / `.csproj`** | Projektbeskrivelse med dependencies |
| **build** | Kompilér, test og pak |
| **jar** | En pakket Java-applikation |
| **deploy** | At installere en ny version på en server |
| **unit test / JUnit** | En automatisk test af en lille del af koden / Javas testframework |
| **rød / grøn test** | Fejler / består |
| **TDD** | Skriv testen først, så koden |
| **grænseværdi / off-by-one** | Værdien lige på kanten / den klassiske fejl med `>` og `>=` |
| **lagdeling** | Controller → service → repository |
| **Spring Boot / ASP.NET Core** | De store backend-frameworks i Java / C# |
| **dependency injection (DI)** | Et objekt får sine afhængigheder udefra i stedet for at lave dem selv |
| **code review** | En kollega læser og kommenterer koden før merge |
| **`git blame`** | Viser, hvem der sidst har ændret hver linje |
