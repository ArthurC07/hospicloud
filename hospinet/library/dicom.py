# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2013 Carlos Flores <cafg10@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.

"""
Convert a DICOM embedded image file to a :class:`ContentFile` suitable for
django's :class:`ImageField`

Based on ConvertPIL.py from gdcm, just made it simpler by cutting a few
unneeded function calls and updating the string formating
"""
import gdcm
import numpy
from PIL import Image, ImageOps #@UnresolvedImport

_gdcm_np = {gdcm.PixelFormat.UINT8  :numpy.int8,
                gdcm.PixelFormat.INT8   :numpy.uint8,
                gdcm.PixelFormat.UINT16 :numpy.uint16,
                gdcm.PixelFormat.INT16  :numpy.int16,
                gdcm.PixelFormat.UINT32 :numpy.uint32,
                gdcm.PixelFormat.INT32  :numpy.int32,
                gdcm.PixelFormat.FLOAT32:numpy.float32,
                gdcm.PixelFormat.FLOAT64:numpy.float64 }

def gdcm_to_numpy(image):
    """Converts a GDCM image to a numpy array.
    """
    pf = image.GetPixelFormat().GetScalarType()
    assert pf in _gdcm_np, "Unsupported array type {0}".format(pf)
    d = image.GetDimension(0), image.GetDimension(1)
    dtype = _gdcm_np[pf]
    gdcm_array = image.GetBuffer()
    result = numpy.frombuffer(gdcm_array, dtype=dtype)
    maxV = float(result[result.argmax()])
    ## linear gamma adjust
    #result = result + .5*(maxV-result)
    ## log gamma
    result = numpy.log(result + 50) ## 50 is apprx background level
    maxV = float(result[result.argmax()])
    result = result * (2.**8 / maxV) ## histogram stretch
    result.shape = d
    return result

def extraer_imagen(filename):
    reader = gdcm.ImageReader()
    reader.SetFileName(filename)
    if not reader.Read():
        raise IOError("Can not read file {0}".format(filename))
    
    numpy_array = gdcm_to_numpy(reader.GetImage())
    ## L is 8 bit grey
    ## http://www.pythonware.com/library/pil/handbook/concepts.htm
    pilImage = Image.frombuffer('L',
                           numpy_array.shape,
                           numpy_array.astype(numpy.uint8),
                           'raw', 'L', 0, 1)
    ## cutoff removes background noise and spikes
    pilImage = ImageOps.invert(ImageOps.autocontrast(pilImage, cutoff=.1))
    return pilImage
