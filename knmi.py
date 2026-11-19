"""Haalt de KNMI-waarschuwingen op via MeteoAlarm en schrijft warnings.json naast de app."""
import json, sys, urllib.request, datetime, os

URL = "https://feeds.meteoalarm.org/api/v1/warnings/feeds-netherlands"
OUT = "warnings.json"
HEARTBEAT_HOURS = 2  # ook zonder wijziging elke 2 uur verversen, zodat de app ziet dat de koppeling leeft


def trim(feed):
    out = []
    for w in feed.get("warnings", []):
        infos = (w.get("alert") or {}).get("info") or []
        nl = [i for i in infos if i.get("language") == "nl-NL"] or infos[:1]
        keep = []
        for i in nl:
            keep.append({
                "language": i.get("language"),
                "event": i.get("event"),
                "headline": i.get("headline"),
                "onset": i.get("onset"),
                "effective": i.get("effective"),
                "expires": i.get("expires"),
                "parameter": [p for p in (i.get("parameter") or []) if p.get("valueName") in ("awareness_level", "awareness_type")],
                "area": [{"areaDesc": a.get("areaDesc"), "polygon": a.get("polygon") or []} for a in (i.get("area") or [])],
            })
        # verlopen waarschuwingen weglaten
        def verlopen(i):
            try:
                return datetime.datetime.fromisoformat(i["expires"]) < datetime.datetime.now(datetime.timezone.utc)
            except Exception:
                return False
        keep = [i for i in keep if not verlopen(i)]
        if keep:
            out.append({"alert": {"info": keep}})
    return out


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "extreem-weer-check (Hanab HSE)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        feed = json.load(r)
    new = trim(feed)
    now = datetime.datetime.now(datetime.timezone.utc)
    old = None
    if os.path.exists(OUT):
        try:
            old = json.load(open(OUT, encoding="utf-8"))
        except Exception:
            old = None
    changed = old is None or old.get("warnings") != new
    stale = True
    if old and old.get("fetched"):
        try:
            age = now - datetime.datetime.fromisoformat(old["fetched"].replace("Z", "+00:00"))
            stale = age > datetime.timedelta(hours=HEARTBEAT_HOURS)
        except Exception:
            stale = True
    if changed or stale:
        json.dump({"fetched": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "KNMI via MeteoAlarm", "warnings": new},
                  open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
        print("bijgewerkt:", len(new), "waarschuwingen", "(gewijzigd)" if changed else "(verversing)")
    else:
        print("geen wijziging")


if __name__ == "__main__":
    main()
