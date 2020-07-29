import json
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
    log.info("Starting model creation operator")


    def execute(vis_pickle, advice_pickle):
        log.debug("Executing model creation")
        vis_list = pickle.loads(vis_pickle)
        advice = pickle.loads(advice_pickle)
        vis_slices = advice['vis_slices']
        npixel = advice['npixel']
        cellsize = advice['cellsize']
        model_list = []
        for vis in vis_list:
            model_list.append(
                create_image_from_visibility(
                    vis,
                    npixel=npixel,
                    frequency=[vis.frequency[0]],
                    channel_bandwidth=[vis.channel_bandwidth[0]],
                    cellsize=cellsize,
                    phasecentre=vis.phasecentre,
                    polarisation_frame=PolarisationFrame("stokesI")
                )
            )
        api.send("output", pickle.dumps(model_list, protocol=2))


    api.add_shutdown_handler(lambda: log.info(
        "Shutting down model creation operator"))
    api.set_port_callback(["inputvis", "inputadvice"], execute)


# ////////////////////////////////////////////////////////

try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)
