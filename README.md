# Klar til start som IT-konsulent

Et forløb på 10 moduler og 6 dage, der skal give dig sproget og de mentale modeller, så du kan følge med fra første dag i et IT-projekt.

Målet er **ikke**, at du kan det hele. Målet er, at du ved, hvad folk taler om i standup og refinement, og at du ved, hvad du skal spørge om eller google. Resten lærer du på projektet og i Netcompanys eget onboarding-forløb.

## Sådan bruger du forløbet

- **Kerne og fordybelse.** Øverst i hver tutorial står, hvilke dele der er **kerne**, og hvilke der er **fordybelse**. Kernen er planlagt til 4–5 timer om dagen. Fordybelsen er der, hvis du har tid eller lyst, nu eller senere på jobbet.
- **Lav øvelserne.** Du lærer mere af at skrive kommandoerne selv end af at læse om dem.
- **Aflevér via pull requests.** Tutorial 01 lærer dig Git. Derefter afleverer du dine noter og løsninger som PR'er til det her repo, præcis som du kommer til at gøre på jobbet. Kun kerneøvelserne skal afleveres.
- **Videoer.** Hver tutorial har en liste med videoer og interaktivt materiale med anvisninger om, *hvornår* du skal se hvad. De er et supplement, ikke et krav.
- **Claude som tutor.** Fra dag 1b bruger du Claude Code som tutor. Kør `claude` i repoet, og spørg løs. Den er sat op (i `CLAUDE.md`) til at give hints frem for svar.
- **Ordliste.** Hver tutorial slutter med en ordliste. [ORDLISTE.md](ORDLISTE.md) samler alle ordene alfabetisk. Den er god at have, når du er startet.

Forløbet er på dansk, men fagudtrykkene står på engelsk, fordi det er dem, du kommer til at høre.

## Plan for de 6 dage

| Dag | Kerne | Ca. tid |
|-----|-------|---------|
| 1 | [00 Gør din Mac klar](00-opsaetning/README.md) og [01 Terminal og Git](01-terminal-og-git/README.md) | 4 t |
| 2 | [01b AI som arbejdsredskab](01b-ai-som-arbejdsredskab/README.md) og [02 Hvordan et system hænger sammen](02-system-og-api/README.md) | 5 t |
| 3 | [03 Data: SQL og datamodellering](03-sql-og-datamodellering/README.md) | 4 t |
| 4 | [04 At læse kode i Java og C#](04-kode-java-csharp/README.md) og [06 Drift og cloud](06-drift-og-cloud/README.md), del A–B | 4½ t |
| 5 | [05 Fra behov til løsning](05-fra-behov-til-loesning/README.md) og 06 Drift og cloud, del D og F | 5 t |
| 6 | [06b Kryptografi i praksis](06b-kryptografi/README.md) og [07 Sikkerhed og konsulentlivet](07-sikkerhed-og-konsulentlivet/README.md) | 5 t |

Hvis du har en ekstra dag, så brug den på fordybelsen i 03, 05 og 06 eller på at gentage det, der var svært.

## Modulerne

| Modul | Kort fortalt |
|-------|--------------|
| [00 Gør din Mac klar](00-opsaetning/README.md) | Claude- og GitHub-konto, Ghostty, VS Code, Homebrew, Git og Python |
| [01 Terminal og Git](01-terminal-og-git/README.md) | Hvor koden bor, og hvordan et team arbejder i den samme kode |
| [01b AI som arbejdsredskab](01b-ai-som-arbejdsredskab/README.md) | LLM'er, Claude Code som din tutor, og hvad du må og ikke må som konsulent |
| [02 Hvordan et system hænger sammen](02-system-og-api/README.md) | Klient/server, HTTP, REST, JSON, netværk og porte. Du bygger et mini-API i Python |
| [03 Data: SQL og datamodellering](03-sql-og-datamodellering/README.md) | Fra `pandas` til SQL, tabeller, nøgler, ER-diagrammer og normalisering |
| [04 At læse kode i Java og C#](04-kode-java-csharp/README.md) | Fortolket, kompileret og JIT. Typer, klasser, interfaces og tests, så du kan læse enterprise-kode |
| [05 Fra behov til løsning](05-fra-behov-til-loesning/README.md) | Krav, user stories, acceptkriterier, Scrum, Jira, testniveauer og miljøer |
| [06 Drift og cloud](06-drift-og-cloud/README.md) | Docker, Kubernetes i overblik, cloud, netværkszoner og overvågning |
| [06b Kryptografi i praksis](06b-kryptografi/README.md) | Hashes, symmetrisk og asymmetrisk kryptering, signaturer, certifikater og SSH-nøgler |
| [07 Sikkerhed og konsulentlivet](07-sikkerhed-og-konsulentlivet/README.md) | Login, OAuth2/OIDC, JWT, MitID/NemLog-in, GDPR og livet som konsulent |

## Kom i gang

1. **Læs i browseren til at begynde med.** Forløbet ligger på [github.com/goldbach/SofiesITlearning](https://github.com/goldbach/SofiesITlearning). GitHub viser Markdown-filerne pænt formateret, så du kan læse dag 0 og dag 1 direkte her.
2. **Start med [dag 0](00-opsaetning/README.md).** Den gør din Mac klar og opretter de konti, du skal bruge.
3. **Clone repoet på dag 1, del D.** Her henter du din egen kopi til din Mac og lærer at aflevere via pull requests. Kommandoerne er:
   ```bash
   mkdir -p ~/kursus && cd ~/kursus
   git clone https://github.com/goldbach/SofiesITlearning.git
   cd SofiesITlearning
   code .
   ```
   Fra da af læser du tutorials i VS Code (`Cmd-Shift-V` for preview, se dag 0) og laver øvelserne i din kopi.
4. **Hent nyt indhold fra GitHub.** Hvis forløbet bliver opdateret, efter du har clonet, henter du ændringerne med `git switch main` og `git pull`.
