# -*- coding: utf-8 -*-

"""Main module."""

import cdo
import xarray as xr

import os
import pkgutil
import subprocess
import sys


def build_cdo_object():
    try:
        return cdo.Cdo()
    except Exception as e:
        print("Python exception:", e)
        print("Unable to use CDO, this won't work, sorry...")
        print("You may consider running >> module load cdo << and trying to run again")
        sys.exit(1)

def _get_template_file():
    """
    Creates a local copy of the gfw_atmo template file.

    Returns
    -------
    str :
        Path to the file that was generated
    """
    template_file_path = "./gfw_atmo_template.nc"
    template_file_data = pkgutil.get_data("gfw_creator", "data/gfw_atmo_template.nc")
    with open(template_file_path, "wb") as template_file:
        template_file.write(template_file_data)
    return os.path.abspath(template_file_path)


def _load_template_file():
    """
    Loads the template file to be modified.

    Returns
    -------
    xr.Dataset :
        The template dataset, has 0 everywhere with 366 day timesteps. This is
        on the standard ECHAM6 T63 grid.
    """
    df = xr.open_dataset(_get_template_file())
    df.coords["lon"] = (df.coords["lon"] + 180) % 360 - 180
    df = df.sortby(df.lon)
    return df


def _lat_lon_area(lat_0, lat_1, lon_0, lon_1):
    """
    Figures out the area of a lat/lon box for distributing a flux across a
    total area
    """
    CDO = build_cdo_object()
    ds = _get_template_file()
    selected_ds = CDO.fldsum(
        input=f"-sellonlatbox,{lon_0},{lon_1},{lat_0},{lat_1} -selname,cell_area {ds}",
        returnXDataset=True,
    )
    return selected_ds.cell_area.data.squeeze()


def create_homogeneous_hosing(lat_0, lat_1, lon_0, lon_1, hosing_strength):
    """
    Creates a homogeneous hosing field
    """
    CDO = build_cdo_object()
    ds = _get_template_file()
    # Notes:
    # ------
    # `hosing_strength` is given in Sv. Convert this to m3/s:
    #
    # 1 Sv = 10**6 m3/s
    hosing_strength *= 1.0e6
    # The gfw_atmo file must be given in m/s, so we divide by the area for
    # conversion m3/s --> m/s :
    hosing_per_area = hosing_strength / _lat_lon_area(lat_0, lat_1, lon_0, lon_1)
    # Now that the hosing strength has been determined, set it in the NetCDF
    # file:
    gfw_atmo_file = CDO.setclonlatbox(
        f"{hosing_per_area},{lon_0},{lon_1},{lat_0},{lat_1}",
        input=ds,
        returnXDataset=True,
    )
    return gfw_atmo_file
