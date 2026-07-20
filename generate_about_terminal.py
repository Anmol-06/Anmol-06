"""
generate_about_terminal.py
Generates about-terminal.svg — a macOS-style terminal card with:
  - LEFT:  Profile photo rendered as colored SVG <rect> block mosaic (no raster)
  - RIGHT: Python syntax-highlighted dataclass code
  - TOP:   macOS window chrome + traffic lights
  - ANIM:  CRT scanline sweep (SMIL)
Palette: #0a0118 bg · #1a0533 card · #a855f7 violet · #06b6d4 cyan · #e0d9ff text
"""
import os
from PIL import Image, ImageEnhance

REPO_ROOT = '/home/anmol/Documents/GitHub/GitHub Profile edit'
IMG_PATH  = os.path.join(REPO_ROOT, 'ref', 'profile pic.png')
OUT_PATH  = os.path.join(REPO_ROOT, 'about-terminal.svg')

GRID_COLS  = 36
GRID_ROWS  = 36
TILE_W     = 6
TILE_H     = 6
MOSAIC_W   = GRID_COLS * TILE_W   # 216
MOSAIC_H   = GRID_ROWS * TILE_H   # 216
MOSAIC_X   = 24
MOSAIC_Y   = 56

SVG_W      = 900
SVG_H      = 385
CODE_X     = MOSAIC_X + MOSAIC_W + 30

