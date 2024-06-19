from pathlib import Path

from colour.difference import delta_E_CIE2000
import numpy as np

from lib import plotting, utilities

import matplotlib.pyplot as plt


def min_max_value_(input_data: dict, de_col):
    extend_all = []

    for idx, (key, values) in enumerate(input_data.items()):
        if utilities.is_nested(values) is True:
            for value in values:
                extend_all.extend(float(value[i]) for i in de_col)
        else:
            extend_all.extend(float(values[i]) for i in de_col)

    z_min, z_max = min(extend_all), max(extend_all)

    return z_min, z_max


def extract_data_values(data: list, extract: tuple):
    x, y, z = [], [], []  # a*, b*, de2000,

    if not isinstance(data, list):
        raise TypeError("Input data type must be list")

    for value in data:
        x.append(float(value[extract[0]]))
        y.append(float(value[extract[1]]))
        z.append(float(value[extract[2]]))

    return x, y, z


def min_max_value(input_data):
    min_val = min(input_data)
    max_val = max(input_data)

    return min_val, max_val


def plot_munsell_value_contour(ref_path, com_path, contour_type, levels_num=11):
    ref_data = utilities.read_csv(ref_path, skip_lines=1)
    com_data = utilities.read_csv(com_path, skip_lines=1)

    for i in range(len(ref_data)):
        ref_lab = ref_data[i][-3:]
        com_lab = com_data[i][-3:]
        de = delta_E_CIE2000(ref_lab, com_lab)
        ref_data[i].append(de)

    de_lst = [x[-1] for x in ref_data]
    min_val, max_val = min_max_value(de_lst)
    lv = np.linspace(min_val, max_val, levels_num)

    ref_group_v = utilities.group_by(ref_data, 1)

    rows = 3
    cols = 3
    contour = plotting.Contour(rows, cols, figsize=(10, 8), sharex=True, sharey=True)

    crnt_row = 0
    crnt_col = 0

    fig = None

    for idx, (key, values) in enumerate(ref_group_v.items()):

        x, y, z = extract_data_values(values, (-3, -2, -1))
        contour.add_points(x, y, z, lv, cmap='coolwarm', title=f"Value {key}", ax_pos=(crnt_row, crnt_col))

        # logical stament of axis row and col
        if crnt_col < cols - 1:
            crnt_col += 1
        else:
            crnt_col = 0
            crnt_row += 1

        if contour_type == "tricontourf":
            fig = contour.plot_tricontourf(xlim=(-95, 90), ylim=(-80, 125))
        # elif contour_type == "tricontour":
        #     z_one_lv = np.linspace(z_min, z_max, 2)
        #     fig = contour.plot_tricontour(title, addition_lv=z_one_lv, xlim=(-90, 90), ylim=(-80, 120))
        #     save_path = Path('output') / f"Toner_4C_Inkjet_contour-Value_{i + 1}.png"
        else:
            raise ValueError(f"Unknown contour_type: {contour_type}")

    return fig




# def plot_munsell_hue_contour(ipt_path, levels_num=11, de_col=(6, 10)):
#     data_lst = utilities.read_csv(ipt_path, skip_lines=2)
#
#     grouped_data: dict = utilities.group_by(data_lst, 0)  # value column is 1
#
#     # Fetch all De and find the min max value for the colorbar range
#     z_min, z_max = min_max_value(grouped_data, de_col)
#     lv = np.linspace(z_min, z_max, levels_num)
#     z_one_lv = np.linspace(z_min, z_max, 2)
#
#     x_all, y_all, z1_all, z2_all = [], [], [], []
#     for i, (key, values) in enumerate(grouped_data.items()):
#         x, y, z1, z2 = extract_data_values(values, de_col)
#
#         x_all.extend(x)
#         y_all.extend(y)
#         z1_all.extend(z1)
#         z2_all.extend(z2)
#
#     contour = plotting.Contour(1, 2, figsize=(13, 6), sharex=True, sharey=True)
#     contour.add_points(x_all, y_all, z1_all, lv, cmap='coolwarm', title='Toner')
#     contour.add_points(x_all, y_all, z2_all, lv, cmap='coolwarm', title='Inkjet')
#
#     plot_functions = [contour.plot_tricontourf, contour.plot_tricontour]
#     for idx, plot_function in enumerate(plot_functions):
#         if idx == 0:
#             fig = plot_function(main_title='Contourf hue', xlim=(-90, 90), ylim=(-80, 120))
#         else:
#             fig = plot_function(main_title='Contour hue', addition_lv=z_one_lv, xlim=(-90, 90), ylim=(-80, 120))
#
#         # plotting.save_plt_figure(fig, f'output/{idx}.png', dpi=1200)
#         plt.show()
#         plt.close()


if __name__ == '__main__':
    data_path = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Analysis\ref_com_de_only.csv"

    ref = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv"
    toner_4c = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C\4C_50_combined.csv"
    toner_4c_b = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-B_unfinished\4C-B_unfinished_50_combined.csv"
    toner_4c_g = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-G_unfinished\4C-G_unfinished_50_combined.csv"
    toner_4c_r = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-R\4C-R_50_combined.csv"
    inkjet = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Deepblue\NTUST_50_20240315.csv"

    file_lst = [toner_4c, toner_4c_b, toner_4c_g, toner_4c_r, inkjet]
    file_name = ['Toner_4C', 'Toner_4C+B', 'Toner_4c+G', 'Toner_4C+R', 'Inkjet']

    for i in range(len(file_lst)):
        fig = plot_munsell_value_contour(ref, file_lst[i], "tricontourf")
        write_dir = f'output/contour-value-{file_name[i]}.png'
        plotting.save_plt_figure(fig, write_dir, dpi=1200)

    # plot_munsell_hue_contour(data_path, de_col=(6, 10))


