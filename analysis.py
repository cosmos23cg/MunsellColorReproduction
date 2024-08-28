import csv
import math
import re

import pandas as pd
from pathlib import Path
from colour.difference import delta_E_CIE2000, delta_E_CIE1976
from lib import error


class ColourComparator:
    """
    function:
    CIE_2000()
    CIE_1976()
    CIE_1976_delta_Cab()
    CIE_1976_delta_Hab()
    """
    def __init__(self, ref_path, com_path):
        self.ref_path = Path(ref_path)
        self.com_path = Path(com_path)
        self.ref_colour_lst = self.read_csv(self.ref_path)
        self.com_colour_lst = self.read_csv(self.com_path)

    def _check_lst_len(self):
        if len(self.ref_colour_lst) != len(self.com_colour_lst):
            raise error.ListLenMismatchErr('Error: The number of colors in reference and comparison lists are different.')

    def _CIE_1976_Cab(self, input_lst):
        return list(map(lambda x: math.sqrt((float(x[-2]) ** 2) + (float(x[-1]) ** 2)), input_lst))

    def _CIE_1976_hab(self, input_lst):
        return list(map(lambda x: math.atan(float(x[-1]) / float(x[-2])), input_lst))

    def read_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            return [line for line in reader]

    def CIE_2000(self) -> list:
        self._check_lst_len()

        ref_lab = list(map(lambda x: x[-3:], self.ref_colour_lst))
        com_lab = list(map(lambda x: x[-3:], self.com_colour_lst))

        return list(delta_E_CIE2000(ref_lab, com_lab))

    def CIE_1976(self) -> list:
        self._check_lst_len()

        ref_lab = list(map(lambda x: x[-3:], self.ref_colour_lst))
        com_lab = list(map(lambda x: x[-3:], self.com_colour_lst))

        return list((delta_E_CIE1976(ref_lab, com_lab)))

    def CIE_1976_delta_L(self, absolute=False) -> list:
        self._check_lst_len()

        if absolute:
            return [abs(float(x[-3]) - float(y[-3])) for x, y in zip(self.ref_colour_lst, self.com_colour_lst)]

        return [float(x[-3]) - float(y[-3]) for x, y in zip(self.ref_colour_lst, self.com_colour_lst)]

    def CIE_1976_delta_Cab(self, absolute=False) -> list:
        self._check_lst_len()

        c1 = self._CIE_1976_Cab(self.ref_colour_lst)
        c2 = self._CIE_1976_Cab(self.com_colour_lst)

        if absolute:
            return [abs(x - y) for x, y in zip(c1, c2)]

        return [x - y for x, y in zip(c1, c2)]

    def CIE_1976_delta_Hab(self, absolute=False):
        self._check_lst_len()

        c1 = self._CIE_1976_Cab(self.ref_colour_lst)
        c2 = self._CIE_1976_Cab(self.com_colour_lst)

        h1 = self._CIE_1976_hab(self.ref_colour_lst)
        h2 = self._CIE_1976_hab(self.com_colour_lst)

        delta_hab = [x - y for x, y in zip(h1, h2)]

        if absolute:
            return [abs(2 * math.sqrt(x * y) * math.sin(z / 2)) for x, y, z in zip(c1, c2, delta_hab)]

        return [2 * math.sqrt(x * y) * math.sin(z / 2) for x, y, z in zip(c1, c2, delta_hab)]


class HVCAnalyzer:
    """
    function:
    hue_avg()
    hue_std()
    """
    def __init__(self, input_lst):
        """
        input_lst: The list which need to be categorized by hue, value, chroma
        """
        self.df = pd.DataFrame.from_records(input_lst)

    def group_avg(self, group_col, cal_col):
        """
        *arg input the col which need to be average
        """
        df_cp = self.df.copy()

        return df_cp.groupby(group_col)[cal_col].mean()

    def group_std(self, group_col, cal_col):
        df_cp = self.df.copy()

        return df_cp.groupby(group_col)[cal_col].std()


def merge_lst(main_lst: list, *arg):
    merged_lst: list = main_lst.copy()

    # for method
    # for i in range(len(merged_lst)):
    #     for j in range(len(arg)):
    #         merged_lst[i].append(arg[j][i])

    # use zip and args for clear and fast way to implement
    for sub_lst, *vals in zip(merged_lst, *arg):
        sub_lst.extend(vals)

    return merged_lst


