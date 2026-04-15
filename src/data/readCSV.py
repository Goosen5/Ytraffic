import csv


def readCSV(path):
    with open(path, "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        data = [row for row in spamreader]
    print(data)


readCSV("assets/datas.csv")