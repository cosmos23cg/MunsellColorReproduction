from lib import utilities

import numpy as np
import matplotlib.pyplot as plt
from lib.error import PlotFunctionError


class Gamut:
    """
    1. plot single gamut (finished)
    2. plot multiple gamut via args (finished)
    3. choose the diagram (CIE xy, CIE 1976Lab, CIE 1976Luv)
    """
    def __init__(self, nrows, ncols, **kwarg):
        self.fig, self.ax = plt.subplots(nrows, ncols, **kwarg)  # Create a figure and axis
        self.points = []
        self.area = []

    def axis_setting(self, xlim=(-130, 130), ylim=(-100, 140)):
        self.ax.set_aspect(aspect='equal', adjustable='box')
        self.ax.grid(which='both', alpha=0.2)

        self.ax.set_xlim(xlim[0], xlim[1])
        self.ax.set_ylim(ylim[0], ylim[1])

        self.ax.set_xlabel("a*")
        self.ax.set_ylabel("b*")

        handles, labels = self.ax.get_legend_handles_labels()
        new_labels = [f'{label:>7}:{area[1]:>8.2f}%' for label, area in zip(labels, self.area)]
        self.ax.legend(handles, new_labels, loc='center left', bbox_to_anchor=(1, 0.5), title='Legend & area ratio\n')

        self.fig.subplots_adjust(right=0.8)

    def add_annotate(self, ant_cor, ant_lst):

        for i in range(len(ant_lst)):
            x = ant_cor[i][0]
            y = ant_cor[i][1]
            annotate = ant_lst[i][0]

            if x > 0 and y > 0:
                # Quadrant 1
                xytext = (10, 3)
            elif y > 0 > x:
                # Quadrant 2
                xytext = (-15, 3)
            elif x < 0 and y < 0:
                # Quadrant 3
                xytext = (-13, -15)
            else:
                # Quadrant 4
                xytext = (15, -15)

            self.ax.annotate(f"{annotate}", (x, y), textcoords='offset points', xytext=xytext, ha='center')

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

    def gamut_area(self, *args: list):
        areas = []
        for arg in args:
            crt_area = 0
            for i in range(0, len(arg) - 1):
                a = arg[i]
                b = arg[i + 1]

                area = utilities.triangle_area(a, b, (0, 0))
                crt_area += area

            areas.append(crt_area)

        self.area = utilities.area_ratio(areas[0], areas)

    def plot_gamut(self):
        for points, color, line, marker, label in self.points:
            x = [x[0] for x in points]
            y = [x[1] for x in points]

            self.ax.plot(x, y, color + line, label=label)  # line
            self.ax.plot(x, y, color + marker)  # marker

        self.axis_setting()

        return self.fig


class Contour:
    # TODO: add the area of the contour
    def __init__(self, nrows=1, ncols=1, **kwargs):
        self.fig, self.axs = plt.subplots(nrows, ncols, **kwargs)
        self.points = []
        self.cont = None
        self.cbar = None

    def _contour_axis_setting(self, cont):
        # The z number show by legend
        self.fig.subplots_adjust(right=0.8)

        artists, labels = cont.legend_elements(str_format='{:.0f}'.format)
        artists = artists[::-1]
        labels = labels[::-1]
        labels = [x.replace('x = ', '') for x in labels]

        self.axs[1].legend(artists,
                           labels,
                           handleheight=2,
                           framealpha=1,
                           loc='center left',
                           bbox_to_anchor=(1.1, 0.5),
                           title='dE2000\n')

        # show each z inline
        # for ax in self.axs:
        #     ax.clabel(cont, fmt="%2.1f", use_clabeltext=True)

    def _contourf_axis_setting(self, cont, lv):
        if self.cbar is None:
            self.fig.subplots_adjust(right=0.8)

            cbar_ax = self.fig.add_axes([0.85, 0.11, 0.02, 0.78])  # setting color bar, (left, bottom, width, height)
            self.cbar = self.fig.colorbar(cont, cax=cbar_ax, format='%.0f', ticks=lv)  # .0f: rounding

    def add_points(self, x, y, z, lv, cmap, title: str):
        self.points.append((x, y, z, lv, cmap, title))

    def axis_setting(self, cont, lv, plotm, **kwargs):
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
        if len(self.points) <= 1:
            raise PlotFunctionError("self.points have two list more")

        for idx, (x, y, z, lv, cmap, title) in enumerate(self.points):
            cont = self.axs[idx].tricontourf(x, y, z, lv, cmap=cmap)
            self.axs[idx].set_title(title)
            self.axis_setting(cont, lv, plotm='filled', **kwargs)

        self.fig.suptitle(main_title, y=0.961, ha='center', size=14, weight='bold')

        return self.fig


