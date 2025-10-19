#!/usr/bin/env python3
import csv
from datetime import datetime

# exact column names expected
CREATED_COL = "Created Date"
CLOSED_COL  = "Closed Date"
ZIP_COL     = "Incident Zip"

def parse_dt(s):
    if not s: return None
    for fmt in ("%m/%d/%Y %I:%M:%S %p","%m/%d/%Y %H:%M","%Y-%m-%d %H:%M:%S","%Y-%m-%d"):
        try: return datetime.strptime(s, fmt)
        except ValueError: pass
    return None

def month_key(dt): # convert datetime into YYYY-MM
    return f"{dt.year:04d}-{dt.month:02d}"

def main():
    in_path = "nyc_311_2024.csv"
    out_zip = "monthly_zip_averages.csv"
    out_all = "monthly_all_averages.csv"

    by_zip = {}   # (month, zip) -> [sum_hours, n]
    by_all = {}   # month -> [sum_hours, n]

    with open(in_path, "r") as f:
        r = csv.DictReader(f)
        for row in r:
            z = (row[ZIP_COL] or "").strip()
            if not z:
                continue                  # drop missing zip
            cr = parse_dt(row[CREATED_COL])
            cl = parse_dt(row[CLOSED_COL])
            if not cr or not cl:
                continue                  # drop missing dates
            hrs = (cl - cr).total_seconds() / 3600.0
            if hrs < 0:
                continue                  # drop negatives
            m = month_key(cl)             # closed month
            by_zip.setdefault((m, z), [0.0, 0])
            by_zip[(m, z)][0] += hrs
            by_zip[(m, z)][1] += 1
            by_all.setdefault(m, [0.0, 0])
            by_all[m][0] += hrs
            by_all[m][1] += 1

    with open(out_zip, "w") as f:
        w = csv.writer(f)
        w.writerow(["month", "zipcode", "avg_hours"])
        for (m, z), (s, n) in sorted(by_zip.items()):
            w.writerow([m, z, s / n])

    with open(out_all, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "avg_hours"])
        for m, (s, n) in sorted(by_all.items()):
            w.writerow([m, s / n])

if __name__ == "__main__":
    main()
