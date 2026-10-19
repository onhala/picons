#!/usr/bin/env python3
"""
Generate missing CZ/SK picons in Marhy's signature flat rectangular style:
- 640x640 px and 1024x1024 px PNG
- Solid brand-colored background
- Clean, centered silhouette/mark (~68% bounding box)
- Automated scale standardization and canvas overflow prevention
"""

import os
import re
import sys
import subprocess
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent
DIR_640 = REPO_ROOT / "640"
DIR_1024 = REPO_ROOT / "1024"
TMP_DIR = Path("/tmp/picon_sources")

TMP_DIR.mkdir(parents=True, exist_ok=True)
DIR_640.mkdir(parents=True, exist_ok=True)
DIR_1024.mkdir(parents=True, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def render_html_to_png(html_content, out_path, size):
    html_file = TMP_DIR / f"temp_{size}.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        f"--screenshot={out_path}",
        f"--window-size={size},{size}",
        str(html_file)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def download_file(url, local_path):
    local_path = Path(local_path)
    if not local_path.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "AntigravityBot/1.0 (ondrej.hala@roboton.com)"})
        with urllib.request.urlopen(req) as resp, open(local_path, "wb") as out:
            out.write(resp.read())
    return str(local_path)


def create_standardized_picon(content, bg_color, base_name, target_ratio=0.68, is_mask=True):
    """
    Standardize picon to exact square bounds with uniform sizing, centering, and margin breathing room:
    - content: PIL Image (L mask or RGBA image)
    - bg_color: Hex string (e.g. '#0080c0') or RGB/RGBA tuple
    - target_ratio: Proportion of canvas to occupy on maximum dimension (default 68%)
    - is_mask: If True, treats content as alpha mask for pure white silhouette. If False, pastes scaled RGBA directly.
    """
    if is_mask:
        bbox = content.getbbox()
    else:
        alpha = content.split()[3] if content.mode == "RGBA" else content.convert("RGBA").split()[3]
        bbox = alpha.getbbox()

    if not bbox:
        raise ValueError(f"Content for {base_name} has empty bounding box!")

    cropped = content.crop(bbox)
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

    print(f"  ✨ [STANDARDIZED] {base_name}.png (640 & 1024, max_dim={target_ratio:.0%})")


def make_symlink(src_name, target_name):
    for d in [DIR_640, DIR_1024]:
        src = d / f"{src_name}.png"
        dst = d / f"{target_name}.png"
        if dst.exists() or dst.is_symlink():
            dst.unlink()
        if src.exists():
            os.link(src, dst)
            print(f"  🔗 [HARDLINK] {target_name}.png -> {src_name}.png in {d.name}/")


