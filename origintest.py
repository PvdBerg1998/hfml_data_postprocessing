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


debug = False

if __name__ == "__main__":
    # Start origin
    print("Starting Origin")
    if op.oext:
        op.set_show(debug)

    plotparams = {
        # x limits
        "xstart": 100,
        "xend": 700,
        # stacking offset
        "offset": 1,
        # coloring of different lines
        "palette": "System Color List",
        # width of plot lines in "origin units"
        "linewidth": 2,
        # legend margin in x units
        "legendmargin": 20
    }

    graph = op.new_graph(template="line")
    # First graph layer
    gl = graph[0]

    # Normalize to zero angle max peak
    df = angle_data(**{
        "sample": "Zr3_5584_nb_sc",
        "direction": "up",
        "var": "Rxx68",
        "type": "fft",
        "angle": 0
    })
    df = df[df.x.between(plotparams["xstart"], plotparams["xend"])]
    normalisation = df.y.max()

    # Add angle data into worksheets and plot layers
    i = 0
    # , 50, 60, 70, 80, 90, 100, 110]:
    for angle in [-10, -5, 0, 5, 10, 20, 30, 40]:
        print(f"Loading angle {angle}")
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
        df.y = df.y / normalisation
        # Shift for stacking
        df.y = df.y + i * plotparams["offset"]

        # Create worksheet
        wks = op.new_sheet("w", lname=f"{angle} deg", hidden=True)
        wks.from_df(df)
        angle = params["angle"]
        wks.set_labels(["Frequency", f"{angle} deg"])

        print(f"Plotting angle {angle}")
        plot = gl.add_plot(wks, colx=0, coly=1)

        i += 1

    print("Postprocessing graph")

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

    # Set colors _after_ applying theme
    for plot in gl.plot_list():
        plot.colormap = plotparams["palette"]
        # Set color increment to stretch to use the entire palette
        plot.colorinc = 2  # Magic number : index into option menu

    # Set line width
    # Multiply by 500 because its defined like this
    width = plotparams["linewidth"] * 500
    graph.lt_exec(f"set %C -w {width};")

    # Hide y tick numbers
    graph.lt_exec("axis -ps Y L 0;")

    # Align legend to top right
    offset = plotparams["legendmargin"]
    max_x = plotparams["xend"]
    max_y = i * plotparams["offset"]
    graph.lt_exec(f"legend.x = {max_x + offset} + legend.dx / 2;")
    graph.lt_exec(f"legend.y = {max_y} - legend.dy / 2;")

    # Save
    print("Saving")
    # Can't use the Python savefig because we need to use a margin flag,
    # otherwise the legend gets cut off.
    out = os.path.join(os.getcwd(), "out.pdf")
    op.lt_exec(f"expGraph type:=pdf path:={out} tr.Margin:=2;")
    op.save(os.path.join(os.getcwd(), "out.opju"))

    if debug:
        input(">")

    print("Exiting Origin")
    if op.oext:
        op.exit()
