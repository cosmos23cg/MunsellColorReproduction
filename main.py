import os.path

import colour.difference
import matplotlib.pyplot as plt
from pathlib import Path

from lib import utilities, plot

class PlotMunsellScatter:
    def __init__(self):
        # TODO: Have to modified because there this info is not nessery needed.
        self.ref_munsell = None
        self.com_munsell = None

    def _extract(self, munsell_path):
        self.ref_munsell = utilities.MunsellColor(munsell_path, '.csv')
        vc_dict = self.ref_munsell.VC()
        rgb_dict = self.ref_munsell.RGB()
        lab_dict = self.ref_munsell.Lab()
        return vc_dict, rgb_dict, lab_dict

    @staticmethod
    def save_fig(fig, path, file_name):
        if not os.path.exists(path):
            os.makedirs(path)
        fig.savefig(Path(path, file_name).with_suffix('.png'), dpi=600)

    def plot_munsell_scatter(self, munsell_path, save_path):
        vc_dict, rgb_dict,_ = self._extract(munsell_path)

        for idx, key in enumerate(self.ref_munsell.munsell_dict.keys()):
            if key == 'header':
                continue
            if len(vc_dict[key]) == len(rgb_dict[key]):
                munsell_scatter = plot.MunsellScatter()
                fig = munsell_scatter.scatter(vc_dict[key], rgb_dict[key], key)
                self.save_fig(fig, save_path, key)
                plt.close()
                # plt.show()

    def plot_munsell_scatter_de(self, munsell_path1, munsell_path2, save_path):
        ref_vc_dict, ref_rgb_dict, ref_lab_dict = self._extract(munsell_path1)
        com_vc_dict, com_rgb_dict, com_lab_dict = self._extract(munsell_path2)

        for idx, key in enumerate(self.ref_munsell.munsell_dict.keys()):
            if key == 'header':
                continue
            if len(ref_rgb_dict[key]) == len(com_rgb_dict[key]):
                de_arr = colour.difference.delta_E_CIE2000(ref_lab_dict[key], com_lab_dict[key])

                munsell_scatter_de = plot.MunsellScatter()
                fig = munsell_scatter_de.scatter_de(ref_vc_dict[key], ref_rgb_dict[key], de_arr, key)
                self.save_fig(fig, save_path, key)
                # plt.show()
                plt.close()

    def plot_contour_chart(self, munsell_path1, munsell_path2, save_path):
        ref_vc_dict, ref_rgb_dict, ref_lab_dict = self._extract(munsell_path1)
        com_vc_dict, com_rgb_dict, com_lab_dict = self._extract(munsell_path2)

        for idx, key in enumerate(self.ref_munsell.munsell_dict.keys()):
            if key == 'header':
                continue
            if len(ref_lab_dict[key]) == len(com_lab_dict[key]):
                de_arr = colour.difference.delta_E_CIE2000(ref_lab_dict[key], com_lab_dict[key])

                contour_chart = plot.ContourChart()
                fig = contour_chart.contourf(ref_vc_dict[key], de_arr, key)
                self.save_fig(fig, save_path, key)
                plt.close()
                # plt.show()

if __name__ == '__main__':
    fol = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction"
    ref = r"Dataset_BabelColour_HVC_RGB_Lab_D50"
    com = r"SunSui\SunSui_deReport_CSV\4C-R"
    save = r"Save_fig\contour"
    fmt = '.csv'
    ref_path = Path(fol, ref)
    com_path = Path(fol, com)
    save_path = Path(fol, save)

    # main
    plotMunsellScatter = PlotMunsellScatter()

    # plotMunsellScatter.plot_munsell_scatter(ref_path)
    # plotMunsellScatter.plot_munsell_scatter_de(ref_path, com_path, save_path)

    # plotMunsellScatter.plot_contour_chart(ref_path, com_path, save_path)



