"""
    pixelinkds.types
    ~~~~~~~~~~~~~~~~

    Common structs and constants

    This file is part of PixeLINKds.

    :copyright: 2016 by PixeLINKds Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import ctypes as ct
import enum
import io

import numpy as np

PDS_MAGIC_NUMBER = 0x04040404
PXL_MAX_STROBES = 16
PXL_MAX_KNEE_POINTS = 4


class PixelFormat(enum.IntEnum):
    MONO8 = 0
    MONO16 = 1
    YUV422 = 2
    BAYER8_GRBG = 3
    BAYER16_GRBG = 4
    RGB24 = 5
    RGB48 = 6
    BAYER8_RGGB = 7
    BAYER8_GBRG = 8
    BAYER8_BGGR = 9
    BAYER16_RGGB = 10
    BAYER16_GBRG = 11
    BAYER16_BGGR = 12
    # BAYER8 = BAYER8_GRBG
    # BAYER16 =  BAYER16_GRBG
    MONO12_PACKED = 13
    BAYER12_GRBG_PACKED = 14
    BAYER12_RGGB_PACKED = 15
    BAYER12_GBRG_PACKED = 16
    BAYER12_BGGR_PACKED = 17
    # BAYER12_PACKED = BAYER12_GRBG_PACKED
    # RGB24_DIB = RGB24
    RGB24_NON_DIB = 18
    # RGB48_NON_DIB = RGB48
    RGB48_DIB = 19
    MONO12_PACKED_MSFIRST = 20
    BAYER12_GRBG_PACKED_MSFIRST = 21
    BAYER12_RGGB_PACKED_MSFIRST = 22
    BAYER12_GBRG_PACKED_MSFIRST = 23
    BAYER12_BGGR_PACKED_MSFIRST = 24
    # BAYER12_PACKED_MSFIRST = BAYER12_GRBG_PACKED_MSFIRST


class Trigger(ct.Structure):
    _fields_ = [
        ('mode', ct.c_float),
        ('type', ct.c_float),
        ('polarity', ct.c_float),
        ('delay', ct.c_float),
        ('parameter', ct.c_float),
    ]


class GPIO(ct.Structure):
    _fields_ = [
        ('mode', ct.c_float * PXL_MAX_STROBES),
        ('polarity', ct.c_float * PXL_MAX_STROBES),
        ('parameter1', ct.c_float * PXL_MAX_STROBES),
        ('parameter2', ct.c_float * PXL_MAX_STROBES),
        ('parameter3', ct.c_float * PXL_MAX_STROBES),
    ]


class ROI(ct.Structure):
    _fields_ = [
        ('left', ct.c_float),
        ('top', ct.c_float),
        ('width', ct.c_float),
        ('height', ct.c_float),
    ]


class HV(ct.Structure):
    _fields_ = [
        ('horizontal', ct.c_float),
        ('vertical', ct.c_float),
    ]


class WhiteShading(ct.Structure):
    _fields_ = [
        ('red_gain', ct.c_float),
        ('green_gain', ct.c_float),
        ('blue_gain', ct.c_float),
    ]


class SharpnessScoreParams(ct.Structure):
    _fields_ = [
        ('left', ct.c_float),
        ('top', ct.c_float),
        ('width', ct.c_float),
        ('height', ct.c_float),
        ('max_value', ct.c_float),
    ]


class FrameDescriptor(ct.Structure):
    """An class wrapping the Frame Descriptor.
    """

    _fields_ = [
        ('size', ct.c_uint32),
        ('frame_time', ct.c_float),
        ('frame_number', ct.c_uint32),

        ('brightness', ct.c_float),
        ('autoexposure', ct.c_float),
        ('sharpness', ct.c_float),
        ('white_balance', ct.c_float),
        ('hue', ct.c_float),
        ('saturation', ct.c_float),
        ('gamma', ct.c_float),
        ('shutter', ct.c_float),
        ('gain', ct.c_float),
        ('iris', ct.c_float),
        ('focus', ct.c_float),
        ('temperature', ct.c_float),

        ('trigger', Trigger),

        ('zoom', ct.c_float),
        ('pan', ct.c_float),
        ('tilt', ct.c_float),
        ('optical_filter', ct.c_float),

        ('gpio', GPIO),

        ('frame_rate', ct.c_float),

        ('roi', ROI),
        ('flip', HV),

        ('decimation', ct.c_float),
        ('pixel_format', ct.c_float),

        ('extended_shutter', ct.c_float * PXL_MAX_KNEE_POINTS),

        ('auto_roi', ROI),

        ('decimation_mode', ct.c_float),

        ('white_shading', WhiteShading),

        ('rotate', ct.c_float),
        ('image_clock_divisor', ct.c_float),
        ('trigger_with_controlled_light', ct.c_float),
        ('max_pixel_size', ct.c_float),

        ('trigger_number', ct.c_float),
        ('image_processing_umask', ct.c_float),

        ('pixel_addressing_value', HV),

        ('frame_time_hr', ct.c_double),
        ('frame_number_hr', ct.c_uint64),

        ('bandwidth_limit', ct.c_float),
        ('actual_frame_rate', ct.c_double),

        ('sharpness_score_roi', SharpnessScoreParams),
        ('sharpness_score', ct.c_float),
    ]

    def get_bytes_per_pixel(self):
        """Return the number of bytes used by each pixel depending on the Pixel Format.
        """
        fmt = self.get_pixel_format()
        if fmt in (PixelFormat.MONO8, PixelFormat.BAYER8_GRBG, PixelFormat.BAYER8_RGGB, PixelFormat.BAYER8_GBRG,
                   PixelFormat.BAYER8_BGGR):
            return 1
        elif fmt in (PixelFormat.YUV422, PixelFormat.MONO16, PixelFormat.BAYER16_GRBG, PixelFormat.BAYER16_RGGB,
                     PixelFormat.BAYER16_GBRG, PixelFormat.BAYER16_BGGR):
            return 2
        elif fmt is PixelFormat.RGB24:
            return 3
        elif fmt is PixelFormat.RGB48:
            return 6

        raise ValueError('Unknown size for format %s' % fmt)

    def get_pixel_format(self):
        """Return the pixel format as a PixelFormat enum.
        """
        return PixelFormat(self.pixel_format)

    def get_image_size(self):
        """Return the image size (height, width)
        """
        return int(self.roi.height / self.decimation), int(self.roi.width / self.decimation)

    @classmethod
    def from_file(cls, fp, size=None):
        """Construct a Frame Descriptor object from binary data.

        Parameters
        ----------
        fp : file-like
             File-like object to read the Frame Descriptor from.
             The cursor must be at the position where the Frame Descriptor starts.

        size : int, optional
               the number of bytes to be read.
               If not given, the value inspected from the fp itself will be used.

        Returns
        -------
        FrameDescriptor

        .. note:: A number of bytes equal to `size` will be consumed from the fp.

        .. warning:
                  If the number of requested bytes is smaller than the size of the
                  Frame Descriptor, some fields might be left unfilled.


        """
        out = FrameDescriptor()

        if size is None:
            size = np.fromfile(fp, dtype=np.uint32, count=1)
            if size.size == 0:
                raise ValueError('Unexpected EOF')

            fp.seek(-size.nbytes, io.SEEK_CUR)

            size = size[0]

        if size > ct.sizeof(FrameDescriptor):
            raise ValueError('Number of requested bytes (%d) do not fit '
                             'in the data structure (%d)' % (size, ct.sizeof(out)))

        buf = fp.read(size)

        ct.memmove(ct.addressof(out), buf, size)

        return out
