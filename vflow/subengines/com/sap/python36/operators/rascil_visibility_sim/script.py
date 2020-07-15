try:
    api
except NameError:
    from pyop_api_mock import api
    api.config.antenna_configuration = "LOWBD2"
    api.config.frequency_hi_hz = 120000000
    api.config.frequency_low_hz = 100000000
    api.config.max_radius = 300
    api.config.n_frequency_windows = 7
    api.config.n_time_steps = 5
    api.config.phasecentre_dec_deg = -60
    api.config.phasecentre_epoch = "J2000"
    api.config.phasecentre_frame = "icrs"
    api.config.phasecentre_ra_deg = 30

# ////////////////////////////////////////////////////////


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
        get_param("frequency_low_hz"),
        get_param("frequency_hi_hz"),
        get_param("n_frequency_windows"))
    bw = (frequency[1]-frequency[0])
    channel_bandwidth = np.ones(get_param("n_frequency_windows")) * bw
    times = np.linspace(-np.pi/3.0, np.pi/3.0, get_param("n_time_steps"))
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
    log.debug("Executing convert_bvis_to_vis")
    vis_list = [convert_bvis_to_vis(bv) for bv in bvis_list]
    log.debug("Visibility simulation complete")
    api.send("output", pickle.dumps(vis_list))


#api.add_shutdown_handler(lambda: log.info(
#    "Shutting down visibility simulation operator"))
api.set_port_callback("input", execute)


# ////////////////////////////////////////////////////////

def test() :
    print('Test: Default')
    print(api.config)
    api.test.write("input","{}") # empty json input
    while api.test.hasnext("output"):
        vis_pickle = api.test.read("output")
        vis_list = pickle.loads(vis_pickle)
        print(str(len(vis_list)))
        print(str(vis_list))
        for vis in vis_list:
            print(str(vis))

    #api.set_port_callback('input', call_on_input)
    #print('Test: config')
    #config = api.config
    #config.var1 = 'own foo'
    #config.var12 = 'own bar'
    #test_msg = api.Message(attributes={'name':'test1'},body =4)
    #new_msg = api.call(config,test_msg)
    #print('Attributes: ', new_msg.attributes)
    #print('Body: ', str(new_msg.body))

if __name__ == "__main__":
    test()
