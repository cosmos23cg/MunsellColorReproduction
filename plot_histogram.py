from lib import plotting, utilities
from pathlib import Path
from colour.difference import delta_E_CIE2000
import matplotlib.pyplot as plt
import numpy as np
# TODO: 還要加上不同檔按重疊色差的直方圖
plt.rcParams['font.sans-serif'] = ['DFKai-SB']


def read_data(ref_path, com_path):
    """
    Reads reference and comparison Lab values from CSV files.
    """
    ref_data = utilities.read_csv(ref_path, skip_lines=1)
    com_data = utilities.read_csv(com_path, skip_lines=1)

    ref_lab = [x[-3:] for x in ref_data]
    com_lab = [x[-3:] for x in com_data]

    return ref_lab, com_lab


def calculate_de2000(ref_lab, com_lab):
    """
    Calculates delta E 2000 values between Lab values.
    """
    return delta_E_CIE2000(ref_lab, com_lab)


def plot_histogram(de_2000):
    """
    Plots a histogram of delta E 2000 values with median and mean lines.
    Optionally takes a title argument.
    """
    # split numbers
    bins = np.arange(0, 11.3, 0.2)

    # plot histogram
    style = {'facecolor': 'none', 'edgecolor': 'grey', 'linewidth': 1.5}
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.hist(de_2000, bins=bins, histtype='step', **style)

    # mark median and mean number as legend
    median_de = np.median(de_2000)
    mean_de = np.mean(de_2000)
    min_de = np.min(de_2000)
    max_de = np.max(de_2000)

    # # Add horizontal line for mean and median value
    # ax.axvline(x=median_de, color='r', linestyle='dashed', linewidth=1,
    #            label=f'Median $\Delta E_{{00}}$: {median_de:.2f}')
    # ax.axvline(x=mean_de, color='b', linestyle='dashed', linewidth=1,
    #            label=f'Mean $\Delta E_{{00}}$\u2003: {mean_de:.2f}')

    # axis setting
    ax.set_xlabel('印刷樣本相對於參考樣本的 $\Delta E_{00}$ 值', labelpad=10, fontsize=14)
    ax.set_ylabel('色塊數量', labelpad=10, fontsize=14)

    ax.set_xlim(0, 11.5)
    ax.set_xticks(np.arange(0, 11.5, 0.5))
    ax.set_ylim(0, 85)

    return fig, [median_de, mean_de, min_de, max_de]

def plot_de_histogram(ref_path, com_path, write_path, txt_output_path):

    ref_lab, com_lab = read_data(ref_path, com_path)
    de_2000 = calculate_de2000(ref_lab, com_lab)
    fig, de_lst = plot_histogram(de_2000)

    with open(txt_output_path, "w") as f:
        f.write(f"Median dE2000: {de_lst[0]:.2f}\n")
        f.write(f"Mean dE2000: {de_lst[1]:.2f}\n")
        f.write(f"mix de2000: {de_lst[2]:.2f}\n")
        f.write(f"max de2000: {de_lst[3]:.2f}\n")

    # plotting.save_plt_figure(fig, write_path, dpi=1200)
    plt.show()


def read_datas(ref_path, com_path0, com_path1):
    """
    Reads reference and comparison Lab values from CSV files.
    """
    ref_data = utilities.read_csv(ref_path, skip_lines=1)
    com_data0 = utilities.read_csv(com_path0, skip_lines=1)
    com_data1 = utilities.read_csv(com_path1, skip_lines=1)

    ref_lab = [x[-3:] for x in ref_data]
    com0_lab = [x[-3:] for x in com_data0]
    com1_lab = [x[-3:] for x in com_data1]

    return ref_lab, com0_lab, com1_lab

def plot_histograms_overlap(de2000_0, de2000_1, lb0, lb1):
    """
    Plots a histogram of delta E 2000 values with median and mean lines.
    Optionally takes a title argument.
    """
    # split numbers
    bins = np.arange(0, 11.3, 0.2)

    # plot histogram
    style0 = {'facecolor': 'none', 'edgecolor': 'gray', 'linestyle': '-', 'linewidth': 1}
    style1 = {'facecolor': 'none', 'edgecolor': 'black', 'linestyle': ':', 'linewidth': 2}
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.hist(de2000_0, bins=bins, histtype='step', label=lb0, **style0)
    ax.hist(de2000_1, bins=bins, histtype='step', label=lb1, **style1)

    # axis setting
    ax.set_xlabel('印刷樣本相對於參考樣本的 $\Delta E_{00}$ 值', labelpad=10, fontsize=14)
    ax.set_ylabel('色塊數量', labelpad=10, fontsize=14)

    ax.set_xlim(0, 11.5)
    ax.set_xticks(np.arange(0, 11.5, 0.5))
    ax.set_ylim(0, 85)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    ax.legend(fontsize=14)

    return fig


def main(ref_path, com_path0, com_path1, lb0, lb1, write_path):
    ref_lab, com0_lab, com1_lab = read_datas(ref_path, com_path0, com_path1)

    com0_de = calculate_de2000(ref_lab, com0_lab)
    com1_de = calculate_de2000(ref_lab, com1_lab)

    fig = plot_histograms_overlap(com0_de, com1_de, lb0=lb0, lb1=lb1)
    plotting.save_plt_figure(fig, write_path, dpi=1200)

    # plt.show()




if __name__ == '__main__':
    ref = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv"
    toner_4c = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C\4C_50_combined.csv"
    toner_4c_b = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-B_unfinished\4C-B_unfinished_50_combined.csv"
    toner_4c_g = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-G_unfinished\4C-G_unfinished_50_combined.csv"
    toner_4c_r = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-R\4C-R_50_combined.csv"
    inkjet = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\Deepblue\NTUST_50_20240315_rgb.csv"

    # file_lst = [toner_4c, toner_4c_r, toner_4c_g, toner_4c_b, inkjet]
    # file_name = ['Toner 4C', 'Toner 4C+R', 'Toner 4c+G', 'Toner 4C+B', 'Inkjet']
    #
    # for i in range(len(file_lst)):
    #     write_path = Path('output') / f"Histogram of DE2000 Value Differences_{file_name[i]}.png"
    #     txt_output_path = Path('output') / f"Histogram of DE2000 Value Differences_{file_name[i]}.txt"
    #     plot_de_histogram(ref, file_lst[i], write_path, txt_output_path)

    write_path = Path('output') / f"Histogram of DE2000 Value Differences-CMYK_inkjet.png"
    main(ref, toner_4c, inkjet, "CMYK 印刷模式", "專業噴墨", write_path)