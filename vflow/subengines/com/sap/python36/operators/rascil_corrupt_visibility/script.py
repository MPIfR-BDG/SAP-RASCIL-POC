import pickle
from rascil.workflows.serial.simulation.simulation_serial import (
    corrupt_list_serial_workflow)

log = api.logger
log.info("Starting visibility corruption operator")


def execute(data_pickle):
    log.debug("Executing visibility corruption")
    data = pickle.loads(data_pickle)
    corrupted_vislist = corrupt_list_serial_workflow(
        data["predicted_vislist"], 
        phase_error=api.config.phase_error)
    data["corrupted_vislist"] = corrupted_vislist
    api.send("output", pickle.dumps(data))


api.add_shutdown_handler(lambda: log.info(
    "Shutting down visibility corruption operator"))
api.set_port_callback("input", execute)
