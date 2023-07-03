import csv
import numpy as np
import matplotlib.pyplot as plt
import colour
import os
import time


class MunsellColor:
    def __init__(self, filePath):
        self.filepath = filePath
        self.data = self.readFile(filePath)

    @staticmethod
    def readFile(filePath):
        data = []
        with open(filePath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                data.append(row)
        return np.array(data)

    def HVC(self):
        """
        :return: array with string data type
        """
        h_index = 0
        v_index = 1
        c_index = 2
        hvc_data = self.data[:, [h_index, v_index, c_index]]
        return np.array(hvc_data)

    def RGB(self):
        r_index = 3
        g_index = 4
        b_index = 5
        rgb_data = []
        empty_mask = self.data[:, r_index] == ''
        if empty_mask.any():
            Lab_data = self.Lab()
            XYZn_arr = colour.Lab_to_XYZ(Lab_data)
            rgb_data = XYZn_to_AdobeRGB(XYZn_arr)
        else:
            rgb_data = self.data[:, [r_index, g_index, b_index]]
        return np.array(rgb_data, dtype="int")

    def Lab(self):
        l_index = 6
        a_index = 7
        b_index = 8
        lab_data = self.data[:, [l_index, a_index, b_index]]
        return np.array(lab_data, dtype="float64")


def gamma_AdobeRGB(c):
    if c <= 0.0:
        return 0.0
    return pow(c, 1 / 2.19921875)


def XYZn_to_AdobeRGB(input):
    """
    :param input: XYZn np.array
    :return : Adobe RGB np.array
    """
    output_arr = []
    for i in input:
        Xn, Yn, Zn = i[0], i[1], i[2]
        Rlin = Xn * 2.04159 + Yn * -0.56501 + Zn * -0.34473
        Glin = Xn * -0.96924 + Yn * 1.87597 + Zn * 0.04156
        Blin = Xn * 0.01344 + Yn * -0.11836 + Zn * 1.01517
        R = round(255 * gamma_AdobeRGB(Rlin))
        G = round(255 * gamma_AdobeRGB(Glin))
        B = round(255 * gamma_AdobeRGB(Blin))
        output_arr.append([R, G, B])
    return np.array(output_arr)


def lab2AdobeRgb(input):
    """
    Lab transfer to XYZn, Then XYZn transfer to Adobe RGB
    :param input: Lab np.array
    :return: Adobe RGB np.array
    """
    XYZn_arr = colour.Lab_to_XYZ(input.Lab())
    return XYZn_to_AdobeRGB(XYZn_arr)


def colorDe2000(Lab1, Lab2):
    de2000_arr = []
    for x, y in zip(Lab1, Lab2):
        de2000 = colour.difference.delta_E_CIE2000(x, y)
        de2000_arr.append(de2000)
    return np.array(de2000_arr)


def phraseTitle(path):
    return os.path.basename(path)[:-4]


def axisSetting(ax, file_name):
    # Axis setting
    x_ticks = np.arange(2, 22, 2)
    x_lables = [f'/{x}' for x in x_ticks]
    y_ticks = np.arange(1, 10)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_lables)
    ax.set_yticks(y_ticks)
    ax.tick_params(axis='x', direction='in', pad=-18)
    ax.tick_params(axis='y', direction='in', pad=-18)
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 10)
    ax.xaxis.set_tick_params(color='none')
    ax.yaxis.set_tick_params(color='none')
    ax.set_xlabel(file_name, fontsize=26, loc='right', labelpad=-54)
    # ax.set_ylabel("Value", fontsize=15)
    # ax.set_title(phraseTitle(munsell.filepath), fontsize=20, y=1.0, pad=-20)

    # Spines setting
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


def plotMunsellScatter(munsell1, munsell2):
    # Load ata
    c_arr = (munsell2.HVC()[:, 2]).astype(float)
    v_arr = (munsell1.HVC()[:, 1]).astype(float)
    colors_arr = munsell2.RGB() / 255.0
    de2000_arr = colorDe2000(munsell1.Lab(), munsell2.Lab())

    # Plot fig
    fig, ax = plt.subplots(figsize=(10, 9))

    for i in range(len(c_arr)):
        text_c = 'w' if v_arr[i] <= 4 else 'k'
        text_c = 'r' if de2000_arr[i] > 2.0 else text_c
        face_c = '#C5C9C7' if de2000_arr[i] > 2.0 else 'none'
        ax.scatter(c_arr[i], v_arr[i], marker='s', s=1600, color=colors_arr[i])
        ax.scatter(c_arr[i], v_arr[i], s=750, facecolors=face_c, edgecolors='w')
        ax.text(c_arr[i], v_arr[i], round(de2000_arr[i], 1), c=text_c, ha='center', va='center_baseline')

    file_name = phraseTitle(munsell2.filepath)
    axisSetting(ax, file_name)
    return fig


def saveFig(fig, path, title):
    save_path = path
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    fig.savefig(os.path.join(save_path, title + '.png'), dpi=600)


if __name__ == '__main__':
    start_time = time.time()

    ref_path = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiment\Munsell_Reproduction\dataset_HVC_RGB_Lab"
    compared_path = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiment\Munsell_Reproduction\SunSui\DE_CSV"
    save_path = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiment\Munsell_Reproduction\SunSui\Munsell_chart_with_de"

    ref_folders = os.listdir(ref_path)
    compared_folders = os.listdir(compared_path)
    common_folders = set(ref_folders) & set(compared_folders)

    for folder in common_folders:
        print(f'Processing the folder {folder}')
        if folder != "N":
            ref_folder_path = os.path.join(ref_path, folder)
            com_folder_path = os.path.join(compared_path, folder)
            ref_base_files = os.listdir(ref_folder_path)  # base file
            com_base_files = os.listdir(com_folder_path)  # base file

            for ref_base_file in ref_base_files:
                ref_hue_name = ref_base_file[:-4]
                for com_base_file in com_base_files:
                    com_hue_name = com_base_file[:-4].split('-')[0]

                    if ref_hue_name == com_hue_name:
                        ref_data = MunsellColor(os.path.join(ref_folder_path, ref_base_file))
                        com_data = MunsellColor(os.path.join(com_folder_path, com_base_file))
                        if ref_data.RGB().shape == com_data.RGB().shape:
                            fig = plotMunsellScatter(ref_data, com_data)
                            saveFig(fig, os.path.join(save_path, folder), com_base_file)
                            plt.close()
                            print(f"File is saved at {os.path.join(save_path, folder)} named {com_base_file[:-4]}")
                        else:
                            print(f"{ref_hue_name} and {com_hue_name} shape are not the same")
        else:
            pass

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Programing execution time: {execution_time} seconds")
