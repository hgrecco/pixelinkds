"""
    pixelinkds.types
    ~~~~~~~~~~~~~~~~

    PixeLINK Data Steam Files in Python.

    This file is part of PixeLINKds.

    :copyright: 2016 by PixeLINKds Authors, see AUTHORS for more details.
    :license: BSD, see COPYING for more details.
"""

import os

from .converters import FORMATS
from .reader import Reader
from .types import FrameDescriptor, PixelFormat


def read(filename):
    """Read a PDS file and return the timestamps and data.

    Parameters
    ----------
    filename : str
               Full path of the file to read.

    Returns
    -------
    timestamps : np.array
                 Vector indicating the time of each frame.
                 Shape: (frames, )
    stack : np.ndarray
            3D array with the image stack.
            Shape: (frames, height, width)
    """
    with Reader(filename) as r:
        return r.read_stack()


def convert(input, output):
    """Read a PDS file and write the content in another format.

    Parameters
    ----------
    input : str or Reader
            Full path of the file to read or a Reader object.
    output : str
             Full path of the file to write.
             (the format will be obtained from the name of the file)

    """
    _, ext = os.path.splitext(output)

    try:
        _, func = FORMATS[ext.lower()]
    except KeyError:
        raise ValueError('%s is an unknown extension. See help for details.' % ext)

    if isinstance(input, Reader):
        func(input, output)
    else:
        with Reader(input) as r:
            func(r, output)