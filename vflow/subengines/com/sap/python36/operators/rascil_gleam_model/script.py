import pickle
import numpy as np
from rascil.data_models.polarisation import PolarisationFrame
from rascil.processing_components.imaging import advise_wide_field
from rascil.processing_components.simulation import (
    create_low_test_image_from_gleam)

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
    vis_list = pickle.loads(vis_pickle)
    advice = pickle.loads(advice_pickle)
    vis_slices = advice['vis_slices']
    npixel = advice['npixels2']
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
    api.send("output", pickle.dumps(gleam_model))


api.add_shutdown_handler(lambda: log.info(
    "Shutting down GLEAM model generation operator"))
api.set_port_callback(["inputvis", "inputadvice"], execute)
