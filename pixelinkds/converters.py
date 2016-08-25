"""
    pixelinkds.convert
    ~~~~~~~~~~~~~~~~~~

    Convenience function to save stacks in other formats.

    This file is part of PixeLINKds.

    :copyright: 2016 by PixeLINKds Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import numpy as np


def write_timestamps(filename, ts):
    with open(filename, 'w', encoding='utf-8') as fo:
        for t in ts:
            fo.write('%.6f\n' % t)


def save_np(reader, output_filename):
    ts, data = reader.read_stack()
    np.savez(output_filename, timestamps=ts, data=data)


def save_mat(reader, output_filename):
    try:
        from scipy import io
    except ImportError:
        print('Please install scipy to use this format.')
        raise

    ts, data = reader.read_stack()
    io.savemat(output_filename, dict(timestamps=ts, data=data))


def save_tif(reader, output_filename):
    try:
        from tifffile import imsave
    except ImportError:
        print('Please install tifffile to use this format.')
        raise

    ts, data = reader.read_stack()
    imsave(output_filename, data)

    write_timestamps(output_filename + '.txt', ts)


def save_avi(reader, output_filename):
    try:
        import cv2
    except ImportError:
        print('Please install OpenCV2 to use this format.')
        raise

    writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'PIM1'),
                             25, reader.image_size1, False)

    ts = []
    for t, img in reader:
        ts.append(t)
        writer.write(img)

    write_timestamps(output_filename + '.txt', ts)


FORMATS = {
    '.npz': ('Uncompressed Numpy array', save_np),
    '.tif': ('Multipage tif', save_tif),
    '.mat': ('Matlab v5', save_mat),
    '.avi': ('AVI format with PIM1 encoding.', save_avi),
}
