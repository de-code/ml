import csv

with open("test.csv", "ab") as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Spam'] * 5 + ['Baked Beans'])
    writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    #f.write("appended text")
    f.close()

with open("test.csv", "rb") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        print ', '.join(row)
    f.close()

