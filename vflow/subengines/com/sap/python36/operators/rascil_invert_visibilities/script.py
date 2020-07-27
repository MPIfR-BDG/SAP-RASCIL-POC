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
    log.info("Starting visibility inversion operator")

    def execute(model_pickle, vis_pickle, advice_pickle):
        log.debug("Executing visibility inversion")
        model_list = pickle.loads(codecs.decode(model_pickle.encode(), "base64"))
        vis_list = pickle.loads(codecs.decode(vis_pickle.encode(), "base64"))
        advice = pickle.loads(codecs.decode(advice_pickle.encode(), "base64"))
        image_list = invert_list_serial_workflow(
            vis_list,
            model_list,
            context='wstack',
            vis_slices=advice["vis_slices"],
            dopsf=api.config.dopsf)
        pickled = codecs.encode(pickle.dumps(image_list), "base64").decode()
        api.send("output", pickled)

    api.add_shutdown_handler(lambda: log.info(
        "Shutting down visibility inversion operator"))
    api.set_port_callback(["inputmodel", "inputvis", "inputadvice"], execute)


try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)
