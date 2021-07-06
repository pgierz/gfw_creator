from . import gfw_creator

import sys

from loguru import logger


def create_hosing_files(config):
    if config["general"]["setup_name"] == "awiesm":
        if config["fesom"].get("do_hosing"):
            logger.info("Creating hosing files...")
            hosing_type = config["fesom"].get("hosing_type")
            config['oasis3mct']['coupling_target_fields']['a2o_flux'].append("gfw_atmo <--input-- from_file")
            if hosing_type == "homogeneous":
                lat_0 = config["fesom"]["hosing_lat0"]
                lat_1 = config["fesom"]["hosing_lat1"]
                lon_0 = config["fesom"]["hosing_lon0"]
                lon_1 = config["fesom"]["hosing_lon1"]
                hosing_strength = config["fesom"]["hosing_strength"]
                gfw_atmo_file = gfw_creator.create_homogeneous_hosing(
                    lat_0, lat_1, lon_0, lon_1, hosing_strength
                )
                gfw_atmo_file.to_netcdf(
                    config["fesom"]["thisrun_forcing_dir"] + "/gfw_atmo.nc"
                )
                logger.info(
                    f"Wrote {config['fesom']['thisrun_forcing_dir'] + '/gfw_atmo.nc'} for use in the simulation!"
                )
                config["oasis3mct"].setdefault("coupling_input_fields", {})
                config["oasis3mct"]["coupling_input_fields"]["gfw_atmo"] = {
                    "freq": 86400,
                    "field_filepath": "gfw_atmo.nc",
                }
                config["fesom"].setdefault("forcing_files", {})
                config["fesom"].setdefault("forcing_sources", {})
                config["fesom"].setdefault("forcing_in_work", {})

                config["fesom"]["forcing_files"]["gfw_atmo"] = "gfw_atmo"
                config["fesom"]["forcing_sources"]["gfw_atmo"] = (
                    config["fesom"]["thisrun_forcing_dir"] + "/gfw_atmo.nc"
                )
                config["fesom"]["forcing_in_work"]["gfw_atmo"] = "gfw_atmo.nc"
                return config
            elif hosing_type == "from_file":
                logger.error("Sorry, hosing from a file has no yet been implemented!")
                sys.exit(1)
                # TODO(PG): Later...
                # hosing_file = config["fesom"]["hosing_file"]
            else:
                logger.error(
                    "Sorry, you must select between hosing_type: 'homogeneous' or hosing_type: 'from_file' in your fesom configuration!"
                )
                sys.exit(1)

    return config
