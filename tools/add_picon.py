#!/usr/bin/env python3
"""
Picons Contributor CLI Helper: Add & Standardize a Channel
===========================================================
Jednoduchý nástroj pro přispěvatele, který automatizuje celý proces přidání nové stanice:
1. Zkontroluje nebo stáhne surový podklad (SVG / PNG) do source/raw/
2. Vytvoří standardizovaný picon v 640x640 i 1024x1024 (vycentrování, škálování, bezpečné okraje)
3. Automaticky provede audit kvality přes validační engine
4. Zaregistruje zdroj a licenci do source/sources.json
5. Případně vytvoří alias v source/hardlinks.sh

Použití:
  python3 tools/add_picon.py --name "Nova Sport 5" --id "novasport5" --raw "https://example.com/logo.svg" --bg "#003366"
  python3 tools/add_picon.py --name "Moje TV" --id "mojetv" --raw "source/raw/mojetv.png" --bg "#e63946"
"""

import os
import sys
import json
import argparse
import urllib.request
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
DIR_640 = REPO_ROOT / "640"
DIR_1024 = REPO_ROOT / "1024"
RAW_DIR = REPO_ROOT / "source" / "raw"
SOURCES_JSON = REPO_ROOT / "source" / "sources.json"
HARDLINKS_SH = REPO_ROOT / "source" / "hardlinks.sh"

sys.path.append(str(REPO_ROOT / "tools"))
from validate_picons import audit_single_picon, generate_gallery, generate_contact_sheet


def download_raw(url, target_name):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".svg" if ".svg" in url.lower() else ".png"
    dest = RAW_DIR / f"{target_name}_raw{ext}"
    if not dest.exists():
        print(f"📥 Stahuji podklad z {url} do {dest}...")
        req = urllib.request.Request(url, headers={"User-Agent": "AntigravityPiconsBot/1.0"})
        with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
            f.write(resp.read())
    return dest


def standardize_and_save(raw_path, bg_color, base_name, target_ratio=0.68, is_mask=True):
    im = Image.open(raw_path)
    if is_mask:
        if im.mode == "RGBA":
            # If transparent PNG, use alpha
            _, _, _, mask = im.split()
            bbox = mask.getbbox()
            cropped = mask.crop(bbox)
        else:
            # Grayscale invert
            mask = im.convert("L")
            bbox = mask.getbbox()
            cropped = mask.crop(bbox)
    else:
        im_rgba = im.convert("RGBA")
        bbox = im_rgba.split()[3].getbbox()
        cropped = im_rgba.crop(bbox)

    orig_w, orig_h = cropped.size

    for size, out_dir in [(640, DIR_640), (1024, DIR_1024)]:
        canvas = Image.new("RGBA", (size, size), bg_color)
        target_max = int(size * target_ratio)
        scale = target_max / max(orig_w, orig_h)
        new_w = max(1, int(orig_w * scale))
        new_h = max(1, int(orig_h * scale))

        scaled = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
        pos_x = (size - new_w) // 2
        pos_y = (size - new_h) // 2

        if is_mask:
            white = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 255))
            canvas.paste(white, (pos_x, pos_y), scaled)
        else:
            canvas.paste(scaled, (pos_x, pos_y), scaled)

        out_path = out_dir / f"{base_name}.png"
        canvas.save(out_path, "PNG", optimize=True)

    print(f"✅ Vytvořeny picony {base_name}.png v 640/ i 1024/ (poměr: {target_ratio:.0%})")


