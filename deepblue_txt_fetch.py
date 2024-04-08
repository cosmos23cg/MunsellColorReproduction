"""
This script use for fetch the txt file to csv from Deepblue.
"""


import csv
import re
from lib import datasets
from pathlib import Path

class TxtReader:
    def __init__(self):
        self.lines = None

    def txt_reader(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as txtfile:
            self.lines = txtfile.readlines()


class FetchData(TxtReader):
    def __init__(self):
        super().__init__()

    @staticmethod
    def split_line(line):
        line = line.replace('\n', '')
        line = line.split('\t')

        if len(line) >= 2:
            line[1] = line[1].split('-')
            return [item for sublist in line for item in (sublist if isinstance(sublist, list) else [sublist])]

    @staticmethod
    def remove_col(line):
        del line[0]  # munsell
        del line[3]  # index (100.00)
        del line[7]  # ref L*
        del line[7]  # ref a*
        del line[7]  # ref b*

        return line

    def txt_reader(self, file_path, start_line=0):
        super().txt_reader(file_path)
        self.lines = self.lines[start_line:]

    def remove_rows(self):
        """
        Each Color name store two index which are 0.00 and 100.0
        """
        lst = []
        for line in self.lines:
            line = self.split_line(line)

            if isinstance(line, list):
                if line[4] != '0.00':
                    line = self.remove_col(line)
                    lst.append(line)
        return lst


def split_num_text(input_lst, col=0):
    input_lst_cp = input_lst.copy()
    input_lst_cp[col] = re.sub(r'\d+(\.\d+)?([a-zA-Z])', r'\2', input_lst_cp[col])
    return input_lst_cp


def reindex(input_lst: list):
    def sort_key(line):
        hue_order_dict = datasets.munsell_hue_order_dict

        lst = split_num_text(line, col=0)
        hue_order = hue_order_dict.get(lst[0], 11)
        return hue_order, int(line[1]), int(line[2])

    return sorted(input_lst, key=lambda line: sort_key(line))


def save_csv(save_path, save_lst):
    header = ['H', 'V', 'C', 'Cyan', 'Magenta', 'Yellow', 'Black', 'L*', 'a*', 'b*']

    with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(save_lst)


def main(input_path):
    if not isinstance(input_path, Path):
        input_path = Path(input_path)

    fetch = FetchData()
    fetch.txt_reader(input_path, start_line=3)  # The color data start at third line
    lst = fetch.remove_rows()
    reindex_lst = reindex(lst)

    output_path = Path('output') / (input_path.stem + '.csv')
    save_csv(output_path, reindex_lst)
    print(f'File saved at: {output_path}')


if __name__ == '__main__':
    p = Path(r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Deepblue\NTUST_50_20240315.txt")
    main(p)

