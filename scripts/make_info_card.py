from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent

details = [
    ("Name", "Mohammed Youssef Chafiki"),
    ("Education", "Al Akhawayn University"),
    ("Major", "Computer Science"),
    ("Focus", "Cybersecurity & Software Development"),
    ("Languages", "Python, C, Java, Bash"),
    ("Tools", "Linux, Git, Next.js, SQL"),
    ("Projects", "StudentFlow, LogAnalyzer, Connect 4"),
]

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="850" height="350" viewBox="0 0 850 350">',
    '<rect width="850" height="350" rx="14" fill="#0d1117"/>',
    '<rect x="15" y="15" width="820" height="320" rx="10" fill="#161b22" stroke="#30363d"/>',
    '<circle cx="42" cy="40" r="7" fill="#ff5f56"/>',
    '<circle cx="65" cy="40" r="7" fill="#ffbd2e"/>',
    '<circle cx="88" cy="40" r="7" fill="#27c93f"/>',
    '<text x="115" y="45" fill="#8b949e" font-family="monospace" font-size="16">youssef@github: ~</text>',
    '<style>@keyframes appear {from {opacity:0;transform:translateY(8px)} to {opacity:1;transform:translateY(0)}} .line {opacity:0;animation:appear .5s ease forwards}</style>',
]

for i, (key, value) in enumerate(details):
    y = 90 + i * 33
    delay = i * 0.25
    svg.append(
        f'<g class="line" style="animation-delay:{delay}s">'
        f'<text x="45" y="{y}" fill="#3fb950" font-family="monospace" font-size="16">{escape(key)}:</text>'
        f'<text x="185" y="{y}" fill="#c9d1d9" font-family="monospace" font-size="16">{escape(value)}</text>'
        '</g>'
    )

svg.append("</svg>")

(ROOT / "info-card.svg").write_text("\n".join(svg), encoding="utf-8")
print("Created info-card.svg")
