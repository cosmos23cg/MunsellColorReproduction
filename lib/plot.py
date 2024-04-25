from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from lib.error import PlotFunctionError

class Gamut:
    """
    1. plot single gamut (finished)
    2. plot multiple gamut via args (finished)
    3. choose the diagram (CIE xy, CIE 1976Lab, CIE 1976Luv)
    """
    def __init__(self, figsize):
        self.fig, self.ax = plt.subplots(figsize=figsize)  # Create a figure and axis
        self.points = []

    def axis_setting(self, xlim=(-130, 130), ylim=(-100, 130)):
        self.ax.grid(which='both', alpha=0.2)
        self.ax.set_xlim(xlim[0], xlim[1])
        self.ax.set_ylim(ylim[0], ylim[1])

        self.ax.set_xlabel("a*")
        self.ax.set_ylabel("b*")
        self.ax.legend(loc='lower left')

    def add_points(self, points: list, c: str, ln: str, m: str, lb: str):
        """
        Parameters
        ----------
        points:
            points list(points, color, label)
        c:
            the color plotted in figure
        ln:
            line symbol
        m:
            marker symbol
        lb:
            label name
        """
        self.points.append((points, c, ln, m, lb))

    def plot_gamut(self):
        for points, color, line, marker, label in self.points:
            x, y = zip(*points)

            self.ax.plot(x, y, color + line, label=label)  # line
            self.ax.plot(x, y, color + marker)  # marker

        self.axis_setting()

        return self.fig


class Contour:
    def __init__(self, nrows=1, ncols=1, **kwargs):
        self.fig, self.axs = plt.subplots(nrows, ncols, **kwargs)
        self.points = []
        self.cont = None
        self.cbar = None

    def _contour_axis_setting(self, cont):
        # The z number show by legend
        self.fig.subplots_adjust(right=0.8)

        artists, labels = cont.legend_elements(str_format='{:2.1f}'.format)
        self.axs[1].legend(artists, labels, handleheight=2, framealpha=1, loc='center left', bbox_to_anchor=(1.1, 0.5))

        # show each z inline
        # for ax in self.axs:
        #     ax.clabel(cont, fmt="%2.1f", use_clabeltext=True)

    def _contourf_axis_setting(self, cont, lv):
        if self.cbar is None:
            self.fig.subplots_adjust(right=0.8)

            cbar_ax = self.fig.add_axes([0.85, 0.11, 0.02, 0.78])  # setting color bar, (left, bottom, width, height)
            self.cbar = self.fig.colorbar(cont, cax=cbar_ax, format='%.2f', ticks=lv)

    def add_points(self, x, y, z, lv, cmap, title: str):
        self.points.append((x, y, z, lv, cmap, title))

    def axis_setting(self, cont, lv, plotm, **kwargs):
        """
        parameters
        ----------
        plotm:
            plot method: 'unfilled', 'filled'
        """
        # Common settings
        self.fig.text(0.5, 0.02, 'a*', ha='center', size=12)
        self.fig.text(0.07, 0.5, 'b*', va='center', size=12, rotation='vertical')

        # sub_figure settings
        for ax in self.axs:
            ax.set_aspect(aspect='equal', adjustable='box')
            ax.grid(True, alpha=0.2)

        # set x, y limit
        if 'xlim' in kwargs and 'ylim' in kwargs:
            for ax in self.axs.flat:
                ax.set_xlim(kwargs['xlim'])
                ax.set_ylim(kwargs['ylim'])

        # Custom settings
        if plotm == 'unfilled':
            self._contour_axis_setting(cont)

        if plotm == 'filled':
            self._contourf_axis_setting(cont, lv)

    def plot_tricontour(self, main_title, **kwargs):
        if len(self.points) <= 1:
            raise PlotFunctionError("self.points have two list more")

        for idx, (x, y, z, lv, cmap, title) in enumerate(self.points):
            cont = self.axs[idx].tricontour(x, y, z, lv, cmap=cmap)
            self.axs[idx].set_title(title)
            self.axis_setting(cont, lv, plotm="unfilled", **kwargs)

        self.fig.suptitle(main_title, y=0.961, ha='center', size=14, weight='bold')

        return self.fig

    def plot_tricontourf(self, main_title, **kwargs):
        """
        Plot the contour fig

        Parameters
        ----------

        """
        if len(self.points) <= 1:
            raise PlotFunctionError("self.points have two list more")

        for idx, (x, y, z, lv, cmap, title) in enumerate(self.points):
            cont = self.axs[idx].tricontourf(x, y, z, lv, cmap=cmap)
            self.axs[idx].set_title(title)
            self.axis_setting(cont, lv, plotm='filled',**kwargs)

        self.fig.suptitle(main_title, y=0.961, ha='center', size=14, weight='bold')

        return self.fig


