from lib import utilities, plotting, conversion
from pathlib import Path
import re
from colour.difference import delta_E_CIE2000
import colour
import matplotlib.pyplot as plt
import numpy as np


hue_angles = {
    'R': 0, 'YR': 36, 'Y': 72, 'GY': 108,
    'G': 144, 'BG': 180, 'B': 216, 'PB': 252, 'P': 288, 'RP': 324
}

def norm_rgb(rgb: list):
    """
    input data is 1D array
    """
    result = []
    for val in rgb:
        val = int(val)
        norm_val = val / 255.0
        result.append(norm_val)

    return result


def plot_munsell_hue_page(ref_path, write_dir):
    ref_data = utilities.read_csv(ref_path, skip_lines=1)
    ref_grouped = utilities.group_by(ref_data, group_col=0)

    for idx, key in enumerate(ref_grouped.keys()):
        v = [int(x[1]) for x in ref_grouped[key]]
        c = [int(x[2]) // 2 for x in ref_grouped[key]]

        ref_lab = [x[-3:] for x in ref_grouped[key]]

        illuminant_D50 = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D50']
        com_XYZ = colour.Lab_to_XYZ(ref_lab, illuminant_D50)

        com_sRGB = colour.XYZ_to_sRGB(com_XYZ, illuminant_D50, 'Bradford')
        com_sRGB_clipped = np.clip(com_sRGB, 0, 1)

        # com_AdobeRGB = colour.XYZ_to_RGB(com_XYZ,
        #                                  colour.models.RGB_COLOURSPACE_ADOBE_RGB1998,
        #                                  illuminant_D50,
        #                                  "Bradford")
        #
        # com_sRGB = colour.RGB_to_RGB(com_AdobeRGB,
        #                              colour.models.RGB_COLOURSPACE_ADOBE_RGB1998,
        #                              colour.models.RGB_COLOURSPACE_sRGB,
        #                              chromatic_adaptation_transform='Bradford')

        rgb = [norm_rgb(x[3:6]) for x in ref_grouped[key]]

        hue_page = plotting.MunsellHuePage(1, 1, figsize=(10, 8))
        fig = hue_page.plot_munsell_hue_page(x=c, y=v, color=com_sRGB_clipped, title=key)

        write_path = write_dir + f'-{key}.png'
        plotting.save_plt_figure(fig, write_path=write_path, dpi=1200)
        # plt.show()
        plt.close()


def pass_rate(de):
    pass_num = 0

    for d in de:
        if d <= 2:
            pass_num += 1

    return pass_num, len(de), (pass_num / len(de)) * 100


def plot_munsell_hue_page_de(ref_path, com_path, write_dir):
    ref_data = utilities.read_csv(ref_path, skip_lines=1)
    com_data = utilities.read_csv(com_path, skip_lines=1)

    ref_grouped = utilities.group_by(ref_data, group_col=0)
    com_grouped = utilities.group_by(com_data, group_col=0)

    for idx, key in enumerate(ref_grouped.keys()):

        v = [int(x[1]) for x in com_grouped[key]]
        c = [int(x[2]) // 2 for x in com_grouped[key]]

        ref_lab = [x[-3:] for x in ref_grouped[key]]
        com_lab = [x[-3:] for x in com_grouped[key]]

        de2000 = delta_E_CIE2000(ref_lab, com_lab)

        illuminant_D50 = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D50']

        com_XYZ = colour.Lab_to_XYZ(com_lab, illuminant_D50)
        com_sRGB = colour.XYZ_to_sRGB(com_XYZ, illuminant_D50, 'Bradford')
        com_sRGB_clipped = np.clip(com_sRGB, 0, 1)

        hue_page = plotting.MunsellHuePage(1, 1, figsize=(10, 8))
        key = re.sub(r'\.0', '', key)
        fig = hue_page.plot_munsell_hue_page(x=c, y=v, color=com_sRGB_clipped, de=de2000, title=key)

        write_path = write_dir + f'-{key}.png'
        plotting.save_plt_figure(fig, write_path=write_path, dpi=1200)
        # plt.show()
        plt.close()

        # # write passing rate
        # write_txt_path = write_dir + f'_pass_rate-{key}.txt'
        # pass_num, total_patchs, rate = pass_rate(de2000)
        # with open(write_txt_path, 'w') as file:
        #     file.write("total patch:\n")
        #     file.write(str(total_patchs) + '\n')
        #     file.write('pass numbers:\n')
        #     file.write(str(pass_num) + '\n')
        #     file.write('rate:\n')
        #     file.write(str(rate) + '\n')



def plot_munsell_hue_circle(ref_path):
    """
    Plot munsell page as hue circle
    """

    hue_angles = {
        '5.0R': 0, '5.0YR': 36, '5.0Y': 72, '5.0GY': 108,
        '5.0G': 144, '5.0BG': 180, '5.0B': 216, '5.0PB': 252, '5.0P': 288, '5.0RP': 324
    }

    ref_data = utilities.read_csv(ref_path, skip_lines=1)
    ref_grouped = utilities.group_by(ref_data, group_col=1)  # group by value

    for idx, key0 in enumerate(ref_grouped.keys()):
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'polar': True})

        group_hue = utilities.group_by(ref_grouped[key0], group_col=0)
        for idx, key1 in enumerate(group_hue.keys()):
            chroma = [int(x[2]) for x in group_hue[key1]]
            rgb = [norm_rgb(x[3:6]) for x in group_hue[key1]]

            angles = [hue_angles[key1]] * len(chroma)
            ax.scatter(np.deg2rad(angles), chroma, c=rgb, s=300)

            angle = hue_angles[key1]
            ax.text(np.deg2rad(angle), 22, f'{key1}', horizontalalignment='center')

        # Set y-ticks and limit
        yticks = range(2, 20, 2)
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticks)
        ax.set_ylim(-1, 20)

        # Hide angle labels
        ax.set_xticks([])
        ax.set_xticklabels([])

        # Set 0 degrees to North and direction to clockwise
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)

        # Set grid style
        ax.grid(linestyle='--', linewidth=0.5, alpha=0.3)

        # Show legend
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), fontsize=10, frameon=True, framealpha=0.9, borderpad=1)

        plt.tight_layout()
        # plt.show()

        write_path = f'output/hue circle-ref-{key0}.png'
        plotting.save_plt_figure(fig, write_path, dpi=600)