class Box:
    def __init__(self, nrows, ncols, **kwarg):
        self.fig, self.ax = plt.subplots(nrows, ncols, **kwarg)

    @staticmethod
    def _box_setting(bplot, title):
        # R, YR, Y, GY, G, BG, B, PB, P, RP
        colors = ['red', 'red',
                  'orangered', 'orangered',
                  'yellow', 'yellow',
                  'yellowgreen', 'yellowgreen',
                  'green', 'green',
                  'cyan', 'cyan',
                  'blue', 'blue',
                  'blueviolet', 'blueviolet',
                  'purple', 'purple',
                  'deeppink', 'deeppink'
                  ]

        gray_scale = ['black', 'black',
                      'dimgray', 'dimgray',
                      'gray', 'gray',
                      'darkgray', 'darkgray',
                      'silver', 'silver',
                      'lightgray', 'lightgray',
                      'gainsboro', 'gainsboro',
                      'whitesmoke', 'whitesmoke',
                      'white', 'white']

        alpha = [1.0, 1.0,
                 0.9, 0.9,
                 0.8, 0.8,
                 0.7, 0.7,
                 0.6, 0.6,
                 0.5, 0.5,
                 0.4, 0.4,
                 0.3, 0.3,
                 0.2, 0.2,
                 0.1, 0.1]

        match title:
            case 'hue':
                for patch, color in zip(bplot['boxes'], colors):
                    patch.set_facecolor(color)

            case 'value':
                for patch, scale in zip(bplot['boxes'], gray_scale):
                    patch.set_facecolor(scale)

            case 'chroma':
                for patch, alpha in zip(bplot['boxes'], alpha):
                    patch.set_alpha(alpha)

    def _axes_setting(self, xlabel, ylabel):
        self.ax.grid(alpha=0.3)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def plot_box_whisker(self, data, labels, title, write_name):
        bplot = self.ax.boxplot(data, patch_artist=True)
        self.ax.set_xticks(range(1, len(labels) + 1))  # 設置刻度位置
        self.ax.set_xticklabels(labels)  # 設置標籤
        self.ax.set_title(title)
        self._box_setting(bplot, write_name)
        self._axes_setting(xlabel=write_name, ylabel='dE2000')

        return self.fig


class MunsellHuePage:
    def __init__(self, nrows, ncols, **kwarg):
        self.fig, self.ax = plt.subplots(nrows, ncols, **kwarg)
        self.de_threshold = 2.0

    def _axis_setting(self, title):

        self.ax.set_xlim(0.5, 10.5)
        self.ax.set_xticks(list(range(1, 11, 1)))
        self.ax.set_xticklabels([f'/{x}' for x in range(2, 21, 2)])
        self.ax.set_xlabel('Chroma', labelpad=15)

        self.ax.set_ylim(0.5, 9.5)
        self.ax.set_yticks(list(range(1, 10, 1)))
        self.ax.set_yticklabels([f'{x}/' for x in range(1, 10, 1)])
        self.ax.set_ylabel('Value', labelpad=15)

        self.ax.tick_params(axis='both', labelsize=12, color="None")
        self.ax.spines.bottom.set_visible(False)
        self.ax.spines.left.set_visible(False)
        self.ax.spines.right.set_visible(False)
        self.ax.spines.top.set_visible(False)

        self.ax.set_title(title, loc='right', fontsize=28, fontweight='roman')
        self.ax.set_aspect(aspect='equal', adjustable='box')
        self.fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    def _text_de(self, x, y, de):
        for i in range(len(de)):
            ctext = 'r' if de[i] > self.de_threshold else 'w'
            self.ax.text(x[i], y[i], round(de[i], 1), c=ctext, ha='center', va='center_baseline', fontsize=11)

    def _warn_circle_hint(self, x, y, de):
        face_color = np.where(de > self.de_threshold, '#C5C5C5', '#696969')
        self.ax.scatter(x, y, s=800, facecolors=face_color, edgecolor='w')

    def plot_munsell_hue_page(self, x, y, color, title, de=None):
        self.ax.scatter(x, y, c=color, marker='s', s=1700)
        self._axis_setting(title)

        if de is not None:
            self._text_de(x, y, de)
            self._warn_circle_hint(x, y, de)

        return self.fig


def save_plt_figure(figure: plt.Figure, write_path, **kwargs):
    figure.savefig(write_path, **kwargs)
    print(f"Fig saved: {write_path}")
    plt.close()
