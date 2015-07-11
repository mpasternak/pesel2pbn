from unittest import mock
from unittest.mock import MagicMock, Mock

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox, QApplication
import pytest
from pesel2pbn.main import Pesel2PBNWindow

WYGENEROWANY_PESEL = '00891702980'  # http://www.bogus.ovh.org/generatory/all.html


@pytest.fixture
def p2p_window(qtbot):
    window = Pesel2PBNWindow(networkAccessManager=mock.Mock())
    window.show()
    qtbot.addWidget(window)
    return window


def test_pesel2pbn_pastePESEL(qtbot, p2p_window):
    with mock.patch('PyQt5.QtWidgets.QApplication.clipboard') as cb:
        clipboard = cb.return_value
        clipboard.text.return_value = "123"

        qtbot.mouseClick(p2p_window.ui.pastePESEL, QtCore.Qt.LeftButton)
        assert p2p_window.ui.numeryPESEL.toPlainText() == '123'


def test_pesel2pbn_copyPBN(qtbot, p2p_window):
    with mock.patch('PyQt5.QtWidgets.QApplication.clipboard') as cb:
        clipboard = cb.return_value
        clipboard.setText = MagicMock()

        p2p_window.ui.numeryPBN.setPlainText("123")
        qtbot.mouseClick(p2p_window.ui.copyPBN, QtCore.Qt.LeftButton)
        assert clipboard.setText.called_with("123", mode=clipboard.Clipboard)


def test_about_box(qtbot, p2p_window):
    with mock.patch.object(QMessageBox, 'about', new=Mock) as about:
        qtbot.mouseClick(p2p_window.ui.oProgramie, QtCore.Qt.LeftButton)
        assert about.called


def test_wykonaj_brak_PESELi(qtbot, p2p_window):
    with mock.patch.object(QMessageBox, 'critical', new=Mock) as critical:
        qtbot.mouseClick(p2p_window.ui.wykonajButton, QtCore.Qt.LeftButton)
        assert critical.called


def test_wykonaj_zle_PESELe(qtbot, p2p_window):
    p2p_window.ui.numeryPESEL.setPlainText('123')

    with mock.patch.object(QMessageBox, 'critical', new=Mock) as critical:
        qtbot.mouseClick(p2p_window.ui.wykonajButton, QtCore.Qt.LeftButton)
        assert critical.called


def test_wykonaj_dobre_PESELe_bez_tokena(qtbot, p2p_window):
    p2p_window.ui.numeryPESEL.setPlainText(WYGENEROWANY_PESEL)

    with mock.patch.object(QMessageBox, 'critical', new=Mock) as critical:
        qtbot.mouseClick(p2p_window.ui.wykonajButton, QtCore.Qt.LeftButton)
        assert critical.called


def test_wykonaj_dobre_PESELe_bez_tokena(qtbot, p2p_window):
    p2p_window.ui.numeryPESEL.setPlainText(WYGENEROWANY_PESEL)
    p2p_window.ui.token.setText('token-123')

    qtbot.mouseClick(p2p_window.ui.wykonajButton, QtCore.Qt.LeftButton)
    assert len(p2p_window.networkAccessManager.mock_calls) == 3
