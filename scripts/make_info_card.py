
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "info-card.svg"

WIDTH, HEIGHT = 850, 700

details = [
    ("NAME", "Mohammed Youssef Chafiki", "#79c0ff"),
    ("EDUCATION", "Al Akhawayn University", "#d2a8ff"),
    ("MAJOR", "Computer Science", "#79c0ff"),
    ("FOCUS", "Cybersecurity & Software Development", "#3fb950"),
]

languages = ["Python", "C", "Java", "Bash"]
tools = ["Linux", "Git", "Next.js", "SQL"]
projects = ["StudentFlow", "LogAnalyzer", "Connect 4"]

svg = [f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<rect width="{WIDTH}" height="{HEIGHT}" rx="14" fill="#0d1117"/>
<rect x="12" y="12" width="826" height="676" rx="10"
      fill="#161b22" stroke="#30363d"/>

<circle cx="35" cy="35" r="6" fill="#ff5f56"/>
<circle cx="55" cy="35" r="6" fill="#ffbd2e"/>
<circle cx="75" cy="35" r="6" fill="#27c93f"/>

<text x="100" y="40" fill="#8b949e"
      font-family="monospace" font-size="15">
youssef@github:~ — neofetch
</text>

<line x1="28" y1="57" x2="822" y2="57" stroke="#30363d"/>

<style>
.label {{
    font-family: monospace;
    font-size: 15px;
    font-weight: bold;
}}
.value {{
    font-family: monospace;
    font-size: 16px;
}}
.section {{
    font-family: monospace;
    font-size: 16px;
    font-weight: bold;
}}
.tag {{
    font-family: monospace;
    font-size: 14px;
}}
</style>

<text x="35" y="91" fill="#3fb950"
      font-family="monospace" font-size="14">
$ whoami &amp;&amp; neofetch
</text>
''']

# Main profile information
for i, (label, value, color) in enumerate(details):
    y = 133 + i * 48
    delay = i * 0.2

    svg.append(f'''
<g opacity="0">
  <animate attributeName="opacity"
           values="0;1;1" keyTimes="0;0.12;1"
           dur="6s" begin="{delay}s"
           repeatCount="indefinite"/>
  <text x="38" y="{y}" class="label" fill="#3fb950">
    {escape(label)}:
  </text>
  <text x="205" y="{y}" class="value" fill="{color}">
    {escape(value, quote=True)}
  </text>
</g>
''')

# Divider and skills section
svg.append('''
<line x1="35" y1="315" x2="815" y2="315" stroke="#30363d"/>
<text x="38" y="350" class="section" fill="#79c0ff">
&gt; TECH STACK
</text>
''')

def add_tags(items, y, color):
    x = 38
    for item in items:
        width = len(item) * 9 + 26
        svg.append(f'''
<rect x="{x}" y="{y - 23}" width="{width}" height="34"
      rx="7" fill="#0d1117" stroke="{color}" stroke-opacity=".65"/>
<text x="{x + 13}" y="{y}" class="tag" fill="{color}">
  {escape(item)}
</text>
''')
        x += width + 12

svg.append('<text x="38" y="395" class="label" fill="#8b949e">LANGUAGES</text>')
add_tags(languages, 432, "#ffa657")

svg.append('<text x="38" y="485" class="label" fill="#8b949e">TOOLS</text>')
add_tags(tools, 522, "#56d4dd")

svg.append('''
<line x1="35" y1="557" x2="815" y2="557" stroke="#30363d"/>
<text x="38" y="591" class="section" fill="#d2a8ff">
&gt; FEATURED PROJECTS
</text>
''')
add_tags(projects, 635, "#d2a8ff")

svg.append('''
<line x1="35" y1="657" x2="815" y2="657" stroke="#30363d"/>
<text x="38" y="678" fill="#3fb950"
      font-family="monospace" font-size="12">
$ system status: online
</text>
</svg>
''')

OUTPUT.write_text("\n".join(svg), encoding="utf-8")
print(f"Created {OUTPUT}")
