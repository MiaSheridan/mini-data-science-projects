#!/usr/bin/env python3
import sys
import csv
from datetime import datetime
import argparse 

CREATED_COL = "Created Date"
COMPLAINT_COL = "Complaint Type"
BOROUGH_COL = "Borough"

def parse_date(text):
    if not text:
        return None

    for fmt in ("%m/%d/%Y %I:%M:%S %p",):
        try:
            return datetime.strptime(text,fmt)
        except ValueError:
            pass

    return None

def main():
    parser = argparse.ArgumentParser()

    #required input file
    parser.add_argument("-i", "--input", required=True, help="Input CSV.")

    #required start data
    parser.add_argument("-s", "--start", required=True, help="Start date Incluse")

    #required end data
    parser.add_argument("-e", "--end", required=True, help="End date Incluse")

    #optional output if not given print to stdout
    parser.add_argument("-o","--output",default=None, help="Optional output CSV path")

    args = parser.parse_args()
    
    #convert to time
    start_day = datetime.strptime(args.start, "%Y-%m-%d")

    end_day = datetime.strptime(args.end, "%Y-%m-%d")

    #inclusive to to the end of the date
    end_day = end_day.replace(hour=23,minute=59)


    counts = {}

    #read csv and count compplaints
    with open(args.input, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            created_text = row.get(CREATED_COL, "")
            created_dt = parse_date(created_text)

            complaint = row.get(COMPLAINT_COL, "").strip().lower()
            borough = row.get(BOROUGH_COL, "").strip().lower().title()

            if not complaint or not borough or created_dt is None:
                continue

            if not (start_day <= created_dt <= end_day):
                continue

            # Count using tuple key
            key = (complaint, borough)
            counts[key] = counts.get(key, 0) + 1

    # Convert counts dict to a list of tuples
    output_rows = [(complaint, borough, count) for (complaint, borough), count in counts.items()]

    # Sort by count descending
    output_rows.sort(key=lambda x: x[2], reverse=True)

    # Output to file or stdout
    if args.output:
        out_f = open(args.output, "w", newline="")
    else:
        out_f = sys.stdout

    writer = csv.writer(out_f)
    writer.writerow(["complaint type", "borough", "count"])
    for row in output_rows:
        writer.writerow(row)

    if args.output:
        out_f.close()


if __name__ == "__main__":
    main()

