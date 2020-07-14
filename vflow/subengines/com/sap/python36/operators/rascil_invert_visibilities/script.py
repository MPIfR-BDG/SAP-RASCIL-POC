import pickle
from rascil.workflows.serial.imaging.imaging_serial import invert_list_serial_workflow

log = api.logger
log.info("Starting PSF creation operator")

def execute(rascil_model_pickle, rascil_visibility_pickle):
    log.debug("Executing visibility prediction")
    model_data = pickle.loads(rascil_model_pickle)
    vis_data = pickle.loads(rascil_visibility_pickle)
    image_list = invert_list_serial_workflow(
        vis_data["visibilities"], 
        model_data["images"], 
        context='wstack',
        vis_slices=model_data["metadata"]["visibility_slices"], 
        dopsf=api.config.dopsf)
    message = {}
    message["metadata"] = {}
    message["metadata"].update(model_data["metadata"])
    message["metadata"].update(vis_data["metadata"])
    message["images"] = image_list
    api.send("output", pickle.dumps(message))

api.add_shutdown_handler(lambda: log.info(
    "Shutting down visibility prediction operator"))
api.set_port_callback(["inputmodel", "inputvislist"], execute)
