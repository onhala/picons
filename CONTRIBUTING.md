# 🤝 Příručka pro přispěvatele (Contributing Guide)

Děkujeme za zájem o rozvoj a vylepšování balíčku piconů! Aby si celá sada udržela profesionální vizuální standard, maximální ostrost a 100% stabilitu v klientských aplikacích (Tvheadend, Kodi, Apple TV TvhClient, Enigma2), dodržujte prosím následující pravidla a postupy.

---

## 🎨 Designový standard Marhyho Piconů

1. **Čtvercový formát 1:1 a dvojí rozlišení:**
   - Každá stanice musí existovat ve dvou identických rozlišeních:
     - `640/` ➔ **640×640 px** (pro standardní 1080p obrazovky, Kodi a Enigma2).
     - `1024/` ➔ **1024×1024 px** (pro 4K televize a Apple Retina displeje).
   - Formát: **8-bit RGBA PNG** s plně neprůhledným podkladem dlaždice.

2. **Dominantní barva a bezpečné okraje:**
   - Pozadí tvoří sytá primární barva stanice (případně její oficiální barevný gradient).
   - Logo je čistě bílé (`#ffffff`), vycentrované vodorovně i svisle.
   - **Velikost loga:** Maximální rozměr loga (šířka nebo výška) je standardizován na **65 % až 72 % canvasu** (cca 435–460 px u 640px verze).
   - **Bezpečný odstup (Safe Margin):** Logo nesmí zasahovat blíže než **5 % od okraje canvasu** (zákaz oříznutí / canvas overflow).

3. **Pojmenování souborů (SNP standard):**
   - Všechny soubory jsou pojmenovány malými písmeny bez mezer a diakritiky: např. `novasport5.png`, `warnertv.png`.
   - Alternativní názvy multiplexů a aliasy (např. `test4.png` ➔ `warnertv.png`) se definují v [`source/hardlinks.sh`](source/hardlinks.sh).

---

## ⚡ Rychlý start pro vývojáře

1. **Naklonujte repozitář a nainstalujte závislosti:**
   ```bash
   git clone https://github.com/onhala/picons.git
   cd picons
   make install
   ```

2. **Spusťte stávající sadu testů:**
   ```bash
   make test
   ```

---

## 🚀 Jak přidat novou stanici (2 způsoby)

### Možnost A: Přidání přes CLI asistenta (Doporučeno)

K dispozici je automatizovaný skript [`tools/add_picon.py`](tools/add_picon.py), který provede stažení, normalizaci, vycentrování, validaci i zápis do manifestu v jediném kroku:

```bash
# Ze vzdáleného SVG / PNG URL (např. z Wikimedia Commons):
python3 tools/add_picon.py \
  --name "Nova Sport 5" \
  --id "novasport5" \
  --raw "https://upload.wikimedia.org/wikipedia/commons/.../Logo.svg" \
  --bg "#003366" \
  --url "https://tv.nova.cz/"

# Nebo z lokálního surového souboru:
python3 tools/add_picon.py \
  --name "Moje TV" \
  --id "mojetv" \
  --raw "source/raw/mojetv.png" \
  --bg "#e63946"
```

Nástroj automaticky:
- Vytvoří `640/novasport5.png` a `1024/novasport5.png`.
- Spustí validační test na obou rozlišeních.
- Zaeviduje licenci a původ do [`source/sources.json`](source/sources.json).
- Přegeneruje interaktivní galerii [index.html](index.html) i kontaktní list [docs/dvbt2_contact_sheet.png](docs/dvbt2_contact_sheet.png).

---

### Možnost B: Ruční přidání nebo kompozice

Pokud stanice vyžaduje specifickou typografii nebo kombinaci prvků (jako např. `jc1` nebo `ockostar`):

1. Uložte původní surový podklad do [`source/raw/<nazev>_raw.png`](source/raw/) nebo `.svg`.
2. Využijte standardizovanou funkci `create_standardized_picon()` v [`generate_missing_picons.py`](generate_missing_picons.py):
   ```python
   create_standardized_picon(raw_mask, bg_color="#003366", base_name="novasport5", target_ratio=0.68)
   ```
3. Otestujte konkrétní picon bleskovým lokálním auditem:
   ```bash
   python3 tools/validate_picons.py --file 640/novasport5.png
   ```

---

## 🛠️ Příkazy Make

| Příkaz | Popis |
| :--- | :--- |
| `make test` / `make validate` | Spustí kompletní kontrolu všech 1232 piconů, parity a manifestu |
| `make gallery` | Validuje repozitář a zaktualizuje `index.html` i kontaktní list |
| `make fix` | Automaticky doplní chybějící velikosti z jednoho rozlišení do druhého |
| `make build-missing` | Přegeneruje celou DVB-T2 sadu přes `generate_missing_picons.py` |
| `make clean` | Odstraní dočasné mezisoubory |

---

## 🔍 Co kontroluje Validační Pipeline

Při každém pushi a v každém Pull Requestu spouští GitHub Actions kontrolu:

- `ERR_DIMENSIONS`: Picon musí mít přesně 640×640 px nebo 1024×1024 px.
- `ERR_PARITY`: Každá stanice musí mít obě velikosti (640 i 1024).
- `ERR_CANVAS_OVERFLOW`: Logo nesmí zasahovat přímo do okraje canvasu (margin < 5 %).
- `ERR_TOO_SMALL` / `WARN_SMALL`: Logo nesmí být mikroskopické (max rozměr < 30 %).
- `ERR_SOLID_BLOCK`: Odhaluje chyby v maskování (plný neprůhledný blok bez výřezu písmen).
- `ERR_SOURCES_PICON_MISSING`: Zabraňuje rozbitým odkazům v [`source/sources.json`](source/sources.json).

---

## 📤 Odeslání Pull Requestu

1. Vytvořte si novou větev:
   ```bash
   git checkout -b feat/nova-sport-5
   ```
2. Zkontrolujte, že `make gallery` proběhne s **0 chybami**.
3. Commitněte změny podle konvence [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat(picons): add Nova Sport 5 picon"
   ```
4. Pošlete Pull Request na GitHubu. Naše automatická CI pipeline váš návrh okamžitě otestuje!
