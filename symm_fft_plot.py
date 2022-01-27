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


def symm_data(sample, measurement, var, name):
    path = f"C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe/{sample}/output/{measurement}/{var}/fft/{name}.csv"
    if not os.path.exists(path):
        return None
    return pd.read_csv(path, names=["x", "y"])


# region of interest
a = 100
b = 700

for sample in ["Zr3_5584_nb_hf"]:
    for measurement in ["1p3K_pos_up", "1p3K_neg_up"]:
        for var in ["Rxx_10_14", "Rxy_7_9"]:
            if "pos" in measurement:
                name = "pos"
            else:
                name = "neg"

            df = symm_data(
                sample=sample,
                measurement=measurement,
                var=var,
                name=name
            )
            assert(df is not None)
            df = df[df.x.between(a, b)]

            print(
                f"Processing {sample}: {measurement} {var} {name}")

            # Normalize
            df.y = df.y / df.y.max()

            op.fft_plot(
                df,
                name=name,
                xstart=a,
                xend=b,
                xtick_interval=100,
                ystart=0,
                yend=df.y.max() * 1.1,
                ytick_interval=0.2,
                directory=os.path.join(
                    "C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe", f"plots/{sample}/symm/{var}/"),
                filename=f"{name}"
            )

        #
        # Plot rxx together with rxy
        #

        if "pos" in measurement:
            name = "pos"
        else:
            name = "neg"

        df_rxx = symm_data(
            sample=sample,
            measurement=measurement,
            var="Rxx_10_14",
            name=name
        )
        assert(df_rxx is not None)
        df_rxx = df_rxx[df_rxx.x.between(a, b)]

        df_rxy = symm_data(
            sample=sample,
            measurement=measurement,
            var="Rxy_7_9",
            name=name
        )
        assert(df_rxy is not None)
        df_rxy = df_rxy[df_rxy.x.between(a, b)]

        #normalisation = max(df_rxx.y.max(), df_rxy.y.max())
        #df_rxx.y = df_rxx.y / normalisation
        #df_rxy.y = df_rxy.y / normalisation
        df_rxx.y = df_rxx.y / df_rxx.y.max()
        df_rxy.y = df_rxy.y / df_rxy.y.max()

        print(f"Processing {sample}: {var} Rxx+Rxy")

        op.fft_overlapped_plot(
            [df_rxx, df_rxy],
            ["Rxx_10_14", "Rxy_7_9"],
            xstart=a,
            xend=b,
            xtick_interval=100,
            ystart=0,
            yend=1.1,
            ytick_interval=0.2,
            palette="Classic",
            palette_stretch=False,
            directory=os.path.join(
                "C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe", f"plots/{sample}/symm/"),
            filename=f"both_{name}"
        )

        #
        # Plot boxcar rxx together with boxcar rxy
        #

        if "pos" in measurement:
            continue
        else:
            name = "neg_boxcar"

        df_rxx = symm_data(
            sample=sample,
            measurement=measurement,
            var="Rxx_10_14",
            name=name
        )
        assert(df_rxx is not None)
        df_rxx = df_rxx[df_rxx.x.between(a, b)]

        df_rxy = symm_data(
            sample=sample,
            measurement=measurement,
            var="Rxy_7_9",
            name=name
        )
        assert(df_rxy is not None)
        df_rxy = df_rxy[df_rxy.x.between(a, b)]

        #normalisation = max(df_rxx.y.max(), df_rxy.y.max())
        #df_rxx.y = df_rxx.y / normalisation
        #df_rxy.y = df_rxy.y / normalisation
        df_rxx.y = df_rxx.y / df_rxx.y.max()
        df_rxy.y = df_rxy.y / df_rxy.y.max()

        print(f"Processing {sample}: {var} Rxx+Rxy")

        op.fft_overlapped_plot(
            [df_rxx, df_rxy],
            ["Rxx_10_14", "Rxy_7_9"],
            xstart=a,
            xend=b,
            xtick_interval=100,
            ystart=0,
            yend=1.1,
            ytick_interval=0.2,
            palette="Classic",
            palette_stretch=False,
            directory=os.path.join(
                "C:/Users/pim/Sync/University/MEP/Data/1_ZrSiSe", f"plots/{sample}/symm/"),
            filename=f"both_{name}"
        )

op.close_origin()
