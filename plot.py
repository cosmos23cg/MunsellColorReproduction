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
    def max_Cab(data_lst: list, col):
        grouped_data: dict = data_processing.group_by(data_lst, group_key=1)  # 1 is hue in Excel file

        result_lst = []
        for key, value in grouped_data.items():
            for i in range(len(value)):
                # slice the list
                value[i] = [value[i][j] for j in [0, 1, 2, 3, col[0], col[1]]]

                # calculate the Cab then append in lst
                cab = data_processing.cie_1976_cab(value[i][-2], value[i][-1])
                grouped_data[key][i].append(cab)

            max_lst = max(grouped_data[key], key=lambda x: x[-1])
            max_lst = data_processing.check_float(max_lst)
            result_lst.append(max_lst)

        hvc = [x[1:4] for x in result_lst]
        points = [x[4:6] for x in result_lst]

        return hvc, points

    data_lst = data_processing.read_csv(input_path, skip_lines=2)

    ref_hue, ref_points = max_Cab(data_lst, (5, 6))
    _, toner_4c_points = max_Cab(data_lst, (8, 9))
    _, injeck_points = max_Cab(data_lst, (20, 21))

    # Make the data can plot a circle
    ref_points.append(ref_points[0])
    toner_4c_points.append(toner_4c_points[0])
    injeck_points.append(injeck_points[0])

    gamut = plot.Gamut(1, 1, figsize=(8, 6))
    gamut.add_points(ref_points, c='k', ln='-', m='o', lb="Ref")
    gamut.add_points(toner_4c_points, c='y', ln='--', m='^', lb="4C")
    gamut.add_points(injeck_points, c='m', ln='--', m='^', lb="Inkjet")

    gamut.gamut_area(ref_points, toner_4c_points, injeck_points)
    gamut.add_annotate(ref_points, ref_hue)
    fig = gamut.plot_gamut()
    write_path = Path('output') / 'gamut and ratio.png'
    plot.save_plt_figure(fig, write_path, dpi=1200)


def plot_contour(ipt_path, contour_type, split_num=11):
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
        contour.add_points(x, y, z1, lv, cmap='coolwarm', title='Toner')
        contour.add_points(x, y, z2, lv, cmap='coolwarm', title='Inkjet')

        title = f"Value {i+1}"

        match contour_type:
            case "tricontourf":
                fig = contour.plot_tricontourf(title, xlim=(-90, 90), ylim=(-80, 120))
                save_path = Path('output') / f"Toner_4C_Inkjet_contourf-Value_{i + 1}.png"
                # plot.save_plt_figure(fig, save_path, dpi=1200)

            case "tricontour":
                fig = contour.plot_tricontour(title, xlim=(-90, 90), ylim=(-80, 120))
                save_path = Path('output') / f"Toner_4C_Inkjet_contour-Value_{i + 1}.png"
                # plot.save_plt_figure(fig, save_path, dpi=1200)

            # case "contour":
            #     fig = contour.plot_contour(title, xlim=(-90, 90), ylim=(-80, 120))

        plt.show()
        break


def plot_box_whisker(data_path, group_key, write_name):
    data_lst = data_processing.read_csv(data_path, skip_lines=2)
    grouped_data: dict = data_processing.group_by(data_lst, group_key)  # 1 hue, 2 value, 3 chroma

    all_data = []
    all_labels = []

    for key, values in grouped_data.items():
        printer_0 = [float(value[7]) for value in values]
        printer_1 = [float(value[11]) for value in values]

        all_data.extend([printer_0, printer_1])
        all_labels.extend([f'{key}\nToner\n4C', f'{key}\nInkjet'])

    box = plot.Box(1, 1, figsize=(16, 9))
    fig = box.plot_box_whisker(all_data, all_labels, 'Box and whisker', write_name)

    write_path = Path('output') / f'box_whisker-{write_name}.png'
    plot.save_plt_figure(fig, write_path, dpi=1200)


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
    # p = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Analysis\Summary_lab.csv"
    # plot_gamut(p)

    p = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Analysis\ref_com_de_only.csv"
    plot_contour(p, "contour")
    # plot_box_whisker(p, 3, 'chroma')