def main():
    print("=" * 65)
    print("🚀 Picon Builder & Scale Normalization Pipeline")
    print("=" * 65)

    # 1. Seznam.cz TV (fix clipped white S)
    print("\n--- 1. Seznam.cz TV ---")
    seznam_src = DIR_640 / "seznamtv.png"
    if seznam_src.exists():
        im_s = Image.open(seznam_src).convert("RGB")
        mask_s = Image.new("L", im_s.size, 0)
        for x in range(im_s.width):
            for y in range(im_s.height):
                r, g, b = im_s.getpixel((x, y))
                gb_avg = (g + b) / 2.0
                val = int(max(0, min(255, (255.0 - gb_avg) / (255.0 - 16.5) * 255.0)))
                mask_s.putpixel((x, y), val)
        create_standardized_picon(mask_s, "#de0a17", "seznamcz", target_ratio=0.68, is_mask=True)
        make_symlink("seznamcz", "seznamcztv")
        make_symlink("seznamcz", "seznamcztvt2")

    # 2. Warner TV
    print("\n--- 2. Warner TV ---")
    warnertv_raw = download_file(
        "https://upload.wikimedia.org/wikipedia/commons/c/c9/WarnerTV_2021.png",
        TMP_DIR / "warnertv_raw.png"
    )
    w_im = Image.open(warnertv_raw).convert("RGBA")
    _, _, _, w_mask = w_im.split()
    create_standardized_picon(w_mask, "#002244", "warnertv", target_ratio=0.68, is_mask=True)
    make_symlink("warnertv", "test4")

    # 3. Nova Krimi
    print("\n--- 3. Nova Krimi ---")
    novakrimi_raw = download_file(
        "https://upload.wikimedia.org/wikipedia/commons/7/7b/Logo_Nova_Krimi.png",
        TMP_DIR / "novakrimi_raw.png"
    )
    raw_nk = Image.open(novakrimi_raw).convert("RGB")
    bg_nk = (128, 54, 38)
    mask_nk = Image.new("L", raw_nk.size, 0)
    for x in range(raw_nk.width):
        for y in range(raw_nk.height):
            px = raw_nk.getpixel((x, y))
            if max(abs(px[0] - bg_nk[0]), abs(px[1] - bg_nk[1]), abs(px[2] - bg_nk[2])) > 35:
                mask_nk.putpixel((x, y), 255)
    create_standardized_picon(mask_nk, "#800020", "novakrimi", target_ratio=0.68, is_mask=True)

    # 4. A11
    print("\n--- 4. A11 ---")
    a11_html = """<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#0055b8;display:flex;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 460" style="width:70vw;height:auto;fill:#ffffff;">
    <path d="m509.4 207.7l-74-88.6q19.2-15.9 41.2-36.3 22-20.3 43.1-42 21-21.7 36.3-40.1h140.4v458.6h-127.6v-303.2q-11.5 13.4-27.1 26.8-15.7 13.3-32.3 24.8z"></path>
    <path d="m813 207.7l-74-88.6q19.2-15.9 41.2-36.3 22-20.3 43-42 21.1-21.7 36.4-40.1h140.4v458.6h-127.6v-303.2q-11.5 13.4-27.1 26.8-15.7 13.3-32.3 24.8z"></path>
    <path d="m215.8 459.3h-135.3l154.5-458.6h157l154.5 458.6h-134.7l-26.2-82.3h-143.6zm44.7-172.9h95.1l-47.2-149.3z"></path>
    </svg>
    </body></html>"""
    render_html_to_png(a11_html, DIR_640 / "a11.png", 640)
    render_html_to_png(a11_html, DIR_1024 / "a11.png", 1024)
    print("  ✨ Generated a11.png")

    # 5. JTV
    print("\n--- 5. JTV ---")
    jtv_raw = download_file(
        "https://upload.wikimedia.org/wikipedia/commons/f/f0/Logo_JTV.png",
        TMP_DIR / "jtv_raw.png"
    )
    jtv_im = Image.open(jtv_raw).convert("RGBA")
    _, _, _, jtv_mask = jtv_im.split()
    create_standardized_picon(jtv_mask, "#004b97", "jtv", target_ratio=0.68, is_mask=True)

    # 6. JČ1 & JČ2 (Jihočeská televize 1 & 2)
    print("\n--- 6. JČ1 & JČ2 ---")
    def build_jc_channel(digit):
        for size, out_dir in [(640, DIR_640), (1024, DIR_1024)]:
            scale = size / 640.0
            bg_color = (0, 128, 192, 255)

            font_path = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
            font_size_jc = int(175 * scale)
            font_jc = ImageFont.truetype(font_path, font_size_jc)

            # Measure JČ text bounds
            dummy = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            d_draw = ImageDraw.Draw(dummy)
            tb_jc = d_draw.textbbox((0, 0), "JČ", font=font_jc)
            w_jc = tb_jc[2] - tb_jc[0]
            h_jc = tb_jc[3] - tb_jc[1]

            # Capsule properties
            capsule_w = int(140 * scale)
            capsule_h = int(190 * scale)
            gap = int(28 * scale)
            corner_radius = int(36 * scale)

            total_w = w_jc + gap + capsule_w
            start_x = (size - total_w) // 2
            start_y_capsule = (size - capsule_h) // 2
            start_y_jc = (size - h_jc) // 2 - tb_jc[1]

            canvas = Image.new("RGBA", (size, size), bg_color)
            draw = ImageDraw.Draw(canvas)

            # 1. Clean vector JČ text
            draw.text((start_x - tb_jc[0], start_y_jc), "JČ", font=font_jc, fill=(255, 255, 255, 255))

            # 2. Rounded white capsule
            capsule_x = start_x + w_jc + gap
            draw.rounded_rectangle(
                [capsule_x, start_y_capsule, capsule_x + capsule_w, start_y_capsule + capsule_h],
                radius=corner_radius,
                fill=(255, 255, 255, 255)
            )

            # 3. Cutout number inside capsule
            font_size_num = int(145 * scale)
            font_num = ImageFont.truetype(font_path, font_size_num)
            tb_num = draw.textbbox((0, 0), str(digit), font=font_num)
            nw = tb_num[2] - tb_num[0]
            nh = tb_num[3] - tb_num[1]
            num_x = capsule_x + (capsule_w - nw) // 2 - tb_num[0]
            num_y = start_y_capsule + (capsule_h - nh) // 2 - tb_num[1]
            draw.text((num_x, num_y), str(digit), font=font_num, fill=bg_color)

            out_path = out_dir / f"jc{digit}.png"
            canvas.save(out_path, "PNG", optimize=True)
            print(f"  ✨ Generated jc{digit}.png in {out_dir.name}/ (clean vector JČ, zero artifacts)")

    build_jc_channel(1)
    build_jc_channel(2)

    # 7. Prima Sport
    print("\n--- 7. Prima Sport ---")
    prima_svg_path = REPO_ROOT / "source/svg/CZ-SK/prima.svg"
    with open(prima_svg_path, "r", encoding="utf-8") as f:
        prima_svg = f.read()
    prima_sport_html = f"""<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#f36917;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="width:65vw;height:auto;display:flex;justify-content:center;">
    {prima_svg.replace('class="cls-1"', 'style="display:none;"').replace('viewBox="0 0 283.46 283.46"', 'viewBox="40 100 200 90" style="width:100%;height:auto;"')}
    </div>
    <div style="font-family:'Arial Black', Impact, sans-serif;font-size:11vw;font-weight:900;color:#ffffff;letter-spacing:1.2vw;margin-top:2vh;">SPORT</div>
    </body></html>"""
    render_html_to_png(prima_sport_html, DIR_640 / "primasport.png", 640)
    render_html_to_png(prima_sport_html, DIR_1024 / "primasport.png", 1024)
    print("  ✨ Generated primasport.png")

    # 8. Óčko Star (matching ÓČKO size with bold STAR underneath)
    print("\n--- 8. Óčko Star ---")
    ocko_src = DIR_640 / "ocko.png"
    if ocko_src.exists():
        im_ocko = Image.open(ocko_src).convert("RGBA")
        ocko_mask = Image.new("L", im_ocko.size, 0)
        for x in range(im_ocko.width):
            for y in range(im_ocko.height):
                r, g, b, a = im_ocko.getpixel((x, y))
                if r > 200 and g > 200 and b > 200:
                    ocko_mask.putpixel((x, y), 255)
                elif r > 150 and g > 80 and b > 80:
                    ocko_mask.putpixel((x, y), int((g + b) / 2))
        cropped_ocko = ocko_mask.crop(ocko_mask.getbbox())

        bg_ocko_star = (248, 156, 14, 255)
        for size, out_dir in [(640, DIR_640), (1024, DIR_1024)]:
            scale = size / 640.0
            w_ocko = int(cropped_ocko.width * scale)
            h_ocko = int(cropped_ocko.height * scale)
            scaled_ocko = cropped_ocko.resize((w_ocko, h_ocko), Image.Resampling.LANCZOS)

            canvas = Image.new("RGBA", (size, size), bg_ocko_star)
            draw = ImageDraw.Draw(canvas)

            font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
            font_size = int(82 * scale)
            font = ImageFont.truetype(font_path, font_size)
            star_text = "S T A R"
            tb = draw.textbbox((0, 0), star_text, font=font)
            tw, th = tb[2] - tb[0], tb[3] - tb[1]

            total_h = h_ocko + int(40 * scale) + th
            start_y = (size - total_h) // 2

            white_ocko = Image.new("RGBA", (w_ocko, h_ocko), (255, 255, 255, 255))
            canvas.paste(white_ocko, ((size - w_ocko) // 2, start_y), scaled_ocko)

            star_y = start_y + h_ocko + int(36 * scale)
            star_x = (size - tw) // 2 - tb[0]
            draw.text((star_x, star_y), star_text, font=font, fill=(255, 255, 255, 255))

            out_path = out_dir / "ockostar.png"
            canvas.save(out_path, "PNG", optimize=True)
            print(f"  ✨ Generated ockostar.png in {out_dir.name}/")

    # 9. Hit TV
    print("\n--- 9. Hit TV ---")
    hittv_html = """<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#d90429;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="border:1.2vw solid #ffffff;border-radius:3vw;padding:2vw 6vw;display:flex;flex-direction:column;align-items:center;">
      <div style="font-family:'Arial Black', Impact, sans-serif;font-size:20vw;font-weight:900;color:#ffffff;line-height:0.85;letter-spacing:-0.5vw;">HIT</div>
      <div style="font-family:'Helvetica Neue', Arial, sans-serif;font-size:9vw;font-weight:900;color:#ffffff;letter-spacing:1.5vw;margin-top:1vw;">TELEVIZE</div>
    </div>
    </body></html>"""
    render_html_to_png(hittv_html, DIR_640 / "hittv.png", 640)
    render_html_to_png(hittv_html, DIR_1024 / "hittv.png", 1024)
    make_symlink("hittv", "test5")

    # 10. ABC TV
    print("\n--- 10. ABC TV ---")
    abctv_html = """<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#00509d;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="display:flex;align-items:baseline;">
      <span style="font-family:'Arial Black', Impact, sans-serif;font-size:24vw;font-weight:900;color:#ffffff;letter-spacing:-1vw;">ABC</span>
      <span style="font-family:'Helvetica Neue', Arial, sans-serif;font-size:12vw;font-weight:900;color:#ffffff;margin-left:2vw;">TV</span>
    </div>
    </body></html>"""
    render_html_to_png(abctv_html, DIR_640 / "abctv.png", 640)
    render_html_to_png(abctv_html, DIR_1024 / "abctv.png", 1024)

    # 11. ČRo Pohoda
    print("\n--- 11. ČRo Pohoda ---")
    pohoda_svg_path = download_file(
        "https://upload.wikimedia.org/wikipedia/commons/8/84/%C4%8CRo_Pohoda_Logo_2021.svg",
        TMP_DIR / "cro_pohoda.svg"
    )
    with open(pohoda_svg_path, "r", encoding="utf-8") as f:
        pohoda_svg = f.read()
    pohoda_html = f"""<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#800080;display:flex;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="width:70vw;height:auto;filter:brightness(0) invert(1);">
    {pohoda_svg}
    </div>
    </body></html>"""
    render_html_to_png(pohoda_html, DIR_640 / "cropohodat2.png", 640)
    render_html_to_png(pohoda_html, DIR_1024 / "cropohodat2.png", 1024)
    make_symlink("cropohodat2", "cropohoda")

    # 12. ČRo Radiožurnál Sport
    print("\n--- 12. ČRo Radiožurnál Sport ---")
    rz_sport_svg_path = download_file(
        "https://upload.wikimedia.org/wikipedia/commons/6/6b/%C4%8CRo_Radio%C5%BEurn%C3%A1l_Sport_Logo_2021.svg",
        TMP_DIR / "cro_rz_sport.svg"
    )
    with open(rz_sport_svg_path, "r", encoding="utf-8") as f:
        rz_sport_svg = f.read()
    rz_sport_html = f"""<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#00a651;display:flex;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="width:70vw;height:auto;filter:brightness(0) invert(1);">
    {rz_sport_svg}
    </div>
    </body></html>"""
    render_html_to_png(rz_sport_html, DIR_640 / "crorzsportt2.png", 640)
    render_html_to_png(rz_sport_html, DIR_1024 / "crorzsportt2.png", 1024)
    make_symlink("crorzsportt2", "croradiozurnalsport")

    # 13. Radio Impuls (HD official vector-quality source on brand yellow)
    print("\n--- 13. Radio Impuls ---")
    impuls_raw = download_file(
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/R%C3%A1dio_Impuls.png",
        TMP_DIR / "impuls_raw.png"
    )
    hd_imp = Image.open(impuls_raw).convert("RGBA")
    create_standardized_picon(hd_imp, "#f5a623", "radioimpuls", target_ratio=0.70, is_mask=False)

    # 14. Český Impuls
    print("\n--- 14. Český Impuls ---")
    ci_html = """<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#0b2545;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="font-family:'Arial Black', Impact, sans-serif;font-size:16vw;font-weight:900;color:#ffffff;line-height:0.9;letter-spacing:-0.5vw;">ČESKÝ</div>
    <div style="font-family:'Arial Black', Impact, sans-serif;font-size:16vw;font-weight:900;color:#f5a623;line-height:0.9;letter-spacing:-0.5vw;margin-top:1.5vh;">IMPULS</div>
    <div style="font-family:'Helvetica Neue', Arial, sans-serif;font-size:6.5vw;font-weight:700;color:#ffffff;letter-spacing:0.8vw;margin-top:2.5vh;">RÁDIO PRO POHODU</div>
    </body></html>"""
    render_html_to_png(ci_html, DIR_640 / "ceskyimpuls.png", 640)
    render_html_to_png(ci_html, DIR_1024 / "ceskyimpuls.png", 1024)

    # 15. Radio Čas & Čas Rock
    print("\n--- 15. Radio Čas & Rock ---")
    cas_svg_path = download_file(
        "https://upload.wikimedia.org/wikipedia/commons/e/ed/Logo_Radio_%C4%8Cas.svg",
        TMP_DIR / "radio_cas.svg"
    )
    with open(cas_svg_path, "r", encoding="utf-8") as f:
        cas_svg = f.read()
    cas_svg_scalable = re.sub(r'(width|height)="[^"]+"', '', cas_svg)

    cas_html = f"""<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#ffc107;display:flex;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="width:72vw;height:auto;filter:brightness(0) invert(1);">
    {cas_svg_scalable}
    </div>
    </body></html>"""
    render_html_to_png(cas_html, DIR_640 / "radiocas.png", 640)
    render_html_to_png(cas_html, DIR_1024 / "radiocas.png", 1024)

    cas_rock_html = f"""<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#1a1a1a;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="width:68vw;height:auto;filter:brightness(0) invert(1);">
    {cas_svg_scalable}
    </div>
    <div style="font-family:'Arial Black', Impact, sans-serif;font-size:14vw;font-weight:900;color:#ffffff;letter-spacing:1vw;margin-top:2vh;">ROCK</div>
    </body></html>"""
    render_html_to_png(cas_rock_html, DIR_640 / "radiocasrock.png", 640)
    render_html_to_png(cas_rock_html, DIR_1024 / "radiocasrock.png", 1024)

    # 16. Radio Dechovka (full descenders without frequency clutter)
    print("\n--- 16. Radio Dechovka ---")
    dechovka_raw = download_file(
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/Logo_Radia_Dechovka_s_kmito%C4%8Dty.png",
        TMP_DIR / "dechovka_raw.png"
    )
    raw_dec = Image.open(dechovka_raw).convert("RGBA")
    bbox_dec = raw_dec.split()[3].getbbox()
    cropped_dec = raw_dec.crop(bbox_dec)
    # y=950 separates the letters from the frequency text
    dechovka_letters = cropped_dec.crop((0, 0, cropped_dec.width, 950))
    mask_dec = dechovka_letters.split()[3]
    create_standardized_picon(mask_dec, "#800020", "radiodechovka", target_ratio=0.68, is_mask=True)

    # 17. Rock Zone 105,9
    print("\n--- 17. Rock Zone 105,9 ---")
    rockzone_html = """<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#111111;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="font-family:'Arial Black', Impact, sans-serif;font-size:16vw;font-weight:900;color:#ffffff;line-height:0.9;letter-spacing:-0.5vw;">ROCK</div>
    <div style="font-family:'Arial Black', Impact, sans-serif;font-size:16vw;font-weight:900;color:#ffffff;line-height:0.9;letter-spacing:-0.5vw;">ZONE</div>
    <div style="font-family:'Helvetica Neue', Arial, sans-serif;font-size:8vw;font-weight:900;color:#ff0055;letter-spacing:0.8vw;margin-top:1.5vh;">105.9 FM</div>
    </body></html>"""
    render_html_to_png(rockzone_html, DIR_640 / "rockzone1059.png", 640)
    render_html_to_png(rockzone_html, DIR_1024 / "rockzone1059.png", 1024)
    make_symlink("rockzone1059", "rockzone")

    # 18. Ukrajinske Radio
    print("\n--- 18. Ukrajinske Radio ---")
    ukr_html = """<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#0057b7;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="border:1vw solid #ffffff;border-radius:2.5vw;padding:2vw 5vw;text-align:center;">
      <div style="font-family:'Helvetica Neue', Arial, sans-serif;font-size:9vw;font-weight:900;color:#ffffff;letter-spacing:0.5vw;">УКРАЇНСЬКЕ</div>
      <div style="font-family:'Arial Black', Impact, sans-serif;font-size:18vw;font-weight:900;color:#ffffff;line-height:0.9;margin-top:1vh;">РАДІО</div>
    </div>
    </body></html>"""
    render_html_to_png(ukr_html, DIR_640 / "ukrajinskeradio.png", 640)
    render_html_to_png(ukr_html, DIR_1024 / "ukrajinskeradio.png", 1024)

    # 19. CRA Info & Test carriers
    print("\n--- 19. CRA Info & Test carriers ---")
    cra_html = """<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#003366;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="font-family:'Arial Black', Impact, sans-serif;font-size:22vw;font-weight:900;color:#ffffff;letter-spacing:-1vw;">CRA</div>
    <div style="font-family:'Helvetica Neue', Arial, sans-serif;font-size:7vw;font-weight:700;color:#00a8e8;letter-spacing:0.5vw;margin-top:1vh;">DVB-T2 VYSÍLÁNÍ</div>
    </body></html>"""
    render_html_to_png(cra_html, DIR_640 / "naladtesenadigitalnivysilanicra.png", 640)
    render_html_to_png(cra_html, DIR_1024 / "naladtesenadigitalnivysilanicra.png", 1024)
    make_symlink("naladtesenadigitalnivysilanicra", "televizepresantenu")

    test_html = """<!DOCTYPE html>
    <html><body style="margin:0;padding:0;overflow:hidden;background:#2b2d42;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100vw;height:100vh;">
    <div style="font-family:'Arial Black', Impact, sans-serif;font-size:22vw;font-weight:900;color:#8d99ae;letter-spacing:-1vw;">TEST</div>
    <div style="font-family:'Helvetica Neue', Arial, sans-serif;font-size:8vw;font-weight:700;color:#edf2f4;letter-spacing:1vw;">MUX 24</div>
    </body></html>"""
    render_html_to_png(test_html, DIR_640 / "dbtest1.png", 640)
    render_html_to_png(test_html, DIR_1024 / "dbtest1.png", 1024)
    make_symlink("dbtest1", "dbtest2")

    # Additional standard symlinks
    make_symlink("slagrtv", "slageroriginal")
    make_symlink("slagr2", "slagermuzika")

    print("\n" + "=" * 65)
    print("✅ VŠECHNY PICONY ÚSPĚŠNĚ VYGENEROVÁNY S AUTOMATICKÝM SJEDNOCENÍM MĚŘÍTKA!")
    print("=" * 65)


if __name__ == "__main__":
    main()
