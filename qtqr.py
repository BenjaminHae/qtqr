#!/bin/env python
#-*- encoding: utf-8 -*-

# GUI front end for qrencode based on the work of David Green:
# <david4dev@gmail.com> https://launchpad.net/qr-code-creator/
# and inspired by
# http://www.omgubuntu.co.uk/2011/03/how-to-create-qr-codes-in-ubuntu/
#
# This is FREE SOFTWARE: GNU GPLv3
#
# copyright (C) 2011 Ramiro Algozino <algozino@gmail.com>

import sys #, os, subprocess
from PyQt4 import QtCore, QtGui
# import Image
# import zbar
from qrtools import QR

class MainWindow(QtGui.QMainWindow): 
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle(u'QtQR: QR Code Generator')
        self.setWindowIcon(QtGui.QIcon(u'icon.png'))
        self.w = QtGui.QWidget()
        self.setCentralWidget(self.w)
        self.lineEdit = QtGui.QLineEdit()
        self.l1 = QtGui.QLabel(u'Insert &text to be encoded:')
        self.qrcode = QtGui.QLabel(u"Start typing to create QRcode.")
        self.l2 = QtGui.QLabel(u'&Pixel Size:')
        self.pixelSize = QtGui.QSpinBox()
        self.saveButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(u'document-save'), u'&Save QRCode')
        self.exitButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(u'application-exit'),u'&Exit')
        self.decodeButton = QtGui.QPushButton(u'&Decode')
        
        self.decodeMenu = QtGui.QMenu()
        self.decodeFileAction = self.decodeMenu.addAction(QtGui.QIcon.fromTheme(u'document-open'),
                                                          u'Decode from File')
        self.decodeWebcamAction = self.decodeMenu.addAction(QtGui.QIcon.fromTheme(u'image-png'), 
                                                            u'Decode from WebCam')
        self.decodeButton.setMenu(self.decodeMenu)
        
        self.qrcode.setFrameShape(QtGui.QFrame.StyledPanel)
        self.saveButton.setEnabled(False)
        self.pixelSize.setValue(3)
        self.pixelSize.setMinimum(1)
        self.l1.setBuddy(self.lineEdit)
        self.l2.setBuddy(self.pixelSize)

        self.buttons = QtGui.QHBoxLayout()
        self.buttons.addWidget(self.saveButton)
        self.buttons.addWidget(self.decodeButton)
        
        self.codeControls = QtGui.QVBoxLayout()
        self.codeControls.addWidget(self.l1)
        self.codeControls.addWidget(self.lineEdit)
        
        self.pixControls = QtGui.QVBoxLayout()
        self.pixControls.addWidget(self.l2)
        self.pixControls.addWidget(self.pixelSize)
        
        self.controls = QtGui.QHBoxLayout()
        self.controls.addLayout(self.codeControls)
        self.controls.addLayout(self.pixControls)
        
        self.layout = QtGui.QVBoxLayout(self.w)
        self.layout.addLayout(self.controls)
        self.layout.addWidget(self.qrcode, 1)
        self.layout.addLayout(self.buttons)
        self.layout.addWidget(self.exitButton)

        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL('textChanged(QString)'), self.qrencode)
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL('clicked()'), self.saveCode)
        QtCore.QObject.connect(self.exitButton, QtCore.SIGNAL('clicked()'), self.close)
        QtCore.QObject.connect(self.decodeFileAction, QtCore.SIGNAL('triggered()'), self.decodeFile)
        QtCore.QObject.connect(self.decodeWebcamAction, QtCore.SIGNAL('triggered()'), self.decodeWebcam)

    def qrencode(self, text):
        if text:
            qr = QR(pixel_size = unicode(self.pixelSize.value()),
                    data=text,
                    )
            if qr.encode() == 0:
                self.qrcode.setPixmap(QtGui.QPixmap(qr.filename))
                self.saveButton.setEnabled(True)
            else:
                print >>sys.stderr, u"ERROR: Something went wrong while trying to generate de qrcode."
        else:
            self.saveButton.setEnabled(False)
                
    def saveCode(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, u'Save QRCode', filter=u'PNG Images (*.png);; All Files (*.*)')
        if fn:
            self.qrcode.pixmap().save(fn)
            print "Saving to file: %s" % fn
            QtGui.QMessageBox.information(self, u'Save QRCode',u'QRCode succesfully saved.')
        
    def decodeFile(self):
        fn = unicode(QtGui.QFileDialog.getOpenFileName(self, u'Open QRCode', filter=u'PNG Images (*.png);; All Files (*.*)'))

        if fn:
            qr = QR(filename=fn)
            if qr.decode():
                QtGui.QMessageBox.information(self, u'Decode QRCode', qr.data_to_string())

    def decodeWebcam(self):
        qr = QR()
        qr.decode_webcam()
        if qr.data_to_string() != 'NULL':
            QtGui.QMessageBox.information(self, u'Decode QRCode', qr.data_to_string())

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    
    sys.exit(app.exec_())
