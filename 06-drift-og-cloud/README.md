# Dag 6: Drift og cloud

*Ca. 2 timer for kernen. **Kerne:** del A, B, D og F. **Fordybelse:** del C (Docker Compose) og del E (Kubernetes i praksis). I planen tager du A–B på dag 4 og D og F på dag 5.*

**Start:** Modul 06 er delt over to dage. Lav branchen `opgaver/dag-6` fra en frisk `main`, når du går i gang med del A på dag 4 (`git switch main && git pull && git switch -c opgaver/dag-6`). På dag 5 fortsætter du på samme branch med `git switch opgaver/dag-6`. Lav først din PR, når del D og F er færdige. Se [ritualet på dag 1](../01-terminal-og-git/README.md#ritualet-hver-dag-fremover).

## Hvorfor?

Indtil nu har din kode kørt på din egen Mac. Et rigtigt system skal køre på servere, døgnet rundt, for tusindvis af brugere. Det skal kunne opdateres uden nedetid og overleve, at en maskine går i stykker. Det er **drift** (*operations*, "ops").

Som analytiker skal du ikke selv drifte, men du kommer til at høre om containere, pods, clustre og deploys hver dag. Du skal også kunne svare på driftsspørgsmål i krav og kontrakter: Hvor skal data ligge? Hvad sker der, hvis systemet går ned? Hvor hurtigt skal det være oppe igen?

I dag pakker du API'et fra dag 2 i en **container**, kører det sammen med en database og ser, hvordan **Kubernetes** holder det kørende.

## Videoer og interaktivt materiale

| Hvornår | Hvad | Længde |
|---------|------|--------|
| **Før du starter** | [Docker in 100 Seconds](https://www.youtube.com/watch?v=Gjnup-PuquQ) (Fireship) | 2 min |
| **Før del D** | [Kubernetes Explained in 100 Seconds](https://www.youtube.com/watch?v=PziYflu8cB8) (Fireship) | 2 min |
| **Før del D** | [The Illustrated Children's Guide to Kubernetes](https://www.youtube.com/watch?v=4ht22ReBjno): Kubernetes forklaret som en børnebog. Den er faktisk rigtig god | 8 min |
| **Opslag** | [Docker: Get started](https://docs.docker.com/get-started/) | – |
| **Opslag** | [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/): den officielle tutorial | – |

## Installation

Installér **Docker Desktop**:

```bash
brew install --cask docker-desktop
```

Eller hent den fra [docker.com](https://docs.docker.com/desktop/setup/install/mac-install/). Start Docker fra *Programmer*, og vent til hvalen i menulinjen holder op med at bevæge sig. Tjek i Ghostty:

```bash
docker version
docker run hello-world
```

> Docker Desktop er gratis til privat brug og små virksomheder. Større virksomheder skal have licens. På jobbet bruger du det, Netcompany stiller til rådighed.

---

## Del A: Fra server til container (ca. 30 min)

### Problemet: "Det virker på min maskine"

Dit API fra dag 2 kræver Python 3.10 eller nyere, FastAPI i en bestemt version og et venv. På en server skal alt det installeres præcis ens, og på 20 servere skal det være *præcis* ens. En anden applikation på samme server vil måske have en anden Python-version. Det er et klassisk mareridt i drift.

### Løsningen: containere

En **container** pakker programmet sammen med *alt*, det skal bruge: styresystemets biblioteker, Python, dependencies og koden. Det svarer til en standard-skibscontainer. Kranen er ligeglad med, hvad der er indeni, og den passer på alle skibe.

```
   Fysisk server            Virtuelle maskiner (VM)        Containere
 ┌────────────────┐       ┌──────┐┌──────┐┌──────┐     ┌────┐┌────┐┌────┐┌────┐
 │   App A + B    │       │App A ││App B ││App C │     │ A  ││ B  ││ C  ││ D  │
 │ (konflikter!)  │       │ OS   ││ OS   ││ OS   │     └────┘└────┘└────┘└────┘
 │                │       └──────┘└──────┘└──────┘     ┌──────────────────────┐
 │       OS       │       ┌──────────────────────┐     │  Container runtime   │
 │                │       │      Hypervisor      │     │   (deler OS-kernen)  │
 └────────────────┘       └──────────────────────┘     └──────────────────────┘
                          tunge: hver har sit eget OS   lette: starter på sekunder
```

- En **virtuel maskin** (VM) simulerer en hel computer med sit eget styresystem. Den er tung og starter på minutter.
- En **container** deler styresystemets kerne (*kernel*) med værten. Den er isoleret, men let, og starter på sekunder. Containere er Linux-teknologi. På Mac kører Docker Desktop en lille skjult Linux-VM, som containerne kører i.

### Image og container

| | Hvad | Analogi |
|---|------|---------|
| **Image** | En skabelon: et uforanderligt snapshot af filsystem og opstartskommando | En klasse (dag 4), eller en opskrift |
| **Container** | En kørende instans af et image | Et objekt, eller kagen |
| **Dockerfile** | Opskriften, image bliver bygget fra | Kildekoden |
| **Registry** | Et lager af images, f.eks. *Docker Hub*, *Azure Container Registry* eller *Amazon ECR* | GitHub for images |

### Øvelse A

1. Kør en Python, du ikke har installeret:
   ```bash
   docker run -it --rm python:3.12-slim python
   ```
   Du får en Python-prompt *inde i* en container. Prøv `import platform; platform.platform()`. Hvilket styresystem kører den på? Afslut med `exit()`.
2. Se, hvad der ligger på din maskine nu:
   ```bash
   docker images        # hentede images
   docker ps -a         # containere (-a: også stoppede)
   ```

---

## Del B: Byg dit eget image (ca. 45 min)

Mappen indeholder [`app.py`](app.py), som er API'et fra dag 2 med to nye endpoints:
- `/health` svarer `{"status": "ok"}`. Driftsværktøjer bruger det til at se, om containeren lever.
- `/info` viser **hvilken container** der svarede, og hvilket **miljø** den kører i. Det bliver nyttigt i del E.

Læs [`Dockerfile`](Dockerfile). Hver linje er kommenteret.

### Byg og kør

```bash
cd ~/kursus/SofiesITlearning/06-drift-og-cloud
docker build -t maalinger-api:1.0 .
```

`-t` giver imaget et navn og et **tag** (en version). `.` betyder "byg ud fra mappen her". Kør det:

```bash
docker run -d --name api1 -p 8080:8000 -e MILJOE=test maalinger-api:1.0
curl http://127.0.0.1:8080/info
curl http://127.0.0.1:8080/maalinger
```

- `-d` (*detached*): kør i baggrunden.
- `-p 8080:8000`: **port mapping**. Port 8080 på din Mac sendes videre til port 8000 i containeren (dag 2, del F). Containeren er sit eget lille netværk.
- `-e MILJOE=test`: sæt en **miljøvariabel**. Koden læser den med `os.environ.get("MILJOE")`.

Åbn også http://127.0.0.1:8080/docs. Det er den samme Swagger-side som på dag 2, bare inde i en container.

### Kig ind i containeren

```bash
docker ps                          # kører den?
docker logs api1                   # dens log
docker logs -f api1                # følg loggen live (stop med Ctrl-C)
docker exec -it api1 bash          # åbn en shell *inde i* containeren
```

Inde i containeren kan du prøve `whoami`, `ls`, `cat /etc/os-release` og `python --version`. Det er en Debian Linux med en anden Python end din Mac's. Afslut med `exit`.

### Konfiguration hører til miljøet, ikke til koden

Start en container mere fra *samme* image, men med en anden konfiguration:

```bash
docker run -d --name api2 -p 8081:8000 -e MILJOE=prod -e VERSION=1.0 maalinger-api:1.0
curl http://127.0.0.1:8081/info
```

Det er princippet bag miljøerne fra dag 5: **Det samme image** går fra DEV over TEST til PROD. Kun konfigurationen er forskellig. Så ved man, at det, der blev testet, er præcis det, der kommer i produktion.

**Secrets** (passwords, nøgler) må aldrig ligge i imaget eller i Git. De kommer ind som miljøvariabler eller fra et *secret store* (f.eks. *Azure Key Vault* eller *HashiCorp Vault*), når containeren starter.

### Containere er flygtige

```bash
curl -X POST http://127.0.0.1:8080/maalinger -H "Content-Type: application/json" -d '{"temperatur": 30, "tryk": 1000}'
curl http://127.0.0.1:8080/maalinger      # den nye måling er der
docker rm -f api1                          # slet containeren
docker run -d --name api1 -p 8080:8000 maalinger-api:1.0
curl http://127.0.0.1:8080/maalinger      # væk!
```

En container skal kunne smides væk og erstattes når som helst. Data, der skal gemmes, hører hjemme i en database eller et **volume**, ikke inde i containeren.

### Øvelser B

3. Ret `VERSION` i `app.py` til `"1.1"` som standardværdi. Byg et nyt image med tagget `maalinger-api:1.1`, og kør det på port 8082. Nu har du to versioner side om side. Hvordan ville du rulle tilbage til 1.0?
4. Kør `docker build` igen uden at ændre noget. Hvorfor går det så hurtigt? Kig efter `CACHED` i outputtet, og læs kommentaren i Dockerfile om rækkefølgen.
5. Ryd op: `docker rm -f api1 api2` (og evt. den fra øvelse 3).

---

## Del C: Flere containere med Docker Compose (ca. 30 min, fordybelse)

Et rigtigt system består af flere dele (dag 2). Med **Docker Compose** beskriver du dem alle i én fil. Læs [`compose.yaml`](compose.yaml): et `api` og en `db` (PostgreSQL).

```bash
docker compose up -d --build
docker compose ps
curl http://127.0.0.1:8080/info
```

### Containerne kan finde hinanden via DNS

Compose laver et internt netværk, hvor hver service kan nås på sit **navn**:

```bash
docker compose exec api python -c "import socket; print(socket.gethostbyname('db'))"
```

Det er DNS fra dag 2. `db` bliver oversat til containerens interne IP-adresse. Applikationen skal blot forbinde til `db:5432`.

### En rigtig PostgreSQL

```bash
docker compose exec db psql -U lab
```

Nu er du i PostgreSQL's prompt. Prøv SQL fra dag 3:

```sql
CREATE TABLE forsoeg (id SERIAL PRIMARY KEY, titel TEXT NOT NULL);
INSERT INTO forsoeg (titel) VALUES ('Kalibrering'), ('Temperaturserie');
SELECT * FROM forsoeg;
\q
```

Læg mærke til `SERIAL`. I SQLite skrev vi `INTEGER PRIMARY KEY`. Det er en af de **dialektforskelle**, der blev nævnt på dag 3.

### Volumes: data, der overlever

```bash
docker compose down                         # stop og slet containerne
docker compose up -d
docker compose exec db psql -U lab -c "SELECT * FROM forsoeg;"    # data er der stadig!
```

Databasens filer ligger i et **volume** (`db-data` i `compose.yaml`), som lever uafhængigt af containeren. Med `docker compose down -v` slettes volumet også, og så er data væk.

### Øvelser C

6. Hvilken port lytter PostgreSQL på? Brug `nc -vz 127.0.0.1 5432` fra dag 2. Hvad sker der med `nc`, når du har kørt `docker compose down`?
7. Passwordet til databasen står direkte i `compose.yaml`. Hvorfor er det i orden her, men ikke i et rigtigt projekt? Hvad ville du gøre i stedet?
8. Ryd op: `docker compose down -v`.

---

## Del D: Kubernetes – containere i stor skala (ca. 30 min)

Docker kører containere på *én* maskine. I produktion har man brug for:

- at køre mange kopier af hver container på mange maskiner
- at erstatte containere automatisk, hvis de går ned
- at fordele trafikken mellem kopierne
- at opdatere til en ny version uden nedetid, og rulle tilbage, hvis den fejler

Det gør **Kubernetes** (forkortet **k8s**, fordi der står 8 bogstaver mellem k og s). Kubernetes er en **container-orkestrator**, en dirigent for containere. Det er standarden i dag. Docker og Kubernetes er i øvrigt skrevet i Go (dag 4).

### Den vigtigste idé: deklarativ

I Kubernetes siger du ikke *"start 3 containere"*. Du siger *"jeg ønsker, at der altid kører 3"*. Kubernetes sammenligner hele tiden **ønsket tilstand** (*desired state*) med **faktisk tilstand** og retter forskellen. Dør en container, starter den en ny. Det svarer til en termostat: Du sætter en temperatur, og systemet regulerer selv. Det er det samme princip som SQL (dag 3): Du beskriver *hvad*, ikke *hvordan*.

### Begreberne

| Begreb | Hvad |
|--------|------|
| **Cluster** | En samling maskiner, der bliver styret af Kubernetes |
| **Node** | Én maskine (fysisk eller VM) i clusteret |
| **Pod** | Den mindste enhed: én (eller få) containere, der kører sammen |
| **Deployment** | "Kør altid N kopier (*replicas*) af den her pod, og opdatér dem pænt" |
| **Service** | Et fast navn og en fast IP foran en gruppe pods, som fordeler trafikken (**load balancing**) |
| **Ingress** | Indgangen udefra: sender HTTP-trafik videre til de rigtige services ud fra domæne og sti |
| **ConfigMap / Secret** | Konfiguration / hemmeligheder, som bliver givet til pods som miljøvariabler eller filer |
| **Namespace** | En logisk opdeling af clusteret, f.eks. ét pr. team eller pr. miljø |
| **Probes** | Kubernetes kalder `/health` for at se, om en pod er klar (*readiness*) og i live (*liveness*) |

Alt bliver beskrevet i **YAML-filer** (*manifests*). Læs dem i [`k8s/`](k8s/):
- [`deployment.yaml`](k8s/deployment.yaml): 3 replicas af `maalinger-api:1.0`, med probes på `/health` og grænser for CPU og hukommelse.
- [`service.yaml`](k8s/service.yaml): en service foran podsene.
- [`configmap.yaml`](k8s/configmap.yaml): `MILJOE` og `VERSION`.

Kubernetes-manifester ligger i Git ved siden af koden. Ofte bliver de pakket som **Helm charts** (skabeloner) og rullet ud automatisk af et værktøj som *Argo CD*. Det kaldes **GitOps**: Git er sandheden om, hvad der kører.

---

## Del E: Kubernetes i praksis (ca. 45 min, fordybelse)

### Slå Kubernetes til

Åbn Docker Desktop, gå til **Kubernetes**, og vælg **Create cluster**. Vælg **kubeadm**, når du bliver spurgt, og vent på, at det er klar.

> **Tjek altid, hvilket cluster du taler med, før du kører kommandoer.** På jobbet har du adgang til flere clustre, måske også produktion. En `kubectl delete` mod det forkerte cluster er en klassisk og meget dyr fejl.
>
> ```bash
> kubectl config get-contexts        # hvilke clustre kender jeg?
> kubectl config use-context docker-desktop
> kubectl config current-context     # skal sige docker-desktop
> ```

### Deploy

Byg imaget (hvis du ryddede op i del B), og deploy:

```bash
cd ~/kursus/SofiesITlearning/06-drift-og-cloud
docker build -t maalinger-api:1.0 .
kubectl apply -f k8s/
kubectl get pods                   # vent på 3 x Running og READY 1/1
kubectl get deployment,service
```

Hvis podsene står i `ErrImagePull` eller `ImagePullBackOff`, kan clusteret ikke se dit lokale image. Tjek, at du valgte **kubeadm**, eller spørg Claude.

### Load balancing

Start en midlertidig pod med `curl` *inde i* clusteret, og kald servicen ved navn:

```bash
kubectl run curl --rm -it --restart=Never --image=curlimages/curl -- \
  sh -c 'for i in 1 2 3 4 5 6; do curl -s http://maalinger-api:8080/info; echo; done'
```

Se på `"container"`. Svarene kommer fra forskellige pods. Servicen fordeler trafikken.

Vil du ramme API'et fra din Mac, så lav en tunnel:

```bash
kubectl port-forward service/maalinger-api 9090:8080
# i et andet faneblad:
curl http://127.0.0.1:9090/info
```

### Selvheling

```bash
kubectl get pods
kubectl delete pod <navnet-på-en-af-dem>
kubectl get pods                   # en ny pod er allerede på vej!
```

Du slettede en pod, men ønsket tilstand er 3, så Kubernetes startede en ny.

### Skalering

```bash
kubectl scale deployment/maalinger-api --replicas=5
kubectl get pods
```

I produktion kan det ske automatisk ud fra belastningen (*autoscaling*).

### Rolling update og rollback

Opdatér til "version 2.0":

```bash
kubectl set env deployment/maalinger-api VERSION=2.0
kubectl rollout status deployment/maalinger-api
kubectl get pods                   # nye navne: podsene er blevet udskiftet
```

Kubernetes udskifter podsene én ad gangen og venter på, at hver ny pod er *ready* (via `/health`), før den gamle bliver stoppet. Brugerne mærker intet. Det kaldes en **rolling update**. Er der problemer?

```bash
kubectl rollout history deployment/maalinger-api
kubectl rollout undo deployment/maalinger-api
```

### Fejlfinding

```bash
kubectl logs deployment/maalinger-api          # log fra en af podsene
kubectl describe pod <navn>                    # detaljer og hændelser: hvorfor starter den ikke?
kubectl get events --sort-by=.lastTimestamp    # hvad er der sket i clusteret?
```

### Ryd op

```bash
kubectl delete -f k8s/
```

Du kan slette clusteret igen i Docker Desktop under **Kubernetes**.

### Øvelser E

9. Kør curl-løkken igen efter skaleringen til 5. Hvor mange forskellige pods svarer?
10. Ret `replicas` i `deployment.yaml` til 2, og kør `kubectl apply -f k8s/` igen. Hvad sker der? Hvorfor er det bedre end `kubectl scale`? *Hint:* Hvad står der i Git?
11. Fremprovokér en fejl: Ret imaget i `deployment.yaml` til `maalinger-api:9.9` (findes ikke), og kør `apply`. Hvad viser `kubectl get pods` og `kubectl describe pod`? Kører de gamle pods stadig? Ret det tilbage.

---

## Del F: Cloud, netværk og overvågning (ca. 30 min)

### Cloud

**Cloud** betyder, at man lejer computerkraft, lager og færdige tjenester hos en udbyder i stedet for at eje sine egne servere. De tre store:

| Tjeneste | AWS | Microsoft Azure | Google Cloud |
|----------|-----|-----------------|--------------|
| Virtuelle maskiner | EC2 | Azure Virtual Machines | Compute Engine |
| Managed Kubernetes | EKS | AKS | GKE |
| Managed database | RDS | Azure SQL Database / Azure Database for PostgreSQL | Cloud SQL |
| Fil-/objektlager | S3 | Blob Storage | Cloud Storage |
| Container registry | ECR | ACR | Artifact Registry |

"Managed" betyder, at udbyderen står for drift, backup og opdateringer. Man betaler for at slippe.

Man taler om tre niveauer:
- **IaaS** (*infrastructure*): Du lejer maskiner og netværk og står selv for resten.
- **PaaS** (*platform*): Du lejer en platform, f.eks. en managed database eller Kubernetes, og leverer kun din kode og dine data.
- **SaaS** (*software*): Du lejer et færdigt program, f.eks. Microsoft 365 eller Jira Cloud.

Det modsatte af cloud er **on-premise** (*on-prem*): egne servere i eget datacenter eller hos en driftsleverandør. Mange offentlige systemer kører stadig on-prem eller i en **hybrid** opsætning.

### Spørgsmål, du skal stille som analytiker

- **Hvor skal data ligge?** Persondata skal ofte ligge i EU, og nogle gange i Danmark (GDPR og kundens krav). Cloud-udbydere har **regioner**, f.eks. "North Europe" og "West Europe".
- **Hvem har adgang?** Hvem hos udbyderen, hos leverandøren og hos kunden kan se data?
- **Hvor meget nedetid kan forretningen tåle?** Det bestemmer arkitekturen og prisen (dag 5: SLA). To parametre går igen: **RTO** (*recovery time objective*: hvor hurtigt skal vi være oppe igen?) og **RPO** (*recovery point objective*: hvor mange minutters data har vi råd til at miste?).
- **Hvem drifter?** Leverandøren, kunden selv, eller en tredje driftsleverandør? Det afgør meget af samarbejdet.

### Infrastructure as Code

Servere, netværk og databaser bliver ikke sat op ved at klikke i en webportal. De bliver beskrevet i kode, som ligger i Git og bliver reviewet som al anden kode: **Infrastructure as Code** (IaC). Værktøjer: *Terraform*, *Bicep* (Azure), *Pulumi* og *CloudFormation* (AWS). Kubernetes-YAML fra del D er samme idé.

### Netværk i drift (fortsat fra dag 2)

```
  Internet
     │
 ┌───▼──────────────────────────── DMZ ───────────────────────────┐
 │  Firewall ─► Load balancer / reverse proxy / API gateway       │
 └───┬────────────────────────────────────────────────────────────┘
     │   (kun bestemte porte åbnet)
 ┌───▼──────────────────────── Intern zone ───────────────────────┐
 │  Applikationsservere / Kubernetes-cluster (ingress → services)  │
 └───┬────────────────────────────────────────────────────────────┘
     │   (kun databaseport åbnet, kun fra app-zonen)
 ┌───▼──────────────────────── Datazone ──────────────────────────┐
 │  Databaser                                                      │
 └─────────────────────────────────────────────────────────────────┘
```

- **Load balancer**: fordeler trafikken mellem flere servere. Det er samme idé som en Kubernetes-service, bare i stor skala.
- **Reverse proxy**: en server foran applikationen, der tager imod alle requests og sender dem videre. Den står ofte også for HTTPS-certifikater (dag 2). Eksempler: *nginx* og *Traefik*.
- **API gateway**: en reverse proxy til API'er med ekstra funktioner som login-tjek, *rate limiting* (højst N kald pr. minut) og logning.
- **DMZ og netværkszoner**: Netværket er delt op i zoner med firewalls imellem. Internettet kan kun nå DMZ'en. Databasen kan kun nås fra applikationszonen. Bliver én del kompromitteret, er resten stadig beskyttet. Det hedder **defense in depth**.

### Overvågning (observability)

Når systemet kører, skal man kunne se, om det har det godt. Der er tre slags data:

| | Hvad | Eksempel |
|---|------|----------|
| **Logs** | Tekst om hændelser | `"POST /maalinger HTTP/1.1" 201`, som du har set i alle dagenes servere |
| **Metrics** | Tal over tid | Requests pr. sekund, svartid, fejlrate, CPU, hukommelse |
| **Traces** | Én requests rejse gennem flere systemer | Frontend → API → database → CPR-integration, med tiden brugt i hvert led |

Værktøjer: *Grafana*, *Prometheus*, *Elastic/Kibana*, *Splunk*, *Azure Monitor*, *Datadog*. Ud fra metrics laver man **dashboards** og **alarmer** (*alerts*): "Send en besked til vagten, hvis fejlraten er over 5 % i 5 minutter."

Som analytiker er overvågning også kilden til svar på forretningsspørgsmål: Hvor mange ansøgninger kom der i går? Hvor lang tid tager det at indsende en?

### Øvelse F

12. Tilskudssystemet fra dag 3 og 5: Skriv 5 spørgsmål om drift, som du ville stille kunden i en workshop. Formulér mindst to af svarene som testbare ikke-funktionelle krav (dag 5).

---

## Aflevering

Commit og push din branch `opgaver/dag-6`, og aflevér via PR:
- `noter/dag-6.md` med svar på øvelse 1, 3, 4 og 12 (og 6, 7 og 9–11, hvis du har lavet fordybelsen)
- dine ændringer i `app.py` (øvelse 3) og evt. `deployment.yaml` (øvelse 10)

## Spørg Claude

- *"Forklar forskellen på et image og en container med en analogi fra laboratoriet."*
- *"Hvorfor deler containere kernen med værten, og hvad betyder det for sikkerheden?"*
- *"Min pod står i CrashLoopBackOff. Hvad betyder det, og hvordan finder jeg årsagen?"*
- *"Forklar RTO og RPO med et eksempel fra et offentligt system."*
- *"Hvad er forskellen på en load balancer, en reverse proxy og en API gateway?"*

## Tjekliste: kan du...

- [ ] forklare, hvilket problem containere løser, og forskellen på en container og en VM?
- [ ] forklare forskellen på image, container, Dockerfile og registry?
- [ ] bygge et image og køre det med port mapping og miljøvariabler?
- [ ] forklare, hvorfor det samme image skal gå fra TEST til PROD?
- [ ] forklare, hvorfor data ikke må ligge inde i en container, og hvad et volume er?
- [ ] forklare pod, deployment og service i Kubernetes, og hvad "deklarativ" betyder?
- [ ] forklare en rolling update og en rollback?
- [ ] forklare IaaS, PaaS, SaaS og on-prem?
- [ ] tegne netværkszonerne og placere load balancer, applikation og database?
- [ ] forklare logs, metrics og traces?

## Ordliste

| Ord | Betydning |
|-----|-----------|
| **drift / ops** | At holde systemer kørende i produktion |
| **DevOps** | Udvikling og drift i samme team og med samme automatisering |
| **container** | Et isoleret, let miljø med et program og alt, det skal bruge |
| **image / tag** | Skabelonen for en container / dens versionsnavn, f.eks. `1.0` |
| **Dockerfile** | Opskriften på et image |
| **registry** | Et lager af images (Docker Hub, ACR, ECR) |
| **VM / hypervisor** | Virtuel maskine / programmet, der kører VM'er |
| **kernel** | Kernen i styresystemet, som containere deler |
| **port mapping** | Port på værten → port i containeren (`-p 8080:8000`) |
| **miljøvariabel** | En indstilling, der bliver givet til et program udefra (`MILJOE=test`) |
| **secret store / vault** | Et sikkert lager for passwords og nøgler |
| **volume** | Lager, der overlever containeren |
| **Docker Compose** | Beskriver og kører flere containere sammen (`compose.yaml`) |
| **Kubernetes / k8s** | Standarden for at orkestrere containere i stor skala |
| **orkestrering** | Automatisk styring af mange containere på mange maskiner |
| **desired state / deklarativ** | Du beskriver det ønskede resultat, og systemet sørger for det |
| **cluster / node** | Samling af maskiner / én maskine i den |
| **pod** | Den mindste enhed i Kubernetes |
| **deployment / replicas** | Kør N kopier af en pod / kopierne |
| **service / load balancing** | Fast navn foran pods / fordeling af trafik |
| **ingress** | Indgang til clusteret udefra |
| **ConfigMap / Secret** | Konfiguration / hemmeligheder i Kubernetes |
| **namespace** | Logisk opdeling af et cluster |
| **readiness / liveness probe** | Er podden klar til trafik? / Er den i live? |
| **rolling update / rollback** | Opdatering uden nedetid / tilbage til forrige version |
| **autoscaling** | Automatisk flere eller færre replicas efter belastning |
| **kubectl / context** | Kommandolinjen til Kubernetes / hvilket cluster den taler med |
| **YAML / manifest** | Tekstformat / en fil, der beskriver Kubernetes-ressourcer |
| **Helm / GitOps / Argo CD** | Skabeloner til manifester / Git som sandheden / værktøj, der udruller fra Git |
| **cloud / on-prem / hybrid** | Lejet hos udbyder / egne servere / en blanding |
| **IaaS / PaaS / SaaS** | Lejede maskiner / lejet platform / lejet færdigt program |
| **managed service** | Udbyderen står for drift af tjenesten |
| **region** | Geografisk placering af en cloud-udbyders datacentre |
| **RTO / RPO** | Hvor hurtigt skal vi være oppe igen? / Hvor meget data har vi råd til at miste? |
| **Infrastructure as Code (IaC)** | Infrastruktur beskrevet i kode (Terraform, Bicep, Pulumi) |
| **load balancer / reverse proxy / API gateway** | Fordeler trafik / server foran applikationen / reverse proxy til API'er |
| **rate limiting** | Begrænsning af antal kald pr. tidsenhed |
| **DMZ / netværkszone** | Den yderste zone mod internettet / adskilte dele af netværket |
| **defense in depth** | Sikkerhed i flere lag |
| **observability** | Evnen til at se, hvordan et system har det |
| **logs / metrics / traces** | Hændelser / tal over tid / en requests rejse |
| **dashboard / alert** | Overblik over metrics / automatisk alarm |
| **CrashLoopBackOff / ImagePullBackOff** | Podden crasher igen og igen / imaget kan ikke hentes |
