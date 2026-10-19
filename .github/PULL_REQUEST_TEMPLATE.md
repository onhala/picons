## 📋 Popis změn / PR Summary
<!-- Stručně popište, jakou stanici nebo opravu tento Pull Request přináší. -->

- **Název stanice:** 
- **Soubor piconu:** `640/<nazev>.png` a `1024/<nazev>.png`
- **Zdrojový podklad:** `source/raw/...` (nebo odkaz na Wikimedia Commons / media kit)
- **Dominantní barva:** `#......`

---

## ✅ Kontrolní seznam před odesláním (Contributor Checklist)
Před odesláním PR se ujistěte, že jste splnili následující kritéria:

- [ ] **Parita rozlišení:** Picon je nahrán v obou složkách `640/` (640×640 px) i `1024/` (1024×1024 px).
- [ ] **Pravidla designu:** Logo je vycentrované, má syté plné pozadí značky a nezasahuje do zakázaného okraje (< 5 %).
- [ ] **Surový podklad:** Zdrojový soubor (SVG nebo HD PNG master) je uložen v [`source/raw/`](source/raw/).
- [ ] **Evidence v manifestu:** Stanice je zaevidována v [`source/sources.json`](source/sources.json).
- [ ] **Aliasy (volitelné):** Pokud má stanice alternativní názvy v DVB multiplexech, je přidán záznam do [`source/hardlinks.sh`](source/hardlinks.sh).
- [ ] **Validační audit prošel bez chyb:** Spuštěn příkaz `make gallery` nebo `python3 tools/validate_picons.py --gallery` (0 chyb).
