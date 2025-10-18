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
        #csv reader 
        reader = csv.DictReader(f)
        for row in reader:
            #get created_date
            created_dt=parse_date(row.get(CREATED_COL, "Unkown"))
            #print("DEBUG:", row.get(CREATED_COL), "->", created_dt)
            if not created_dt or not (start_day <= created_dt <= end_day):
                continue

            complaint = row.get(COMPLAINT_COL, "Unknown")
            borough=row.get(BOROUGH_COL, "Unkown")


            if complaint not in counts:
                counts[complaint] = {}
            
            if borough not in counts[complaint]:
                counts[complaint][borough] =0

            counts[complaint][borough] +=1

    #output reesults to CSV or stdout

    out_f = open(args.output, "w", newline="") if args.output else sys.stdout
    writer = csv.writer(out_f)
    writer.writerow(["complaint type", "borough", "count"])

    for complaint in sorted(counts):
        for borough in sorted(counts[complaint]):
            writer.writerow([complaint, borough, counts[complaint][borough]])

    if args.output:
        out_f.close()

if __name__ == "__main__":
    main()

