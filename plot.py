import csv
import math
import os.path

import colour.difference
import matplotlib.pyplot as plt
from pathlib import Path

import numpy as np

from lib import utilities, plot


class PlotMunsellScatter:
    @staticmethod
    def _extract(munsell_path):
        munsell_color = utilities.MunsellColor(munsell_path, '.csv')
        vc_dict = munsell_color.VC()
        rgb_dict = munsell_color.RGB()
        lab_dict = munsell_color.Lab()
        return vc_dict, rgb_dict, lab_dict

    @staticmethod
    def save_fig(fig, path, file_name):
        if not os.path.exists(path):
            os.makedirs(path)
        fig.savefig(Path(path, file_name).with_suffix('.png'), dpi=600)

    def plot_munsell_scatter(self, munsell_path, save_path):
        vc_dict, rgb_dict, _ = self._extract(munsell_path)

        for idx, key in enumerate(vc_dict.keys()):
            if key == 'header':
                continue

            if len(vc_dict[key]) == len(rgb_dict[key]):
                munsell_scatter = plot.MunsellScatter()
                fig = munsell_scatter.scatter(vc_dict[key], rgb_dict[key], key)
                # self.save_fig(fig, save_path, key)
                # plt.close()
                plt.show()
                break

    def plot_munsell_scatter_de(self, munsell_path1, munsell_path2, save_path):
        ref_vc_dict, ref_rgb_dict, ref_lab_dict = self._extract(munsell_path1)
        com_vc_dict, com_rgb_dict, com_lab_dict = self._extract(munsell_path2)

        for idx, key in enumerate(ref_vc_dict.keys()):
            if key == 'header':
                continue

            if len(ref_rgb_dict[key]) == len(com_rgb_dict[key]):
                de_arr = colour.difference.delta_E_CIE2000(ref_lab_dict[key], com_lab_dict[key])

                munsell_scatter_de = plot.MunsellScatter()
                fig = munsell_scatter_de.scatter_de(ref_vc_dict[key], ref_rgb_dict[key], de_arr, key)
                # self.save_fig(fig, save_path, key)
                # plt.close()

                plt.show()
                break

    def plot_contour_chart(self, munsell_path1, munsell_path2, save_path):
        ref_vc_dict, ref_rgb_dict, ref_lab_dict = self._extract(munsell_path1)
        com_vc_dict, com_rgb_dict, com_lab_dict = self._extract(munsell_path2)

        for idx, key in enumerate(ref_vc_dict.keys()):
            if key == 'header':
                continue

            if len(ref_lab_dict[key]) == len(com_lab_dict[key]):
                de_arr = colour.difference.delta_E_CIE2000(ref_lab_dict[key], com_lab_dict[key])

                contour_chart = plot.ContourChart()
                fig = contour_chart.contourf(ref_vc_dict[key], de_arr, key)
                # self.save_fig(fig, save_path, key)
                # plt.close()
                plt.show()
                break

    def plot_polar(self, munsell_path1):
        # TODO: Sort out the data by value. Nine value with a polar patch
        ref_vc_dict, ref_rgb_dict, ref_lab_dict = self._extract(munsell_path1)

        for inx, key in enumerate(ref_vc_dict.keys()):
            if key == 'header':
                continue

            polar = plot.Polar()
            polar.polar(ref_vc_dict)


def plot_gamut(temp_path):
    def group(lab_lst, col) -> dict:
        result = {}

        for lab in lab_lst:
            k = lab[1]
            result[k] = []

        for lab in lab_lst:
            k = lab[1]
            lab_s = [lab[i] for i in col]
            if k in result:
                result[k].append(lab_s)
        return result

    def max_Cab(lab_lst: list, col: list) -> dict:
        lab_dict: dict = group(lab_lst, col)

        max_dict = {}
        for k in lab_dict.keys():
            for i in range(len(lab_dict[k])):
                cab = math.sqrt(float(lab_dict[k][i][-2]) ** 2 + float(lab_dict[k][i][-1]) ** 2)
                lab_dict[k][i].append(cab)

            max_value = max(lab_dict[k], key=lambda x: x[-1])
            max_dict[k] = max_value

        return max_dict

    def max_Cab_lab(lab_lst: list, col:list) -> list:
        Cab_dict = max_Cab(lab_lst, col)
        opt_lst = [(float(value[1]), float(value[2])) for value in Cab_dict.values()]
        opt_lst.append(opt_lst[0])

        return opt_lst


    with open(temp_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        next(reader)
        lab_lst: list = [line for line in reader]

    ref_points = max_Cab_lab(lab_lst, col=[4, 5, 6])
    toner_4c = max_Cab_lab(lab_lst, col=[7, 8, 9])
    toner_4c_r = max_Cab_lab(lab_lst, col=[10, 11, 12])
    toner_4c_g = max_Cab_lab(lab_lst, col=[13, 14, 15])
    toner_4c_b = max_Cab_lab(lab_lst, col=[16, 17, 18])
    injeck = max_Cab_lab(lab_lst, col=[19, 20, 21])

    gamut = plot.Gamut()
    # gamut.add_points(ref_points, color='k', label="Ref")
    gamut.add_points(toner_4c, color='y', label="4C")
    gamut.add_points(toner_4c_r, color='r', label="4C+R")
    gamut.add_points(toner_4c_g, color='g', label="4C+G")
    gamut.add_points(toner_4c_b, color='b', label="4C+B")
    # gamut.add_points(injeck, color='m', label="Inkjet")
    gamut.plot()


def plot_polar(ipt_path):

    def group_value(ipt_lst: list, value: str) -> list:
        result = []
        for i in ipt_lst:
            if i[1] == value:
                result.append(i)

        return result

    def group_by_key(ipt_lst: list, value: str) -> dict:
        value_lst = group_value(ipt_lst, value)

        result = {}
        for v in value_lst:
            result[v[0]] = []

        for v in value_lst:
            result[v[0]].append(v)

        return result

    with open(ipt_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        ipt_lst = [line for line in reader]

    value_3 = group_by_key(ipt_lst, '3')

    key = 'R'
    x = np.array([float(x[1]) for x in value_3[key]])
    y = np.array([float(x[2]) for x in value_3[key]])
    x, y = np.meshgrid(x, y)

    plt.plot(x, y, 'o')
    plt.show()

    # z = np.array([float(x[-1]) for x in value_3[key]])
    #
    # lv = np.linspace(min(z), max(z), 10)
    #
    # polar = plot.Polar()
    # polar.add_points([x, y, z, lv])
    # polar.plot()











if __name__ == '__main__':
    # fol = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction"
    # ref = r"Dataset_BabelColour_HVC_RGB_Lab_D50"
    # com = r"SunSui\SunSui_deReport_CSV\4C-R"
    # save = r"Save_fig\contour"
    # fmt = '.csv'
    # ref_path = Path(fol, ref)
    # com_path = Path(fol, com)
    # save_path = Path(fol, save)
    #
    # # main
    # plotMunsellScatter = PlotMunsellScatter()
    #
    # plotMunsellScatter.plot_munsell_scatter(ref_path, save_path)
    # plotMunsellScatter.plot_munsell_scatter_de(ref_path, com_path, save_path)
    #
    # plotMunsellScatter.plot_contour_chart(ref_path, com_path, save_path)
    p = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Analysis\Summary_lab.csv"
    # plot_gamut(p)

    p1 = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Analysis\4C_50_combine_delta_without.csv"
    plot_polar(p1)
