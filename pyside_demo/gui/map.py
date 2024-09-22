import folium
from PySide6.QtWebEngineWidgets import QWebEngineView


class MapWidget(QWebEngineView):
    def __init__(
        self,
    ):
        super().__init__()
        map = folium.Map(location=[0, 0], zoom_start=2)
        html_string = map.get_root().render()
        self.setHtml(html_string)