def register_source(ch_id, name, picon_file, raw_path, origin_url, bg_color, license_str, notes):
    SOURCES_JSON.parent.mkdir(parents=True, exist_ok=True)
    if SOURCES_JSON.exists():
        with open(SOURCES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"title": "Picons Asset Attribution", "channels": []}

    channels = data.get("channels", [])
    # Update existing or append
    existing = next((c for c in channels if c.get("id") == ch_id), None)
    entry = {
        "id": ch_id,
        "name": name,
        "picon": picon_file,
        "source_type": "svg" if str(raw_path).endswith(".svg") else "png_hd",
        "origin_url": origin_url or "Local source",
        "local_raw_path": str(Path(raw_path).relative_to(REPO_ROOT)) if Path(raw_path).is_relative_to(REPO_ROOT) else str(raw_path),
        "license": license_str or "Trademark / Logo",
        "brand_color": bg_color,
        "notes": notes or f"Standardized via add_picon.py"
    }

    if existing:
        existing.update(entry)
    else:
        channels.append(entry)

    data["channels"] = channels
    with open(SOURCES_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"📝 Zaevidováno v source/sources.json")


def main():
    parser = argparse.ArgumentParser(description="Picons Contributor CLI Helper")
    parser.add_argument("--name", required=True, help="Oficiální název stanice (např. 'Nova Sport 5')")
    parser.add_argument("--id", required=True, help="SNP identifikátor bez přípony (např. 'novasport5')")
    parser.add_argument("--raw", required=True, help="Cesta k lokálnímu souboru nebo URL ke stažení")
    parser.add_argument("--bg", required=True, help="Dominantní hex barva pozadí (např. '#003366')")
    parser.add_argument("--ratio", type=float, default=0.68, help="Cílová velikost bounding boxu (výchozí 0.68 = 68%%)")
    parser.add_argument("--color-logo", action="store_true", help="Ponechat původní barvy loga místo bílé siluety")
    parser.add_argument("--url", default="", help="Originální URL původce pro sources.json")
    parser.add_argument("--license", default="Trademark / Logo", help="Licence loga")
    parser.add_argument("--notes", default="", help="Poznámka k převodu")
    args = parser.parse_args()

    ch_id = args.id.lower().strip()
    picon_file = f"{ch_id}.png"

    # 1. Získání surového souboru
    if args.raw.startswith("http://") or args.raw.startswith("https://"):
        raw_path = download_raw(args.raw, ch_id)
    else:
        raw_path = Path(args.raw)
        if not raw_path.exists():
            print(f"❌ Soubor {raw_path} neexistuje!", file=sys.stderr)
            sys.exit(1)

    # 2. Generování piconů
    print(f"\n🎨 Generuji picon pro {args.name} ({ch_id})...")
    standardize_and_save(
        raw_path=raw_path,
        bg_color=args.bg,
        base_name=ch_id,
        target_ratio=args.ratio,
        is_mask=not args.color_logo
    )

    # 3. Okamžitý audit kvality
    print("\n🔍 Validace vytvořených souborů...")
    e640, w640 = audit_single_picon(DIR_640 / picon_file, 640)
    e1024, w1024 = audit_single_picon(DIR_1024 / picon_file, 1024)

    all_errs = e640 + e1024
    all_warns = w640 + w1024

    if all_warns:
        for w in all_warns:
            print(f"  • {w}")
    if all_errs:
        for e in all_errs:
            print(f"  ❌ {e}")
        print("\n❌ Soubory neprošly validací. Upravte parametry ořezu.")
        sys.exit(1)
    else:
        print("  ✅ Validační testy prošly na 100 %!")

    # 4. Registrace do sources.json
    register_source(
        ch_id=ch_id,
        name=args.name,
        picon_file=picon_file,
        raw_path=raw_path,
        origin_url=args.url or (args.raw if args.raw.startswith("http") else ""),
        bg_color=args.bg,
        license_str=args.license,
        notes=args.notes
    )

    # 5. Aktualizace galerie
    print("\n🖼️ Aktualizuji galerii a kontaktní list...")
    generate_gallery()
    generate_contact_sheet()

    print("\n" + "=" * 60)
    print("🎉 Stanice byla úspěšně přidána a zkontrolována!")
    print(f"👉 Zkontrolujte náhled v index.html nebo docs/dvbt2_contact_sheet.png")
    print(f"👉 Pro odeslání do repozitáře: git add 640/ 1024/ source/ && git commit -m 'feat(picons): add {args.name}'")
    print("=" * 60)


if __name__ == "__main__":
    main()
