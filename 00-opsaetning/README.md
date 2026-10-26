# Dag 0: Gør din Mac klar

*Ca. 1 time. Gør det, inden du går i gang med dag 1. Det hele er kerne.*

Håndværkere starter med at have styr på deres værktøj, og det gør vi også her. Når du er færdig, har du:

1. En **Claude-konto**, så du kan bruge Claude som tutor fra dag 1b.
2. En god **terminal**: Ghostty.
3. En opdateret **VS Code**, sat op til det her forløb.
4. En **GitHub-konto**, **Homebrew** og **GitHub CLI** (`gh`).
5. Tjekket **Git** og **Python**.

---

## 1. Opret en Claude-konto

1. Gå til [claude.ai](https://claude.ai), og opret en konto.
2. Vælg abonnementet **Pro**. Gratisversionen giver ikke adgang til Claude Code, som du skal bruge i terminalen.
3. Du kan også bruge Claude i browseren og i mobil-appen, men forløbet bruger primært **Claude Code** i terminalen. Den installerer du på dag 1b.

> Brug din **private** e-mail til den her konto. Det, du laver på jobbet, skal foregå i de værktøjer og på de konti, Netcompany og kunden har godkendt. Mere om det på dag 1b.

---

## 2. En god terminal: Ghostty

macOS har en indbygget app, der hedder *Terminal*. Den virker, men [Ghostty](https://ghostty.org) er hurtigere, pænere og bedre til de værktøjer, du skal bruge, blandt andet Claude Code. Den er gratis og open source.

### Installér

Hent `.dmg`-filen fra [ghostty.org/download](https://ghostty.org/download), åbn den, og træk Ghostty over i *Programmer*.

Start Ghostty fra Spotlight (`Cmd-Space`, skriv "ghostty"). Højreklik på ikonet i Dock'en, og vælg *Behold i Dock*.

### Tilpas den

Ghostty bruger en almindelig tekstfil til opsætning. Åbn den med `Cmd-,` (komma). Indsæt for eksempel:

```
font-size = 15
theme = light:Rose Pine Dawn,dark:Rose Pine
window-save-state = always
```

- `font-size`: skriftstørrelsen.
- `theme`: farvetema. Med `light:...,dark:...` følger det, om din Mac kører i lys eller mørk tilstand. Se alle temaer med `ghostty +list-themes` i terminalen.
- `window-save-state = always`: åbner dine vinduer og faneblade igen, når du genstarter Ghostty.

Gem filen, og genindlæs opsætningen med `Cmd-Shift-,`.

### Taster der er gode at kende

| Tast | Hvad |
|------|------|
| `Cmd-T` | Nyt faneblad |
| `Cmd-D` | Del vinduet lodret. Godt til f.eks. en server i den ene halvdel og `curl` i den anden (dag 2) |
| `Cmd-Shift-D` | Del vinduet vandret |
| `Cmd-W` | Luk faneblad eller del |
| `Cmd-+` / `Cmd--` | Større/mindre skrift |

---

## 3. VS Code

Du har VS Code i forvejen. Den skal opdateres og sættes op.

### Opdatér

Vælg menuen **Code → Check for Updates…**, og installér, hvis der er en ny version. Du kan se din version under **Code → About Visual Studio Code**.

### Kommandoen `code` i terminalen

Med kommandoen `code` kan du åbne filer og mapper i VS Code direkte fra terminalen. Git kan også bruge den, når du skal skrive en commit-besked eller løse en konflikt.

1. Åbn VS Code.
2. Tryk `Cmd-Shift-P` (**Command Palette**, VS Codes kommandolinje. Den skal du bruge tit).
3. Skriv `shell command`, og vælg **Shell Command: Install 'code' … command in PATH**.
4. Luk og genåbn Ghostty, og afprøv:
   ```bash
   code --version
   ```

### Extensions

Installér det, du skal bruge, fra terminalen:

```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension anthropic.claude-code
```

- **Python** (Microsoft): syntaksfarver, fejlfinding, debugger og valg af Python-miljø. Pylance kommer med automatisk.
- **Jupyter**: notebooks direkte i VS Code. Du kender dem sikkert fra dine lab-analyser.
- **Claude Code**: Claude i et panel i VS Code. Vi starter med Claude i terminalen på dag 1b, men panelet er godt, når du læser kode.

Senere i forløbet kommer der flere extensions til, f.eks. til SQL.

### Indstillinger

Tryk `Cmd-Shift-P`, skriv `user settings json`, og vælg **Preferences: Open User Settings (JSON)**. Hvis filen er tom eller kun indeholder `{}`, erstatter du indholdet med nedenstående. Hvis der allerede står indstillinger, kopierer du kun linjerne inden for `{ }` ind og sætter et komma efter den sidste eksisterende linje. VS Code markerer fejl med rødt.

```json
{
  "files.autoSave": "afterDelay",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "editor.fontSize": 14,
  "editor.rulers": [100],
  "editor.minimap.enabled": false,
  "terminal.integrated.fontSize": 14,
  "git.autofetch": true,
  "markdown.preview.breaks": true
}
```

| Indstilling | Hvorfor |
|-------------|---------|
| `files.autoSave` | Gemmer automatisk, så du ikke kører en gammel version af din fil |
| `files.trimTrailingWhitespace` | Fjerner usynlige mellemrum i enden af linjer. De giver støj i Git-diffs og code review |
| `files.insertFinalNewline` | Filer slutter med et linjeskift. Det er konvention, og Git klager ellers |
| `editor.rulers` | En lodret streg ved 100 tegn. Mange projekter har en grænse for linjelængde |
| `editor.minimap.enabled` | Slår det lille kodekort i højre side fra. Det fylder uden at hjælpe en begynder |
| `git.autofetch` | VS Code tjekker selv, om der er nyt på serveren |
| `markdown.preview.breaks` | Et linjeskift i markdown bliver vist som et linjeskift i preview |

### Markdown preview

Alle tutorials er skrevet i **Markdown**, et simpelt tekstformat med `#` til overskrifter, `**fed**`, tabeller og kodeblokke. Åbn en tutorial i VS Code, og tryk `Cmd-Shift-V`. Så ser du den pænt formateret. Med `Cmd-K V` får du preview ved siden af teksten.

Markdown bliver brugt overalt: README-filer, pull requests, Jira, Confluence og wikis. Det er værd at lære.

---

## 4. Homebrew og GitHub CLI

### GitHub-konto

Forløbet ligger på GitHub, og fra dag 1 afleverer du via pull requests. Det kræver en konto og skriveadgang til repoet:

1. Opret en gratis konto på [github.com](https://github.com), hvis du ikke har en.
2. Send dit brugernavn til din far, så han kan invitere dig til repoet.
3. Acceptér invitationen. Den kommer på e-mail og på [github.com/notifications](https://github.com/notifications).

### Homebrew

**Homebrew** er en *package manager* til macOS: en app-butik til terminalen, hvor du installerer udviklerværktøjer med én kommando. Installér den med kommandoen fra [brew.sh](https://brew.sh):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Følg instruktionerne til sidst. Du skal muligvis køre et par linjer, så `brew` kommer på din PATH. Luk og genåbn derefter Ghostty, og installér **GitHub CLI** (`gh`):

```bash
brew install gh
gh --version
```

Med `gh` logger du ind på GitHub fra terminalen, så du kan pushe på dag 1.

---

## 5. Tjek Git og Python

I Ghostty:

```bash
git --version
python3 --version
python3 -m pip --version
python3 -m venv --help | head -1
```

- Hvis `git` ikke er installeret, tilbyder macOS at installere *Command Line Developer Tools*. Sig ja, og vent til det er færdigt.
- Alle fire kommandoer skal svare uden fejl. Hvis Python-versionen er ældre end 3.10, så sig til.

---

## Tjekliste

- [ ] Jeg har en Claude Pro-konto.
- [ ] Ghostty er installeret, ligger i Dock'en og er sat op.
- [ ] VS Code er opdateret, og `code --version` virker i terminalen.
- [ ] Extensions og indstillinger er på plads.
- [ ] Jeg kan åbne en `.md`-fil i preview.
- [ ] Jeg har en GitHub-konto og har accepteret invitationen til repoet.
- [ ] `brew` og `gh` er installeret.
- [ ] `git`, `python3`, `pip` og `venv` svarer alle sammen.

## Ordliste

| Ord | Betydning |
|-----|-----------|
| **terminal emulator** | Programmet, der viser terminalen, f.eks. Ghostty eller Terminal.app. Shellen (`zsh`) kører inde i den |
| **IDE / editor** | Programmet, man skriver kode i. VS Code er en editor, der med extensions kan næsten det samme som en IDE (*integrated development environment*) |
| **extension / plugin** | En udvidelse til et program |
| **Command Palette** | `Cmd-Shift-P` i VS Code: søg efter enhver kommando |
| **package manager** | Et værktøj, der installerer og opdaterer software, f.eks. Homebrew på macOS og `pip` til Python |
| **CLI** | *Command-line interface*: et program, man bruger fra terminalen, f.eks. `gh` |
| **PATH** | Listen over mapper, shellen leder i, når du skriver en kommando |
| **Markdown** | Et simpelt tekstformat til dokumentation (`.md`-filer) |
| **dotfile / config-fil** | En opsætningsfil, ofte med et navn, der starter med `.` |
