#
#   origin.py
#   Interfaces with OriginPro and creates graphs in a predefined format.
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
import sys


# Initially, origin is not started/imported
global op
op = None

# This will keep Origin open for debugging
debug = False


def fft_overlapped_plot(
    # list of pandas dataframes
    dataset,
    # names corresponding to dataframes
    names,
    # x limits
    xstart,
    xend,
    xtick_interval,
    # y limits
    ystart,
    yend,
    ytick_interval,
    # legend margin in percent of x range
    legendmargin=1,
    # output directory
    directory=os.getcwd(),
    # output filename
    filename="fft_overlapped",
    # coloring of different lines
    palette="System Color List",
    # use palette stretching
    palette_stretch=True,
    # width of plot lines in "origin units"
    linewidth=2
):
    _start_origin(show=debug)

    # Create graph container in line mode
    graph = op.new_graph(template="line")
    # First graph layer
    gl = graph[0]

    # Add angle data into worksheets and plot layers
    i = 0
    for df in dataset:
        # Create worksheet
        wks = op.new_sheet("w", lname=names[i], hidden=True)
        wks.from_df(df)
        wks.set_labels(["Frequency", names[i]])

        print(f"Plotting dataframe {names[i]}")
        plot = gl.add_plot(wks, colx=0, coly=1)

        i += 1

    # Change plot formatting
    print("Postprocessing graph")

    # Group plots
    gl.group()

    # Zoom
    gl.set_xlim(xstart, xend)
    gl.set_ylim(ystart, yend)

    # Axis labels
    gl.axis("x").title = "Frequency (T)"
    gl.axis("y").title = "FFT Amplitude (a.u.)"

    # Apply PRL theme
    # For some reason this is not implemented in the Python API so we use Labtalk
    graph.lt_exec(
        "themeApply2g theme:=\"Physical Review Letters\" option:=project;")

    # Apply theme tweaks _after_ PRL theme

    # Set colors
    if palette is not None:
        for plot in gl.plot_list():
            plot.colormap = palette
            if palette_stretch:
                plot.colorinc = 2  # Magic number : index into option menu
            else:
                plot.colorinc = 1

    # Set line width
    # Multiply by 500 because its defined like this
    width = linewidth * 500
    graph.lt_exec(f"set %C -w {width};")

    # Set ticks
    gl.lt_exec(f"layer.x.inc = {xtick_interval};")
    gl.lt_exec("layer.x.minorTicks = 1;")
    gl.lt_exec(f"layer.y.inc = {ytick_interval};")
    gl.lt_exec("layer.y.minorTicks = 1;")

    # Enable grid
    gl.lt_exec("layer.x.showGrids = 1;")

    # Hide y tick numbers
    graph.lt_exec("axis -ps Y L 0;")

    # Flip legend
    graph.lt_exec("legendupdate update:=reconstruct order:=descend;")

    # Align legend to top right
    graph.lt_exec(
        f"legend.x = layer.x.to + {legendmargin / 100 * (xend - xstart)} + legend.dx / 2;")
    graph.lt_exec(f"legend.y = layer.y.to - legend.dy / 2;")

    # Export graph
    print("Saving")
    # Can't use the Python savefig because we need to use a margin flag,
    # otherwise the legend gets cut off.
    os.makedirs(directory, exist_ok=True)
    op.lt_exec(
        f"expGraph type:=pdf path:=\"{directory}\" filename:=\"{filename}.pdf\" tr.Margin:=1 overwrite:=1;")
    op.lt_exec(
        f"expGraph type:=png path:=\"{directory}\" filename:=\"{filename}.png\" tr.Margin:=1 overwrite:=1;")
    originsave = os.path.join(directory, f"{filename}.opju")
    op.lt_exec(f"save {originsave};")


