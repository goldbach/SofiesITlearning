# Dag 6b: Kryptografi i praksis

*Ca. 2 timer. Tag den før dag 7, som bygger videre på den.*

## Hvorfor?

Kryptografi er overalt i det, du har lært: Git identificerer commits med hashes (dag 1), HTTPS beskytter trafikken med certifikater (dag 2), passwords bliver hashet, og login-tokens bliver signeret (dag 7). Du skal ikke selv opfinde kryptografi. Det skal *ingen*. Men du skal forstå byggeklodserne, så du kan læse et sikkerhedskrav, følge en arkitekturdiskussion og undgå de klassiske fejl.

Der er kun tre byggeklodser:

| Byggeklods | Spørgsmål den besvarer | Nøgle |
|------------|------------------------|-------|
| **Hashfunktion** | *Er data uændrede?* | Ingen |
| **Symmetrisk kryptering** | *Kan kun vi to læse det?* | Én fælles hemmelig nøgle |
| **Asymmetrisk kryptering og signaturer** | *Kan kun modtageren læse det? Kom det fra afsenderen?* | Et nøglepar: privat og offentlig |

Alt andet, som TLS, JWT, SSH og MitID, er kombinationer af de tre.

Alle værktøjer i dag er allerede på din Mac: `shasum`, `openssl`, `ssh-keygen` og Python. Lav en mappe at lege i:

```bash
mkdir -p ~/kursus/krypto && cd ~/kursus/krypto
```

## Videoer og interaktivt materiale

