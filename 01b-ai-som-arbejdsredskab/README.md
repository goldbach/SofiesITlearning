# Dag 1b: AI som arbejdsredskab

*Ca. 1½–2 timer. Lav det efter dag 1, fordi du skal bruge terminalen og Git.*

## Hvorfor?

AI-værktøjer er blevet en del af hverdagen i IT-projekter. De bruges til at forklare kode, skrive udkast til tests og dokumentation, finde fejl og lære nyt hurtigt. Som ny i branchen kan det være din bedste læringsmakker.

Der er to ting, du skal have med fra starten:

1. **AI'en kan tage fejl og lyde helt sikker samtidig.** Ansvaret for det, du afleverer, er dit.
2. **Som konsulent arbejder du med kundens kode og data.** Hvad du må lægge ind i et AI-værktøj, bestemmer kunden og Netcompany, ikke dig.

I resten af forløbet bruger du **Claude Code** som tutor. Repoet indeholder en fil, `CLAUDE.md`, der får Claude til at opføre sig som underviser. Den giver hints frem for færdige løsninger, og den bygger forklaringerne på det, du allerede kan.

## Videoer og interaktivt materiale

| Hvornår | Hvad | Længde |
|---------|------|--------|
| **Før du starter** | [Large Language Models explained briefly](https://www.youtube.com/watch?v=LPZh9BOjkQs) (3Blue1Brown): hvad en LLM er, flot visualiseret | 8 min |
| **Til fordybelse** | [Transformers, the tech behind LLMs](https://www.youtube.com/watch?v=wjZofJX0v4M) (3Blue1Brown): matematikken bag, med vektorer, matricer og sandsynligheder. Den er til dig | 27 min |
| **Til fordybelse** | [Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) (Andrej Karpathy): et overblik fra en af feltets kendte forskere, også om sikkerhed | 60 min |
| **Opslag** | [Claude Code quickstart](https://code.claude.com/docs/en/quickstart): den officielle introduktion | – |

---

## Del A: Den mentale model (ca. 20 min)

### Hvad er en LLM?

En **LLM** (*large language model*) er en model, der er trænet på enorme mængder tekst til at forudsige det næste stykke tekst. Den beregner en sandsynlighedsfordeling over, hvad der kommer næste gang, vælger noget, og gentager processen. Det, der ligner forståelse og ræsonnement, opstår ud af det.

Du kan tænke på den som en meget stor, ikke-lineær model, der er fittet til data. Det giver dig også intuitionen for dens svagheder.

### Begreber du vil høre

- **Token**: det stykke tekst, modellen arbejder med. Det svarer omtrent til et ord eller en del af et ord. Pris og grænser opgøres i tokens.
- **Prompt**: det, du skriver til modellen.
- **Context / context window**: alt det, modellen kan "se" lige nu, altså samtalen, filer den har læst, og instruktioner. Det svarer til dens arbejdshukommelse. Den er stor, men ikke uendelig, og den forsvinder, når du starter en ny session. Derfor findes filer som `CLAUDE.md`, der bliver læst ind hver gang.
- **Hallucination**: når modellen finder på noget, der lyder plausibelt, men er forkert, f.eks. et kommando-flag, der ikke findes, eller en kilde, der ikke eksisterer. Det svarer til at **ekstrapolere et fit uden for dataområdet**: modellen giver et svar, men intet garanterer, at det er rigtigt.
- **Training cutoff**: modellen kender kun verden frem til et vist tidspunkt.
- **Chat vs. agent**: en chat svarer kun med tekst. En **agent** kan også bruge **værktøjer**: læse filer, køre kommandoer, søge på nettet. Den arbejder i en løkke, hvor den tænker, handler, ser resultatet og handler igen. Claude Code er en agent, der kører i din terminal.
- **MCP** (*Model Context Protocol*): en standard for at koble en AI til andre systemer som Jira, databaser eller mail. Du vil høre ordet.

---

## Del B: Kom i gang med Claude Code (ca. 30 min)

### Installation

Du oprettede din Claude Pro-konto på [dag 0](../00-opsaetning/README.md). Nu skal du installere Claude Code. Skriv i Ghostty:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Åbn derefter et **nyt** terminalvindue, og tjek installationen:

```bash
claude --version
```

> **Læg mærke til** `curl ... | bash`. Kommandoen henter et script fra nettet og kører det med det samme. Det er normalt til installation, men gør det kun med kilder, du stoler på. Du kan altid læse scriptet først: `curl -fsSL https://claude.ai/install.sh | less`.

### Første session

```bash
cd ~/kursus/SofiesITlearning
claude
```

Første gang bliver du bedt om at logge ind via browseren. Claude læser automatisk `CLAUDE.md` i mappen. Prøv at skrive:

> Hvad er din rolle i det her repo?

### Det vigtigste at kunne

| Tast / tegn | Hvad det gør |
|-------------|--------------|
| `Esc` | Afbryd Claude midt i et svar, så du kan rette kursen |
| `Ctrl-C` to gange | Afslut Claude Code |
| `Shift-Tab` | Skift tilstand, f.eks. til **plan mode**, hvor Claude kun planlægger og ikke ændrer noget |
| `/help` | Vis hjælp og kommandoer |
| `/clear` | Start en frisk samtale (tømmer context) |
| `@fil` | Henvis til en fil, f.eks. `@01-terminal-og-git/README.md` |
| `!kommando` | Kør en shell-kommando direkte, f.eks. `!git status`. Claude ser outputtet |

### Tilladelser: læs, før du siger ja

Når Claude vil køre en kommando eller rette i en fil, beder den om lov. **Læs, hvad der står, før du godkender.** En agent arbejder på din maskine med dine rettigheder. Det svarer til at skrive under på en laboratorieprotokol: man skriver ikke under uden at have læst den.

Hvis du ikke forstår kommandoen, så tryk nej og spørg: *"Hvad gør den kommando, du ville køre?"*

---

## Del C: Lær med AI og ikke kun af AI (ca. 20 min)

Den store fælde er at lade AI'en lave arbejdet. Så føles det, som om man lærer, men man lærer ikke noget. Brug den i stedet som en tålmodig ekspert, du kan spørge om alt.

### Gode prompts til læring

- **Giv kontekst:** *"Jeg er fysiker og kan Python. Forklar mig, hvad en merge-konflikt er."*
- **Bed om analogier:** *"Forklar staging area med en analogi fra laboratoriearbejde."*
- **Tjek din forståelse:** *"Jeg tror, at en branch er en kopi af alle filerne. Har jeg ret?"* (Svaret er nej. Prøv selv.)
- **Bed om hints:** *"Jeg sidder fast i øvelse C3. Giv mig et hint, ikke løsningen."*
- **Få forklaret fejl:** Indsæt fejlbeskeden og spørg *"Hvad betyder den, og hvad er typiske årsager?"*
- **Bliv quizzet:** *"Quiz mig i ordlisten fra dag 1, ét spørgsmål ad gangen."*
- **Få forklaret kode:** *"Forklar linje for linje, hvad den her kode gør."* Det bliver meget nyttigt på dag 4.

### Kontrollér svarene

- **Kør det.** Kode og kommandoer kan afprøves. Det er den bedste kontrol.
- **Slå det op.** Brug `git help <kommando>`, `man` og den officielle dokumentation.
- **Spørg ind.** *"Hvor sikker er du? Hvordan kan jeg selv tjekke det?"*
- **Vær ekstra skeptisk ved** versionsnumre, kommando-flag, navne på biblioteker, kilder og alt, hvad der er sket for nylig.

---

## Del D: AI på jobbet som konsulent (ca. 15 min)

Det her afsnit er det vigtigste.

### Data og kode tilhører kunden

Netcompany laver mange systemer for offentlige myndigheder og store virksomheder. Det betyder:

- **Kundens kode og dokumenter er fortrolige.** Det er dem, der ejer dem.
- **Persondata** som CPR-numre, navne og helbredsoplysninger er beskyttet af **GDPR**. Det kan være ulovligt at sende dem til en ekstern tjeneste.
- Når du sætter noget ind i et AI-værktøj, **sender du det til en ekstern server**, medmindre værktøjet er sat op til at køre et godkendt sted.

**Tommelfingerregel:** Brug kun de AI-værktøjer, som projektet udtrykkeligt har godkendt, og kun på den måde, de er godkendt til. Hvis du er i tvivl, så lad være og spørg.

Det her forløb kender ikke Netcompanys interne regler. De varierer sikkert fra kunde til kunde. Gør det til en af dine første opgaver at finde ud af, hvad der gælder på dit projekt.

### Spørgsmål til din første uge

- Hvilke AI-værktøjer er godkendt på projektet, f.eks. GitHub Copilot, ChatGPT Enterprise, Claude eller interne værktøjer?
- Må jeg bruge dem på kundens kode? På dokumenter? På testdata?
- Er der regler for at markere, at noget er lavet med AI?
- Hvem kan jeg spørge, hvis jeg er i tvivl?

### Ansvaret er dit

AI-genereret kode, tekst og SQL skal reviewes som alt andet. "Det var AI'en, der skrev det" er ikke et forsvar. Hvis du ikke kan forklare, hvad noget gør, så aflever det ikke.

---

## Øvelser

Lav dem i en Claude-session i repoet.

1. **Mød din tutor.** Spørg Claude, hvad dens rolle er, og bed den forklare forskellen på `git add` og `git commit` med en analogi fra laboratoriet. Var analogien god?
2. **Quiz.** Bed om en quiz med 5 spørgsmål i ordlisten fra dag 1.
3. **Find en hallucination.** Spørg Claude om en meget specifik detalje, f.eks. *"Hvilke flag har `git log`, der kan vise commits fra en bestemt forfatter i et bestemt tidsrum?"*. Kontrollér svaret med `git help log`. Passede det hele?
4. **Forklar uden at løse.** Lav en merge-konflikt som i øvelse C3 fra dag 1. Bed Claude forklare, hvad der står i filen, *uden* at løse den. Løs den selv.
5. **Brug tilladelserne bevidst.** Bed Claude om at vise indholdet af mappen `01-terminal-og-git`. Læs tilladelsesprompten, før du svarer.
6. **Aflevér.** Skriv i `noter/dag-1b.md`:
   - Hvad var Claudes svar i øvelse 3, og hvad viste `git help log`?
   - Én ting, du *ikke* ville lægge ind i et AI-værktøj på jobbet, og hvorfor.

   Aflever via en PR, som du lærte på dag 1. Du laver selv Git-kommandoerne. Claude er sat op til ikke at gøre det for dig.

---

## Tjekliste: kan du...

- [ ] forklare, hvad en LLM er, og hvorfor den kan hallucinere?
- [ ] forklare forskellen på en chat og en agent?
- [ ] starte Claude Code, afbryde den og henvise til en fil?
- [ ] forklare, hvorfor du skal læse en tilladelsesprompt, før du godkender?
- [ ] sige, hvilke typer data du aldrig lægger ind i et AI-værktøj, som projektet ikke har godkendt?

## Ordliste

| Ord | Betydning |
|-----|-----------|
| **LLM** | *Large language model*: en model, der genererer tekst ved at forudsige, hvad der kommer næste gang |
| **token** | Den enhed tekst, en LLM arbejder med (omtrent et ord eller en del af et ord) |
| **prompt** | Det, du skriver til modellen |
| **context window** | Den mængde tekst, modellen kan se på én gang, altså dens arbejdshukommelse |
| **hallucination** | Et overbevisende, men forkert svar |
| **training cutoff** | Det tidspunkt, modellens viden går frem til |
| **agent** | En AI, der kan bruge værktøjer (filer, kommandoer, web) i en løkke for at løse en opgave |
| **tool use** | Når modellen kalder et værktøj i stedet for kun at svare med tekst |
| **MCP** | *Model Context Protocol*: en standard for at koble AI til andre systemer |
| **Copilot** | GitHubs/Microsofts AI-assistent i editoren. Meget udbredt i virksomheder |
| **plan mode** | En tilstand i Claude Code, hvor den planlægger uden at ændre noget |
| **`CLAUDE.md`** | En fil med instruktioner, som Claude Code læser ved hver start |
| **GDPR** | EU's databeskyttelsesforordning. Den bestemmer, hvordan persondata må behandles |
| **persondata** | Oplysninger, der kan identificere en person, f.eks. CPR-nummer, navn eller adresse |
