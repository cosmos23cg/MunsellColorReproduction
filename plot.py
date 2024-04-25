import csv
import math
import os.path

import colour.difference
import matplotlib.pyplot as plt
from pathlib import Path

import numpy as np

from lib import utilities, plot, data_processing


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


def plot_gamut(input_path):
    def max_Cab(lab_lst: list, col: list) -> dict:
        # TODO: pre slice the list range
        lab_dict: dict = data_processing.group_by(lab_lst, group_key=1)

        max_dict = {}
        for k in lab_dict.keys():
            for i in range(len(lab_dict[k])):
                cab = math.sqrt(float(lab_dict[k][i][-2]) ** 2 + float(lab_dict[k][i][-1]) ** 2)
                lab_dict[k][i].append(cab)

            max_value = max(lab_dict[k], key=lambda x: x[-1])
            max_dict[k] = max_value

        return max_dict

    def max_Cab_lab(lab_lst: list, col: list) -> list:
        Cab_dict = max_Cab(lab_lst, col)
        opt_lst = [(float(value[1]), float(value[2])) for value in Cab_dict.values()]
        opt_lst.append(opt_lst[0])  # add the first element let the gamut be lined

        return opt_lst

    data_lst = data_processing.read_csv(input_path, 2)

    ref_points = max_Cab_lab(data_lst, col=[4, 5, 6])
    toner_4c = max_Cab_lab(data_lst, col=[7, 8, 9])
    # toner_4c_r = max_Cab_lab(lab_lst, col=[10, 11, 12])
    # toner_4c_g = max_Cab_lab(lab_lst, col=[13, 14, 15])
    # toner_4c_b = max_Cab_lab(lab_lst, col=[16, 17, 18])
    injeck = max_Cab_lab(data_lst, col=[19, 20, 21])

    gamut = plot.Gamut((7, 6))
    gamut.add_points(ref_points, c='k', ln='-', m='o', lb="Ref")
    gamut.add_points(toner_4c, c='y', ln='--', m='.', lb="4C")
    # gamut.add_points(toner_4c_r, color='r', label="4C+R")
    # gamut.add_points(toner_4c_g, color='g', label="4C+G")
    # gamut.add_points(toner_4c_b, color='b', label="4C+B")
    gamut.add_points(injeck, c='m', ln='--', m='.', lb="Inkjet")
    fig = gamut.plot_gamut()
    plt.show()


def plot_polar(ipt_path, split_num=11):
    data_lst = data_processing.read_csv(ipt_path, 2)

    value_col = 2  # 1 hue, 2 value, 3 chroma
    grouped_data: dict = data_processing.group_by(data_lst, value_col)

    # Fetch all De and find the min max value for the colorbar range
    de_col = [7, 11]  # Toner_printer_4C, Inkjet_printer
    z_all = []

    for key, value in grouped_data.items():
        if data_processing.is_nested(value) is True:
            for sub_value in value:
                z_all.extend(float(sub_value[i]) for i in de_col)
        else:
            z_all.extend([float(value[i]) for i in de_col])

    z_min, z_max = min(z_all), max(z_all)
    lv = np.linspace(z_min, z_max, split_num)

    # Split the input data into two figures
    for i, (key, data) in enumerate(grouped_data.items()):
        x, y, z1, z2 = [], [], [], []  # a*, b*, de2000_1, de2000_2

        for value in data:
            x.append(float(value[5]))
            y.append(float(value[6]))
            z1.append(float(value[7]))
            z2.append(float(value[11]))

        contour = plot.Contour(1, 2, figsize=(13, 6), sharex=True, sharey=True)
        contour.add_points(x, y, z1, lv, cmap='RdBu_r', title='Toner printer 4C')
        contour.add_points(x, y, z2, lv, cmap='RdBu_r', title='Inkjet printer')

        title = f"Value {i+1}"
        fig = contour.plot_tricontourf(title, xlim=(-90, 90), ylim=(-80, 120))
        # fig = contour.plot_tricontour(title, xlim=(-90, 90), ylim=(-80, 120))

        save_path = Path('output') / f"Toner_4C_Inkjet_contour-Value_{i+1}.png"
        plot.save_plt_figure(fig, save_path, dpi=1200)


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
    plot_gamut(p)

    # p = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Analysis\ref_com_de_only.csv"
    # plot_polar(p)
