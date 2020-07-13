import pickle
from rascil.workflows.serial.imaging.imaging_serial import invert_list_serial_workflow

log = api.logger
log.info("Starting PSF creation operator")

def execute(data_pickle):
    log.debug("Executing visibility prediction")
    data = pickle.loads(data_pickle)
    psf_list = invert_list_serial_workflow(
        data["predicted_vislist"], 
        data["model_list"], 
        context='wstack',
        vis_slices=data["vis_slices"], 
        dopsf=api.config.dopsf)
    data["psf_list"] = psf_list
    api.send("output", pickle.dumps(data))

api.add_shutdown_handler(lambda: log.info(
    "Shutting down visibility prediction operator"))
api.set_port_callback("input", execute)
