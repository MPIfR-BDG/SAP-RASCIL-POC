import pickle
from rascil.workflows.serial.imaging.imaging_serial import (
    predict_list_serial_workflow)

log = api.logger
log.info("Starting visibility prediction operator")


def execute(data_pickle):
    log.debug("Executing visibility prediction")
    data = pickle.loads(data_pickle)
    predicted_vislist = predict_list_serial_workflow(
        data["vis_list"], 
        data["gleam_model"],  
        context='wstack', 
        vis_slices=data["vis_slices"])
    data["predicted_vislist"] = predicted_vislist
    api.send("output", pickle.dumps(data))


api.add_shutdown_handler(lambda: log.info(
    "Shutting down visibility prediction operator"))
api.set_port_callback("input", execute)
