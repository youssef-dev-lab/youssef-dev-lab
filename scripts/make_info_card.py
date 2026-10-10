
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "info-card.svg"

details = [
    ("Name", "Mohammed Youssef Chafiki", "#79c0ff"),
    ("Education", "Al Akhawayn University", "#d2a8ff"),
    ("Major", "Computer Science", "#79c0ff"),
    ("Focus", "Cybersecurity & Software Development", "#3fb950"),
    ("Languages", "Python, C, Java, Bash", "#ffa657"),
    ("Tools", "Linux, Git, Next.js, SQL", "#56d4dd"),
    ("Projects", "StudentFlow, LogAnalyzer, Connect 4", "#d2a8ff"),
]

WIDTH, HEIGHT = 850, 350

svg = [f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<rect width="850" height="350" rx="14" fill="#0d1117"/>
<rect x="12" y="12" width="826" height="326" rx="10"
      fill="#161b22" stroke="#30363d"/>

<circle cx="35" cy="35" r="6" fill="#ff5f56"/>
<circle cx="55" cy="35" r="6" fill="#ffbd2e"/>
<circle cx="75" cy="35" r="6" fill="#27c93f"/>

<text x="100" y="40" fill="#8b949e"
      font-family="monospace" font-size="15">
youssef@github:~ — neofetch
</text>

<line x1="28" y1="57" x2="822" y2="57"
      stroke="#30363d"/>

<style>
.label {{
    font-family: monospace;
    font-size: 16px;
    font-weight: bold;
}}
.value {{
    font-family: monospace;
    font-size: 15px;
}}
</style>
''']

for i, (label, value, color) in enumerate(details):
    y = 91 + i * 34
    delay = i * 0.25

    svg.append(f'''
<g opacity="0">
  <animate attributeName="opacity"
           values="0;1;1"
           keyTimes="0;0.12;1"
           dur="6s"
           begin="{delay}s"
           repeatCount="indefinite"/>

  <text x="35" y="{y}" class="label" fill="#3fb950">
    {escape(label)}:
  </text>

  <text x="185" y="{y}" class="value" fill="{color}">
    {escape(value)}
  </text>
</g>
''')

svg.append('''
<text x="35" y="323" fill="#8b949e"
      font-family="monospace" font-size="12">
$ system status: online
</text>
</svg>
''')

OUTPUT.write_text("\\n".join(svg), encoding="utf-8")
print(f"Created {OUTPUT}")
