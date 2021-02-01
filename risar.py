# coding=utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

class QGraphicsViewWMouse(QGraphicsView):
    def __init__(self, *args, **kw):
        super(QGraphicsViewWMouse, self).__init__(*args, **kw)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, ev):
        # Takole se programirajo samo zasilni moduli za Programiranje 1!!!
        global miska
        miska = ev.x(), ev.y()
        super(QGraphicsViewWMouse, self).mouseMoveEvent(ev)

    def mousePressEvent(self, ev):
        # Takole se programirajo samo zasilni moduli za Programiranje 1!!!
        global miska, klik
        miska = ev.x(), ev.y()
        klik = True
        super(QGraphicsViewWMouse, self).mousePressEvent(ev)

    def _changeKey(self, pressed, key):
        global levo, desno, gor, dol, presledek
        if key == Qt.Key_Left:
            levo = pressed
        if key == Qt.Key_Right:
            desno = pressed
        if key == Qt.Key_Down:
            dol = pressed
        if key == Qt.Key_Up:
            gor = pressed
        if key == Qt.Key_Space:
            presledek = pressed

    def keyPressEvent(self, ev):
        super().keyPressEvent(ev)
        self._changeKey(True, ev.key())

    def keyReleaseEvent(self, ev):
        super().keyReleaseEvent(ev)
        self._changeKey(False, ev.key())


app=QApplication([])
widget = QDialog()
widget.setWindowTitle("Janezovo zasilno platno")
widget.setLayout(QVBoxLayout())
widget.layout().setContentsMargins(2, 2, 2, 2)
widget.scene = QGraphicsScene(widget)
widget.scene.setBackgroundBrush(Qt.black)
widget.view = QGraphicsViewWMouse(widget.scene, widget)
widget.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
widget.view.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
widget.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
widget.layout().addWidget(widget.view)
widget.resize(800, 500)
widget.scene.setSceneRect(0, 0, widget.view.width(), widget.view.height())
widget.view.setSceneRect(0, 0, widget.view.width(), widget.view.height())
widget.show()
widget.raise_()
#widget.setWindowState(widget.windowState() | Qt.WindowFullScreen)
maxX = widget.view.width()
maxY = widget.view.height()

barve = bela, crna, rdeca, zelena, modra, vijolicna, rumena, siva, rjava = Qt.white, Qt.black, Qt.red, Qt.green, Qt.blue, Qt.magenta, Qt.yellow, Qt.gray, Qt.darkRed
barva = QColor

miska = maxX/2, maxY/2
klik = False
levo = desno = gor = dol = presledek = False
obnavljaj = True

def nakljucna_barva():
    from random import randint
    return barva(randint(0, 255), randint(0, 255), randint(0, 255))

def nakljucne_koordinate():
    from random import randint
    return randint(0, maxX), randint(0, maxY)

def obnovi():
    """
    Obnovi sliko na zaslonu.

    Funkcije ni potrebno klicati, če je 'obnavljaj' nastavljen na True. Prav
    tako funkcija 'cakaj' sama pokliče tudi 'obnovi'.
    """
    widget.scene.update()
    qApp.processEvents()

def cakaj(t: int):
    """Počaka t sekund."""
    import time
    obnovi()
    time.sleep(t)

def barvaOzadja(barva):
    """Nastavi barvo ozadja."""
    widget.scene.setBackgroundBrush(barva)
    if obnavljaj:
        obnovi()

def crta(x0, y0, x1, y1, barva=bela, sirina=1):
    """Potegni črto med podanima točkama."""
    crta = widget.scene.addLine(0, 0, x1-x0, y1-y0, QPen(QBrush(barva), sirina))
    crta.setPos(x0, y0)
    if obnavljaj:
        obnovi()
    return crta

def tocka(x, y, barva=bela):
    """Nariše točko na podanih koordinatah."""
    if obnavljaj:
        obnovi()
    return widget.scene.addLine(x, y, x, y, QPen(QBrush(barva), 1))

