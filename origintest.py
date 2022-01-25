import os
import originpro as op
import numpy as np
import pandas as pd
import sys


def origin_shutdown_exception_hook(exctype, value, traceback):
    op.exit()
    sys.__excepthook__(exctype, value, traceback)


if op and op.oext:
    sys.excepthook = origin_shutdown_exception_hook


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


if __name__ == "__main__":
    # Start origin
    if op.oext:
        op.set_show(True)

    plotparams = {
        # x limits
        "xstart": 100,
        "xend": 700,
        # stacking offset
        "offset": 0.75,
        "palette": "System Color List"
    }

    graph = op.new_graph(template="line")
    # First graph layer
    gl = graph[0]

    # Add angle data into worksheets and plot layers
    i = 0
    for angle in [-10, -5, 0, 5, 10]:
        params = {
            "sample": "Zr3_5584_nb_sc",
            "direction": "up",
            "var": "Rxx68",
            "type": "fft",
            "angle": angle
        }

        # Load data
        df = angle_data(**params)
        df = df[df.x.between(plotparams["xstart"], plotparams["xend"])]

        # Normalize
        df.y = df.y / df.y.max()
        # Shift for stacking
        df.y = df.y + i * plotparams["offset"]

        # Create worksheet
        wks = op.new_sheet("w", lname=f"{angle} deg", hidden=True)
        wks.from_df(df)
        angle = params["angle"]
        wks.set_labels(["Frequency", f"{angle} deg"])

        plot = gl.add_plot(wks, colx=0, coly=1)

        i += 1

    # Zoom
    gl.set_xlim(plotparams["xstart"], plotparams["xend"])
    gl.rescale(skip="x")

    gl.axis("x").title = "Frequency"
    gl.axis("y").title = "FFT Amplitude"

    # Group plots
    gl.group()

    # Apply PRL theme
    # For some reason this is not implemented in the Python API so we use Labtalk
    graph.lt_exec(
        "themeApply2g theme := \"Physical Review Letters\" option := project;")

    # # Patch colors
    i = 0
    for plot in gl.plot_list():
        plot.colormap = plotparams["palette"]
        plot.colorinc = 2  # Magic number : index into option menu
        i += 1

    # Wait for inspection
    input(">")
    if op.oext:
        op.exit()
