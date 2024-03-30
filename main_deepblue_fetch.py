import csv
import statistics

import numpy
from colour import difference
from pathlib import Path

from lib import datasets

class FetchData:
    def __init__(self):
        self.lines = None  # list
        self.clean_lines = None  # list
        self.sorted_file = None  # list
        self.ref_lab_lst = []
        self.dif_lst = None

    def open_file(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # list
            self.lines = lines[3:]

    @staticmethod
    def split_by_tab(line):
        line = line.replace('\n', '')
        line = line.split('\t')
        if len(line) >= 2:
            line[1] = line[1].split('-')
        return flatten(line)

    @staticmethod
    def check_value_zero(line):
        # Due to there are some value is zero in L*a*b* column, This function check the value and return the line
        for i in line:
            if i == '0.00':
                print(line)

    @staticmethod
    def remove_col(line):
        del line[0]
        del line[3]
        return line

    def remove_rows(self):
        lst = []
        for line in self.lines:
            line = self.split_by_tab(line)

            if len(line) < 2:
                continue

            if line[4] != '0.00':
                line = self.remove_col(line)
                # self.check_value_zero(line)
                lst.append(line)

        self.clean_lines = lst

    def re_index(self):
        hue_order_dict = datasets.munsell_hue_order_dict

        def sort_key(line):
            hue = line[0][2:]
            hue_order = hue_order_dict.get(hue, 10)
            return hue_order, int(line[1]), int(line[2])

        self.sorted_file = sorted(self.clean_lines, key=lambda line: sort_key(line))

    def pop_ref_lab(self):
        for line in self.sorted_file:
            ref_lab = [line.pop(7), line.pop(7), line.pop(7)]
            self.ref_lab_lst.append(ref_lab)

    def difference(self):
        self.pop_ref_lab()
        act_lab_lst = [sublist[7:] for sublist in self.sorted_file]
        self.dif_lst = difference.delta_E_CIE2000(self.ref_lab_lst, act_lab_lst)

    def progress(self, path):
        self.open_file(path)
        self.remove_rows()
        self.re_index()
        self.difference()

        self.sorted_file = numpy.column_stack((self.sorted_file, self.dif_lst))
        return self.sorted_file


def flatten(lst):
    flatten_lst = []
    for item in lst:
        if isinstance(item, list):
            flatten_lst.extend(item)
        else:
            flatten_lst.append(item)
    return flatten_lst


def save_csv(save_path, lst):
    header = ['H', 'V', 'C', 'Cyan', 'Magenta', 'Yellow', 'Black', 'L*', 'a*', 'b*', 'de2000']

    with open(save_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(lst)


def show_mean_max_min(lst):
    last_column = [float(item[-1]) for item in lst[:]]
    print(f'Avg.: {statistics.mean(last_column)}')
    print(f'Max: {max(last_column)}')
    print(f'Min: {min(last_column)}')


def main(path):
    path = Path(path)

    fetch_data = FetchData()
    ogn_lst = fetch_data.progress(path)

    save_path = Path('output') / (path.stem + '.csv')
    save_csv(save_path, ogn_lst)
    show_mean_max_min(ogn_lst)


if __name__ == '__main__':
    p = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Deepblue\NTUST_50_20240315.txt"
    main(p)
