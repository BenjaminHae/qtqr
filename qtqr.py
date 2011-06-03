#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""
GUI front end for qrencode based on the work of David Green:
<david4dev@gmail.com> https://launchpad.net/qr-code-creator/
and inspired by
http://www.omgubuntu.co.uk/2011/03/how-to-create-qr-codes-in-ubuntu/
"""

import sys, os
from PyQt4 import QtCore, QtGui
from qrtools import QR

__author__ = "Ramiro Algozino"
__email__ = "algozino@gmail.com"
__copyright__ = "copyright (C) 2011 Ramiro Algozino"
__credits__ = "David Green"
__license__ = "GPLv3"
__version__ = "1.1"

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle(u'QtQR: QR Code Generator')
        icon = os.path.join(os.path.dirname(__file__), u'logo_a_la_faenza.png')
        if not QtCore.QFile(icon).exists():
            icon = u'/usr/share/pixmaps/qtqr.png'
        self.setWindowIcon(QtGui.QIcon(icon))
        self.w = QtGui.QWidget()
        self.setCentralWidget(self.w)
        self.setAcceptDrops(True)

        #Templates for creating QRCodes supported by qrtools
        self.templates = {
            "text": "Text",
            "url": "URL",
            "bookmark": "Bookmark",
            "emailmessage": "E-Mail",
            "telephone": "Telephone Number",
            "phonebook": "Contact Information (PhoneBook)",
            "sms": "SMS",
            "mms": "MMS",
            "geo": "Geolocalization",
            }
        #With this we make the dict bidirectional
        self.templates.update( dict((self.templates[k], k) for k in self.templates))

        #Tabs
        # self.tabs = QtGui.QTabWidget()
        # self.tabs.setTabPosition(2)
        self.templateNames = (
            self.templates["text"],
            self.templates["url"],
            self.templates["bookmark"],
            self.templates["emailmessage"],
            self.templates["telephone"],
            self.templates["phonebook"],
            self.templates["sms"],
            self.templates["mms"],
            self.templates["geo"],
            )
        self.selector = QtGui.QComboBox()
        self.selector.addItems(self.templateNames)
        self.tabs = QtGui.QStackedWidget()
        self.textTab = QtGui.QWidget()
        self.urlTab = QtGui.QWidget()
        self.bookmarkTab = QtGui.QWidget()
        self.emailTab = QtGui.QWidget()
        self.telTab = QtGui.QWidget()
        self.phonebookTab = QtGui.QWidget()
        self.smsTab = QtGui.QWidget()
        self.mmsTab = QtGui.QWidget()
        self.geoTab = QtGui.QWidget()
        # self.tabs.addTab(self.textTab, u"&Text")
        self.tabs.addWidget(self.textTab)
        # self.tabs.addTab(self.urlTab, u"&URL")
        self.tabs.addWidget(self.urlTab)
        # self.tabs.addTab(self.bookmarkTab, u"&Bookmark")
        self.tabs.addWidget(self.bookmarkTab)
        # self.tabs.addTab(self.emailTab, u"&Email")
        self.tabs.addWidget(self.emailTab)
        # self.tabs.addTab(self.telTab, u"&Telephone")
        self.tabs.addWidget(self.telTab)
        # self.tabs.addTab(self.phonebookTab, u"&Contact Information")
        self.tabs.addWidget(self.phonebookTab)
        # self.tabs.addTab(self.smsTab, u"&SMS")
        self.tabs.addWidget(self.smsTab)
        # self.tabs.addTab(self.mmsTab, u"&MMS")
        self.tabs.addWidget(self.mmsTab)
        # self.tabs.addTab(self.geoTab, u"&Geolocalization")
        self.tabs.addWidget(self.geoTab)

        #Widgets for Text Tab
        self.l1 = QtGui.QLabel(u'Text to be encoded:')
        self.textEdit = QtGui.QPlainTextEdit()

        #Widgets for URL Tab
        self.urlLabel = QtGui.QLabel(u'URL to be encoded:')
        self.urlEdit = QtGui.QLineEdit(u'http://')

        #Widgets for BookMark Tab
        self.bookmarkTitleLabel = QtGui.QLabel(u"Title:")
        self.bookmarkTitleEdit = QtGui.QLineEdit()
        self.bookmarkUrlLabel = QtGui.QLabel(u"URL:")
        self.bookmarkUrlEdit = QtGui.QLineEdit()

        #Widgets for EMail Tab
        self.emailLabel = QtGui.QLabel(u'E-Mail address:')
        self.emailEdit = QtGui.QLineEdit(u"@.com")
        self.emailSubLabel = QtGui.QLabel(u'Subject:')
        self.emailSubjectEdit = QtGui.QLineEdit()
        self.emailBodyLabel = QtGui.QLabel(u'Message Body:')
        self.emailBodyEdit = QtGui.QPlainTextEdit()

        #Widgets for Telephone Tab
        self.telephoneLabel = QtGui.QLabel(u'Telephone Number:')
        self.telephoneEdit = QtGui.QLineEdit()

        #Widgets for Contact Information Tab
        self.phonebookNameLabel = QtGui.QLabel(u"Name:")
        self.phonebookNameEdit = QtGui.QLineEdit()
        self.phonebookTelLabel = QtGui.QLabel(u"Telephone:")
        self.phonebookTelEdit = QtGui.QLineEdit()
        self.phonebookEMailLabel = QtGui.QLabel(u"E-Mail:")
        self.phonebookEMailEdit = QtGui.QLineEdit()

        #Widgets for SMS Tab
        self.smsNumberLabel = QtGui.QLabel(u'Telephone Number:')
        self.smsNumberEdit = QtGui.QLineEdit()
        self.smsBodyLabel = QtGui.QLabel(u'Message:')
        self.smsBodyEdit = QtGui.QPlainTextEdit()

        #Widgets for MMS Tab
        self.mmsNumberLabel = QtGui.QLabel(u'Telephone Number:')
        self.mmsNumberEdit = QtGui.QLineEdit()
        self.mmsBodyLabel = QtGui.QLabel(u'Content:')
        self.mmsBodyEdit = QtGui.QPlainTextEdit()

        #Widgets for GEO Tab
        self.geoLatLabel = QtGui.QLabel(u"Latitude")
        self.geoLatEdit = QtGui.QLineEdit()
        self.geoLongLabel = QtGui.QLabel(u"Longitude")
        self.geoLongEdit = QtGui.QLineEdit()

        #Widgets for QREncode Parameters Configuration
        self.optionsGroup = QtGui.QGroupBox(u'Parameters:')

        self.l2 = QtGui.QLabel(u'&Pixel Size:')
        self.pixelSize = QtGui.QSpinBox()

        self.l3 = QtGui.QLabel(u'&EC Level:')
        self.ecLevel = QtGui.QComboBox()
        self.ecLevel.addItems((u'Lowest', u'Medium', u'QuiteGood', u'Highest'))

        self.l4 = QtGui.QLabel(u'&Margin Size:')
        self.marginSize = QtGui.QSpinBox()

        #QLabel for displaying the Generated QRCode
        self.qrcode = QtGui.QLabel(u'Start typing to create QR Code\n or  drop here a file for decoding.')
        self.qrcode.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qrcode.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        #Save and Decode Buttons
        self.saveButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(u'document-save'), u'&Save QRCode')
        self.decodeButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(u'preview-file'), u'&Decode')

        self.decodeMenu = QtGui.QMenu()
        self.decodeFileAction = self.decodeMenu.addAction(QtGui.QIcon.fromTheme(u'document-open'), u'Decode from &File')
        self.decodeWebcamAction = self.decodeMenu.addAction(QtGui.QIcon.fromTheme(u'image-png'), u'Decode from &WebCam')
        self.decodeButton.setMenu(self.decodeMenu)

        self.exitAction = QtGui.QAction(QtGui.QIcon.fromTheme(u'application-exit'), u'E&xit', self)
        self.addAction(self.exitAction)
        self.aboutAction = QtGui.QAction(QtGui.QIcon.fromTheme(u"help-about"), u"&About", self)
        self.addAction(self.aboutAction)

        # UI Tunning
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
        self.saveButton.setShortcut(u"Ctrl+S")
        self.exitAction.setShortcut(u"Ctrl+Q")
        self.aboutAction.setShortcut(u"F1")

        self.buttons = QtGui.QHBoxLayout()
        self.buttons.addWidget(self.saveButton)
        self.buttons.addWidget(self.decodeButton)

        #Text Tab
        self.codeControls = QtGui.QVBoxLayout()
        self.codeControls.addWidget(self.l1)
        self.codeControls.addWidget(self.textEdit, 1)
        self.textTab.setLayout(self.codeControls)

        #URL Tab
        self.urlTabLayout = QtGui.QVBoxLayout()
        self.urlTabLayout.addWidget(self.urlLabel)
        self.urlTabLayout.addWidget(self.urlEdit)
        self.urlTabLayout.addStretch()
        self.urlTab.setLayout(self.urlTabLayout)

        #Bookmark Tab
        self.bookmarkTabLayout = QtGui.QVBoxLayout()
        self.bookmarkTabLayout.addWidget(self.bookmarkTitleLabel)
        self.bookmarkTabLayout.addWidget(self.bookmarkTitleEdit)
        self.bookmarkTabLayout.addWidget(self.bookmarkUrlLabel)
        self.bookmarkTabLayout.addWidget(self.bookmarkUrlEdit)
        self.bookmarkTabLayout.addStretch()
        self.bookmarkTab.setLayout(self.bookmarkTabLayout)

        #Email Tab
        self.emailTabLayout = QtGui.QVBoxLayout()
        self.emailTabLayout.addWidget(self.emailLabel)
        self.emailTabLayout.addWidget(self.emailEdit)
        self.emailTabLayout.addWidget(self.emailSubLabel)
        self.emailTabLayout.addWidget(self.emailSubjectEdit)
        self.emailTabLayout.addWidget(self.emailBodyLabel)
        self.emailTabLayout.addWidget(self.emailBodyEdit, 1)
        self.emailTabLayout.addStretch()
        self.emailTab.setLayout(self.emailTabLayout)

        #Telephone Tab
        self.telTabLayout = QtGui.QVBoxLayout()
        self.telTabLayout.addWidget(self.telephoneLabel)
        self.telTabLayout.addWidget(self.telephoneEdit)
        self.telTabLayout.addStretch()
        self.telTab.setLayout(self.telTabLayout)

        #Contact Tab
        self.phonebookTabLayout = QtGui.QVBoxLayout()
        self.phonebookTabLayout.addWidget(self.phonebookNameLabel)
        self.phonebookTabLayout.addWidget(self.phonebookNameEdit)
        self.phonebookTabLayout.addWidget(self.phonebookTelLabel)
        self.phonebookTabLayout.addWidget(self.phonebookTelEdit)
        self.phonebookTabLayout.addWidget(self.phonebookEMailLabel)
        self.phonebookTabLayout.addWidget(self.phonebookEMailEdit)
        self.phonebookTabLayout.addStretch()
        self.phonebookTab.setLayout(self.phonebookTabLayout)

        #SMS Tab
        self.smsTabLayout = QtGui.QVBoxLayout()
        self.smsTabLayout.addWidget(self.smsNumberLabel)
        self.smsTabLayout.addWidget(self.smsNumberEdit)
        self.smsTabLayout.addWidget(self.smsBodyLabel)
        self.smsTabLayout.addWidget(self.smsBodyEdit, 1)
        self.smsTabLayout.addStretch()
        self.smsTab.setLayout(self.smsTabLayout)

        #MMS Tab
        self.mmsTabLayout = QtGui.QVBoxLayout()
        self.mmsTabLayout.addWidget(self.mmsNumberLabel)
        self.mmsTabLayout.addWidget(self.mmsNumberEdit)
        self.mmsTabLayout.addWidget(self.mmsBodyLabel)
        self.mmsTabLayout.addWidget(self.mmsBodyEdit, 1)
        self.mmsTabLayout.addStretch()
        self.mmsTab.setLayout(self.mmsTabLayout)

        #Geolocalization Tab
        self.geoTabLayout = QtGui.QVBoxLayout()
        self.geoTabLayout.addWidget(self.geoLatLabel)
        self.geoTabLayout.addWidget(self.geoLatEdit)
        self.geoTabLayout.addWidget(self.geoLongLabel)
        self.geoTabLayout.addWidget(self.geoLongEdit)
        self.geoTabLayout.addStretch()
        self.geoTab.setLayout(self.geoTabLayout)

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
        self.selectorBox = QtGui.QGroupBox("Select data type:")
#        self.selectorLayout = QtGui.QVBoxLayout()
#        self.selectorLayout.addWidget(self.selector)

        self.vlayout1 = QtGui.QVBoxLayout()
#        self.vlayout1.addWidget(self.selectorBox)
        self.vlayout1.addWidget(self.selector)
        self.vlayout1.addWidget(self.tabs, 1)

        self.vlayout2 = QtGui.QVBoxLayout()
        self.vlayout2.addWidget(self.optionsGroup)
        self.vlayout2.addWidget(self.qrcode, 1)
        self.vlayout2.addLayout(self.buttons)

        self.layout = QtGui.QHBoxLayout(self.w)
#        self.layout.addLayout(self.vlayout1)
        self.selectorBox.setLayout(self.vlayout1)
        self.layout.addWidget(self.selectorBox)
        self.layout.addLayout(self.vlayout2)

        #Signals
        self.selector.currentIndexChanged.connect(self.tabs.setCurrentIndex)
        self.tabs.currentChanged.connect(self.selector.setCurrentIndex)
        self.textEdit.textChanged.connect(self.qrencode)
        self.urlEdit.textChanged.connect(self.qrencode)
        self.bookmarkTitleEdit.textChanged.connect(self.qrencode)
        self.bookmarkUrlEdit.textChanged.connect(self.qrencode)
        self.emailEdit.textChanged.connect(self.qrencode)
        self.emailSubjectEdit.textChanged.connect(self.qrencode)
        self.emailBodyEdit.textChanged.connect(self.qrencode)
        self.phonebookNameEdit.textChanged.connect(self.qrencode)
        self.phonebookTelEdit.textChanged.connect(self.qrencode)
        self.phonebookEMailEdit.textChanged.connect(self.qrencode)
        self.smsNumberEdit.textChanged.connect(self.qrencode)
        self.smsBodyEdit.textChanged.connect(self.qrencode)
        self.mmsNumberEdit.textChanged.connect(self.qrencode)
        self.mmsBodyEdit.textChanged.connect(self.qrencode)
        self.telephoneEdit.textChanged.connect(self.qrencode)
        self.geoLatEdit.textChanged.connect(self.qrencode)
        self.geoLongEdit.textChanged.connect(self.qrencode)
        self.pixelSize.valueChanged.connect(self.qrencode)
        self.ecLevel.currentIndexChanged.connect(self.qrencode)
        self.marginSize.valueChanged.connect(self.qrencode)
        self.saveButton.clicked.connect(self.saveCode)
        self.exitAction.triggered.connect(self.close)
        self.aboutAction.triggered.connect(self.about)
        self.decodeFileAction.triggered.connect(self.decodeFile)
        self.decodeWebcamAction.triggered.connect(self.decodeWebcam)

        self.qrcode.setAcceptDrops(True)
        self.qrcode.__class__.dragEnterEvent = self.dragEnterEvent
        self.qrcode.__class__.dropEvent = self.dropEvent

    def qrencode(self):
        #Functions to get the correct data
        data = {
            "text": unicode(self.textEdit.toPlainText()),
            "url": unicode(self.urlEdit.text()),
            "bookmark": ( unicode(self.bookmarkTitleEdit.text()), unicode(self.bookmarkUrlEdit.text()) ),
            "emailmessage": ( unicode(self.emailEdit.text()), unicode(self.emailSubjectEdit.text()), unicode(self.emailBodyEdit.toPlainText()) ),
            "telephone": unicode(self.telephoneEdit.text()),
            "phonebook": (unicode(self.phonebookNameEdit.text()), unicode(self.phonebookTelEdit.text()), unicode(self.phonebookEMailEdit.text()) ),
            "sms": ( unicode(self.smsNumberEdit.text()), unicode(self.smsBodyEdit.toPlainText()) ),
            "mms": ( unicode(self.mmsNumberEdit.text()), unicode(self.mmsBodyEdit.toPlainText()) ),
            "geo": ( unicode(self.geoLatEdit.text()), unicode(self.geoLongEdit.text()) ),
        }

        level = (u'L',u'M',u'Q',u'H')

        if data[self.templates[unicode(self.selector.currentText())]]:
            qr = QR(pixel_size = unicode(self.pixelSize.value()),
                    data = data[self.templates[unicode(self.selector.currentText())]],
                    level = unicode(level[self.ecLevel.currentIndex()]),
                    margin_size = unicode(self.marginSize.value()),
                    data_type = unicode(self.templates[unicode(self.selector.currentText())]),
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
            QtGui.QMessageBox.information(self, u'Save QRCode',u'QRCode succesfully saved to <b>%s</b>.' % fn)

    def decodeFile(self, fn=None):
        if not fn:
            fn = unicode(QtGui.QFileDialog.getOpenFileName(
                self,
                u'Open QRCode',
                filter=u'Images (*.png *.jpg);; All Files (*.*)'
                )
            )
        if os.path.isfile(fn):
            qr = QR(filename=fn)
            if qr.decode():
                self.showInfo(qr)
            else:
                QtGui.QMessageBox.information(
                    self,
                    u'Decode File',
                    u'No QRCode could be found in file: <b>%s</b>.' % fn
                )
#        else:
#            QtGui.QMessageBox.information(
#                self,
#                u"Decode from file",
#                u"The file <b>%s</b> doesn't exist." %
#                os.path.abspath(fn),
#                QtGui.QMessageBox.Ok
#            )

    def showInfo(self, qr):
        dt = qr.data_type
        print dt.encode(u"utf-8") + ':',
        data = qr.data_decode[dt](qr.data)
        if type(data) == tuple:
            for d in data:
                print d.encode(u"utf-8")
        else:
            print data.encode(u"utf-8")
        msg = {
            'text': lambda : u"QRCode contains the following text:\n\n%s" % (data),
            'url': lambda : u"QRCode contains the following url address:\n\n%s" % (data),
            'bookmark': lambda: u"QRCode contains a bookmark:\n\nTitle: %s\nURL: %s" % (data),
            'email': lambda : u"QRCode contains the following e-mail address:\n\n%s" % (data),
            'emailmessage': lambda : u"QRCode contains an e-mail message:\n\nTo: %s\nSubject: %s\nMessage: %s" % (data),
            'telephone': lambda : u"QRCode contains a telephone number: " + (data),
            'phonebook': lambda : u"QRCode contains a phonebook entry:\n\nName: %s\nTel: %s\nE-Mail: %s" % (data),
            'sms': lambda : u"QRCode contains the following SMS message:\n\nTo: %s\nMessage: %s" % (data),
            'mms': lambda : u"QRCode contains the following MMS message:\n\nTo: %s\nMessage: %s" % (data),
            'geo': lambda : u"QRCode contains the following coordinates:\n\nLatitude: %s\nLongitude:%s" % (data),
        }
        wanna = u"\n\nDo you want to "
        action = {
            'text': u"",
            'url': wanna + u"open it in a browser?",
            'bookmark': wanna + u"open it in a browser?",
            'email': wanna + u"send an e-mail to the address?",
            'emailmessage': wanna + u"send the e-mail?",
            'telephone': u"",
            'phonebook': u"",
            'sms': u"",
            'mms': u"",
            'geo': wanna + u"open it on Google Maps?",
        }
        if action[qr.data_type] != u"":
            msgBox = QtGui.QMessageBox(
                QtGui.QMessageBox.Question,
                u'Decode QRCode',
                msg[qr.data_type]() + action[qr.data_type],
                QtGui.QMessageBox.No |
                QtGui.QMessageBox.Yes,
                self
                )
            msgBox.addButton(u"&Edit", QtGui.QMessageBox.ApplyRole)
            msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
            rsp = msgBox.exec_()
        else:
            msgBox = QtGui.QMessageBox(
                QtGui.QMessageBox.Information,
                u"Decode QRCode",
                msg[qr.data_type]() + action[qr.data_type],
                QtGui.QMessageBox.Ok,
                self
                )
            msgBox.addButton(u"&Edit", QtGui.QMessageBox.ApplyRole)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            rsp = msgBox.exec_()

        if rsp == QtGui.QMessageBox.Yes:
            #Open Link
            if qr.data_type == 'emailmessage':
                link = 'mailto:%s?subject=%s&body=%s' % (data)
            elif qr.data_type == 'geo':
                link = 'http://maps.google.com/maps?q=%s,%s' % data
            elif qr.data_type == 'bookmark':
                link = qr.data[1]
            else:
                link = qr.data_decode[qr.data_type](qr.data)
            print u"Opening " + link
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))
        elif rsp == 0:
            #Edit the code
            data = qr.data_decode[qr.data_type](qr.data)
            if qr.data_type == 'text':
                self.tabs.setCurrentIndex(0)
                self.textEdit.setPlainText(data)
            elif qr.data_type == 'url':
                self.tabs.setCurrentIndex(1)
                self.urlEdit.setText(data)
            elif qr.data_type == 'bookmark':
                self.bookmarkTitleEdit.setText(data[0])
                self.bookmarkUrlEdit.setText(data[1])
                self.tabs.setCurrentIndex(2)
            elif qr.data_type == 'emailmessage':
                self.emailEdit.setText(data[0])
                self.emailSubjectEdit.setText(data[1])
                self.emailBodyEdit.setPlainText(data[2])
                self.tabs.setCurrentIndex(3)
            elif qr.data_type == 'email':
                self.emailEdit.setText(data)
                self.emailSubjectEdit.setText("")
                self.emailBodyEdit.setPlainText("")
                self.tabs.setCurrentIndex(3)
            elif qr.data_type == 'telephone':
                self.telephoneEdit.setText(data)
                self.tabs.setCurrentIndex(4)
            elif qr.data_type == 'phonebook':
                self.phonebookNameEdit.setText(data[0])
                self.phonebookTelEdit.setText(data[1])
                self.phonebookEMailEdit.setText(data[2])
                self.tabs.setCurrentIndex(5)
            elif qr.data_type == 'sms':
                self.smsNumberEdit.setText(data[0])
                self.smsBodyEdit.setPlainText(data[1])
                self.tabs.setCurrentIndex(6)
            elif qr.data_type == 'mms':
                self.mmsNumberEdit.setText(data[0])
                self.mmsBodyEdit.setPlainText(data[1])
                self.tabs.setCurrentIndex(7)
            elif qr.data_type == 'geo':
                self.geoLatEdit.setText(data[0])
                self.geoLongEdit.setText(data[1])
                self.tabs.setCurrentIndex(8)

    def decodeWebcam(self):
        QtGui.QMessageBox.information(
            self,
            u"Decode from webcam",
            u"You are about to decode from your webcam. Please put the code in front of your webcam with a good light source and keep it steady. Once you see a green rectangle you can close the window by pressing any key.",
            QtGui.QMessageBox.Ok
        )
        qr = QR()
        qr.decode_webcam()
        if qr.data_decode[qr.data_type](qr.data) == 'NULL':
            QtGui.QMessageBox.warning(
                self,
                u"Decoding Failed",
                u"<p>Oops! no code was found.<br /> \
                Maybe your webcam didn't focus.</p>",
                QtGui.QMessageBox.Ok
            )
        else:
            self.showInfo(qr)

    def about(self):
        QtGui.QMessageBox.about(
            self,
            u"About QtQR",
            u'<h1>QtQR %s</h1>\
            <p>A simple software for creating and decoding QR Codes that uses <a href="https://code.launchpad.net/~qr-tools-developers/qr-tools/python-qrtools-trunk">python-qrtools</a> as backend. Both are part of the <a href="https://launchpad.net/qr-tools">QR Tools</a> project.</p>\
            <p></p>\
            <p>This is Free Software: GNU-GPLv3</p> \
            <p></p>\
            <p>Please visit our website for more information and to check out the code:<br />\
            <a href="https://launchpad.net/~qr-tools-developers/qtqr">\
            https://launchpad.net/~qr-tools-developers/qtqr</p> \
            <p>copyright &copy; Ramiro Algozino \
            &lt;<a href="mailto:algozino@gmail.com">algozino@gmail.com</a>&gt;</p>' % __version__,
        )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for fn in event.mimeData().urls():
            fn = fn.toLocalFile()
            self.decodeFile(unicode(fn))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    if len(app.argv())>1:
        #Open the file and try to decode it
        for fn in app.argv()[1:]:
            mw.decodeFile(fn)
    sys.exit(app.exec_())
