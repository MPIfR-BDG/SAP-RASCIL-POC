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
    log.info("Starting GLEAM model generation operator")

    def execute(vis_pickle, advice_pickle):
        """
        @brief   Create a visibility set based on the operator configuration

        @param   config_json   A JSON string containing optional configuration
                               parameters. Where required configuration parameters
                               are not present, defaults are taken from the
                               operator configuration.
        """
        log.debug("Executing GLEAM model generation")
        vis_list = pickle.loads(codecs.decode(vis_pickle.encode(), "base64"))
        advice = pickle.loads(codecs.decode(advice_pickle.encode(), "base64"))
        npixel = advice['npixel']
        cellsize = advice['cellsize']
        gleam_model = []
        for vis in vis_list:
            gleam_model.append(
                create_low_test_image_from_gleam(
                    npixel=npixel,
                    frequency=[vis.frequency[0]],
                    channel_bandwidth=[vis.channel_bandwidth[0]],
                    cellsize=cellsize,
                    phasecentre=vis.phasecentre,
                    polarisation_frame=PolarisationFrame("stokesI"),
                    flux_limit=api.config.flux_limit,
                    applybeam=True))
        pickled = codecs.encode(pickle.dumps(gleam_model), "base64").decode()
        api.send("output", pickled)

    api.add_shutdown_handler(lambda: log.info(
        "Shutting down GLEAM model generation operator"))
    api.set_port_callback(["inputvis", "inputadvice"], execute)


try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)
