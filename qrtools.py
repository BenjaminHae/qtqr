#!/usr/bin/env python

# Authors:
#   David Green <david4dev@gmail.com>
#   Ramiro Algozino <algozino@gmail.com>
#
# qr.py: Library for encoding/decoding QR Codes (2D barcodes).
# Copyright (C) 2011 David Green <david4dev@gmail.com>
#
# `qr.py` is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# `qr.py` is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along
# with `qr.py`.  If not, see <http://www.gnu.org/licenses/>.
import subprocess
import os
import time
import shutil
import hashlib
import zbar
import Image

class QR(object):

    #use these for custom data formats eg. url, phone number, VCARD
    data_encode = {
        'text' : lambda data: str(data),
        'url' : lambda data: 'http://' + re.compile(
                r'^http://', re.IGNORECASE
            ).sub('', str(data)),
        'email' : 'mailto:' : lambda data: 'mailto:' + re.compile(
                r'^mailto:', re.IGNORECASE
            ).sub('', str(data)),
        'telephone' : 'tel:' : lambda data: 'tel:' + re.compile(
                r'^tel:', re.IGNORECASE
            ).sub('', str(data)),
    }

    data_decode = {}

    data_recognise = {}

    def __init__(
        self, pixel_size=3, level='L', margin_size=4,
        data_type='text', data='NULL', filename=None
    ):
        self.pixel_size = pixel_size
        self.level = level
        self.margin_size = margin_size
        self.data_type = data_type
        self.data = data
        #get a temp directory
        self.directory = os.path.join('/tmp', 'qr-%f' % time.time())
        self.filename = filename
        os.makedirs(self.directory)

    def data_to_string(self):
        return self.__class__.data_encode[self.data_type](self.data)

    def get_tmp_file(self):
        return os.path.join(
            self.directory,
            #filename is hash of data
            hashlib.sha256(self.data_to_string()).hexdigest() + '.png'
        )

    def encode(self, filename=None):
        self.filename = filename or self.get_tmp_file()
        if not self.filename.endswith('.png'):
            self.filename += '.png'
        return subprocess.Popen([
            'qrencode',
            '-o', self.filename,
            '-s', str(self.pixel_size),
            '-m', str(self.margin_size),
            '-l', self.level,
            self.data_to_string()
        ]).wait()

    def decode(self, filename=None):
        self.filename = filename or self.filename
        if self.filename:
            scanner = zbar.ImageScanner()
            # configure the reader
            scanner.parse_config('enable')
            # obtain image data
            pil = Image.open(self.filename).convert('L')
            width, height = pil.size
            raw = pil.tostring()
            # wrap image data
            image = zbar.Image(width, height, 'Y800', raw)
            # scan the image for barcodes
            scanner.scan(image)
            # extract results
            for symbol in image:
                pass
            # clean up
            del(image)
            self.data = symbol.data
            self.data_type = 'text'
            return True
        else:
            return False

    def decode_webcam(self, callback=lambda s:None, device='/dev/video0'):
        # create a Processor
        proc = zbar.Processor()

        # configure the Processor
        proc.parse_config('enable')

        # initialize the Processor
        proc.init(device)

        # setup a callback
        def my_handler(proc, image, closure):
            # extract results
            for symbol in image:
                if not symbol.count:
                    self.data = symbol.data
                    self.data_type = 'text'
                    callback(symbol.data)

        proc.set_data_handler(my_handler)

        # enable the preview window
        proc.visible = True

        # initiate scanning
        proc.active = True
        try:
            proc.user_wait()
        except zbar.WindowClosed:
            pass

    def destroy(self):
        shutil.rmtree(self.directory)
