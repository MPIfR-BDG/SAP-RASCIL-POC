import json
import codecs
import pickle
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from rascil.processing_components.visibility import (
    convert_blockvisibility_to_visibility as convert_bvis_to_vis)
from rascil.workflows.serial.simulation.simulation_serial import (
    simulate_list_serial_workflow)
from rascil.processing_components.imaging import advise_wide_field
from rascil.data_models.polarisation import PolarisationFrame
from rascil.processing_components.simulation import (
    create_low_test_image_from_gleam)
from rascil.workflows.serial.imaging.imaging_serial import (
    predict_list_serial_workflow)
from rascil.workflows.serial.imaging.imaging_serial import invert_list_serial_workflow
from rascil.data_models.polarisation import PolarisationFrame
from rascil.processing_components.imaging import create_image_from_visibility
from rascil.workflows.serial.simulation.simulation_serial import (
    corrupt_list_serial_workflow)
from rascil.workflows.serial.imaging.imaging_serial import deconvolve_list_serial_workflow


def wrapper(api):
    log = api.logger
    log.info("Starting advise wide field operator")
    log.debug("api configuration variables:")
    log.debug("delA = {}".format(api.config.delA))
    log.debug("guard_band_image = {}".format(api.config.guard_band_image))
    log.debug("wprojection_planes = {}".format(api.config.wprojection_planes))

    def execute(vis_pickle):
        log.debug("Executing advise wide field")
        vis_list = pickle.loads(codecs.decode(vis_pickle.encode(), "base64"))
        log.debug("vis_list size = {}".format(len(vis_list)))
        wprojection_planes = api.config.wprojection_planes
        log.debug("wprojection_planes = {}".format(wprojection_planes))
        advice_low = advise_wide_field(
            vis_list[0],
            guard_band_image=api.config.guard_band_image,
            delA=api.config.delA,
            wprojection_planes=wprojection_planes)
        log.debug("advice_low = {}".format(advice_low))
        advice_high = advise_wide_field(
            vis_list[-1],
            guard_band_image=api.config.guard_band_image,
            delA=api.config.delA,
            wprojection_planes=wprojection_planes)
        log.debug("advice_high = {}".format(advice_high))
        advice = {
            "vis_slices": advice_low['vis_slices'],
            "npixel": advice_high['npixels2'],
            "cellsize": min(advice_low['cellsize'], advice_high['cellsize'])
        }
        api.send("output", pickle.dumps(advice))

    api.add_shutdown_handler(lambda: log.info(
        "Shutting down advise wide field operator"))
    api.set_port_callback(["input"], execute)


try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)
