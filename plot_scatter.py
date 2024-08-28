from lib import plotting, utilities

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from colour.difference import delta_E_CIE2000
import colour

valid_props = ['hue', 'chroma', 'value']

hue_labels = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']

hue_colors = ['red', 'orangered', 'yellow', 'yellowgreen', 'green', 'cyan',
              'blue', 'blueviolet', 'purple', 'deeppink']


def calculate_confidence_interval(data, confidence_level=0.95):
    if len(data) < 2:
        raise ValueError("Data must contain at least two values.")

    n = len(data)
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)

    if n < 30:
        ci = stats.t.interval(confidence_level, df=n - 1, loc=mean, scale=std_dev / np.sqrt(n))
    else:
        ci = stats.norm.interval(confidence_level, loc=mean, scale=std_dev / np.sqrt(n))

    return mean, ci[0], ci[1]


def hue_method(data0, data1, prop):
    ref_data_group = utilities.group_by(data0, 0)
    com_data_group = utilities.group_by(data1, 0)

    scatter_confidence = plotting.ScatterConfidenceArea(plot_type=prop, figsize=(8, 6))

    ms, ls, us = [], [], []
    for idx, key in enumerate(ref_data_group.keys()):
        ref_lab: list = [list(map(float, x[-3:])) for x in ref_data_group[key]]
        com_lab: list = [list(map(float, x[-3:])) for x in com_data_group[key]]

        # # convert lab to lch to plot the x-axis
        # com_lch = colour.Lab_to_LCHab(com_lab)
        # com_h = com_lch[:, -1]

        de2000 = delta_E_CIE2000(ref_lab, com_lab)

        # Make a list for x-axis
        x = idx + 1
        xs = [x] * len(de2000)

        scatter_confidence.plot_scatter(xs, de2000, c=hue_colors[idx])

        # ref_lch = colour.Lab_to_LCHab(ref_lab)
        # ref_h_mean = np.mean(ref_lch[:, -1])
        # m, l, u = calculate_confidence_interval(de2000)
        # ms.append([ref_h_mean, m])
        # ls.append([ref_h_mean, l])
        # us.append([ref_h_mean, u])
        m, l, u = calculate_confidence_interval(de2000)
        ms.append([x, m])
        ls.append([x, l])
        us.append([x, u])

    fig = scatter_confidence.plot_confidence_area(ms, ls, us)
    # scatter_confidence.axs.set_title("$\Delta$E$_{00}$" + " scatter with 95% confidence interval", pad=28)

    return fig, [ms, ls, us]


def value_method(data0, data1, prop):
    ref_data_group = utilities.group_by(data0, 1)
    com_data_group = utilities.group_by(data1, 1)

    scatter_confidence = plotting.ScatterConfidenceArea(plot_type=prop, figsize=(8, 6))

    ms, ls, us = [], [], []
    s_alpha = 1
    for idx, key in enumerate(ref_data_group.keys()):
        ref_lab: list = [list(map(float, x[-3:])) for x in ref_data_group[key]]
        com_lab: list = [list(map(float, x[-3:])) for x in com_data_group[key]]

        de2000 = delta_E_CIE2000(ref_lab, com_lab)

        # Make a list for x-axis
        x = idx + 1
        xs = [x] * len(de2000)

        scatter_confidence.plot_scatter(xs, de2000, c='k', alpha=s_alpha)

        m, l, u = calculate_confidence_interval(de2000)
        ms.append([x, m])
        ls.append([x, l])
        us.append([x, u])

        s_alpha -= 0.08

    fig = scatter_confidence.plot_confidence_area(ms, ls, us)
    # scatter_confidence.axs.set_title("$\Delta$E$_{00}$" + " scatter with 95% confidence interval")

    return fig, [ms, ls, us]