class MunsellScatter:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 9))
        self.marker_type = 's'

    def _basic_scatter(self, x, y, color):
        self.ax.scatter(x, y, s=1500, c=color, marker=self.marker_type)

    def _scatter_axis(self, title):
        self.ax.set_xlim(0, 21)
        self.ax.set_ylim(0, 10)
        # ticks
        x_ticks = list(range(2, 21, 2))
        y_ticks = list(range(1, 10, 1))
        self.ax.set_xticks(x_ticks)
        self.ax.set_yticks(y_ticks)
        self.ax.tick_params(axis='both', pad=-18, labelsize=14, color="None")
        # label
        x_labels = [f'/{x}' for x in x_ticks]
        y_labels = [f'{y}/' for y in y_ticks]
        self.ax.set_xticklabels(x_labels)
        self.ax.set_yticklabels(y_labels)
        # title
        self.ax.set_title(title, fontsize=20)
        # spines
        self.ax.spines.bottom.set_visible(False)
        self.ax.spines.left.set_visible(False)
        self.ax.spines.right.set_visible(False)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    def scatter(self, val_chroma: list, rgb: list, title: str):
        """
        Plot the scatter, x-axis: chroma, y-axis: value

        Parameters
        ----------
        val_chroma:
            value and chroma list or array by each hue
        rgb:
            rgb list by each hue
        title:
            hue name
        """
        val_arr = np.array(val_chroma[:, 0])
        chroma_arr = np.array(val_chroma[:, 1])
        rgb_arr = np.array(rgb)

        self._basic_scatter(chroma_arr, val_arr, rgb_arr)
        self._scatter_axis(title)
        return self.fig

    def scatter_de(self, val_chroma: list, rgb: list, de, title):
        """
        Plot the scatter, x-axis: chroma, y-axis: value

        Parameters
        ----------
        val_chroma:
            value and chroma list or array by each hue
        rgb:
            rgb list by each hue
        de:
            color differance by each hue
        title:
            hue name
        """
        val_arr = np.array(val_chroma[:, 0])
        chroma_arr = np.array(val_chroma[:, 1])
        de_arr = np.array(de)
        face_color = np.where(de_arr > 0, '#C5C5C5', '#696969')

        self._basic_scatter(chroma_arr, val_arr, rgb)
        self.ax.scatter(
            chroma_arr,
            val_arr,
            s=900,
            facecolors=face_color,
            edgecolor='w'
        )

        for i in range(len(de_arr)):
            text_color = 'w'
            text_color = 'r' if de_arr[i] > 2.0 else text_color
            self.ax.text(
                chroma_arr[i],
                val_arr[i],
                round(de_arr[i], 1),
                c=text_color,
                ha='center',
                va='center_baseline',
                fontsize=13
            )
            self._scatter_axis(title)
        return self.fig


def save_plt_figure(figure: plt.Figure, write_path, **kwargs):
    figure.savefig(write_path, **kwargs)
    print(f"Fig saved: {write_path}")
    plt.close()
