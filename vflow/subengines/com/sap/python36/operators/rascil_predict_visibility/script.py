import pickle
from rascil.workflows.serial.imaging.imaging_serial import (
    predict_list_serial_workflow)

log = api.logger
log.info("Starting visibility prediction operator")


def execute(vis_pickle, model_pickle, advice_pickle):
    log.debug("Executing visibility prediction")
    vis_list = pickle.loads(vis_pickle)
    model_list = pickle.loads(model_pickle)
    advice = pickle.loads(advice_pickle)
    predicted_vislist = predict_list_serial_workflow(
        vis_list, 
        model_list,  
        context='wstack', 
        vis_slices=advice["vis_slices"])
    api.send("output", pickle.dumps(predicted_vislist))


api.add_shutdown_handler(lambda: log.info(
    "Shutting down visibility prediction operator"))
api.set_port_callback(["inputvis", "inputmodel", "inputadvice"], execute)
