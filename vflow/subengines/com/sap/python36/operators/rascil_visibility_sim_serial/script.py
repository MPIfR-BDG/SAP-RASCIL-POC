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
    log.info("Starting visibility simulation operator")

    def execute(config_json):
        """
        @brief   Create a visibility set based on the operator configuration

        @param   config_json   A JSON string containing optional configuration
                               parameters. Where required configuration parameters
                               are not present, defaults are taken from the
                               operator configuration.
        """
        config = json.loads(config_json)

        def get_param(key):
            return config.get(key, getattr(api.config, key))

        log.debug("Executing visibility simulation")
        frequency = np.linspace(
            get_param("frequency_low_hz"),
            get_param("frequency_hi_hz"),
            get_param("n_frequency_windows"))
        bw = (frequency[1] - frequency[0])
        channel_bandwidth = np.ones(get_param("n_frequency_windows")) * bw
        times = np.linspace(-np.pi / 3.0, np.pi / 3.0, get_param("n_time_steps"))
        phasecentre = SkyCoord(
            ra=get_param("phasecentre_ra_deg") * u.deg,
            dec=get_param("phasecentre_dec_deg") * u.deg,
            frame=get_param("phasecentre_frame"),
            equinox=get_param("phasecentre_epoch"))
        antenna_configuration = get_param("antenna_configuration")
        log.debug("Executing simulate_list_serial_workflow")
        bvis_list = simulate_list_serial_workflow(
            antenna_configuration,
            frequency=frequency,
            channel_bandwidth=channel_bandwidth,
            times=times,
            phasecentre=phasecentre,
            order="frequency",
            rmax=get_param("max_radius"),
            format="blockvis")
        api.send("outputsize",len(bvis_list))
        for bv in bvis_list:
            vis = convert_bvis_to_vis(bv)
            # single element list expected at the output
            vis_list = []
            vis_list.append(vis)
            pickled = codecs.encode(pickle.dumps(vis_list), "base64").decode()
            api.send("output", pickled)

    api.add_shutdown_handler(lambda: log.info(
        "Shutting down visibility simulation operator"))
    api.set_port_callback("input", execute)


try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)
