# 📂 Původ a zdrojové podklady log (Asset Attribution & Raw Sources)

Tento dokument a přidružená složka [`source/raw/`](file:///Users/ondre/Projects/picons/source/raw/) evidují původ všech zdrojových souborů, master vektorů a podkladů před jejich zpracováním a transformací do Marhyho plochého designového systému.

Cílem je zajistit **100% reprodukovatelnost**, otevřenost pro další vývojáře/přispěvatele a transparentní evidenci licencí a ochranných známek.

---

## 🗂️ Struktura zdrojových podkladů

- **`source/svg/`**: Originální vektorové SVG soubory rozdělené podle regionů (`CZ-SK`, `DE-AT`, `International`, `PL`, `Radio`, `UA`, `US`).
- **`source/raw/`**: Původní nezpracované soubory (vektory SVG, oficiální PNG mastery ve vysokém rozlišení z Wikimedia Commons a webů stanic).
- **`source/sources.json`**: Strojově čitelný manifest (JSON Schema) mapující každý picon na zdrojový soubor, URL původce, barvu a licenci.
- **`source/hardlinks.sh`**: Skript spravující aliasy a hardlinky pro alternativní názvy stanic.

---

## 📋 Přehled zdrojů nově doplněných a DVB-T2 stanic

| Stanice | Výsledný picon | Typ podkladu | Původní soubor v repozitáři | Zdroj / Původce | Barva pozadí |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **Warner TV** | `warnertv.png` | PNG Master | [`source/raw/warnertv_raw.png`](file:///Users/ondre/Projects/picons/source/raw/warnertv_raw.png) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:WarnerTV_2021.png) | `#002244` |
| **Nova Krimi** | `novakrimi.png` | PNG Master | [`source/raw/novakrimi_raw.png`](file:///Users/ondre/Projects/picons/source/raw/novakrimi_raw.png) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Logo_Nova_Krimi.png) | `#800020` |
| **JTV (Jihočeská TV)** | `jtv.png` | PNG HD | [`source/raw/jtv_raw.png`](file:///Users/ondre/Projects/picons/source/raw/jtv_raw.png) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Logo_JTV.png) | `#004b97` |
| **JČ1 (Jihočeská TV 1)**| `jc1.png` | Vector / Typography | [`source/raw/jc1_raw.png`](file:///Users/ondre/Projects/picons/source/raw/jc1_raw.png) | [jc1.cz](https://www.jc1.cz/) / Vektorová rekonstrukce | `#0080c0` |
| **JČ2 (Jihočeská TV 2)**| `jc2.png` | Vector / Typography | [`source/raw/jc1_raw.png`](file:///Users/ondre/Projects/picons/source/raw/jc1_raw.png) | Identický brand layout jako JČ1 | `#0080c0` |
| **Seznam.cz TV** | `seznamcztv.png` | Vector | [`640/seznamtv.png`](file:///Users/ondre/Projects/picons/640/seznamtv.png) | [Seznam.cz Media Kit](https://o.seznam.cz/pro-media/) | `#de0a17` |
| **ÓČKO STAR** | `ockostar.png` | Vektorová kompozice | [`source/svg/CZ-SK/ocko.svg`](file:///Users/ondre/Projects/picons/source/svg/CZ-SK/ocko.svg) | MAFRA / STANICE O s.r.o. | `#f89c0e` |
| **Prima SPORT** | `primasport.png` | Vektorová kompozice | [`source/svg/CZ-SK/prima.svg`](file:///Users/ondre/Projects/picons/source/svg/CZ-SK/prima.svg) | FTV Prima | `#f36917` |
| **A11 TV** | `a11.png` | Vektorové SVG | [`generate_missing_picons.py`](file:///Users/ondre/Projects/picons/generate_missing_picons.py) | [a11.cz](https://a11.cz/) | `#0055b8` |
| **ČRo Pohoda** | `cropohodat2.png` | Škálovatelné SVG | [`source/raw/cro_pohoda.svg`](file:///Users/ondre/Projects/picons/source/raw/cro_pohoda.svg) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:%C4%8CRo_Pohoda_Logo_2021.svg) | `#800080` |
| **ČRo Rádiožurnál Sport** | `crorzsportt2.png` | Škálovatelné SVG | [`source/raw/cro_rz_sport.svg`](file:///Users/ondre/Projects/picons/source/raw/cro_rz_sport.svg) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:%C4%8CRo_Radio%C5%BEurn%C3%A1l_Sport_Logo_2021.svg) | `#00a651` |
| **Rádio Impuls** | `radioimpuls.png` | HD Master (1915×756) | [`source/raw/impuls_raw.png`](file:///Users/ondre/Projects/picons/source/raw/impuls_raw.png) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:R%C3%A1dio_Impuls.png) | `#f5a623` |
| **Český Impuls** | `ceskyimpuls.png` | PNG HD | [`source/raw/cesky_impuls_raw.png`](file:///Users/ondre/Projects/picons/source/raw/cesky_impuls_raw.png) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:%C4%8Cesk%C3%BD_Impuls.png) | `#0b2545` |
| **Radio Čas** | `radiocas.png` | Škálovatelné SVG | [`source/raw/radio_cas.svg`](file:///Users/ondre/Projects/picons/source/raw/radio_cas.svg) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Logo_Radio_%C4%8Cas.svg) | `#ffc107` |
| **Radio Čas Rock** | `radiocasrock.png` | SVG kompozice | [`source/raw/radio_cas.svg`](file:///Users/ondre/Projects/picons/source/raw/radio_cas.svg) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Logo_Radio_%C4%8Cas.svg) | `#1a1a1a` |
| **Rádio Dechovka** | `radiodechovka.png` | HD Master (2775×1269) | [`source/raw/dechovka_raw.png`](file:///Users/ondre/Projects/picons/source/raw/dechovka_raw.png) | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Logo_Radia_Dechovka_s_kmito%C4%8Dty.png) | `#800020` |
| **Hit TV** | `hittv.png` | Vector Render | [`generate_missing_picons.py`](file:///Users/ondre/Projects/picons/generate_missing_picons.py) | [hittelevize.cz](https://www.hittelevize.cz/) | `#d90429` |
| **ABC TV** | `abctv.png` | Vector Render | [`generate_missing_picons.py`](file:///Users/ondre/Projects/picons/generate_missing_picons.py) | [abctv.cz](https://abctv.cz/) | `#00509d` |
| **Rock Zone 105.9** | `rockzone1059.png` | Vector Render | [`generate_missing_picons.py`](file:///Users/ondre/Projects/picons/generate_missing_picons.py) | Media Bohemia | `#111111` |
| **Ukrajinske Radio** | `ukrajinskeradio.png` | Vector Render | [`generate_missing_picons.py`](file:///Users/ondre/Projects/picons/generate_missing_picons.py) | [suspilne.media](https://suspilne.media/) | `#0057b7` |
| **CRA DVB-T2 Info** | `naladtesenadigitalnivysilanicra.png` | Vector Render | [`generate_missing_picons.py`](file:///Users/ondre/Projects/picons/generate_missing_picons.py) | České Radiokomunikace a.s. | `#003366` |
| **Test MUX 24** | `dbtest1.png` | Vector Render | [`generate_missing_picons.py`](file:///Users/ondre/Projects/picons/generate_missing_picons.py) | Digital Broadcasting s.r.o. | `#2b2d42` |

---

## 🛠️ Postup pro přispěvatele (Jak přidat novou stanici)

1. **Uložení surového podkladu:**
   Stáhněte vektor (SVG) nebo originální HD PNG z Wikimedia Commons / tiskového media kitu stanice a uložte jej do `source/raw/<nazev_stanice>_raw.svg` nebo `.png`.
2. **Zaevidování v manifestu:**
   Přidejte položku do [`source/sources.json`](file:///Users/ondre/Projects/picons/source/sources.json) s URL původce, licencí a dominantní barvou značky.
3. **Generování piconu:**
   Použijte standardizovanou pipeline v [`generate_missing_picons.py`](file:///Users/ondre/Projects/picons/generate_missing_picons.py):
   ```python
   create_standardized_picon(raw_mask, bg_color="#RRGGBB", base_name="stanice", target_ratio=0.68)
   ```
4. **Validace a kontrolní list:**
   Spusťte audit před commitem:
   ```bash
   python3 tools/validate_picons.py --gallery
   ```
