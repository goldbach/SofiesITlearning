# Dag 1: Terminal og Git

*Ca. 3½ time inkl. Learn Git Branching. Del A–D er kerne. Videoerne til fordybelse er valgfri.*

## Hvorfor starter vi her?

I et IT-projekt ligger alt i **Git**: koden, SQL-scripts, testdata, konfiguration og ofte også dokumentation og krav. Hver ændring bliver gennemgået af en kollega, før den kommer ind. Det gælder for udviklere, testere og analytikere.

Du kender princippet fra laboratoriet. En god labjournal er dateret, man retter ikke i gamle sider, og man skriver *hvorfor* man gjorde noget. Git er en labjournal for kode, som et helt team kan skrive i på samme tid.

Terminalen lærer du først, fordi Git er født i den. Den er også det værktøj, du vil se kollegerne bruge.

## Videoer og interaktivt materiale

Alt er på engelsk.

| Hvornår | Hvad | Længde |
|---------|------|--------|
| **Før du starter** | [Git Explained in 100 Seconds](https://www.youtube.com/watch?v=hwP7WQkmECE) (Fireship): det store billede på to minutter | 2 min |
| **Efter del B** | [Learn Git Branching](https://learngitbranching.js.org/): interaktivt i browseren, hvor du ser commit-træet ændre sig, mens du skriver. Lav *Introduction Sequence*. Har du tid, så tag også *Push & Pull*. | 20–40 min |
| **Til fordybelse** | [MIT Missing Semester, Lecture 1: The Shell](https://www.youtube.com/watch?v=Z56Jmr9Z34Q): fra MIT-kurset om de værktøjer, uddannelserne glemmer at lære fra sig | 50 min |
| **Til fordybelse** | [MIT Missing Semester, Lecture 6: Version Control (git)](https://www.youtube.com/watch?v=2sjqTHE0zok): hvordan Git er bygget indeni. Godt for den analytiske type | 85 min |
| **Til fordybelse** | [Git and GitHub for Beginners – Crash Course](https://www.youtube.com/watch?v=RGOj5yH7evk) (freeCodeCamp): alternativ gennemgang med GitHub og pull requests | 70 min |

Se ikke det hele på én gang. Lav øvelserne, og brug videoerne, når noget ikke giver mening.

---

## Del A: Terminalen (ca. 45 min)

Terminalen er en tekstbaseret måde at styre computeren på. Du skriver en kommando, trykker Enter og får et svar. Programmet, der fortolker kommandoerne, hedder en **shell**. På macOS er det `zsh`, på Linux typisk `bash`, og Git Bash på Windows er `bash`.

### Hvor er jeg?

Filsystemet er et træ af mapper (**directories**). Du står altid ét sted i træet, i din **working directory**.

```bash
pwd                 # print working directory: hvor står jeg?
ls                  # list: hvad ligger her?
ls -la              # alle filer, også skjulte (dem der starter med .), med detaljer
cd Documents        # change directory: gå ned i en mappe
cd ..               # gå én mappe op
cd ~                # gå til din hjemmemappe
cd -                # gå tilbage til hvor du var før
```

**Stier (paths):**
- En **absolut sti** starter fra roden: `/Users/sofie/Documents`
- En **relativ sti** starter fra der, hvor du står: `Documents/rapport.txt`
- `.` betyder "her", og `..` betyder "mappen ovenover"
- `~` er din hjemmemappe

> **Tip:** Tryk **Tab**, så fuldfører terminalen fil- og mappenavne. Tryk **pil op** for at hente tidligere kommandoer. **Ctrl-C** afbryder en kommando, der hænger.

### Filer

```bash
mkdir labdata              # make directory
cd labdata
echo "temp,tryk" > maaling.csv      # skriv tekst til en fil (> overskriver)
echo "21.3,1013" >> maaling.csv     # >> tilføjer i bunden
cat maaling.csv            # vis indholdet
cp maaling.csv kopi.csv    # copy
mv kopi.csv backup.csv     # move eller omdøb
rm backup.csv              # remove. Der er ingen papirkurv!
```

### Kombinér kommandoer med pipes

Med `|` (pipe) sender du output fra én kommando videre som input til den næste. Hver kommando gør én ting godt, og du sætter dem sammen. Det svarer lidt til at kæde metoder i pandas: `df.query(...).groupby(...).sum()`.

```bash
for i in $(seq 1 100); do echo "$i,$((RANDOM % 30))" >> maaling.csv; done
wc -l maaling.csv                # hvor mange linjer?
head -5 maaling.csv              # de første 5 linjer
grep ",2[0-9]$" maaling.csv      # linjer der slutter med 20-29
grep ",2[0-9]$" maaling.csv | wc -l   # ...og hvor mange er der?
```

### Få hjælp

```bash
man ls          # manualen (tryk q for at lukke)
git --help      # de fleste programmer har --help
```

### Øvelse A

1. Lav en mappe `~/kursus`, og gå ind i den.
2. Skriv et lille Python-script `hej.py`, der printer `"Hej fra terminalen"`. Brug din editor, eller prøv `nano hej.py` (gem med Ctrl-O og Enter, luk med Ctrl-X).
3. Kør det med `python3 hej.py`.
4. Kør `python3 hej.py > output.txt`, og vis filen med `cat`. Hvad skete der med outputtet?

---

## Del B: Git, den mentale model (ca. 30 min)

Inden du skriver kommandoer, skal du have billedet i hovedet. Så giver kommandoerne sig selv.

### Snapshots, ikke ændringer

Et **repository** (repo) er en mappe, hvor Git holder øje med historikken. Hver gang du laver et **commit**, gemmer Git et **snapshot** af alle filerne sammen med en besked, et navn og et tidspunkt. Et commit kan ikke ændres bagefter. Det er som en underskrevet side i labjournalen.

Hvert commit har et unikt ID (en **hash**), f.eks. `a3f9c21`, og peger på sin forælder. Historikken bliver dermed en kæde:

```
A ← B ← C ← D      (main)
```

### De tre områder

```
 working directory  →  staging area  →  repository
  (dine filer)        (git add)         (git commit)
```

- **Working directory**: filerne, som du ser og redigerer dem.
- **Staging area** (også kaldet *index*): her lægger du det, der skal med i næste commit. Du kan altså vælge at committe nogle ændringer og vente med andre.
- **Repository**: historikken af commits.

### Branches

En **branch** er en navngivet pegepind til et commit. Når du laver en ny branch, kan du arbejde videre uden at forstyrre andre:

```
A ← B ← C ← D          (main)
         \
          E ← F        (feature/login)
```

Når arbejdet er færdigt og godkendt, **merger** man branchen ind i `main`. Sådan kan 20 personer arbejde på det samme system uden at træde hinanden over tæerne.

### Remote: samarbejdet

Repoet ligger på din computer, men der er også en fælles kopi på en server, et **remote**, som typisk hedder `origin`. Det kan være GitHub, GitLab, Bitbucket eller Azure DevOps.

- `git clone`: hent en kopi af et remote repo
- `git pull`: hent andres nye commits
- `git push`: send dine commits op

Man pusher ikke direkte til `main`. Man pusher sin branch og åbner en **pull request** (PR), som i GitLab hedder *merge request* (MR). Det er en forespørgsel om at få sine ændringer merget. En kollega laver **code review**: læser ændringerne, kommenterer og godkender (**approve**). Samtidig kører en **pipeline** automatisk tests. Først når både review og pipeline er godkendt, bliver PR'en merget.

Det svarer til peer review: ingen ændringer kommer ind uden en anden persons godkendelse.

---

## Del C: Git i praksis (ca. 60 min)

### Opsætning (én gang)

Git har du tjekket på [dag 0](../00-opsaetning/README.md). Fortæl nu Git, hvem du er:

```bash
git config --global user.name "Dit Navn"
git config --global user.email "din@email.dk"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
```

Den sidste linje får Git til at åbne VS Code, når du skal skrive en længere commit-besked eller en merge-besked. Uden den åbner Git editoren `vim`, som er svær at komme ud af, hvis man ikke kender den. Når du er færdig, gemmer du og lukker fanebladet. Så fortsætter Git.

### Øvelse C1: Dit første repo

```bash
mkdir ~/kursus/git-leg && cd ~/kursus/git-leg
git init                     # gør mappen til et repo (laver en skjult .git-mappe)
echo "# Mine forsøg" > README.md
git status                   # dit vigtigste værktøj: hvad er status?
git add README.md            # læg filen i staging
git status                   # se forskellen
git commit -m "Tilføj README"
git log                      # se historikken
```

Ret nu i `README.md`. Tilføj f.eks. en linje `Forsøg 1: kalibrering`. Kør derefter:

```bash
git status
git diff                     # hvad har jeg ændret siden sidste commit?
git add README.md
git commit -m "Beskriv forsøg 1"
git log --oneline            # kort format
```

> **Gode commit-beskeder** beskriver *hvad* og gerne *hvorfor* i bydeform: "Tilføj validering af CPR-nummer", ikke "fix" eller "ændringer". Mange projekter sætter også et Jira-nummer på, f.eks. `PROJ-123: Tilføj validering af CPR-nummer`.

### Øvelse C2: Branches og merge

```bash
git switch -c forsoeg-2      # lav en ny branch og skift til den
echo "Forsøg 2: temperaturserie" >> README.md
git commit -am "Beskriv forsøg 2"   # -a: tag alle ændrede filer med (kun filer git kender i forvejen)
git log --oneline --all --graph

git switch main              # tilbage til main. Kig i README.md: forsøg 2 er væk!
git merge forsoeg-2          # merge branchen ind
cat README.md                # nu er den der
git branch -d forsoeg-2      # slet branchen, den er merget
```

### Øvelse C3: En merge-konflikt (med vilje)

Konflikter opstår, når to har rettet *samme linje* på hver sin branch. Git kan ikke gætte, hvem der har ret, så det må du afgøre. Konflikter er helt normale og ikke farlige.

```bash
git switch -c enhed-celsius
sed -i.bak 's/temperaturserie/temperaturserie (°C)/' README.md && rm README.md.bak
git commit -am "Angiv enhed i celsius"

git switch main
sed -i.bak 's/temperaturserie/temperaturserie (K)/' README.md && rm README.md.bak
git commit -am "Angiv enhed i kelvin"

git merge enhed-celsius      # CONFLICT!
git status
cat README.md
```

Filen indeholder nu markører:

```
<<<<<<< HEAD
Forsøg 2: temperaturserie (K)
=======
Forsøg 2: temperaturserie (°C)
>>>>>>> enhed-celsius
```

Åbn filen, vælg den rigtige version (eller skriv en ny), og slet markørerne. Afslut derefter:

```bash
git add README.md
git commit -m "Merge enhed-celsius, vælg kelvin"
git log --oneline --graph
```

### Øvelse C4: Fortryd

```bash
echo "noget rod" >> README.md
git restore README.md        # kassér ændringer i en fil, der ikke er committet
git log --oneline
git show HEAD                # vis det seneste commit (HEAD = "hvor jeg står nu")
```

> **Vigtigt:** Når et commit er pushet og andre har hentet det, skal det ikke omskrives. Til gengæld kan man lave et nyt commit, der fortryder et gammelt (`git revert <hash>`). Hvis du får brug for at fortryde noget i en delt branch, så spørg en kollega først. Ingen synes, det er et dumt spørgsmål.

### `.gitignore`

Nogle filer skal ikke med i repoet: midlertidige filer, store datafiler og især **adgangskoder og nøgler**. Dem skriver man i en fil, der hedder `.gitignore`:

```
__pycache__/
*.log
.env
data/raa/
```

Et password, der er committet, ligger i historikken for altid, også selvom det bliver slettet i næste commit. Det er en af de få fejl, der er rigtigt dyre.

---

## Del D: Samarbejde via GitHub (ca. 45 min)

Nu laver du det rigtige workflow på det her repo.

0. **Log ind på GitHub fra terminalen** (kun første gang). Du skal have accepteret invitationen til repoet på dag 0. Git skal vide, at det er dig, før du må pushe. Kommandoen `gh` installerede du på dag 0:
   ```bash
   gh auth login
   ```
   Vælg **GitHub.com**, **HTTPS**, svar **Yes** til at bruge dine GitHub-oplysninger til Git, og log ind via browseren.
1. **Clone** forløbet. Indtil nu har du læst det på GitHub. Nu henter du din egen kopi:
   ```bash
   cd ~/kursus
   git clone https://github.com/goldbach/SofiesITlearning.git
   cd SofiesITlearning
   code .                      # åbn det i VS Code. Fra nu af læser du tutorials her
   ```
2. **Lav en branch** til dine noter. Navngiv den efter konventionen `<type>/<beskrivelse>`:
   ```bash
   git switch -c noter/dag-1
   ```
3. Lav mappen med `mkdir -p noter`, og lav filen `noter/dag-1.md` med:
   - 3 ting du lærte i dag
   - 1 ting der stadig er uklar
   - Din løsning på øvelse A4: hvad gjorde `>`?
4. **Commit og push**:
   ```bash
   git add noter/dag-1.md
   git commit -m "Tilføj noter fra dag 1"
   git push -u origin noter/dag-1    # -u: husk koblingen mellem lokal og remote branch
   ```
5. Gå ind på GitHub. Der står et banner med **"Compare & pull request"**. Klik på det, skriv en kort beskrivelse, og tilføj din far som **reviewer**.
6. Vent på review. Hvis du får kommentarer, retter du lokalt, laver commit og push igen. PR'en opdaterer sig selv.
7. Når PR'en er godkendt og merget, rydder du op. Branchen på GitHub bliver slettet automatisk ved merge:
   ```bash
   git switch main
   git pull                     # hent den mergede version
   git branch -d noter/dag-1    # slet din lokale kopi af branchen
   ```

Det er hele arbejdsgangen. Du kommer til at gøre det hundredvis af gange.

### Ritualet hver dag fremover

Start **hver** ny dag og hver ny opgave med en frisk branch fra `main`, også selvom gårsdagens PR stadig venter på review:

```bash
cd ~/kursus/SofiesITlearning
git switch main
git pull                          # hent det, der er merget siden sidst
git switch -c opgaver/dag-2       # ny branch til dagens opgaver
```

Laver du i stedet den nye branch, mens du står på gårsdagens, kommer gårsdagens commits med i den nye PR. Så bliver PR'erne lagt oven på hinanden og er svære at reviewe. Gårsdagens PR kan sagtens leve videre for sig selv. Får du kommentarer til den, skifter du tilbage med `git switch opgaver/dag-1`, retter, committer og pusher.

**Om `main`:** Efterhånden som dine PR'er bliver merget, kommer dine løsninger ind i kursusfilerne på `main`. `main` bliver altså *din* version af forløbet, og koden vil afvige fra det, der står i tutorials. Det er meningen. Hvis din far senere retter i en fil, du også har rettet i, får du en merge-konflikt ved `git pull`. Den løser du som i øvelse C3.

---

## Spørg Claude

Når du har lavet dag 1b og installeret Claude Code, kan du vende tilbage hertil og prøve:

- *"Forklar forskellen på working directory, staging area og repository med en analogi fra laboratoriet."*
- *"Jeg tror, en branch er en kopi af alle filerne. Har jeg ret?"*
- *"Hvad sker der egentlig inde i `.git`-mappen, når jeg laver et commit?"*
- *"Quiz mig i ordlisten fra dag 1, ét spørgsmål ad gangen."*

## Tjekliste: kan du...

- [ ] navigere rundt med `cd`, `ls` og `pwd`, og forklare forskellen på en absolut og en relativ sti?
- [ ] forklare forskellen på working directory, staging area og et commit?
- [ ] lave en branch, committe på den og merge den?
- [ ] løse en merge-konflikt?
- [ ] forklare, hvad en pull request er, og hvorfor man laver code review?
- [ ] forklare, hvorfor passwords aldrig må committes?

## Ordliste

| Ord | Betydning |
|-----|-----------|
| **terminal / shell / CLI** | Tekstbaseret styring af computeren. CLI = *command-line interface* |
| **repo (repository)** | En mappe med Git-historik |
| **commit** | Et gemt snapshot med besked, forfatter og tidspunkt. Bruges også som verbum: "har du committet?" |
| **hash** | Et commits unikke ID, f.eks. `a3f9c21` |
| **staging area / index** | Det, der kommer med i næste commit |
| **branch** | En parallel udviklingslinje. "Lav en branch til det" |
| **main / master** | Hovedbranchen. Det, der virker og bliver sendt i produktion |
| **feature branch** | En branch til én opgave, typisk navngivet efter Jira-sagen |
| **merge** | Flet en branch ind i en anden |
| **merge-konflikt** | To har rettet samme sted, og et menneske skal vælge |
| **remote / origin** | Den fælles kopi af repoet på en server |
| **clone / pull / push** | Hent repo / hent ændringer / send ændringer |
| **PR / MR** | Pull request / merge request: en anmodning om at få ændringer merget |
| **code review** | En kollega læser og godkender ændringerne |
| **approve** | Godkend en PR |
| **pipeline / CI** | Automatisk build og test ved hver ændring. Kommer på dag 5 og 6 |
| **HEAD** | Det commit, du står på lige nu |
| **revert** | Fortryd et commit ved at lave et nyt, modsat commit |
| **rebase** | Flyt sine commits, så de ligger oven på den nyeste main. Du vil høre ordet. Lær det, når du får brug for det |
| **.gitignore** | En liste over filer, Git skal ignorere |
| **secret** | Password, API-nøgle, certifikat. Må aldrig ligge i Git |
| **Azure DevOps / GitLab / Bitbucket / GitHub** | Platforme, der hoster Git-repos og PR'er. Kunderne bruger forskellige |
