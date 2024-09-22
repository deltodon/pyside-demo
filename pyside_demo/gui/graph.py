from pyqtgraph import PlotWidget


class GraphWidget(PlotWidget):
    def __init__(
        self,
    ):
        super().__init__()
        self.clear()
        x = [0, 1, 2, 3, 4, 5]
        y = [0, 1, 4, 9, 16, 25]
        self.plot(x, y)
