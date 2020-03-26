import csv

def fileRead( filename ):
    csvData = []
    ifile = open(filename)
    reader = csv.reader(ifile)
    
    rownum = 0
    for row in reader:
        if rownum == 0:
            rownum += 1
        else:
            csvData.append(row)
    
    ifile.close()
    return csvData