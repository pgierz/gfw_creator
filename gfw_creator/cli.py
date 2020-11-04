# -*- coding: utf-8 -*-

"""Console script for gfw_creator."""
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