| Hvornår | Hvad | Længde |
|---------|------|--------|
| **Opslag** | [Practical Cryptography for Developers](https://cryptobook.nakov.com/): gratis online-bog med god dækning af alt i dag | – |
| **Opslag** | [MIT Missing Semester: Security and Cryptography](https://missing.csail.mit.edu/2020/security/): fra samme kursus som dag 1 | 60 min |

---

## Del A: Hashfunktioner (ca. 25 min)

En **hashfunktion** tager input af vilkårlig størrelse og giver et fingeraftryk af fast størrelse, et **digest**. SHA-256 giver altid 256 bit, som skrives som 64 hex-tegn.

```bash
echo "Temperatur: 21.3" > a.txt
echo "Temperatur: 21.4" > b.txt
shasum -a 256 a.txt b.txt
```

Ét ciffer er ændret, og de to hashes ligner ikke hinanden det mindste. Det kaldes **lavineeffekten**.

En kryptografisk hashfunktion har tre egenskaber:

1. **Deterministisk**: Samme input giver altid samme hash.
2. **Envejs**: Ud fra hashen kan man ikke regne inputtet ud. Det eneste, man kan, er at gætte og prøve.
3. **Kollisionsfri**: Det er praktisk umuligt at finde to forskellige input med samme hash.

Med 2²⁵⁶ ≈ 10⁷⁷ mulige værdier er der ifølge gængse skøn flere mulige SHA-256-hashes end atomer i den synlige del af universet. Derfor er kollisioner ikke et praktisk problem.

### Hvad bruges det til?

- **Integritet**: Har filen ændret sig? Når du henter software, står der ofte en SHA-256 ved siden af. Den skal du sammenligne med `shasum -a 256 <fil>`. Maven, pip og Docker tjekker automatisk dependencies og images på den måde. Det er en del af forsvaret mod *supply chain*-angreb (dag 7, OWASP A03).
- **Identitet ud fra indhold**: Git navngiver alt efter dets hash:
  ```bash
  echo 'hej' | git hash-object --stdin
  printf 'blob 4\0hej\n' | shasum -a 1
  ```
  Begge giver det samme. Git beregner SHA-1 af `"blob <længde>\0<indhold>"`. Et commit-ID fra dag 1 er hashen af commitets indhold, inklusive forælderens hash. Derfor kan historikken ikke ændres i det skjulte: Ændrer man ét gammelt commit, ændrer alle hashes efter det sig også. Det er samme princip som en *blockchain*.
- **Passwords**: Det så du på dag 7. Her skal hashfunktionen være *langsom* med vilje (scrypt, bcrypt, Argon2), og et **salt** skal med.

> **Forældede algoritmer:** MD5 og SHA-1 er knækket i den forstand, at man kan konstruere kollisioner. De må ikke bruges til sikkerhed. Git bruger stadig SHA-1, men er ved at skifte til SHA-256. Brug **SHA-256** eller nyere.

### HMAC: hash med en nøgle

En almindelig hash beviser kun, at data er uændrede, hvis man kan stole på hashen selv. En **HMAC** blander en hemmelig nøgle ind, så kun dem, der kender nøglen, kan lave den rigtige værdi. Det er præcis det, `HS256` i JWT er (dag 7).

```python
import hmac, hashlib
hmac.new(b"hemmelig-noegle", b"Temperatur: 21.3", hashlib.sha256).hexdigest()
```

### Øvelser A

1. Lav en hash af en af dine egne lab-filer, ret ét tegn i filen, og hash den igen.
2. Kør `git log --format="%H %s" | head -3` i kursusrepoet. Hvad er de lange tal? Kør `git cat-file -p HEAD`, og find forælderens hash.
3. Hvorfor er SHA-256 alene ikke godt nok til at gemme passwords? Hvor mange gæt i sekundet tror du, en moderne grafikkort-maskine kan lave? Spørg Claude, og vurder svaret kritisk.

---

## Del B: Symmetrisk kryptering (ca. 15 min)

Ved **symmetrisk kryptering** bruger man **samme nøgle** til at kryptere og dekryptere. Den mest brugte algoritme er **AES**.

```bash
echo "Hemmelig måling: 42" > besked.txt
openssl enc -aes-256-cbc -pbkdf2 -salt -in besked.txt -out besked.enc -pass pass:hemmeligt
xxd besked.enc | head -3                 # ulæseligt
openssl enc -d -aes-256-cbc -pbkdf2 -in besked.enc -pass pass:hemmeligt
openssl enc -d -aes-256-cbc -pbkdf2 -in besked.enc -pass pass:forkert     # bad decrypt
```

`-pbkdf2` laver passwordet om til en rigtig 256-bit nøgle med en langsom hashfunktion, samme idé som password-hashing.

Symmetrisk kryptering er **hurtig**. Den bruges til alle store datamængder: diske, databaser, backup og selve trafikken i HTTPS.

**Problemet** er at få nøglen delt. Hvordan giver du nøglen til en server i Frankfurt, du aldrig har mødt, uden at nogen på vejen kan se den? Det løser del C.

---

## Del C: Asymmetrisk kryptering: nøglepar (ca. 30 min)

Ved **asymmetrisk kryptering** har hver part et **nøglepar**:

- en **privat nøgle**, som man holder hemmelig og aldrig deler
- en **offentlig nøgle**, som man giver til alle

De to hænger matematisk sammen. **Det, den ene nøgle låser, kan kun den anden låse op.**

Tænk på en postkasse: Alle kan smide et brev ind gennem sprækken (den offentlige nøgle), men kun den, der har nøglen til lågen (den private nøgle), kan tage det ud.

### Prøv det

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out privat.pem
openssl pkey -in privat.pem -pubout -out offentlig.pem
cat offentlig.pem

# Alle med din offentlige nøgle kan kryptere til dig:
openssl pkeyutl -encrypt -pubin -inkey offentlig.pem -in besked.txt -out besked.rsa
# Kun du kan dekryptere:
openssl pkeyutl -decrypt -inkey privat.pem -in besked.rsa
```

### Matematikken bag: RSA i hånden

Du er fysiker, så det her er til dig. RSA bygger på, at det er let at gange to store primtal sammen, men ekstremt svært at finde dem igen ud fra produktet (**faktorisering**). Prøv med små tal i Python:

```python
p, q = 61, 53                 # to hemmelige primtal
n = p * q                     # 3233: en del af den offentlige nøgle
phi = (p - 1) * (q - 1)       # 3120: kan kun beregnes, hvis man kender p og q
e = 17                        # offentlig eksponent
d = pow(e, -1, phi)           # 2753: privat eksponent, så e·d ≡ 1 (mod phi)

# Offentlig nøgle: (n, e).  Privat nøgle: (n, d).
m = 65                        # beskeden, som et tal
c = pow(m, e, n)              # kryptér med den offentlige: 65^17 mod 3233 = 2790
pow(c, d, n)                  # dekryptér med den private:  2790^2753 mod 3233 = 65
```

Det virker på grund af Eulers sætning: m^(e·d) ≡ m (mod n). For at finde `d` skal man kende `phi`, og for at kende `phi` skal man kende `p` og `q`. Med n = 3233 kan du faktorisere i hovedet. Med et n på 617 cifre (RSA-2048) kan ingen kendt computer gøre det i universets levetid.

Ud over RSA bruges **elliptiske kurver** (ECC, f.eks. *Ed25519*). De giver samme sikkerhed med meget kortere nøgler og er standarden i nyere systemer.

> **Kvantecomputere:** En stor nok kvantecomputer ville kunne knække RSA og ECC. Derfor er man i gang med at indføre *post-quantum*-algoritmer. Du vil høre ordet. Symmetrisk kryptering og hashes er langt mindre berørt.

### Asymmetrisk er langsom, så man kombinerer

Asymmetrisk kryptering er tusindvis af gange langsommere end symmetrisk og kan kun kryptere små mængder data. Derfor kombinerer man dem næsten altid i en **hybrid kryptering**: Man bruger asymmetrisk kryptering til at blive enige om en tilfældig **symmetrisk nøgle**, og derefter krypterer man alle data symmetrisk med den. Det er præcis, hvad HTTPS gør (del E).

### Øvelser C

4. Regn RSA-eksemplet igennem i Python. Kryptér så tallet 42 i stedet for 65, og dekryptér det igen.
5. Hvad sker der, hvis du prøver at dekryptere med den *offentlige* nøgle? Prøv med de små tal: `pow(c, e, n)`.
6. Hvorfor må `m` ikke være større end `n`? *Hint:* Hvad er `pow(4000, e, n)` dekrypteret?

---

## Del D: Digitale signaturer (ca. 20 min)

Vend nøgleparret om:

- **Kryptering**: kryptér med *modtagerens offentlige* nøgle. Kun modtageren kan læse.
- **Signatur**: signér med *din egen private* nøgle. Alle kan verificere med din offentlige nøgle, at det kom fra dig, og at det ikke er ændret.

I praksis signerer man ikke hele dokumentet, men dets **hash**.

```bash
openssl dgst -sha256 -sign privat.pem -out a.sig a.txt
openssl dgst -sha256 -verify offentlig.pem -signature a.sig a.txt     # Verified OK

cp a.txt c.txt && echo "snyd" >> c.txt
openssl dgst -sha256 -verify offentlig.pem -signature a.sig c.txt     # Verification Failure
```

Med RSA-tallene fra før:

```python
s = pow(m, d, n)     # signér med den private: 588
pow(s, e, n)         # alle kan verificere med den offentlige: 65 = m. Ægte!
```

En signatur giver tre garantier:
- **Ægthed**: Det kom fra indehaveren af den private nøgle.
- **Integritet**: Det er ikke ændret.
- **Uafviselighed** (*non-repudiation*): Afsenderen kan ikke senere benægte at have signeret det.

### Hvor du møder signaturer

- **JWT med RS256** (dag 7): Identity provideren signerer tokenet med sin private nøgle. Alle API'er verificerer med den offentlige nøgle, som den offentliggør. Kun IdP'en kan udstede tokens. Med HS256 skal alle API'er derimod kende den samme hemmelige nøgle.
- **MitID og digital signering**: Når du "underskriver" et dokument digitalt, er det en kryptografisk signatur.
- **Software**: Installationsprogrammer, Docker-images og apps bliver signeret, så man kan se, at de kommer fra udgiveren. Det så du med Temurin og Claude Code.
- **Git-commits** kan signeres, så man ved, hvem der faktisk har lavet dem.

### Øvelse D

7. Forklar med egne ord forskellen på HS256 og RS256 i JWT. Hvorfor foretrækker man RS256, når mange systemer skal verificere tokens fra samme IdP?

---

## Del E: Certifikater og TLS (ca. 20 min)

### Problemet med offentlige nøgler

Når din browser modtager en offentlig nøgle fra "github.com", hvordan ved den så, at nøglen virkelig tilhører GitHub og ikke en angriber på café-wifi'en?

### Løsningen: certifikater

Et **certifikat** er en offentlig nøgle plus et navn (f.eks. `github.com`) og en udløbsdato, **signeret af en CA** (*certificate authority*), som browseren stoler på. CA'en går i god for, at nøglen tilhører navnet.

CA'ens eget certifikat er signeret af en anden CA, og så videre op til et **rodcertifikat**, som ligger indbygget i dit styresystem og din browser. Det kaldes en **certifikatkæde** (*chain of trust*):

```bash
openssl s_client -connect github.com:443 -servername github.com </dev/null 2>/dev/null | grep -E "^ *[0-9] s:|^ *i:"
```

```
 0 s:/CN=github.com                                        ← GitHubs certifikat
   i:/C=GB/O=Sectigo Limited/CN=Sectigo ... CA DV E36       ← signeret af (issuer)
 1 s:/C=GB/O=Sectigo Limited/CN=Sectigo ... CA DV E36       ← mellemled
   i:/C=GB/O=Sectigo Limited/CN=Sectigo ... Root E46
 2 ...                                                     ← op mod roden
```

Se detaljerne og udløbsdatoen:

```bash
echo | openssl s_client -connect github.com:443 -servername github.com 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```

Du kan også se alle de rodcertifikater, din Mac stoler på, i appen **Nøglering** (*Keychain Access*) under *Systemrødder*.

### TLS-handshake i grove træk

Når du åbner `https://github.com`, sker følgende:

1. Browseren siger hej og fortæller, hvilke algoritmer den kan.
2. Serveren sender sit **certifikat**.
3. Browseren tjekker kæden op til en rod, den stoler på, og at navnet og datoen passer.
4. De to parter bruger **asymmetrisk** kryptografi til at blive enige om en tilfældig **symmetrisk** nøgle, som ingen på vejen kan se.
5. Resten af forbindelsen bliver krypteret **symmetrisk** (AES eller ChaCha20), fordi det er hurtigt.

Det er de tre byggeklodser i ét. Nu forstår du også fejlene fra dag 2: *"certifikatet er udløbet"*, *"certifikatet passer ikke til navnet"* og *"ukendt CA"*, som ofte opstår i kundens testmiljøer med interne certifikater.

**mTLS** (*mutual TLS*) betyder, at *begge* parter viser et certifikat. Det bruges tit mellem systemer i offentlige integrationer: Kunden udsteder et certifikat til jeres system, og kun systemer med et gyldigt certifikat bliver lukket ind.

---

## Del F: SSH-nøgler (ca. 15 min)

**SSH** (dag 2, port 22) bruger nøglepar i stedet for passwords. Det bruges til at logge ind på servere og til Git. Lav dit eget nøglepar:

```bash
ssh-keygen -t ed25519 -C "din@email.dk"
```

Tryk Enter for standardplaceringen, og vælg en **passphrase**. Den beskytter den private nøgle, hvis din computer bliver stjålet. Bagefter:

```bash
ls ~/.ssh/
cat ~/.ssh/id_ed25519.pub          # offentlig: må gerne deles
                                   # id_ed25519 uden .pub er PRIVAT: del den aldrig, heller ikke med Claude
ssh-add --apple-use-keychain ~/.ssh/id_ed25519      # husk passphrasen i macOS' nøglering
```

### Valgfrit: Brug SSH til GitHub

```bash
gh auth refresh -h github.com -s admin:public_key   # giv gh lov til at håndtere nøgler
gh ssh-key add ~/.ssh/id_ed25519.pub --title "Min Mac"
ssh -T git@github.com                               # "Hi <brugernavn>! You've successfully authenticated"
cd ~/kursus/SofiesITlearning
git remote set-url origin git@github.com:goldbach/SofiesITlearning.git
git pull
```

Nu bruger Git dit nøglepar i stedet for HTTPS-login. GitHub har kun din *offentlige* nøgle. Ved login sender GitHub en udfordring, som din computer signerer med den private nøgle (del D), og GitHub verificerer signaturen.

Første gang du forbinder til en ny server, spørger SSH, om du stoler på serverens **fingerprint**. Det er en hash af serverens offentlige nøgle (del A). På jobbet skal du sammenligne den med den, driftsfolkene oplyser.

---

## Del G: Ord du vil høre (ca. 5 min)

- **Kryptering i transit / i hvile** (*in transit / at rest*): Data er krypteret, mens de bliver sendt (TLS), og mens de ligger på disk eller i database (f.eks. AES-krypterede diske). Begge dele står typisk i sikkerhedskravene.
- **End-to-end-kryptering**: Kun afsender og modtager kan læse indholdet, ikke serverne imellem.
- **Key management**: Hvem har nøglerne, hvor ligger de, og hvordan bliver de skiftet (**key rotation**)? Ofte er det sværere end selve kryptografien. Nøgler opbevares i et **vault** eller en **HSM** (*hardware security module*), en særlig hardware-boks, som nøglen aldrig forlader.
- **Certifikatfornyelse**: Certifikater udløber, ofte efter 1 år eller kortere. Fornyelse skal automatiseres eller planlægges, ellers holder integrationerne op med at virke (dag 2).
- **"Don't roll your own crypto"**: Byg aldrig dine egne kryptografiske algoritmer eller protokoller, og brug altid velafprøvede biblioteker. `jwt_lab.py` fra dag 7 og RSA-legetøjet her er kun til læring. Rigtig RSA kræver bl.a. *padding*, ellers er den usikker.

---

## Aflevering

Lav en branch `opgaver/dag-6b`, og aflevér via PR:
- `noter/dag-6b.md` med svar på øvelse 1–7

Læg **ikke** nøgler (`*.pem`, `id_ed25519`) i repoet. De er lavet i `~/kursus/krypto` og `~/.ssh`, ikke i kursusrepoet, og sådan skal det blive.

## Spørg Claude

- *"Forklar Eulers sætning, og hvorfor RSA virker. Jeg kan modulær aritmetik."*
- *"Hvorfor bruger TLS både asymmetrisk og symmetrisk kryptering?"*
- *"Hvad er forskellen på at kryptere og at signere?"*
- *"Hvad er en hashkollision, og hvorfor er MD5 knækket?"*
- *"Hvad betyder 'kryptering i hvile' i praksis for en PostgreSQL-database i Azure?"*

## Tjekliste: kan du...

- [ ] forklare de tre egenskaber ved en kryptografisk hashfunktion, og hvad hashes bruges til?
- [ ] forklare, hvordan Git bruger hashes?
- [ ] forklare forskellen på en hash og en HMAC?
- [ ] forklare forskellen på symmetrisk og asymmetrisk kryptering, og hvornår man bruger hvad?
- [ ] forklare, hvad den private og den offentlige nøgle bruges til ved kryptering og ved signering?
- [ ] regne et lille RSA-eksempel igennem og forklare, hvorfor faktorisering er nøglen?
- [ ] forklare, hvad et certifikat og en certifikatkæde er?
- [ ] beskrive TLS-handshaket i grove træk?
- [ ] lave et SSH-nøglepar og forklare, hvilken del der må deles?

## Ordliste

| Ord | Betydning |
|-----|-----------|
| **kryptografi** | Matematiske metoder til at beskytte data |
| **hashfunktion / digest** | Envejsfunktion til et fingeraftryk af fast længde / selve fingeraftrykket |
| **SHA-256 / SHA-1 / MD5** | Moderne hashfunktion / forældet / knækket |
| **checksum** | En hash, der bruges til at tjekke, at en fil er uændret |
| **lavineeffekt** | En lille ændring i input giver en helt anden hash |
| **kollision** | To forskellige input med samme hash |
| **HMAC** | En hash med en hemmelig nøgle. Det er HS256 i JWT |
| **symmetrisk kryptering / AES** | Samme nøgle til at kryptere og dekryptere / den mest brugte algoritme |
| **asymmetrisk kryptering / public key** | Et nøglepar: privat og offentlig |
| **privat nøgle / offentlig nøgle** | Holdes hemmelig / deles med alle |
| **RSA / ECC / Ed25519** | Asymmetriske algoritmer: faktorisering / elliptiske kurver / en populær ECC-variant |
| **hybrid kryptering** | Asymmetrisk til at udveksle en nøgle, symmetrisk til selve data |
| **digital signatur** | Hash signeret med en privat nøgle, verificeret med den offentlige |
| **uafviselighed** | Afsenderen kan ikke benægte at have signeret |
| **certifikat** | Offentlig nøgle + navn + udløbsdato, signeret af en CA |
| **CA / rodcertifikat** | Den, der udsteder certifikater / det øverste, indbyggede tillidsanker |
| **certifikatkæde / chain of trust** | Kæden af signaturer fra et certifikat op til en rod |
| **TLS / handshake** | Protokollen bag HTTPS / indledningen, hvor nøgler bliver aftalt |
| **mTLS** | Begge parter viser certifikat. Bruges mellem systemer |
| **SSH-nøgle / passphrase** | Nøglepar til login på servere og Git / password, der beskytter den private nøgle |
| **fingerprint** | En hash af en offentlig nøgle, så man kan genkende den |
| **kryptering i transit / i hvile** | Når data sendes / når data ligger gemt |
| **end-to-end-kryptering** | Kun afsender og modtager kan læse |
| **key management / key rotation** | Håndtering af nøgler / udskiftning af nøgler med jævne mellemrum |
| **HSM** | Hardware, der opbevarer nøgler sikkert |
| **post-quantum** | Algoritmer, der skal kunne modstå kvantecomputere |
| **padding** | Tilfældigt fyld, som rigtig RSA kræver for at være sikker |
