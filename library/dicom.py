# -*- coding: utf-8 -*-
"""
Convert a DICOM embedded image file to a :class:`ContentFile` suitable for
django's :class:`ImageField`

Based on ConvertPIL.py from gdcm, just made it simpler by cutting a few
unneeded function calls and updating the string formating
"""
import gdcm
import numpy
from PIL import Image, ImageOps #@UnresolvedImport

def gdcm_to_numpy(image):
    
    """Converts a GDCM image to a numpy array."""
    
    _gdcm_np = {
            gdcm.PixelFormat.UINT8  :numpy.int8,
            gdcm.PixelFormat.INT8   :numpy.uint8,
            gdcm.PixelFormat.UINT16 :numpy.uint16,
            gdcm.PixelFormat.INT16  :numpy.int16,
            gdcm.PixelFormat.UINT32 :numpy.uint32,
            gdcm.PixelFormat.INT32  :numpy.int32,
            gdcm.PixelFormat.FLOAT32:numpy.float32,
            gdcm.PixelFormat.FLOAT64:numpy.float64
    }
    
    p_format = image.GetPixelFormat().GetScalarType()
    assert p_format in _gdcm_np, "Unsupported array type {0}".format(p_format)
    dimension = image.GetDimension(0), image.GetDimension(1)
    dtype = _gdcm_np[p_format]
    gdcm_array = image.GetBuffer()
    result = numpy.frombuffer(gdcm_array, dtype=dtype)
    maxV = float(result[result.argmax()])
    ## linear gamma adjust
    #result = result + .5*(maxV-result)
    ## log gamma
    result = numpy.log(result + 50) ## 50 is apprx background level
    result = result * (2.**8 / maxV) ## histogram stretch
    result.shape = dimension
    return result

def extraer_imagen(filename):
    
    """Extrae la imagen de un archivo DICOM
    
    :param filename: Lugar absoluto del archivo
    :returns:        un :class:`Image` de PIL
    """
    
    reader = gdcm.ImageReader()
    reader.SetFileName(filename)
    
    if not reader.Read():
        raise IOError("Can not read file {0}".format(filename))
    
    numpy_array = gdcm_to_numpy(reader.GetImage())
    ## L is 8 bit grey
    ## http://www.pythonware.com/library/pil/handbook/concepts.htm
    image = Image.frombuffer('L',
                             numpy_array.shape,
                             numpy_array.astype(numpy.uint8),
                             'raw', 'L', 0, 1)
    ## cutoff removes background noise and spikes
    image = ImageOps.autocontrast(image, cutoff=.1)
    return image