def chroma_method(data0, data1, prop):
    ref_data_group = utilities.group_by(data0, 2)
    com_data_group = utilities.group_by(data1, 2)

    scatter_confidence = plotting.ScatterConfidenceArea(plot_type=prop, figsize=(8, 6))

    ms, ls, us = [], [], []
    s_alpha = 0.95
    for idx, key in enumerate(ref_data_group.keys()):
        ref_lab: list = [list(map(float, x[-3:])) for x in ref_data_group[key]]
        com_lab: list = [list(map(float, x[-3:])) for x in com_data_group[key]]

        de2000 = delta_E_CIE2000(ref_lab, com_lab)

        # Make a list for x-axis
        x = idx + 1
        xs = [x] * len(de2000)

        scatter_confidence.plot_scatter(xs, de2000, c='k', alpha=s_alpha)

        if not len(de2000) < 2:
            m, l, u = calculate_confidence_interval(de2000)
            ms.append([x, m])
            ls.append([x, l])
            us.append([x, u])



        s_alpha -= 0.08

    fig = scatter_confidence.plot_confidence_area(ms, ls, us)
    # scatter_confidence.axs.set_title("$\Delta$E$_{00}$" + " scatter with 95% confidence interval")

    return fig, [ms, ls, us]


def write_to_txt(file_name, mean_lower_upper):
    mean, lower, upper = mean_lower_upper
    mean = [x[1] for x in mean]
    lower = [x[1] for x in lower]
    upper = [x[1] for x in upper]

    with open(file_name, "w") as file:
        file.write("Mean:\n")
        np.savetxt(file, mean, delimiter=",")  # Save as comma-separated values
        file.write("\nLower:\n")
        np.savetxt(file, lower, delimiter=",")
        file.write("\nUpper:\n")
        np.savetxt(file, upper, delimiter=",")


def plot_scatter_confidence(data_path_1, data_path_2, prop, write_fig_path, write_txt_path):
    valid_props = ['hue', 'value', 'chroma']  # props list

    if prop not in valid_props:
        raise ValueError(f"Invalid property: {prop}. Expected one of {valid_props}.")

    ref_data = utilities.read_csv(data_path_1, skip_lines=1)
    com_data = utilities.read_csv(data_path_2, skip_lines=1)

    fig = None
    mean_lower_upper = None

    if prop == 'hue':
        fig, mean_lower_upper = hue_method(ref_data, com_data, prop)
    elif prop == 'value':
        fig, mean_lower_upper = value_method(ref_data, com_data, prop)
    elif prop == 'chroma':
        fig, mean_lower_upper = chroma_method(ref_data, com_data, prop)
    else:
        raise ValueError(f"Unhandled property: {prop}")

    plotting.save_plt_figure(fig, write_fig_path, dpi=1200)
    write_to_txt(write_txt_path, mean_lower_upper)

    # plt.show()



if __name__ == '__main__':
    # Plot contour or box whisker
    ref = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv"
    toner_4c = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C\4C_50_combined.csv"
    toner_4c_b = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-B_unfinished\4C-B_unfinished_50_combined.csv"
    toner_4c_g = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-G_unfinished\4C-G_unfinished_50_combined.csv"
    toner_4c_r = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-R\4C-R_50_combined.csv"
    inkjet = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\Deepblue\NTUST_50_20240315_rgb.csv"

    file_lst = [toner_4c, toner_4c_b, toner_4c_g, toner_4c_r, inkjet]
    file_name = ['Toner_4C', 'Toner_4C+B', 'Toner_4c+G', 'Toner_4C+R', 'Inkjet']
    munsell_stat = ['hue', 'value', 'chroma']

    for i in range(len(file_lst)):
        for j in range(3):
            state = munsell_stat[j]
            write_fig_path = f'output/scatter_confidence_interval-{file_name[i]}-{state}.png'
            write_txt_path = f'output/scatter_confidence_interval-{file_name[i]}-{state}.txt'
            fig = plot_scatter_confidence(ref, file_lst[i], state, write_fig_path, write_txt_path)

