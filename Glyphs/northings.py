import os
import csv
import pyproj

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

#requires pyproj (pip install pyproj)
osgb36 = pyproj.Proj(init='epsg:27700')
wgs84 = pyproj.Proj(init='epsg:4326')

os.chdir("D:/Projects/Automating-Data-Visualisation/GlyphsPsychoPy")
print( os.getcwd()  )

fileName="sensors.csv"
sensorData = fileRead( fileName )

E_adj = -424132
N_adj = -564179

for data in sensorData:
    latitude = float(data[1])
    longitude = float(data[2])

    E, N = pyproj.transform(wgs84, osgb36, longitude, latitude)

    x = (E + E_adj) / 100
    y = (N + N_adj) / 100
    
    data.append(x)
    data.append(y)
        
ofile = open('outputdata.csv', "w", newline='')
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

for data in sensorData:
    writer.writerow(data)