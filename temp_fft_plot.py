#
#   temp_fft_plot.py
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
import pandas as pd
import origin as op


def temp_data(sample, direction, var, type, temp):
    directory = f"C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe/{sample}/output/Temperature_Dependence_perp_pos_{direction}/{var}/{type}/"
    for file in os.listdir(directory):
        if file.startswith(f"{temp}"):
            return pd.read_csv(os.path.join(directory, file), names=["x", "y"])
    return None


for region in ["low", "high"]:
    for direction in ["up", "down"]:
        for var in ["Rxx68", "Rxy37", "Rxy48"]:
            # region of interest
            if region == "low":
                a = 100
                b = 700
                xtick_interval = 100
            else:
                a = 6000
                b = 8000
                xtick_interval = 400

            dataset = []
            names = []
            for temp in ["1p3", "2p5", "3p2", "4p2", "8p0", "12p0", "18p0", "25p0", "35p0", "50p0"]:
                print(f"Loading temp {temp}")
                df = temp_data(
                    sample="Zr3_5584_nb_sc",
                    direction=direction,
                    var=var,
                    type="fft",
                    temp=temp
                )
                assert(df is not None)
                df = df[df.x.between(a, b)]
                dataset.append(df)

                temp_label = temp.replace("p", ".")
                names.append(f"{temp_label} K")

            # Normalise to 1.3K
            normalisation = dataset[0].y.max()
            for df in dataset:
                df.y = df.y / normalisation

            op.fft_stacked_plot(
                dataset,
                names,
                xstart=a,
                xend=b,
                xtick_interval=xtick_interval,
                palette="Fire",
                filename=f"Zr3_5584_nb_sc_temp_{var}_{direction}_{region}freq"
            )

op.close_origin()