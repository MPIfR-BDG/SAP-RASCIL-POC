import json
import pickle
import codecs
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
    log.info("Starting deconvolution operator")

    def execute(image_pickle, psf_pickle, model_pickle):
        log.debug("Executing deconvolution")
        image_list = pickle.loads(codecs.decode(image_pickle.encode(), "base64"))
        psf_list = pickle.loads(codecs.decode(psf_pickle.encode(), "base64"))
        model_list = pickle.loads(codecs.decode(model_pickle.encode(), "base64"))
        deconvolved = deconvolve_list_serial_workflow(
            image_list,
            psf_list,
            model_imagelist=model_list,
            deconvolve_facets=api.config.deconvolve_facets,
            deconvolve_overlap=api.config.deconvolve_overlap,
            deconvolve_taper=api.config.deconvolve_taper,
            scales=api.config.scales,
            algorithm=api.config.algorithm,
            niter=api.config.niter,
            fractional_threshold=api.config.fractional_threshold,
            threshold=api.config.threshold,
            gain=api.config.gain,
            psf_support=api.config.psf_support)
        pickled = codecs.encode(pickle.dumps(deconvolved), "base64").decode()
        api.send("output", pickled)

    api.add_shutdown_handler(lambda: log.info(
        "Shutting down deconvolution operator"))
    api.set_port_callback(["inputimage", "inputpsf", "inputmodel"], execute)


try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)
