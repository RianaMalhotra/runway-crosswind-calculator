#!/usr/bin/env python3
"""Download one representative airport photograph per station into the repo."""
import json
import pathlib
import urllib.parse
import urllib.request
import time

AIRPORTS = {
 "CYYZ": "Toronto Pearson International Airport",
 "CYTZ": "Billy Bishop Toronto City Airport",
 "CYHM": "John C. Munro Hamilton International Airport",
 "CYOW": "Ottawa Macdonald–Cartier International Airport",
 "CYUL": "Montréal–Trudeau International Airport",
 "CYVR": "Vancouver International Airport",
 "KJFK": "John F. Kennedy International Airport",
 "KLAX": "Los Angeles International Airport",
 "KORD": "O'Hare International Airport",
}
HEADERS = {"User-Agent": "RunwayCrosswindCalculator/1.0 (educational student aviation project; github.com/RianaMalhotra/runway-crosswind-calculator)"}
ROOT = pathlib.Path("assets/airports")
ROOT.mkdir(parents=True, exist_ok=True)

def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as response:
        return response.read()

def api(params):
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    return json.loads(get(url))

def get_page_photo(title):
    data = api({"action":"query","prop":"pageimages","titles":title,"pithumbsize":1000,"format":"json"})
    page = next(iter(data["query"]["pages"].values()))
    return page.get("thumbnail",{}).get("source"), page.get("pageid")

def get_commons_photo(name):
    params={"action":"query","generator":"search","gsrsearch":name+" airport terminal","gsrnamespace":6,"gsrlimit":15,
            "prop":"imageinfo","iiprop":"url|mime","iiurlwidth":1000,"format":"json"}
    url="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(params)
    data=json.loads(get(url))
    for page in data.get("query",{}).get("pages",{}).values():
        info=(page.get("imageinfo") or [{}])[0]
        thumb=info.get("thumburl") or info.get("url")
        if info.get("mime")=="image/jpeg" and thumb:
            return thumb,page.get("title")
    return None,None

attributions={}
failures=[]
for icao,name in AIRPORTS.items():
    target=ROOT/(icao+".jpg")
    if target.exists() and target.stat().st_size>10000:
        print("Already downloaded:",icao)
        continue
    try:
        url,source=get_page_photo(name)
        if not url:
            url,source=get_commons_photo(name)
        if not url:
            raise ValueError("No suitable photo found")
        data=get(url)
        if not data.startswith(bytes.fromhex("ffd8")):
            # Wikipedia lead images can be PNG; search Commons for a JPEG instead.
            url,source=get_commons_photo(name)
            if not url: raise ValueError("No JPEG found")
            data=get(url)
        if not data.startswith(bytes.fromhex("ffd8")) or len(data)<10000:
            raise ValueError("Image download was not a valid JPEG")
        target.write_bytes(data)
        attributions[icao]={"airport":name,"source":str(source),"image_url":url}
        print("Saved",target,len(data),"bytes")
    except Exception as error:
        failures.append(icao)
        print("FAILED",icao,str(error))
    time.sleep(0.3)
(ROOT/"sources.json").write_text(json.dumps(attributions,indent=2,ensure_ascii=False)+"\n")
print("Downloaded",len(list(ROOT.glob("*.jpg"))),"airport photos; failures:",failures)
if failures:
    raise SystemExit("Missing photos: "+", ".join(failures))
