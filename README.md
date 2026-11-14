# IN1000 & IN1010 Treningsleir + AI (`kode.sask.no`)

En interaktiv øvingsapp for **IN1000 (Python)** og **IN1010 (Java)** ved UiO med AI-veiledning drevet av Google Gemini.

Nettside: [https://kode.sask.no](https://kode.sask.no) (`/` for IN1000 Python, `/java.html` for IN1010 Java).

## Funksjoner

- 35 Python-oppgaver på IN1000-nivå (`index.html`) og 11 Java-oppgaver på IN1010-nivå (`java.html`)
- AI-veiledning for å sjekke svarene dine, simulere output, forklare oppgaver og chatte med AI-veileder
- Uendelig oppgavegenerator for ekstra øving
- Fasit for alle oppgaver og lokal fremgangssporing
- Søkemotoroptimalisering med `robots.txt`, `sitemap.xml`, Open Graph, JSON-LD og rene videresendinger (`/in1000`, `/in1010`)

## Oppsett

### 1. Installer avhengigheter

```bash
python -m pip install -r requirements.txt
```

### 2. Konfigurer API-nøkkel

1. Kopier `.env.example` til `.env`:
   ```bash
   cp .env.example .env
   ```

2. Åpne `.env` og legg inn din Gemini API-nøkkel:
   ```
   GEMINI_API_KEY=din_api_nøkkel_her
   ```

   Få en API-nøkkel fra: https://aistudio.google.com/app/apikey

## Bruk

### Lokal tilgang (kun på denne Mac-en)

```bash
python app.py
```

Åpne i nettleseren: http://127.0.0.1:5000

### Nettverkstilgang (fra andre enheter på samme WiFi)

Serveren er allerede konfigurert for nettverkstilgang. Når du kjører `python app.py`, kan andre enheter på samme WiFi få tilgang til appen.

**Finn din IP-adresse:**

```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Eller sjekk i Systeminnstillinger → Nettverk.

**Koble til fra andre enheter:**

Åpne nettleseren på telefonen/nettbrettet/PC-en og gå til:
```
http://DIN_IP_ADRESSE:5000
```

For eksempel: `http://192.168.1.100:5000`

### Tilgang fra internett (dele med venner på andre nettverk)

For å dele appen med noen som ikke er på samme WiFi, bruk **ngrok** for å lage en sikker tunnel:

**1. Start Flask-serveren:**
```bash
python app.py
```

**2. I et nytt terminalvindu, start ngrok:**
```bash
ngrok http 5001
```

**3. Del URL-en:**

Ngrok vil vise en URL som ser slik ut:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:5001
```

Del `https://abc123.ngrok-free.app` med vennene dine! De kan åpne denne URL-en i nettleseren sin fra hvor som helst i verden.

> [!NOTE]
> - Gratis ngrok-URLer endres hver gang du starter ngrok på nytt
> - Gratis tier har en advarsel-side før brukeren kommer til appen (klikk "Visit Site")
> - Serveren må kjøre på Mac-en din for at ngrok-tunnelen skal fungere

## Feilsøking

### Xcode-lisens

Hvis du får en feilmelding om Xcode-lisens når du bruker Git:

```bash
sudo xcodebuild -license
```

Følg instruksjonene for å godta lisensen.

### Git-konfigurasjon

Hvis Git ber om brukerinformasjon:

```bash
git config --global user.name "Ditt Navn"
git config --global user.email "din.email@eksempel.no"
```

### Brannmur

Hvis andre enheter ikke kan koble til, sjekk at Mac-ens brannmur tillater tilkoblinger på port 5000:

Systeminnstillinger → Nettverk → Brannmur → Alternativer

## Teknologi

- **Backend**: Python, Flask (med rate limiting og opprinnelses-/lengdevalidering på `/api/generate`)
- **Frontend**: HTML, Tailwind CSS, JavaScript (med automatisk systemtema, lyst og mørkt tema)
- **AI**: Google Gemini API

## Lisens

Dette prosjektet er lisensiert under [MIT-lisensen](LICENSE).