def hue_rename_reindex(input_df: pd.DataFrame):
    def rename(input_df: pd.DataFrame):
        input_df.index = [re.sub(r'\d+(\.\d+)?([a-zA-Z])', r'\2', idx) for idx in input_df.index]
        return input_df

    def reindex(input_df: pd.DataFrame):
        custom_order = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
        return input_df.reindex(custom_order)

    input_df = rename(input_df)
    return reindex(input_df)


def df_to_list(input_df: pd.DataFrame):
    idx = input_df.index.tolist()
    val = input_df.values.tolist()
    return [[x, *y] for x, y in zip(idx, val)]


def chroma_reindex(input_df: pd.DataFrame):
    input_df.index = [int(idx) for idx in input_df.index]
    return input_df.sort_index()


def save_csv(save_path, write_lst, header=None):
    with open(save_path, 'w', newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if header is not None:
            writer.writerow(header)
        for lst in write_lst:
            writer.writerow(lst)


def main(ref_path, com_path):
    # Calculate the De2000, delta l*, C_ab, H_ab and merge to
    comparator = ColourComparator(ref_path, com_path)
    de_2000: list = comparator.CIE_2000()
    de_1976_L: list = comparator.CIE_1976_delta_L(absolute=True)
    de_1976_Cab: list = comparator.CIE_1976_delta_Cab(absolute=True)
    de_1976_Hab: list = comparator.CIE_1976_delta_Hab(absolute=True)
    output_lst = comparator.com_colour_lst.copy()
    merged_lst = merge_lst(output_lst, de_2000, de_1976_L, de_1976_Cab, de_1976_Hab)

    # Do the average, stander deviation, max and min number by grouping hue, value, and chroma
    cal_column = [len(merged_lst[0]) - i for i in range(4, 0, -1)]  # catch the last 4 column number in the list

    analyzer = HVCAnalyzer(merged_lst)
    hue_avg = analyzer.group_avg(0, cal_column)
    hue_std = analyzer.group_std(0, cal_column)
    hue_avg = df_to_list(hue_rename_reindex(hue_avg))
    hue_std = df_to_list(hue_rename_reindex(hue_std))
    hue_data = [x + [''] * 2 + y for x, y in zip(hue_avg, hue_std)]

    value_avg = analyzer.group_avg(1, cal_column)
    value_std = analyzer.group_std(1, cal_column)
    value_avg = df_to_list(value_avg)
    value_std = df_to_list(value_std)
    value_data = [x + [''] * 2 + y for x, y in zip(value_avg, value_std)]

    chroma_avg = analyzer.group_avg(2, cal_column)
    chroma_std = analyzer.group_std(2, cal_column)
    chroma_avg = df_to_list(chroma_reindex(chroma_avg))
    chroma_std = df_to_list(chroma_reindex(chroma_std))
    chroma_data = [x + [''] * 2 + y for x, y in zip(chroma_avg, chroma_std)]

    for i in range(len(hue_data)):
        merged_lst[i].extend([''] * 2 + hue_data[i])

    for i in range(len(value_data)):
        idx = i + len(hue_data) + 2
        merged_lst[idx].extend([''] * 2 + value_data[i])

    for i in range(len(chroma_data)):
        idx = i + len(hue_data) + len(value_data) + 4
        merged_lst[idx].extend([''] * 2 + chroma_data[i])

    header = ['Hue', 'Value', 'Chroma', 'R', 'G', 'B', 'L*', 'a*', 'b*', 'De2000', 'ΔL*', 'ΔCab', 'ΔHab', '', '',
              'avg', 'De2000', 'ΔL*', 'ΔCab', 'ΔHab', '', '', 'std', 'De2000', 'ΔL*', 'ΔCab', 'ΔHab']

    sf_f = Path('output') / (com_path.stem + '_delta.csv')
    save_csv(sf_f, merged_lst, header)



if __name__ == '__main__':
    ref = Path(r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv")
    toner_4c = Path(r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C\4C_50_combined.csv")
    toner_4c_b = Path(r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-B_unfinished\4C-B_unfinished_50_combined.csv")
    toner_4c_g = Path(r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-G_unfinished\4C-G_unfinished_50_combined.csv")
    toner_4c_r = Path(r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-R\4C-R_50_combined.csv")
    inkjet = Path(r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Deepblue\NTUST_50_20240315_rgb.csv")

    file_lst = [toner_4c, toner_4c_b, toner_4c_g, toner_4c_r, inkjet]
    file_name = ['Toner 4C', 'Toner 4C+B', 'Toner 4c+G', 'Toner 4C+R', 'Inkjet']

    for i in range(len(file_lst)):
        main(ref, file_lst[i])
