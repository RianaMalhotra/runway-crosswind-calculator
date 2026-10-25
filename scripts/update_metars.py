#!/usr/bin/env python3
"""Fetch current raw METARs server-side for the static GitHub Pages site."""
import datetime as dt
import json
import os
import pathlib
import urllib.request

AIRPORTS = ("CYYZ", "CYTZ", "CYHM", "CYOW", "CYUL", "CYVR", "KJFK", "KLAX", "KORD")
DEST = pathlib.Path(__file__).resolve().parent.parent / "metars.json"
url = "https://aviationweather.gov/api/data/metar?ids=" + ",".join(AIRPORTS) + "&format=json"
req = urllib.request.Request(url, headers={
    "User-Agent": "RunwayCrosswindTrainer/1.0 (GitHub Actions educational METAR display)",
    "Accept": "application/json",
})
with urllib.request.urlopen(req, timeout=25) as response:
    observations = json.load(response)
if not isinstance(observations, list):
    raise ValueError("Unexpected METAR response")
reports = {}
for record in observations:
    if not isinstance(record, dict):
        continue
    code = record.get("icaoId")
    raw = record.get("rawOb")
    if code in AIRPORTS and isinstance(raw, str) and raw.strip():
        reports[code] = raw.strip()
if not reports:
    raise ValueError("No valid METAR reports returned; retaining previous snapshot")
snapshot = {
    "updatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    "source": "AviationWeather.gov",
    "reports": reports,
}
DEST.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Updated METARs for", ", ".join(sorted(reports)))
