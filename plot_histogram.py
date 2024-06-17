from lib import plotting, utilities
from pathlib import Path
from colour.difference import delta_E_CIE2000
import matplotlib.pyplot as plt
import numpy as np


def read_data(ref_path, com_path):
    """
    Read reference and comparison data from CSV files.

    Args:
    ref_path (str): Path to the reference CSV file.
    com_path (str): Path to the comparison CSV file.

    Returns:
    tuple: Two lists containing Lab values for reference and comparison data.
    """
    ref_data = utilities.read_csv(ref_path, skip_lines=1)
    com_data = utilities.read_csv(com_path, skip_lines=1)

    ref_lab = [x[-3:] for x in ref_data]
    com_lab = [x[-3:] for x in com_data]

    return ref_lab, com_lab


def calculate_de2000(ref_lab, com_lab):
    """
    Calculate delta E 2000 values between reference and comparison Lab values.

    Args:
    ref_lab (list): List of Lab values for reference data.
    com_lab (list): List of Lab values for comparison data.

    Returns:
    list: List of delta E 2000 values.
    """
    return delta_E_CIE2000(ref_lab, com_lab)


def plot_histogram(de_2000):
    """
    Plot histogram of delta E 2000 values with median and mean lines.

    Args:
    de_2000 (list): List of delta E 2000 values.
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

    ax.axvline(x=median_de, color='r', linestyle='dashed', linewidth=1,
               label=f'Median $\Delta E_{{00}}$: {median_de:.2f}')
    ax.axvline(x=mean_de, color='b', linestyle='dashed', linewidth=1,
               label=f'Mean $\Delta E_{{00}}$\u2003: {mean_de:.2f}')

    # axis setting
    ax.set_xlabel('Printed sample $\Delta E_{00}$ from reference sample', labelpad=10)
    ax.set_ylabel('Numbers of Color Patches', labelpad=10)

    ax.set_xlim(0, 11.5)
    ax.set_xticks(np.arange(0, 11.5, 0.5))
    ax.set_ylim(0, 85)

    ax.legend(fontsize=10)

    return fig


def plot_de_histogram(ref_path, com_path, write_path):
    """
    Main function to read data, calculate delta E 2000 values, and plot histogram.

    Args:
    ref_path (str): Path to the reference CSV file.
    com_path (str): Path to the comparison CSV file.
    """
    ref_lab, com_lab = read_data(ref_path, com_path)
    de_2000 = calculate_de2000(ref_lab, com_lab)
    fig = plot_histogram(de_2000)
    plotting.save_plt_figure(fig, write_path, dpi=1200)
    # plt.show()

if __name__ == '__main__':
    ref = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv"
    toner_4c = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C\4C_50_combined.csv"
    toner_4c_b = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-B_unfinished\4C-B_unfinished_50_combined.csv"
    toner_4c_g = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-G_unfinished\4C-G_unfinished_50_combined.csv"
    toner_4c_r = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-R\4C-R_50_combined.csv"
    inkjet = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Deepblue\NTUST_50_20240315_rgb.csv"

    file_lst = [toner_4c, toner_4c_b, toner_4c_g, toner_4c_r, inkjet]
    file_name = ['Toner 4C', 'Toner 4C+B', 'Toner 4c+G', 'Toner 4C+R', 'Inkjet']

    for i in range(len(file_lst)):
        write_path = Path('output') / f"Histogram of DE2000 Value Differences_{file_name[i]}.png"
        plot_de_histogram(ref, file_lst[i], write_path)