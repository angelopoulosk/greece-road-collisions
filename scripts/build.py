#!/usr/bin/env python3
"""Turn the raw dump collected from accidents.maps.gov.gr into the repo's data files.

Input : raw JSON  {"sigrousi": [[id, lon, lat, description, timestamp, ota, color], ...],
                   "diakomidi": [...]}   (already de-duplicated by record id)
Output: data/collisions.csv, data/transports.csv   full records
        data/collisions.xlsx, data/transports.xlsx  same, as Excel
        data/collisions.json, data/transports.json  compact columns for the map

Usage: python3 scripts/build.py raw.json [repo_dir]
"""
import csv, json, sys, os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from openpyxl import Workbook

ATH = ZoneInfo("Europe/Athens")
HEAD = ["id", "datetime_athens", "timestamp_utc", "longitude", "latitude", "municipality", "description", "color"]
NAMES = {"sigrousi": "collisions", "diakomidi": "transports"}


def main(raw_path, repo="."):
    raw = json.load(open(raw_path, encoding="utf-8"))
    out = os.path.join(repo, "data")
    os.makedirs(out, exist_ok=True)
    for key, name in NAMES.items():
        seen, rows = set(), []
        for rid, lon, lat, desc, ts, ota, color in raw[key]:
            if rid in seen:
                continue
            seen.add(rid)
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)
            rows.append((rid, dt, lon, lat, (ota or "").strip(), (desc or "").strip(), color or ""))
        rows.sort(key=lambda r: (r[1], r[0]))

        # CSV
        with open(os.path.join(out, name + ".csv"), "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(HEAD)
            for rid, dt, lon, lat, ota, desc, color in rows:
                w.writerow([rid, dt.astimezone(ATH).strftime("%Y-%m-%d %H:%M"),
                            dt.strftime("%Y-%m-%dT%H:%M:%SZ"), lon, lat, ota, desc, color])

        # Excel
        wb = Workbook(write_only=True)
        ws = wb.create_sheet(name)
        ws.append(HEAD)
        for rid, dt, lon, lat, ota, desc, color in rows:
            ws.append([rid, dt.astimezone(ATH).replace(tzinfo=None),
                       dt.strftime("%Y-%m-%dT%H:%M:%SZ"), lon, lat, ota, desc, color])
        wb.save(os.path.join(out, name + ".xlsx"))

        # compact JSON for the map
        causes, places = {}, {}
        col = {"x": [], "y": [], "t": [], "c": [], "o": []}
        for rid, dt, lon, lat, ota, desc, color in rows:
            col["x"].append(round(lon * 1e5))
            col["y"].append(round(lat * 1e5))
            col["t"].append(int(dt.timestamp() // 60))
            col["c"].append(causes.setdefault(desc, len(causes)))
            col["o"].append(places.setdefault(ota, len(places)))
        col["causes"], col["places"] = list(causes), list(places)
        with open(os.path.join(out, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(col, f, ensure_ascii=False, separators=(",", ":"))

        print(name, len(rows), rows[0][1].date(), "→", rows[-1][1].date())


if __name__ == "__main__":
    main(*sys.argv[1:])
