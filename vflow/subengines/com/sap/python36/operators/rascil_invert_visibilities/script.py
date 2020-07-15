import pickle
from rascil.workflows.serial.imaging.imaging_serial import invert_list_serial_workflow

log = api.logger
log.info("Starting PSF creation operator")

def execute(model_pickle, vis_pickle, advice_pickle):
    log.debug("Executing visibility prediction")
    model_list = pickle.loads(model_pickle)
    vis_list = pickle.loads(vis_pickle)
    advice = pickle.loads(advice_pickle)
    image_list = invert_list_serial_workflow(
        vis_list, 
        model_list, 
        context='wstack',
        vis_slices=advice["vis_slices"], 
        dopsf=api.config.dopsf)
    api.send("output", pickle.dumps(image_list))

api.add_shutdown_handler(lambda: log.info(
    "Shutting down visibility prediction operator"))
api.set_port_callback(["inputmodel", "inputvis", "inputadvice"], execute)
