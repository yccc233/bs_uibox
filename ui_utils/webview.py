from PySide2 import QtWebEngineWidgets, QtCore


class WebView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent):
        QtWebEngineWidgets.QWebEngineView.__init__(self, parent)
        self.load(QtCore.QUrl('http://localhost:7474/browser/'))

