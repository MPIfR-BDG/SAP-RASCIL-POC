import json
import pickle
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from rascil.processing_components.visibility import (
    convert_blockvisibility_to_visibility as convert_bvis_to_vis)
from rascil.workflows.serial.simulation.simulation_serial import (
    simulate_list_serial_workflow)

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
        get_param("fbottom"),
        get_param("ftop"),
        get_param("nfreqwin"))
    bw = (frequency[1]-frequency[0])
    channel_bandwidth = np.ones(get_param("nfreqwin")) * bw
    times = np.linspace(-np.pi/3.0, np.pi/3.0, get_param("ntimes"))
    phasecentre = SkyCoord(
        ra=get_param("ra") * u.deg,
        dec=get_param("deg") * u.deg,
        frame=get_param("frame"),
        equinox=get_param("epoch"))
    array_configuration = get_param("array_configuration")
    log.debug("Executing simulate_list_serial_workflow")
    bvis_list = simulate_list_serial_workflow(
        array_configuration,
        frequency=frequency,
        channel_bandwidth=channel_bandwidth,
        times=times,
        phasecentre=phasecentre,
        order="frequency",
        rmax=get_param("rmax"),
        format="blockvis")
    log.debug("Executing convert_bvis_to_vis")
    vis_list = [convert_bvis_to_vis(bv) for bv in bvis_list]
    log.debug("Visibility simulation complete")
    api.send("output", pickle.dumps(vis_list))


api.add_shutdown_handler(lambda: log.info(
    "Shutting down visibility simulation operator"))
api.set_port_callback("input", execute)
