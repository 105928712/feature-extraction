import csv, sys

src, dst = sys.argv[1], sys.argv[2]


with open(src, newline="") as fin, open(dst, "w", newline="") as fout:
    w = csv.writer(fout)
    w.writerow(["url", "type"])
    

    for row in csv.reader(fin):
        if row:
            w.writerow([row[1], "legitimate"])