"""This module demonstrates 2D plotting capabilities in pyqtgraph.

This functionality is originally from:
.venv/Lib/site-packages/pyqtgraph/examples/Plotting.py

It can also be accessed by running:
    poetry run python -m pyqtgraph.examples
and selecting 'Basic Plotting'.

The module showcases various 2D plotting features available in pyqtgraph.
All plots can be panned/scaled by dragging with left/right mouse buttons.
Right-clicking on any plot displays a context menu.

Attributes:
    None

Todo:
    * None

"""

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QGridLayout, QWidget


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        # Create plots
        plot_1 = pg.PlotWidget(title="Basic array plotting")
        plot_1.plot(y=np.random.normal(size=100))
        layout.addWidget(plot_1, 0, 0)

        plot_2 = pg.PlotWidget(title="Multiple curves")
        plot_2.plot(
            np.random.normal(size=100), pen=(255, 0, 0), name="Red curve"
        )
        plot_2.plot(
            np.random.normal(size=110) + 5, pen=(0, 255, 0), name="Green curve"
        )
        plot_2.plot(
            np.random.normal(size=120) + 10, pen=(0, 0, 255), name="Blue curve"
        )
        layout.addWidget(plot_2, 0, 1)

        plot_3 = pg.PlotWidget(title="Drawing with points")
        plot_3.plot(
            np.random.normal(size=100),
            pen=(200, 200, 200),
            symbolBrush=(255, 0, 0),
            symbolPen="w",
        )
        layout.addWidget(plot_3, 0, 2)

        plot_4 = pg.PlotWidget(title="Parametric, grid enabled")
        x = np.cos(np.linspace(0, 2 * np.pi, 1000))
        y = np.sin(np.linspace(0, 4 * np.pi, 1000))
        plot_4.plot(x, y)
        plot_4.showGrid(x=True, y=True)
        layout.addWidget(plot_4, 1, 0)

        plot_5 = pg.PlotWidget(title="Scatter plot, axis labels, log scale")
        x = np.random.normal(size=1000) * 1e-5
        y = x * 1000 + 0.005 * np.random.normal(size=1000)
        y -= y.min() - 1.0
        mask = x > 1e-15
        x = x[mask]
        y = y[mask]
        plot_5.plot(
            x,
            y,
            pen=None,
            symbol="t",
            symbolPen=None,
            symbolSize=10,
            symbolBrush=(100, 100, 255, 50),
        )
        plot_5.setLabel("left", "Y Axis", units="A")
        plot_5.setLabel("bottom", "Y Axis", units="s")
        plot_5.setLogMode(x=True, y=False)
        layout.addWidget(plot_5, 1, 1)

        plot_6 = pg.PlotWidget(title="Updating plot")
        self.curve = plot_6.plot(pen="y")
        self.data = np.random.normal(size=(10, 1000))
        self.ptr = 0
        layout.addWidget(plot_6, 1, 2)

        plot_7 = pg.PlotWidget(title="Filled plot, axis disabled")
        y = np.sin(np.linspace(0, 10, 1000)) + np.random.normal(
            size=1000, scale=0.1
        )
        plot_7.plot(y, fillLevel=-0.3, brush=(50, 50, 200, 100))
        plot_7.showAxis("bottom", False)
        layout.addWidget(plot_7, 2, 0)

        plot_8 = pg.PlotWidget(title="Region Selection")
        x2 = np.linspace(-100, 100, 1000)
        data2 = np.sin(x2) / x2
        plot_8.plot(data2, pen=(255, 255, 255, 200))
        self.lr = pg.LinearRegionItem([400, 700])
        self.lr.setZValue(-10)
        plot_8.addItem(self.lr)
        layout.addWidget(plot_8, 2, 1)

        plot_9 = pg.PlotWidget(title="Zoom on selected region")
        plot_9.plot(data2)
        layout.addWidget(plot_9, 2, 2)

        def updatePlot():
            plot_9.setXRange(*self.lr.getRegion(), padding=0)

        def updateRegion():
            self.lr.setRegion(plot_9.getViewBox().viewRange()[0])

        self.lr.sigRegionChanged.connect(updatePlot)
        plot_9.sigXRangeChanged.connect(updateRegion)
        updatePlot()

        # Setup timer for updating plot
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def update(self):
        self.curve.setData(self.data[self.ptr % 10])
        self.ptr += 1
