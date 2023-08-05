from lib import munsell, plot

import numpy as np
import matplotlib.pyplot as plt
import colour
import os
import time


def phraseTitle(path):
    return os.path.basename(path)[:-4]


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
                        ref_data = munsell.MunsellColor(os.path.join(ref_folder_path, ref_base_file))
                        com_data = munsell.MunsellColor(os.path.join(com_folder_path, com_base_file))
                        if ref_data.RGB().shape != com_data.RGB().shape:
                            fig = plot.PlotScatter.plotMunsellScatter(ref_data, com_data)
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
