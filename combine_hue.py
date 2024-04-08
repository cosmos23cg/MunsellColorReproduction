"""

"""

import csv
import re
import sys
from pathlib import Path
from lib import datasets


class CSVReader:
    def read_csvfile(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            file_data = [line for line in reader]
        return file_data


class CombineCSV(CSVReader):
    def __init__(self):
        super().__init__()
        self.path = None
        self.data_dict = {}

    def read_file(self, folder_path, file_format):
        self.path = folder_path
        # use path.glob to find all match file in folder
        file_path_lst = list(self.path.glob('*' + file_format))

        for file_path in file_path_lst:
            file_data = self.read_csvfile(file_path)

            key = file_path.stem.split('-')[0]  # split hue name as key
            number, symbol = split_text_num(key)
            self.data_dict[symbol] = file_data

        return self.data_dict


def split_text_num(string):
    pattern = re.compile(r'(\d+)([A-Z]+)')
    match = pattern.match(string)
    if match:
        number = match.group(1)
        symbol = match.group(2)
        return number, symbol


def save_csv(write_path, write_file: dict):
    header = ['H', 'V', 'C', 'R', 'G', 'B', 'L*', 'a*',	'b*']

    with open(write_path, 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for key in datasets.munsell_hue_order_dict.keys():
            for data in write_file.get(key, []):
                writer.writerow(data)

    print(f'File saved at {write_path}')


def main(dir_path):
    dir_p = Path(dir_path)

    combine_csv_ref = CombineCSV()
    ref_dict = combine_csv_ref.read_file(dir_p, '.csv')
    ref_dir_parts = dir_p.parts
    ref_write_p = Path("output") / (ref_dir_parts[-2] + "_" + ref_dir_parts[-1] + "_combine.csv")
    save_csv(ref_write_p, ref_dict)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit()
    else:
        main(sys.argv[1])
