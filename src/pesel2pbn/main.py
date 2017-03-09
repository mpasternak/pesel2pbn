# -*- encoding: utf-8 -*-
from PyQt5 import QtGui
import json

from PyQt5.QtCore import QUrl, Qt, QLocale, QLibraryInfo, QTranslator
from PyQt5.QtCore import QEventLoop
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressDialog, QMessageBox
from pesel2pbn.pesel2pbn_auto import Ui_MainWindow
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QSettings, QPoint
from pesel2pbn.version import VERSION

def get_QSettings():
    return QSettings('IPL', 'PESEL2PBN')

class Pesel2PBNWindow(QMainWindow):
    def __init__(self, networkAccessManager):
        super(Pesel2PBNWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("pesel2pbn %s" % VERSION)
        self.ui.wykonajButton.clicked.connect(self.startWork)
        self.ui.pastePESEL.clicked.connect(self.pastePESEL)
        self.ui.copyPBN.clicked.connect(self.copyPBN)

        self.ui.oProgramie.clicked.connect(self.aboutBox)

        self.networkAccessManager = networkAccessManager
        self.networkAccessManager.finished.connect(self.finished)

        self.networkResults = {}
        self.progressDialog = None

        self.currentQuery = None
        self.currentLine = None

    def aboutBox(self):
        QMessageBox.about(
            self,
            "O programie",
            "<b>PESEL2PBN</b>"
            "<br>"
            "wersja {wersja}"
            "<p>"
            "(C) 2015-2017 Michał Pasternak &lt;<a href=mailto:michal.dtz@gmail.com>michal.dtz@gmail.com</a>>"
            "<br>"
            "(C) 2015-2017 <a href=http://iplweb.pl>iplweb.pl</a>"
            "<p>"
            "Program rozpowszechniany jest na zasadach licencji MIT."
            "<br>"
            "Kod źródłowy i issue tracker dostępny na<br>"
            "<a href=\"http://github.com/mpasternak/pesel2pbn/\">http://github.com/mpasternak/pesel2pbn</a>".format(
                wersja=VERSION
            )

        )

    def pastePESEL(self):
        cb = QApplication.clipboard()
        value = cb.text(mode=QClipboard.Clipboard)
        self.ui.numeryPESEL.setPlainText(value)

    def copyPBN(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.ui.numeryPBN.toPlainText(), mode=cb.Clipboard)

    def saveSettings(self):
        settings = get_QSettings()
        settings.setValue('token', self.ui.token.text().strip())
        settings.setValue('url', self.ui.url.text().strip())
        settings.setValue('empty_line', self.ui.emptyLineIfNoPBN.checkState())

    def loadSettings(self):
        settings = get_QSettings()
        self.ui.token.setText(settings.value('token', ''))
        self.ui.url.setText(settings.value("url", "https://pbn.nauka.gov.pl/sedno-webapp/data/persons/auth/{token}/pesel.{pesel}/id.pbn"))
        self.ui.emptyLineIfNoPBN.setCheckState(settings.value('empty_line', False))

    def getPESELfromUI(self):
        dane = self.ui.numeryPESEL.toPlainText().split("\n")

        # Pozwól na ostatnią pustą linię
        while dane and dane[-1] == '':
            dane = dane[:-1]

        return dane


    def startWork(self, *args, **kw):
        self.saveSettings()
        self.ui.numeryPBN.clear()

        self.cancelNetworkOperations()

        self.closeProgressBar()

        token = self.ui.token.text()

        if not token.strip():
            QMessageBox.critical(
                self,
                'Problem z tokenem',
                "Wartość token jest pusta. Wpisz token autoryzacyjny.",
                QMessageBox.Ok)
            return

        self.ui.numeryPBN.clear()

        self.dane = self.getPESELfromUI()

        if not self.dane:
            QMessageBox.critical(
                self,
                "Brak wpisanych danych",
                "Pole z numerami PESEL jest puste.",
                QMessageBox.Ok)
            return

        for linia in self.dane:
            if not linia.strip():
                QMessageBox.critical(
                    self,
                    "Problem z danymi wejściowymi",
                    "Proszę, usuń puste linie z listy numerów PESEL.",
                    QMessageBox.Ok)
                return

            if len(linia) != 11:
                QMessageBox.critical(
                    self,
                    "Problem z danymi wejściowymi",
                    "Na liście numerów PESEL znajduje się niepoprawny numer: %s. Skoryguj, proszę, "
                    "dane wejściowe." % linia,
                    QMessageBox.Ok)
                return

        URL = self.ui.url.text().strip()

        self.progressDialog = QProgressDialog("Kontaktuję się z serwerem PBN...", "Anuluj", 0, len(self.dane), self)
        self.progressDialog.setWindowModality(Qt.WindowModal)
        self.progressDialog.setValue(0)
        self.progressDialog.show()
        self.progressDialog.canceled.connect(self.progressDialogCancelled)

        self.URL = URL
        self.token = token

        self.currentLine = 0
        self.processNextLine()

    def processNextLine(self):
        self.progressDialog.setValue(self.currentLine)
        self.currentQuery = self.networkAccessManager.get(QNetworkRequest(
            QUrl(self.URL.format(token=self.token, pesel=self.dane[self.currentLine]))))

    def cancelNetworkOperations(self):
        if self.currentQuery is not None:
            if not self.currentQuery.isFinished():
                self.currentQuery.abort()
                # self.currentQuery.deleteLater()

    def closeProgressBar(self):
        if self.progressDialog is not None:
            self.progressDialog.close()

    def progressDialogCancelled(self, *args, **kw):
        self.cancelNetworkOperations()

    def finished(self, reply):

        err = reply.error()

        if err == QNetworkReply.OperationCanceledError:
            return

        BRAK_W_PBN = "Brak w PBN"
        if self.ui.emptyLineIfNoPBN.checkState():
            BRAK_W_PBN = ''

        if err != QNetworkReply.NoError:

            if err == QNetworkReply.ContentOperationNotPermittedError:
                self.cancelAllRequests()
                QMessageBox.critical(
                    self,
                    "Nieprawidłowy token.",
                    "Serwer nie pozwala na połączenia z tym tokenem. Sprawdź, czy token jest wpisany poprawnie. "
                    "Sprawdź również, czy okres jego ważności nie zakończył się. ",
                    QMessageBox.Ok
                )
                self.progressDialog.close()
                return

            elif err == QNetworkReply.ContentNotFoundError:
                buf = BRAK_W_PBN

            else:
                buf = reply.errorString()

        else:

            buf = reply.readAll()

            dane = bytes(buf).decode('utf-8')

            try:
                buf = json.loads(dane)['value']
            except (ValueError, KeyError):
                buf = "Odpowiedź z serwera nie do analizy (%r)" % dane
                pass

        self.ui.numeryPBN.appendPlainText(buf)
        self.currentLine += 1
        if self.currentLine == len(self.dane):
            self.everythingFinished()
        else:
            self.processNextLine()

    def everythingFinished(self):
        self.closeProgressBar()
        self.cancelNetworkOperations()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    QLocale.setDefault(QLocale("pl"))

    translator = QTranslator()
    if len(sys.argv) > 1:
        locale = sys.argv[1]
    else:
        locale = QLocale.system().name()
    translator.load('qt_%s' % locale,
        QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)


    networkAccessManager = QNetworkAccessManager(app)
    window = Pesel2PBNWindow(networkAccessManager=networkAccessManager)
    window.show()

    window.loadSettings()

    sys.exit(app.exec_())
