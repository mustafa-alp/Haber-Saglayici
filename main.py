import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextBrowser
from PyQt5.QtGui import QTextCursor, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
import requests
from bs4 import BeautifulSoup
import time

class HaberlerUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NTV Spor Haberleri")
        self.resize(800, 600)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.label = QLabel("Haber Başlıkları:")
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setLineWrapMode(QTextBrowser.NoWrap)
        self.text_browser.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_browser)

        self.setLayout(self.layout)

    def get_haberler(self):
        url = "https://www.ntvspor.net/"
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        isim = soup.find_all("div", attrs={"class", "slider-item"})
        link = soup.find_all("a", attrs={"class", "slider-item-link is-bg-shadow"})

        haberler = []
        for isim, link in zip(isim, link):
            isim = isim.text.strip().replace("\n", "")
            link = "https://www.ntvspor.net/" + link.get("href")
            haber = f'<a href="{link}">{isim}</a>'
            haberler.append(haber)

        return haberler

    def guncelle(self):
        haberler = self.get_haberler()
        self.text_browser.clear()
        for haber in haberler:
            self.text_browser.append(haber)

app = QApplication(sys.argv)
uygulama = HaberlerUygulamasi()
uygulama.guncelle()
uygulama.show()
sys.exit(app.exec_())
