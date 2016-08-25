PixeLINKds: PixeLINK Data Steam Files in Python
===============================================

PixeLINK Data Steam (PDS) is a file format used by PixeLINK software.

It is extremely easy to use

.. code-block:: python

    >>> import pixelinkds as pds
    >>> timestamps, stack = pds.read('myfile.pds')

You can also iterate over each frame:

.. code-block:: python

    >>> with pds.Reader('myfile.pds') as reader:
    ...     for timestamp, img in reader:
    ...         print(timestamp)
    ...         # do something with your image


Or you can convert into another format:

.. code-block:: python

    >>> pds.convert('myfile.pds', 'myfile.tif')


Current supported formats are tif (Multipage tif), npz (Numpy), mat (Matlab), avi (PIM1 encoded)
For tif an avi files you will get an extra file with .txt appended to the name with the timestamps.

You can also convert or get info form the command line:

.. code-block:: bash

    $ python -m pixelinkds convert myfile.pds myfile.tif
    $ python -m pixelinkds info myfile.pds


Quick Installation
------------------

To install PixeLINKds, simply:

.. code-block:: bash

    $ pip install pixelinkds


Dependencies
------------

 * Numpy
 * SciPy (optional, to export mat files)
 * tifffile (optional, to export tif files)
 * OpenCV2 (optional, to export avi files)