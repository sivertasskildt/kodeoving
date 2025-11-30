# 🌐 Ngrok Guide - Del appen din med venner

Denne guiden viser deg hvordan du deler Python-appen din med venner som ikke er på samme nettverk som deg.

## Hva er ngrok?

Ngrok lager en sikker tunnel fra internett til din lokale server. Det betyr at venner kan få tilgang til appen din selv om de er på et helt annet nettverk!

## Steg-for-steg instruksjoner

### 1️⃣ Start Flask-serveren

Åpne et terminalvindu og kjør:

```bash
cd "/Users/sivertasskildt/VS Code/python_øving"
python app.py
```

Du skal se:
```
Starting server on http://127.0.0.1:5001
```

**La dette terminalvinduet stå åpent!**

---

### 2️⃣ Start ngrok i et nytt terminalvindu

Åpne et **nytt** terminalvindu (⌘+T) og kjør:

```bash
ngrok http 5001
```

Du vil se noe som dette:

```
ngrok                                                                    

Session Status                online
Account                       Free (Limited)
Version                       3.x.x
Region                        Europe (eu)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:5001

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

---

### 3️⃣ Del URL-en med vennen din

Se etter linjen som starter med **"Forwarding"**. Den inneholder din offentlige URL:

```
https://abc123.ngrok-free.app
```

**Del denne URL-en med vennen din!** De kan åpne den i nettleseren sin fra hvor som helst.

---

## 📱 Slik bruker vennen din appen

1. Åpne URL-en du delte (f.eks. `https://abc123.ngrok-free.app`)
2. Ngrok viser en advarsel-side (gratis tier)
3. Klikk på **"Visit Site"** knappen
4. Nå er de inne i appen din! 🎉

---

## ⚠️ Viktig å vite

### Gratis tier-begrensninger:
- ✅ **Fungerer perfekt** for å dele med venner
- ⚠️ URL-en **endres** hver gang du starter ngrok på nytt
- ⚠️ Besøkende må klikke "Visit Site" på en advarsel-side først
- ⚠️ Begrenset antall tilkoblinger per minutt (40 requests/minutt)

### For å stoppe:
- Trykk `Ctrl+C` i ngrok-terminalvinduet for å stoppe tunnelen
- Trykk `Ctrl+C` i Flask-terminalvinduet for å stoppe serveren

### Hvis du vil ha en permanent URL:
- Opprett en gratis ngrok-konto på [ngrok.com](https://ngrok.com)
- Autentiser med: `ngrok authtoken <din_token>`
- Bruk en statisk domene (krever betalt plan) eller bruk samme URL med `ngrok http 5001 --domain=<ditt-domene>`

---

## 🔍 Feilsøking

### "command not found: ngrok"
Ngrok er ikke installert. Installer med:
```bash
brew install ngrok
```

### "Failed to listen on localhost:5001"
Flask-serveren kjører ikke. Start den først med `python app.py`.

### Vennen din får "502 Bad Gateway"
Flask-serveren har stoppet. Sjekk at `python app.py` fortsatt kjører.

### Ngrok-tunnelen stopper
Gratis tier har ingen tidsbegrensning, men hvis Mac-en går i dvale, stopper tunnelen. Hold Mac-en våken mens du deler.

---

## 🎯 Rask oppsummering

```bash
# Terminal 1: Start Flask
python app.py

# Terminal 2: Start ngrok
ngrok http 5001

# Del URL-en som vises (f.eks. https://abc123.ngrok-free.app)
```

**Det er alt!** 🚀