def hex_of(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def build_mosaic_rects(img_path):
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    side = min(w, h)
    img  = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
    img  = ImageEnhance.Contrast(img).enhance(1.3)
    img  = ImageEnhance.Color(img).enhance(1.4)
    img  = img.resize((GRID_COLS, GRID_ROWS), Image.Resampling.LANCZOS)
    pixels = img.load()
    tiles = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            r, g, b = pixels[col, row]
            tiles.append({
                "x": MOSAIC_X + col * TILE_W,
                "y": MOSAIC_Y + row * TILE_H,
                "fill": hex_of(r, g, b),
            })
    return tiles

def build_svg(tiles):
    cx = MOSAIC_X + MOSAIC_W // 2
    cy = MOSAIC_Y + MOSAIC_H // 2
    r  = min(MOSAIC_W, MOSAIC_H) // 2  # 108

    mosaic_lines = ['  <g id="mosaic" clip-path="url(#mosaicClip)">']
    for t in tiles:
        mosaic_lines.append(
            f'    <rect x="{t["x"]}" y="{t["y"]}" width="{TILE_W}" height="{TILE_H}" fill="{t["fill"]}"/>'
        )
    mosaic_lines.append("  </g>")
    mosaic_group = "\n".join(mosaic_lines)

    grid_lines = ['  <g id="grid" clip-path="url(#mosaicClip)" opacity="0.18">']
    for col in range(1, GRID_COLS):
        gx = MOSAIC_X + col * TILE_W
        grid_lines.append(f'    <line x1="{gx}" y1="{MOSAIC_Y}" x2="{gx}" y2="{MOSAIC_Y+MOSAIC_H}" stroke="#000" stroke-width="0.5"/>')
    for row in range(1, GRID_ROWS):
        gy = MOSAIC_Y + row * TILE_H
        grid_lines.append(f'    <line x1="{MOSAIC_X}" y1="{gy}" x2="{MOSAIC_X+MOSAIC_W}" y2="{gy}" stroke="#000" stroke-width="0.5"/>')
    grid_lines.append("  </g>")
    grid_group = "\n".join(grid_lines)

    COLOR = {"kw":"#a855f7","dec":"#06b6d4","cls":"#06b6d4","str":"#e0d9ff","br":"#8b83a8","cmt":"#6b7280","dflt":"#e0d9ff"}

    def span(kind, text):
        t = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
        col = COLOR.get(kind, "#e0d9ff")
        fw  = ' font-weight="600"' if kind in ("kw","dec","cls") else ''
        return f'<tspan fill="{col}"{fw}>{t}</tspan>'

    def code_line(lx, ly, parts):
        inner = "".join(span(k,t) for k,t in parts)
        return f'    <tspan x="{lx}" y="{ly}" xml:space="preserve">{inner}</tspan>'

    LX = CODE_X
    LY0 = MOSAIC_Y + 12
    LS  = 21

    code_svg = "\n".join([
        code_line(LX, LY0,       [("kw","from"), ("dflt"," dataclasses "), ("kw","import"), ("dflt"," dataclass")]),
        code_line(LX, LY0+LS,    [("dec","@dataclass")]),
        code_line(LX, LY0+2*LS,  [("kw","class"), ("dflt"," "), ("cls","Anmol"), ("dflt",":")]),
        code_line(LX, LY0+3*LS,  [("dflt","    "), ("kw","name"), ("dflt","    = "), ("str",'"Anmol Kumar Gorain"')]),
        code_line(LX, LY0+4*LS,  [("dflt","    "), ("kw","role"), ("dflt","    = "), ("str",'"Systems Engineer & Automated Dev"')]),
        code_line(LX, LY0+5*LS,  [("dflt","    "), ("kw","edu"), ("dflt","     = "), ("str",'"B.Tech CSE, BIT Sindri (2028)"')]),
        code_line(LX, LY0+6*LS,  [("dflt","    "), ("kw","loc"), ("dflt","     = "), ("str",'"Bokaro Steel City, Jharkhand"')]),
        code_line(LX, LY0+7*LS,  [("dflt","    "), ("kw","focus"), ("dflt","   = "), ("br","[")]),
        code_line(LX, LY0+8*LS,  [("dflt","        "), ("str",'"Computer Vision & Deep Learning"'), ("dflt",",")]),
        code_line(LX, LY0+9*LS,  [("dflt","        "), ("str",'"Generative AI / Applied ML"'), ("dflt",",")]),
        code_line(LX, LY0+10*LS, [("dflt","        "), ("str",'"Intelligent Full-Stack Systems"'), ("dflt",",")]),
        code_line(LX, LY0+11*LS, [("dflt","    "), ("br","]")]),
        code_line(LX, LY0+13*LS, [("cmt","# Building end-to-end automated systems")]),
    ])

    sep_x = MOSAIC_X + MOSAIC_W + 15

    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="100%" height="auto" viewBox="0 0 {SVG_W} {SVG_H}">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="35%" r="80%">
      <stop offset="0%"   stop-color="#1a0533"/>
      <stop offset="100%" stop-color="#0a0118"/>
    </radialGradient>
    <clipPath id="mosaicClip">
      <circle cx="{cx}" cy="{cy}" r="{r}"/>
    </clipPath>
    <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
    <linearGradient id="sweepGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#06b6d4" stop-opacity="0"/>
      <stop offset="40%"  stop-color="#06b6d4" stop-opacity="0.1"/>
      <stop offset="50%"  stop-color="#06b6d4" stop-opacity="0.5"/>
      <stop offset="60%"  stop-color="#a855f7" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#0a0118" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow" x="-5%" y="-200%" width="110%" height="500%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="crt" width="2" height="4" patternUnits="userSpaceOnUse">
      <rect width="2" height="1" y="1" fill="#06b6d4" opacity="0.02"/>
    </pattern>
    <linearGradient id="sepGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#a855f7" stop-opacity="0"/>
      <stop offset="30%"  stop-color="#a855f7" stop-opacity="0.5"/>
      <stop offset="70%"  stop-color="#06b6d4" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#06b6d4" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{SVG_W}" height="{SVG_H}" rx="14"
        fill="url(#bgGlow)" stroke="#a855f7" stroke-width="1.5" stroke-opacity="0.4"/>
  <rect width="{SVG_W}" height="{SVG_H}" rx="14" fill="url(#crt)"/>

  <!-- Titlebar -->
  <rect x="1" y="1" width="{SVG_W-2}" height="40" rx="13" fill="#0f0225" fill-opacity="0.97"/>
  <rect x="1" y="27" width="{SVG_W-2}" height="14" fill="#0f0225" fill-opacity="0.97"/>
  <circle cx="26" cy="21" r="5.5" fill="#EF4444"/>
  <circle cx="44" cy="21" r="5.5" fill="#F59E0B"/>
  <circle cx="62" cy="21" r="5.5" fill="#10B981"/>
  <text x="{SVG_W//2}" y="25" text-anchor="middle"
        font-family="'JetBrains Mono','Fira Code','Courier New',monospace"
        font-size="11.5" fill="#8b83a8">anmol@bit-sindri: ~/about_me.py</text>

  <!-- Block Mosaic Avatar -->
{mosaic_group}

  <!-- Grid overlay for terminal cell aesthetic -->
{grid_group}

  <!-- Ring border -->
  <circle cx="{cx}" cy="{cy}" r="{r + 3}"
          fill="none" stroke="url(#ringGrad)" stroke-width="4" opacity="0.9"/>

  <!-- Vertical separator -->
  <rect x="{sep_x}" y="48" width="1" height="{SVG_H - 60}" fill="url(#sepGrad)"/>

  <!-- Python Code -->
  <text font-family="'JetBrains Mono','Fira Code','Courier New',Consolas,monospace"
        font-size="13" xml:space="preserve">
{code_svg}
  </text>

  <!-- CRT Scanline Sweep -->
  <rect x="0" y="0" width="{SVG_W}" height="14"
        fill="url(#sweepGrad)" filter="url(#glow)" rx="7">
    <animate attributeName="y" values="-14;{SVG_H};-14"
             dur="4s" repeatCount="indefinite" calcMode="linear"/>
    <animate attributeName="opacity" values="0.1;0.9;0.1"
             dur="4s" repeatCount="indefinite"/>
  </rect>

</svg>
"""

if __name__ == "__main__":
    print("Reading profile picture...")
    tiles = build_mosaic_rects(IMG_PATH)
    print(f"Built {len(tiles)} mosaic tiles ({GRID_COLS}x{GRID_ROWS})")
    svg = build_svg(tiles)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"Written: {OUT_PATH}  ({len(svg):,} bytes)")
