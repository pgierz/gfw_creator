#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the main command line interface for the ``gfw_creator``. You can view
this help by typing either of the following::

    $ man gfw_creator
    $ pydoc gfw_creator.cli

You can create a uniform hosing field over a rectangular area with the
following command::

    $ gfw_creator -- lat_0 lat_1 lon_0 lon_1 hosing_strength

Hosing strength is assumed to be in Sv. lat and lon can be negative, and a -180
to 180 degree domain is assumed for longitude.

The generated output file, ``out.nc`` is created in the current working
directory, and can be used with the AWI-ESM gfw_atmo switch. Below is the result of::

    $ gfw_creator -- 45 60 -30 -10 0.15
    $ ncview out.nc

.. image:: _static/ncview_screenshot.png
  :width: 400
  :alt: Alternative text
"""
import gfw_creator

import sys
import click


@click.command()
@click.argument("lat_0", type=float)
@click.argument("lat_1", type=float)
@click.argument("lon_0", type=float)
@click.argument("lon_1", type=float)
@click.argument("hosing", type=float)
def main(lat_0, lat_1, lon_0, lon_1, hosing):
    ds = gfw_creator.create_homogeneous_hosing(lat_0, lat_1, lon_0, lon_1, hosing)
    ds.to_netcdf("out.nc")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
