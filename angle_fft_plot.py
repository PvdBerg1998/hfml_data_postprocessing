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


def angle_data(sample, commutation, direction, var, type, angle):
    directory = f"C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe/{sample}/output/Angle_Dependence_{commutation}_{direction}/{var}/{type}/"
    if not os.path.exists(directory):
        return None
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

for sample in ["Zr3_1458_nb_hf"]: # "Zr3_5584_nb_sc", 
    for var in ["Rxx68", "Rxy37", "Rxy48", "Rxx_1_7", "Rxx_2_7", "Rxx_17_18", "Rxy_2_17"]:
        for commutation in ["pos", "neg"]:
            for direction in ["up", "down"]:
                dataset = []
                names = []
                for angle in [-10, -5, 0, 5, 10, 20, 25, 30, 40, 45, 50, 60, 70, 75, 80, 90]:
                    df = angle_data(
                        sample=sample,
                        commutation=commutation,
                        direction=direction,
                        var=var,
                        type="fft",
                        angle=angle
                    )
                    # Ignore missing configurations
                    if df is None:
                        continue
                    print(f"Found angle {angle}")
                    df = df[df.x.between(a, b)]
                    dataset.append(df)
                    names.append(f"{angle} deg")

                # Ignore missing configurations
                if len(dataset) == 0:
                    continue

                print(f"Processing {sample}: {var} {commutation} {direction}")

                # Normalise
                normalisation = 0
                for df in dataset:
                    normalisation = max(normalisation, df.y.max())
                for df in dataset:
                    df.y = df.y / normalisation

                op.fft_stacked_plot(
                    dataset,
                    names,
                    xstart=a,
                    xend=b,
                    xtick_interval=100,
                    offset=1.1,
                    directory=os.path.join(
                        "C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe", f"plots/{sample}/angle/{var}/{commutation}/{direction}/"),
                )

op.close_origin()
