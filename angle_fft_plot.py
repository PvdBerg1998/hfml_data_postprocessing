#
#   angle_fft_plot.py
#   Helper script to preload dataframes and push them to Origin.
#
#   Copyright (C) 2021 Pim van den Berg
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import os
import numpy as np
import pandas as pd
import origin as op


def angle_data(sample, direction, var, type, angle):
    directory = f"C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe/{sample}/output/Angle_Dependence_4p2K_pos_{direction}/{var}/{type}/"
    if angle < 0:
        prefix = "m"
    else:
        prefix = ""
    for file in os.listdir(directory):
        if file.startswith(f"{prefix}{int(np.abs(angle))}_"):
            return pd.read_csv(os.path.join(directory, file), names=["x", "y"])
    return None


# region of interest
a = 100
b = 700

dataset = []
names = []
for angle in [-10, -5, 0, 5, 10, 20, 30, 40]:
    print(f"Loading angle {angle}")
    df = angle_data(
        sample="Zr3_5584_nb_sc",
        direction="down",
        var="Rxx68",
        type="fft",
        angle=angle
    )
    assert(df is not None)
    dataset.append(df)
    names.append(f"{angle} deg")

# Normalise to 0 deg
zero_deg = dataset[2]
assert(names[2] == "0 deg")
normalisation = zero_deg[zero_deg.x.between(a, b)].y.max()

op.fft_stacked_plot(
    dataset,
    names,
    normalisation,
    xstart=a,
    xend=b,
    legendmargin=5,
    filename="Zr3_5584_nb_sc_angles_Rxx68_down"
)

op.close_origin()
