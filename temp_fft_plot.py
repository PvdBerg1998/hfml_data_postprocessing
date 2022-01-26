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


def temp_data(sample, commutation, direction, var, type, temp):
    directory = f"C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe/{sample}/output/Temperature_Dependence_perp_{commutation}_{direction}/{var}/{type}/"
    if not os.path.exists(directory):
        return None
    for file in os.listdir(directory):
        if file.startswith(f"{temp}"):
            return pd.read_csv(os.path.join(directory, file), names=["x", "y"])
    return None


for sample in ["Zr3_5584_nb_sc", "Zr3_1458_nb_hf"]:
    for var in ["Rxx68", "Rxy37", "Rxy48", "Rxx_1_7", "Rxx_2_7", "Rxx_17_18", "Rxy_2_17"]:
        for commutation in ["pos", "neg"]:
            for direction in ["up", "down"]:
                for region in ["low", "high"]:
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
                    for temp in ["1p3", "2p5", "3p2", "4p2", "6p0", "8p0", "8p95", "12p0", "18p0", "25p0", "35p0", "45p0", "50p0"]:
                        df = temp_data(
                            sample=sample,
                            commutation=commutation,
                            direction=direction,
                            var=var,
                            type="fft",
                            temp=temp
                        )
                        # Ignore missing configurations
                        if df is None:
                            continue
                        print(f"Found temp {temp}")
                        df = df[df.x.between(a, b)]
                        dataset.append(df)

                        temp_label = temp.replace("p", ".")
                        names.append(f"{temp_label} K")

                    # Ignore missing configurations
                    if len(dataset) == 0:
                        continue

                    print(
                        f"Processing {sample}: {var} {commutation} {direction} {region}freq")

                    # Normalise to 1.3K
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
                        xtick_interval=xtick_interval,
                        palette="Fire",
                        directory=os.path.join(
                            "C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe", f"plots/{sample}/temperature/{var}/{commutation}/{direction}/{region}freq/"),
                    )

                    op.fft_overlapped_plot(
                        dataset,
                        names,
                        xstart=a,
                        xend=b,
                        xtick_interval=xtick_interval,
                        ystart=0,
                        yend=1.1,
                        ytick_interval=0.2,
                        palette="Fire",
                        directory=os.path.join(
                            "C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe", f"plots/{sample}/temperature/{var}/{commutation}/{direction}/{region}freq/"),
                    )

op.close_origin()
