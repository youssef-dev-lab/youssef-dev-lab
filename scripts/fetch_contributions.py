
import json
import re
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen
from html.parser import HTMLParser

USERNAME = "youssef-dev-lab"
ROOT = Path(__file__).resolve().parent.parent

class ContributionsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []

    def handle_starttag(self, tag, attrs):
        if tag != "td":
            return

        attrs = dict(attrs)
        day = attrs.get("data-date")
        level = attrs.get("data-level")

        if day and level is not None:
            self.days.append({
                "date": day,
                "level": int(level),
                "count": None
            })

url = f"https://github.com/users/{USERNAME}/contributions"
request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(request, timeout=20) as response:
    html = response.read().decode("utf-8")

parser = ContributionsParser()
parser.feed(html)

if not parser.days:
    raise RuntimeError("No contribution cells found. GitHub may have changed its HTML.")

output = ROOT / "data" / "contributions.json"
output.parent.mkdir(exist_ok=True)

output.write_text(
    json.dumps({
        "username": USERNAME,
        "updated": date.today().isoformat(),
        "days": parser.days
    }, indent=2),
    encoding="utf-8"
)

print(f"Fetched {len(parser.days)} contribution days")