def elipsa(x, y, rx, ry, barva=bela, sirina=1):
    """Nariše elipso s središčem v (x, y) in polmeroma rx in ry."""
    elipsa = widget.scene.addEllipse(-rx, -ry, 2*rx, 2*ry, QPen(QBrush(barva), sirina))
    elipsa.setPos(x, y)
    if obnavljaj:
        obnovi()
    return elipsa

def krog(x, y, r, barva=bela, sirina=1):
    """Nariše krog s polmerom r in središčem v (x, y)."""
    class ClickableEllipse(QGraphicsEllipseItem):
        def __init__(self, *args, onClick=None):
            super().__init__(*args)
            self.setOnClick(onClick)

        def mousePressEvent(self, ev):
            super().mousePressEvent(ev)
            self.onClick and self.onClick()

        def setOnClick(self, onClick):
            self.onClick = onClick

    elipsa = ClickableEllipse(-r, -r, 2 * r, 2 * r)
    elipsa.setPen(QPen(QBrush(barva), sirina))
    elipsa.setPos(x, y)
    widget.scene.addItem(elipsa)
    if obnavljaj:
        obnovi()
    return elipsa

def zapolni(kaj, barva):
    kaj.setBrush(barva)

def sprazni(kaj):
    kaj.setBrush(QBrush())

def spremeni_barvo(kaj, barva):
    kaj.setPen(QPen(barva))

def pravokotnik(x, y, sirina, visina, barva=bela, sirina_peresa=1):
    """Nariše krog s polmerom r in središčem v (x, y)."""
    pravo = widget.scene.addRect(x, y, sirina, visina, QPen(QBrush(barva), sirina_peresa))
    if obnavljaj:
        obnovi()
    return pravo

def besedilo(x, y, txt, barva=bela, velikost=20, pisava="Arial"):
    """Izpiše besedilo txt; koordinati podajata zgornji levi vogal."""
    font = QFont(pisava)
    font.setPixelSize(velikost)
    txt = widget.scene.addText(txt, font)
    txt.setPos(x, y)
    txt.setDefaultTextColor(barva)
    if obnavljaj:
        obnovi()
    return txt

def slika(x, y, fname):
    """
    Naloži sliko iz datoteke fname in jo postavi na sliko tako, da je
    zgornji levi vogal na koordinatah (x, y)
    """
    pict = QPixmap(fname)
    pixmap = widget.scene.addPixmap(pict)
    pixmap.setPos(x, y)
    rect = pixmap.boundingRect()
#    pixmap.translate(-rect.width() / 2, -rect.height() / 2)
    if obnavljaj:
        obnovi()
    return pixmap

def odstrani(stvar):
    widget.scene.removeItem(stvar)

def pobrisi():
    widget.scene.clear()
    obnovi()

def shrani(filename):
    import os
    scene = widget.scene
    source = scene.itemsBoundingRect().adjusted(-15, -15, 15, 15)
    size = source.size()
    buffer = QPixmap(int(size.width()), int(size.height()))

    painter = QPainter()
    painter.begin(buffer)
    try:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(buffer.rect(), scene.backgroundBrush())
        target = QRectF(0, 0, source.width(), source.height())
        scene.render(painter, target, source)
        buffer.save(filename, os.path.splitext(filename)[1][1:])
    finally:
        painter.end()

def stoj():
    qApp.exec()

def premakni_na(objekt, x, y):
    objekt.setPos(x, y)

def premakni_za(objekt, x, y):
    objekt.moveBy(x, y)

def obrni_na(objekt, kot):
    objekt.setRotation(kot)

def obrni_za(objekt, kot):
    objekt.setRotation(objekt.rotation() + kot)

def predvajaj(ime):
    global player
    player = QMediaPlayer()
    player.setMedia(QMediaContent(QUrl.fromLocalFile(ime)))
    player.play()

def pobarvaj(objekt, notranjost, rob):
    objekt.setPen(QPen(QBrush(rob), objekt.pen().width()))
    objekt.setBrush(QBrush(notranjost))

