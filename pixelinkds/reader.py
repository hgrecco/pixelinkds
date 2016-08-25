"""
    pixelinkds.reader
    ~~~~~~~~~~~~~~~~~

    Provides a Reader class for PixeLINK Data Steam Files.

    The structure of the file is as follows:

    Header
    ------

    u32              - "magic number" 0x04040404,
                       indicating that this is a valid PDS file.
    u32              - number of frames in the file


    Data (frames times the following)
    ---------------------------------

    Frame Descriptor - a data structure providing information
                       about the structure of the frame
    Frame            - image stored as described in the frame descriptor.


    This file is part of PixeLINKds.

    :copyright: 2016 by PixeLINKds Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""


import io
import warnings

import numpy as np

from .types import FrameDescriptor, PixelFormat, PDS_MAGIC_NUMBER


class Reader:
    """A class to read a PixeLINK Data Steam Files.

    Parameters
    ----------
    filename_or_fp : str o file-like
                     The name of the file or
                     a readable and seekable file-like object (i.e. a stream)
                     of binary data.
    """

    def __init__(self, filename_or_fp):

        if hasattr(filename_or_fp, "read"):
            self._filename = None
            self._fin = filename_or_fp
        else:
            self._filename = filename_or_fp
            self._fin = open(filename_or_fp, "rb")

        header = self._fin_read_one(dtype=np.uint32)

        if header != PDS_MAGIC_NUMBER:
            raise ValueError('Not a PixeLINK Data Stream file (0x%x)' % header)

        self._frames = self._fin_read_one(dtype=np.uint32)
        self._offset = self._fin.tell()

        self._fd1 = d = FrameDescriptor.from_file(self._fin)

        self._image_size1 = d.get_image_size()
        self._read_count = cnt = self._image_size1[0] * self._image_size1[1]

        bpp = d.get_bytes_per_pixel()

        self._bytes_per_fd = d.size
        self._bytes_per_frame = bpp * cnt + self._bytes_per_fd

        self._pixel_format1 = fmt = self._fd1.get_pixel_format()

        self._read_shape = self._image_size1

        if fmt is PixelFormat.MONO8:
            self._read_dtype1 = np.uint8

        elif fmt is PixelFormat.MONO16:
            self._read_dtype1 = np.uint16

        else:
            self._read_dtype1 = np.uint8
            warnings.warn('%s is not currently supported by the Reader.\n'
                          'Raw data will be returned' % fmt)

            self._read_shape = (cnt, 1)
            self._read_count = cnt * d.get_pixel_format()

        self.reset()

    def close(self):
        """Close the stream.
        """
        self._fin.close()
        self._fin = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self._filename is not None:
            self.close()

    @property
    def is_open(self):
        return self._fin is not None

    @property
    def frames(self):
        """The number of frames in the file.
        """
        return self._frames

    @property
    def image_size1(self):
        """The image size (height, width) of the first frame.
        """
        return self._image_size1

    @property
    def pixel_format1(self):
        """The Pixel format of the first frame.
        """
        return self._pixel_format1

    def _fin_read_one(self, dtype):
        """Helper function to read 1 element from the input stream.
        """
        arr = np.fromfile(self._fin, dtype=dtype, count=1)
        if arr.size == 0:
            raise EOFError('Unexpected end of file')
        return arr[0]

    def _fin_read_many(self, dtype, count):
        """Helper function to read N element of the same type from the input stream.
        """
        arr = np.fromfile(self._fin, dtype=dtype, count=count)
        if arr.size != count:
            raise EOFError('Unexpected end of file')
        return arr

    def seek(self, n):
        """Move the cursor the beginning of the n-th frame descriptor.
        """
        self._fin.seek(self._offset + self._bytes_per_frame * n)

    def reset(self):
        """Move the cursor the beginning of the 1st frame descriptor.
        """
        self._fin.seek(self._offset, io.SEEK_SET)

    def __iter__(self):
        self.reset()

        for n in range(self._frames):
            desc, img = self.next()
            yield desc.frame_time, img

    def next(self):
        """Read next frame descriptor and frame

        Returns
        -------
        FrameDescriptor
            A data structure containing the information fo the frame.

        numpy.ndarray
            The frame.
        """

        return (FrameDescriptor.from_file(self._fin, self._bytes_per_fd),
                self._fin_read_many(self._read_dtype1, self._read_count).reshape(self._read_shape))

    def read_stack(self, offset=0, count=None):
        """Read the whole stack to numpy array

        Parameters
        ----------
        offset : int
                 Number of frames to skip from the beginning of the file.
        count : int
                Number of frames to read from the offset.

        Returns
        -------
        timestamps : np.array
                     Vector indicating the time of each frame.
                     Shape: (frames, )
        stack : np.ndarray
                3D array with the image stack.
                Shape: (frames, height, width)
        """
        if count is None:
            frames = self.frames
        else:
            frames = min(count, self.frames)

        if offset > 0:
            frames -= offset

        timestamps = np.empty((frames, ), dtype=np.float)
        stack = np.empty((frames, ) + self.image_size1, dtype=self._read_dtype1)

        for n, (ts, img) in enumerate(self):
            timestamps[n] = ts
            stack[n, :, :] = img

        return timestamps, stack