# def plot_munsell_scatter_lightness(ref_path):
#     ref_data: list = utilities.read_csv(ref_path)
#     ref_munsell = utilities.MunsellColor(ref_data)
#
#     for idx, key in enumerate(ref_munsell.vc().keys()):
#         ref_l: list = [[x[0], 0, 0] for x in ref_munsell.lab()[key]]  # only fetch L* and attend 0 in a* b*
#         ref_XYZ: np.ndarray = colour.Lab_to_XYZ(ref_l)
#         ref_sRGB = colour.XYZ_to_sRGB(ref_XYZ)
#
#         '''
#         # https://e2eml.school/convert_rgb_to_grayscale
#         # https://www.baeldung.com/cs/convert-rgb-to-grayscale
#         # NTSC formula: 0.299 ∙ Red + 0.587 ∙ Green + 0.114 blue
#         # https://stackoverflow.com/questions/8202605/how-to-color-scatter-markers-as-a-function-of-a-third-variable
#         ref_lab = ref_munsell.lab()[key]
#         ref_XYZ = colour.Lab_to_XYZ(ref_lab)
#         ref_adobe_RGB = colour.XYZ_to_RGB(ref_XYZ, colour.RGB_COLOURSPACES['Adobe RGB (1998)'])
#         ref_Y = [str((0.299 * x[0] + 0.587 * x[1] + 0.114 * x[2])) for x in ref_adobe_RGB]
#         '''
#         v = [x[0] for x in ref_munsell.vc()[key]]
#         c = [x[1] / 2 for x in ref_munsell.vc()[key]]
#         str_l = [x[0] for x in ref_l]
#
#         munsell_hue_page = plotting.MunsellHuePage(1, 1, figsize=(10, 8))
#         fig = munsell_hue_page.plot_munsell_hue_page(x=c, y=v, color=ref_sRGB, title=f"{key}", de=str_l)
#         write_path = write_dir.parent.joinpath(write_dir.name + f"_{key}_ab_zero_method.png")
#         # plotting.save_plt_figure(fig, write_path, dpi=1200)
#         # plt.close(fig)


if __name__ == '__main__':
    ref = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv"
    toner_4c = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C\4C_50_combined.csv"
    toner_4c_b = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-B_unfinished\4C-B_unfinished_50_combined.csv"
    toner_4c_g = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-G_unfinished\4C-G_unfinished_50_combined.csv"
    toner_4c_r = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-R\4C-R_50_combined.csv"
    inkjet = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Deepblue\NTUST_50_20240315_rgb.csv"

    file_lst = [toner_4c, toner_4c_b, toner_4c_g, toner_4c_r, inkjet]
    file_name = ['Toner_4C', 'Toner_4C+B', 'Toner_4c+G', 'Toner_4C+R', 'Inkjet']

    for i in range(len(file_lst)):
        write_dir = f'output/hue_page-{file_name[i]}'
        plot_munsell_hue_page_de(ref, file_lst[i], write_dir)


    # plot_munsell_hue_circle(ref)

    # plot_munsell_scatter_lightness(toner_path)

