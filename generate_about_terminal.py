import os
import io
import base64
from PIL import Image

def build_about_terminal_svg():
    # 1. Process profile pic into pixel art
    img_path = '/home/anmol/Documents/GitHub/GitHub Profile edit/ref/profile pic.png'
    img = Image.open(img_path)
    
    # Downsample to 44x44, then scale up to 176x176 with NEAREST for retro 8-bit feel
    small = img.resize((44, 44), Image.Resampling.BILINEAR)
    pixelated = small.resize((176, 176), Image.Resampling.NEAREST)
    
    buf = io.BytesIO()
    pixelated.save(buf, format='PNG')
    img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="auto" viewBox="0 0 850 330">
  <defs>
    <!-- Background Radial Glow -->
    <radialGradient id="bgGlow" cx="50%" cy="30%" r="90%">
      <stop offset="0%" stop-color="#1a0533"/>
      <stop offset="100%" stop-color="#0a0118"/>
    </radialGradient>

    <!-- Cyberpunk Ring Border Gradient -->
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>

    <!-- Scanline Texture Pattern -->
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#06b6d4" opacity="0.04"/>
    </pattern>

    <!-- Laser Sweep Glow Filter -->
    <filter id="scanlineGlow" x="-10%" y="-100%" width="120%" height="300%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Laser Sweep Beam Gradient -->
    <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#06b6d4" stop-opacity="0"/>
      <stop offset="35%" stop-color="#06b6d4" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="#06b6d4" stop-opacity="0.75"/>
      <stop offset="65%" stop-color="#a855f7" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#0a0118" stop-opacity="0"/>
    </linearGradient>

    <!-- Profile Circle Clip -->
    <clipPath id="circleClip">
      <circle cx="75" cy="75" r="68"/>
    </clipPath>
  </defs>

  <!-- Terminal Card Background -->
  <rect width="850" height="330" rx="14" fill="url(#bgGlow)" stroke="#a855f7" stroke-width="1.5" stroke-opacity="0.5"/>
  <rect width="850" height="330" rx="14" fill="url(#scanlines)"/>

  <!-- macOS Window Titlebar -->
  <g id="titlebar">
    <rect x="1" y="1" width="848" height="38" rx="13" fill="#1a0533" fill-opacity="0.9"/>
    <!-- Traffic Light Buttons -->
    <circle cx="24" cy="20" r="5" fill="#EF4444"/>
    <circle cx="40" cy="20" r="5" fill="#F59E0B"/>
    <circle cx="56" cy="20" r="5" fill="#10B981"/>
    <!-- Terminal Title -->
    <text x="425" y="24" text-anchor="middle" font-family="'JetBrains Mono', 'Fira Code', 'Courier New', monospace" font-size="12" fill="#8b83a8">anmol@bit-sindri: ~/about_me.py</text>
  </g>

  <!-- LEFT COLUMN: Pixelated Avatar with Cyberpunk Gradient Ring -->
  <g transform="translate(35, 75)">
    <circle cx="75" cy="75" r="72" fill="none" stroke="url(#borderGrad)" stroke-width="3.5" opacity="0.9"/>
    <image href="data:image/png;base64,{img_b64}" x="7" y="7" width="136" height="136" clip-path="url(#circleClip)" style="image-rendering: pixelated; image-rendering: crisp-edges;"/>
  </g>

  <!-- RIGHT COLUMN: Python Syntax Highlighted Code -->
  <text font-family="'JetBrains Mono', 'Fira Code', 'Courier New', Consolas, monospace" font-size="13" fill="#e0d9ff" xml:space="preserve">
    <tspan x="220" y="80"><tspan fill="#a855f7" font-weight="bold">from</tspan> dataclasses <tspan fill="#a855f7" font-weight="bold">import</tspan> dataclass</tspan>
    
    <tspan x="220" y="106"><tspan fill="#06b6d4" font-weight="bold">@dataclass</tspan></tspan>
    <tspan x="220" y="128"><tspan fill="#a855f7" font-weight="bold">class</tspan> <tspan fill="#06b6d4" font-weight="bold">Anmol</tspan>:</tspan>
    <tspan x="220" y="150">    <tspan fill="#a855f7" font-weight="bold">def</tspan> <tspan fill="#e0d9ff">__init__</tspan>(<tspan fill="#a855f7">self</tspan>):</tspan>
    <tspan x="220" y="174">        <tspan fill="#a855f7">self</tspan>.<tspan fill="#06b6d4">name</tspan>       = <tspan fill="#e0d9ff">&quot;Anmol Kumar Gorain&quot;</tspan></tspan>
    <tspan x="220" y="196">        <tspan fill="#a855f7">self</tspan>.<tspan fill="#06b6d4">role</tspan>       = <tspan fill="#e0d9ff">&quot;Systems Engineer &amp; Automated Systems Dev&quot;</tspan></tspan>
    <tspan x="220" y="218">        <tspan fill="#a855f7">self</tspan>.<tspan fill="#06b6d4">education</tspan>  = <tspan fill="#e0d9ff">&quot;B.Tech CSE, BIT Sindri (Class of 2028)&quot;</tspan></tspan>
    <tspan x="220" y="240">        <tspan fill="#a855f7">self</tspan>.<tspan fill="#06b6d4">location</tspan>   = <tspan fill="#e0d9ff">&quot;Bokaro Steel City, Jharkhand, India 🇮🇳&quot;</tspan></tspan>
    <tspan x="220" y="262">        <tspan fill="#a855f7">self</tspan>.<tspan fill="#06b6d4">focus</tspan>      = <tspan fill="#8b83a8">[</tspan><tspan fill="#e0d9ff">&quot;Computer Vision &amp; DL&quot;</tspan>, <tspan fill="#e0d9ff">&quot;GenAI&quot;</tspan>, <tspan fill="#e0d9ff">&quot;Intelligent Systems&quot;</tspan><tspan fill="#8b83a8">]</tspan></tspan>
    <tspan x="220" y="295"><tspan fill="#8b83a8"># Building intelligent, end-to-end automated systems</tspan></tspan>
  </text>

  <!-- Top-to-Bottom Continuous Sweeping CRT Scanline -->
  <rect x="0" y="0" width="850" height="10" fill="url(#scanGrad)" filter="url(#scanlineGlow)">
    <animate
      attributeName="y"
      values="-10;330;-10"
      keyTimes="0;0.5;1"
      dur="3.6s"
      repeatCount="indefinite"
      calcMode="linear"/>
    <animate
      attributeName="opacity"
      values="0.2;0.8;0.2"
      keyTimes="0;0.5;1"
      dur="3.6s"
      repeatCount="indefinite"/>
  </rect>
</svg>
'''
    target_path = '/home/anmol/Documents/GitHub/GitHub Profile edit/about-terminal.svg'
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("about-terminal.svg generated successfully.")

if __name__ == '__main__':
    build_about_terminal_svg()
