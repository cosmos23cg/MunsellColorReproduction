from test import untitle
from test import ref_data_obj

import colour

if __name__ == '__main__':
    # Check whether a point in a gamut
    in_gamut = untitle.Gamut('Adobe RGB (1998)')
    for i in range(len(ref_data_obj.xyY())):
        result = in_gamut.isInside_CrossMethod(ref_data_obj.xyY()[i])
        if result:
            print(f"{ref_data_obj.HVC()[i]}In the Triangle")
        else:
            print(f"{ref_data_obj.HVC()[i]}Out of the Triangle")

    colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931(
        RGB=ref_data_obj.RGB(),
        spectral_locus_colours="RGB",
        colourspace='Adobe RGB (1998)',
        scatter_kwargs={"s": 5, "alpha": 1},
    )