def fft_stacked_plot(
    # list of pandas dataframes
    dataset,
    # names corresponding to dataframes
    names,
    # x limits
    xstart,
    xend,
    xtick_interval,
    # y limits
    ystart=None,
    yend=None,
    # legend margin in percent of x range
    legendmargin=1,
    # output directory
    directory=os.getcwd(),
    # output filename
    filename="fft_stacked",
    # stacking offset in y units
    offset=1,
    # coloring of different lines
    palette="System Color List",
    # use palette stretching
    palette_stretch=True,
    # width of plot lines in "origin units"
    linewidth=2
):
    if ystart is None:
        ystart = -offset
    if yend is None:
        yend = len(dataset) * offset

    _start_origin(show=debug)

    # Create graph container in line mode
    graph = op.new_graph(template="line")
    # First graph layer
    gl = graph[0]

    # Add angle data into worksheets and plot layers
    i = 0
    for df in dataset:
        # Create worksheet
        wks = op.new_sheet("w", lname=names[i], hidden=True)
        wks.from_df(df)
        wks.set_labels(["Frequency", names[i]])

        print(f"Plotting dataframe {names[i]}")
        plot = gl.add_plot(wks, colx=0, coly=1)

        i += 1

    # Change plot formatting
    print("Postprocessing graph")

    # Group plots
    gl.group()

    # Set group stacking
    # See https://www.originlab.com/doc/en/LabTalk/ref/Layer-cmd
    gl.lt_exec(f"layer -b s 2 {offset};")

    # Zoom
    gl.set_xlim(xstart, xend)
    gl.set_ylim(ystart, yend)

    # Axis labels
    gl.axis("x").title = "Frequency (T)"
    gl.axis("y").title = "FFT Amplitude (a.u.)"

    # Apply PRL theme
    # For some reason this is not implemented in the Python API so we use Labtalk
    graph.lt_exec(
        "themeApply2g theme:=\"Physical Review Letters\" option:=project;")

    # Apply theme tweaks _after_ PRL theme

    # Set colors
    if palette is not None:
        for plot in gl.plot_list():
            plot.colormap = palette
            if palette_stretch:
                plot.colorinc = 2  # Magic number : index into option menu
            else:
                plot.colorinc = 1

    # Set line width
    # Multiply by 500 because its defined like this
    width = linewidth * 500
    graph.lt_exec(f"set %C -w {width};")

    # Set x ticks
    gl.lt_exec(f"layer.x.inc = {xtick_interval};")
    gl.lt_exec("layer.x.minorTicks = 1;")

    # Set major y ticks on every plot line
    gl.lt_exec(f"layer.y.inc = {offset};")
    gl.lt_exec("layer.y.minorTicks = 0;")

    # Enable grid
    gl.lt_exec("layer.x.showGrids = 1;")

    # Hide y tick numbers
    graph.lt_exec("axis -ps Y L 0;")

    # Flip legend
    graph.lt_exec("legendupdate update:=reconstruct order:=descend;")

    # Align legend to top right
    graph.lt_exec(
        f"legend.x = layer.x.to + {legendmargin / 100 * (xend - xstart)} + legend.dx / 2;")
    graph.lt_exec(f"legend.y = layer.y.to - legend.dy / 2;")

    # Export graph
    print("Saving")
    # Can't use the Python savefig because we need to use a margin flag,
    # otherwise the legend gets cut off.
    os.makedirs(directory, exist_ok=True)
    op.lt_exec(
        f"expGraph type:=pdf path:=\"{directory}\" filename:=\"{filename}.pdf\" tr.Margin:=1 overwrite:=1;")
    op.lt_exec(
        f"expGraph type:=png path:=\"{directory}\" filename:=\"{filename}.png\" tr.Margin:=1 overwrite:=1;")
    originsave = os.path.join(directory, f"{filename}.opju")
    op.lt_exec(f"save {originsave};")


def fft_plot(
    # single dataframe
    dataframe,
    # names corresponding to dataframes
    name,
    # x limits
    xstart,
    xend,
    xtick_interval,
    # y limits
    ystart,
    yend,
    ytick_interval,
    # legend margin in percent of x range
    legendmargin=1,
    # output directory
    directory=os.getcwd(),
    # output filename
    filename="fft",
    # width of plot lines in "origin units"
    linewidth=2
):
    _start_origin(show=debug)

    # Create graph container in line mode
    graph = op.new_graph(template="line")
    # First graph layer
    gl = graph[0]

    # Add angle data into worksheets and plot layers
    # Create worksheet
    wks = op.new_sheet("w", lname=name, hidden=True)
    wks.from_df(dataframe)
    wks.set_labels(["Frequency", name])

    print(f"Plotting dataframe {name}")
    plot = gl.add_plot(wks, colx=0, coly=1)

    # Change plot formatting
    print("Postprocessing graph")

    # Zoom
    gl.set_xlim(xstart, xend)
    gl.set_ylim(ystart, yend)

    # Axis labels
    gl.axis("x").title = "Frequency (T)"
    gl.axis("y").title = "FFT Amplitude (a.u.)"

    # Apply PRL theme
    # For some reason this is not implemented in the Python API so we use Labtalk
    graph.lt_exec(
        "themeApply2g theme:=\"Physical Review Letters\" option:=project;")

    # Apply theme tweaks _after_ PRL theme

    # Set line width
    # Multiply by 500 because its defined like this
    width = linewidth * 500
    graph.lt_exec(f"set %C -w {width};")

    # Set ticks
    gl.lt_exec(f"layer.x.inc = {xtick_interval};")
    gl.lt_exec("layer.x.minorTicks = 1;")
    gl.lt_exec(f"layer.y.inc = {ytick_interval};")
    gl.lt_exec("layer.y.minorTicks = 1;")

    # Enable grid
    gl.lt_exec("layer.x.showGrids = 1;")

    # Hide y tick numbers
    graph.lt_exec("axis -ps Y L 0;")

    # Remove legend
    graph.lt_exec("label -r legend;")

    # Export graph
    print("Saving")
    # Can't use the Python savefig because we need to use a margin flag,
    # otherwise the legend gets cut off.
    os.makedirs(directory, exist_ok=True)
    op.lt_exec(
        f"expGraph type:=pdf path:=\"{directory}\" filename:=\"{filename}.pdf\" tr.Margin:=1 overwrite:=1;")
    op.lt_exec(
        f"expGraph type:=png path:=\"{directory}\" filename:=\"{filename}.png\" tr.Margin:=1 overwrite:=1;")
    originsave = os.path.join(directory, f"{filename}.opju")
    op.lt_exec(f"save {originsave};")


def _start_origin(show=False):
    # Do a late import as this takes ages
    global op
    if op is None:
        print("Starting Origin")
        import originpro
        op = originpro

        def origin_shutdown_exception_hook(exctype, value, traceback):
            op.exit()
            sys.__excepthook__(exctype, value, traceback)
        sys.excepthook = origin_shutdown_exception_hook
        op.set_show(show)
    else:
        # Reuse import
        # Create a new project
        op.new()


def close_origin():
    global op
    if op is not None:
        if debug:
            input(">")
        op.exit()
