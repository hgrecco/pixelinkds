"""
    pixelinkds.types
    ~~~~~~~~~~~~~~~~

    PixeLINK Data Steam Files.

    This file is part of PixeLINKds.

    :copyright: 2016 by PixeLINKds Authors, see AUTHORS for more details.
    :license: BSD, see COPYING for more details.
"""

import sys

from .converters import FORMATS
from . import Reader, convert


FORMATS_TXT = '\n'.join('- %s : %s \n' % (fmt, doc)
                        for fmt, (doc, func) in FORMATS.items())


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='pixelinkds', description='PixeLINK Data Steam Files converter.')

    subparsers = parser.add_subparsers(title='command', dest='command')
    subparsers.required = True

    parser_convert = subparsers.add_parser('convert', help='Convert PDS file to another format.')

    parser_convert.add_argument('input', type=str,
                                help='Path of the input pds file.')
    parser_convert.add_argument('output', type=str,
                                help='Path of the output pds file\n'
                                     '(The extension determines the format. '
                                     'Valid values are:\n' + FORMATS_TXT)

    parser_info = subparsers.add_parser('info', help='Print information about a PDS file.')
    parser_info.add_argument('input', type=str,
                             help='Path of the input pds file.')

    args = parser.parse_args()

    if args.command == 'convert':
        convert(args.input, args.output)

    elif args.command == 'info':
        with Reader(args.input) as r:
            print('Frames: %s' % r.frames)
            print('Image Size: %sx%s' % r.image_size1)
            print('Pixel Format: %s' % r._pixel_format1)

    else:
        print('Unknown subcommand %s. See help for details.' % args.command)
        sys.exit(1)
