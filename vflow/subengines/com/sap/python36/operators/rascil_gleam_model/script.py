import pickle
import numpy as np
from rascil.data_models.polarisation import PolarisationFrame
from rascil.processing_components.imaging import advise_wide_field
from rascil.processing_components.simulation import (
    create_low_test_image_from_gleam)

log = api.logger
log.info("Starting GLEAM model generation operator")

def execute(rascil_pickle):
    """
    @brief   Create a visibility set based on the operator configuration

    @param   config_json   A JSON string containing optional configuration
                           parameters. Where required configuration parameters
                           are not present, defaults are taken from the
                           operator configuration.
    """
    log.debug("Executing GLEAM model generation")
    rascil_data = pickle.loads(rascil_pickle)
    vis_list = rascil_data["visibilities"]
    wprojection_planes = api.config.wprojection_planes

    advice_low = advise_wide_field(
        vis_list[0], guard_band_image=8.0, delA=0.02,
        wprojection_planes=wprojection_planes)

    advice_high = advise_wide_field(
        vis_list[-1], guard_band_image=8.0, delA=0.02,
        wprojection_planes=wprojection_planes)

    vis_slices = advice_low['vis_slices']
    npixel = advice_high['npixels2']
    cellsize = min(advice_low['cellsize'], advice_high['cellsize'])

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
                flux_limit=1.0,
                applybeam=True))
    message = {
        "metadata": {
            "visibility_slices": vis_slices,
            "cellsize": cellsize,
        },
            "images": gleam_model,
            "visibilities": vis_list
        }
    api.send("output", pickle.dumps(message))

api.add_shutdown_handler(lambda: log.info(
    "Shutting down GLEAM model generation operator"))
api.set_port_callback("input", execute)
