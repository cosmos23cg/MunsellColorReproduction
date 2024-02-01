import csv
import urllib.request
import re
import os

data_url = 'http://www.rit-mcsl.org/MunsellRenotation/all.dat'
# data_url = 'http://www.rit-mcsl.org/MunsellRenotation/real.dat'
# data_url = 'http://www.rit-mcsl.org/MunsellRenotation/1929.dat'
data_file = ''


def dataFile():
    global data_file
    name = os.path.basename(data_url)
    data_file = data_file.join(name)


def fetch(url=data_url):
    global data_file
    data = urllib.request.urlopen(url)  # data variable read as binary
    with open(data_file, 'w') as f:
        f.write(data.read().decode())  # transfer binary to text


def load():
    global data_file
    with open(data_file) as f:
        return [file for file in f]


heading = []
hues = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
HUE_DIC = {color: [] for color in hues}


def parse(lines):
    global heading

    for line in lines[:]:
        line = line.split()
        if not heading:
            heading = line
        else:
            hue = re.sub(r'[\d.]+', '', line[0])
            if hue in HUE_DIC.keys():
                HUE_DIC[hue].append(line)


def sortValueByHue():
    def str2num(hue):
        number = re.search(r'\d+\.\d+|\d+', hue).group()
        return float(number)

    def custom_sort(item):
        return str2num(item[0])

    for key, value in HUE_DIC.items():
        HUE_DIC[key] = sorted(value, key=custom_sort)


def writeDicData():
    path_folder = "data/" + data_file.split('.')[0]
    print(path_folder)
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)

    for key, value in HUE_DIC.items():
        file_name = key + '.csv'
        with open(path_folder + '/' + file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(heading)
            csv_writer.writerows(value)


def delFile():
    if os.path.exists(data_file):
        os.remove(data_file)
        print(f"file {data_file} deleted!")
    else:
        print(f"File {data_file} is not existing")


def dataProcess():
    parse(load())
    sortValueByHue()


def main():
    dataFile()
    fetch()
    dataProcess()
    writeDicData()
    delFile()

if __name__ == '__main__':
    main()
