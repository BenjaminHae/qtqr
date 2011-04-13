#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# GUI front end for qrencode based on the work of David Green:
# <david4dev@gmail.com> https://launchpad.net/qr-code-creator/
# and inspired by
# http://www.omgubuntu.co.uk/2011/03/how-to-create-qr-codes-in-ubuntu/
#
# This is FREE SOFTWARE: GNU GPLv3
#
# copyright (C) 2011 Ramiro Algozino <algozino@gmail.com>

import sys, os
from PyQt4 import QtCore, QtGui
from qrtools import QR

class MainWindow(QtGui.QMainWindow): 
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle(u'QtQR: QR Code Generator')
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), u'icon.png')))
        self.w = QtGui.QWidget()
        self.setCentralWidget(self.w)

        #Tabs
        self.tabs = QtGui.QTabWidget()
        self.textTab = QtGui.QWidget()
        self.urlTab = QtGui.QWidget()
        self.emailTab = QtGui.QWidget()
        self.smsTab = QtGui.QWidget()
        self.telTab = QtGui.QWidget()
        self.tabs.addTab(self.textTab, u"&Text")
        self.tabs.addTab(self.urlTab, u"&URL")
        self.tabs.addTab(self.emailTab, u"&Email")
        self.tabs.addTab(self.smsTab, u"S&MS")
        self.tabs.addTab(self.telTab, u"&Telephone")
        
        self.l1 = QtGui.QLabel(u'Text to be encoded:')
        self.textEdit = QtGui.QPlainTextEdit()

        self.urlLabel =  QtGui.QLabel(u'URL to be encoded:')
        self.urlEdit = QtGui.QLineEdit(u'http://')
        
        self.emailLabel = QtGui.QLabel(u'E-Mail address:')
        self.emailEdit = QtGui.QLineEdit(u"@.com")
        self.emailSubLabel = QtGui.QLabel(u'Subject:')
        self.emailSubjectEdit = QtGui.QLineEdit()
        self.emailBodyLabel = QtGui.QLabel(u'Message Body:')
        self.emailBodyEdit = QtGui.QLineEdit()
        self.telephoneLabel = QtGui.QLabel(u'Telephone Number:')
        self.telephoneEdit = QtGui.QLineEdit()
        self.smsNumberLabel = QtGui.QLabel(u'Telephone Number:')
        self.smsNumberEdit = QtGui.QLineEdit() 
        self.smsBodyLabel = QtGui.QLabel(u'Message:')
        self.smsBodyEdit = QtGui.QLineEdit()

        self.optionsGroup = QtGui.QGroupBox(u'Parameters:')

        self.l2 = QtGui.QLabel(u'&Pixel Size:')
        self.pixelSize = QtGui.QSpinBox()

        self.l3 = QtGui.QLabel(u'&EC Level:')
        self.ecLevel = QtGui.QComboBox() #LMQH
        self.ecLevel.addItems((u'Lowest',u'Medium',u'Q',u'Highest'))

        self.l4 = QtGui.QLabel(u'&Margin Size:')
        self.marginSize = QtGui.QSpinBox()

        self.qrcode = QtGui.QLabel(u'\n\nStart typing to create QRcode.\n\n')
        self.qrcode.setAlignment(QtCore.Qt.AlignHCenter)

        self.saveButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(u'document-save'), u'&Save QRCode')
        self.exitButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(u'application-exit'),u'E&xit')
        self.decodeButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(u'preview-file'),u'&Decode')
        
        self.decodeMenu = QtGui.QMenu()
        self.decodeFileAction = self.decodeMenu.addAction(QtGui.QIcon.fromTheme(u'document-open'), u'Decode from &File')
        self.decodeWebcamAction = self.decodeMenu.addAction(QtGui.QIcon.fromTheme(u'image-png'), u'Decode from &WebCam')
        self.decodeButton.setMenu(self.decodeMenu)

        self.textEdit.setMaximumHeight(self.textEdit.height()/3.5)        
        self.qrcode.setFrameShape(QtGui.QFrame.StyledPanel)
        self.saveButton.setEnabled(False)
        self.pixelSize.setValue(3)
        self.pixelSize.setMinimum(1)
        self.marginSize.setValue(4)
        self.l1.setBuddy(self.textEdit)
        self.l2.setBuddy(self.pixelSize)
        self.l3.setBuddy(self.ecLevel)
        self.l4.setBuddy(self.marginSize)
        self.ecLevel.setToolTip(u'Error Correction Level')
        self.l3.setToolTip(u'Error Correction Level')
        self.decodeFileAction.setShortcut(u"Ctrl+O")
        self.decodeWebcamAction.setShortcut(u"Ctrl+W")
        self.exitButton.setShortcut(u"Ctrl+Q")
        self.saveButton.setShortcut(u"Ctrl+S")

        self.buttons = QtGui.QHBoxLayout()
        self.buttons.addWidget(self.saveButton)
        self.buttons.addWidget(self.decodeButton)
        
        #Text Tab
        self.codeControls = QtGui.QVBoxLayout()
        self.codeControls.addWidget(self.l1)
        self.codeControls.addWidget(self.textEdit)
        self.codeControls.addStretch()
        self.textTab.setLayout(self.codeControls)
        
        #URL Tab
        self.urlTabLayout = QtGui.QVBoxLayout()
        self.urlTabLayout.addWidget(self.urlLabel)
        self.urlTabLayout.addWidget(self.urlEdit)
        self.urlTabLayout.addStretch()
        self.urlTab.setLayout(self.urlTabLayout)
        
        #Email Tab
        self.emailTabLayout = QtGui.QVBoxLayout()
        self.emailTabLayout.addWidget(self.emailLabel)
        self.emailTabLayout.addWidget(self.emailEdit)
        self.emailTabLayout.addWidget(self.emailSubLabel)
        self.emailTabLayout.addWidget(self.emailSubjectEdit)
        self.emailTabLayout.addWidget(self.emailBodyLabel)
        self.emailTabLayout.addWidget(self.emailBodyEdit)
        self.emailTabLayout.addStretch()
        self.emailTab.setLayout(self.emailTabLayout)
        
        #SMS Tab
        self.smsTabLayout = QtGui.QVBoxLayout()
        self.smsTabLayout.addWidget(self.smsNumberLabel)
        self.smsTabLayout.addWidget(self.smsNumberEdit)
        self.smsTabLayout.addWidget(self.smsBodyLabel)
        self.smsTabLayout.addWidget(self.smsBodyEdit)
        self.smsTabLayout.addStretch()
        self.smsTab.setLayout(self.smsTabLayout)
        
        #Telephone Tab
        self.telTabLayout = QtGui.QVBoxLayout()
        self.telTabLayout.addWidget(self.telephoneLabel)
        self.telTabLayout.addWidget(self.telephoneEdit)
        self.telTabLayout.addStretch()
        self.telTab.setLayout(self.telTabLayout)
        
        #Pixel Size Controls
        self.pixControls = QtGui.QVBoxLayout()
        self.pixControls.addWidget(self.l2)
        self.pixControls.addWidget(self.pixelSize)
        
        #Error Correction Level Controls
        self.levelControls = QtGui.QVBoxLayout()
        self.levelControls.addWidget(self.l3)
        self.levelControls.addWidget(self.ecLevel)
        
        #Margin Size Controls
        self.marginControls = QtGui.QVBoxLayout()
        self.marginControls.addWidget(self.l4)
        self.marginControls.addWidget(self.marginSize)
        
        #Controls Layout
        self.controls = QtGui.QHBoxLayout()
        self.controls.addLayout(self.pixControls)
        self.controls.addSpacing(10)
        self.controls.addLayout(self.levelControls)
        self.controls.addSpacing(10)
        self.controls.addLayout(self.marginControls)
        self.controls.addStretch()
        self.optionsGroup.setLayout(self.controls)
        
        #Main Window Layout
        self.layout = QtGui.QVBoxLayout(self.w)
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.optionsGroup)
        self.layout.addWidget(self.qrcode, 1)
        self.layout.addLayout(self.buttons)
        self.layout.addWidget(self.exitButton)

        #Signals
        self.textEdit.textChanged.connect(self.qrencode)
        self.urlEdit.textChanged.connect(self.qrencode)
        self.emailEdit.textChanged.connect(self.qrencode)
        self.emailSubjectEdit.textChanged.connect(self.qrencode)
        self.emailBodyEdit.textChanged.connect(self.qrencode)
        self.smsNumberEdit.textChanged.connect(self.qrencode)
        self.smsBodyEdit.textChanged.connect(self.qrencode)
        self.telephoneEdit.textChanged.connect(self.qrencode)       
        self.pixelSize.valueChanged.connect(self.qrencode)
        self.ecLevel.currentIndexChanged.connect(self.qrencode)
        self.marginSize.valueChanged.connect(self.qrencode)
        self.saveButton.clicked.connect(self.saveCode)
        self.exitButton.clicked.connect(self.close)
        self.decodeFileAction.triggered.connect(self.decodeFile)
        self.decodeWebcamAction.triggered.connect(self.decodeWebcam)

    def qrencode(self):
        text = [
            unicode(self.textEdit.toPlainText()),
            unicode(self.urlEdit.text()),
            ( unicode(self.emailEdit.text()), unicode(self.emailSubjectEdit.text()), unicode(self.emailBodyEdit.text()) ),
            ( unicode(self.smsNumberEdit.text()), unicode(self.smsBodyEdit.text()) ),
            unicode(self.telephoneEdit.text()),
        ]
        level = (u'L',u'M',u'Q',u'H')
        data_type = (u'text',u'url',u'emailmessage',u'sms',u'telephone')

        if text[self.tabs.currentIndex()]:
            qr = QR(pixel_size = unicode(self.pixelSize.value()),
                    data=text[self.tabs.currentIndex()],
                    level=unicode(level[self.ecLevel.currentIndex()]),
                    margin_size=unicode(self.marginSize.value()),
                    data_type=unicode(data_type[self.tabs.currentIndex()]),
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
            if not fn.toLower().endsWith(u".png"):
                fn += u".png"
            self.qrcode.pixmap().save(fn)
            print "Saving to file: %s" % fn
            QtGui.QMessageBox.information(self, u'Save QRCode',u'QRCode succesfully saved.')
        
    def decodeFile(self):
        fn = unicode(QtGui.QFileDialog.getOpenFileName(self, u'Open QRCode', filter=u'PNG Images (*.png);; All Files (*.*)'))
        if fn:
            qr = QR(filename=fn)
            if qr.decode():
                self.showInfo(qr)

    def showInfo(self, qr):
        msg = {
            'text': lambda : unicode(qr.data_decode[qr.data_type](qr.data)),
            'url': lambda : unicode(qr.data_decode[qr.data_type](qr.data)),
            'email': lambda : u"QRCode contains an e-mail addres.\n%s" % unicode((qr.data_decode[qr.data_type](qr.data))),
            'emailmessage': lambda : u"QRCode contains an e-mail message.\nTo: %s\nSubject: %s\nMessage: %s" % qr.data_decode[qr.data_type](qr.data),
            'telephone': lambda : u"QRCode contains a telephone number: " + unicode(qr.data_decode[qr.data_type](qr.data)),
            'sms': lambda : u"QRCode contains an SMS message.\nTo: %s\nMessage: %s" % qr.data_decode[qr.data_type](qr.data),
        }
        #FIX-ME: Promt to do the related action to the data type
        QtGui.QMessageBox.information(self, u'Decode QRCode', msg[qr.data_type]())
        print qr.data_type + ':', qr.data_decode[qr.data_type](qr.data)

    def decodeWebcam(self):
        qr = QR()
        qr.decode_webcam()
        if qr.data_to_string() != 'NULL':
            self.showInfo(qr)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    
    sys.exit(app.exec_())
