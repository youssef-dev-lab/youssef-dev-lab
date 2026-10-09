
import json
from datetime import date
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
data = json.loads(
    (ROOT / "data" / "contributions.json").read_text(encoding="utf-8")
)

days = sorted(data["days"], key=lambda d: d["date"])
colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

cell = 12
gap = 3
left = 28
top = 35
width = 860
height = 165

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',
    '<style>',
    '@keyframes reveal {from {opacity:0;transform:translateY(-6px)} to {opacity:1;transform:translateY(0)}}',
    '.day {opacity:0;animation:reveal .35s ease forwards}',
    '</style>',
    '<text x="28" y="21" fill="#c9d1d9" font-family="monospace" font-size="13">GitHub contribution activity</text>',
]

if days:
    first = date.fromisoformat(days[0]["date"])
    first_sunday = first.toordinal() - (first.weekday() + 1) % 7

    for item in days:
        current = date.fromisoformat(item["date"])
        week = (current.toordinal() - first_sunday) // 7
        weekday = (current.weekday() + 1) % 7

        x = left + week * (cell + gap)
        y = top + weekday * (cell + gap)
        level = max(0, min(4, item["level"]))
        delay = min(week * 0.025 + weekday * 0.035, 2.5)

        svg.append(
            f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" '
            f'rx="2" fill="{colors[level]}" style="animation-delay:{delay:.2f}s">'
            f'<title>{escape(item["date"])}</title></rect>'
        )

svg.append(
    '<text x="28" y="154" fill="#8b949e" font-family="monospace" font-size="12">'
    'Live public contribution history</text>'
)
svg.append("</svg>")

(ROOT / "contrib-heatmap.svg").write_text(
    "\n".join(svg), encoding="utf-8"
)

print("Created contrib-heatmap.svg")
