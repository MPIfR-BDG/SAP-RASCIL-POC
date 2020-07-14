import pickle
from rascil.workflows.serial.simulation.simulation_serial import (
    corrupt_list_serial_workflow)

log = api.logger
log.info("Starting visibility corruption operator")

def execute(rascil_pickle):
    log.debug("Executing visibility corruption")
    data = pickle.loads(rascil_pickle)
    corrupted_vislist = corrupt_list_serial_workflow(
        data["visibilities"], 
        phase_error=api.config.phase_error)
    message = data
    message["visibilities"] = corrupted_vislist
    api.send("output", pickle.dumps(message))


api.add_shutdown_handler(lambda: log.info(
    "Shutting down visibility corruption operator"))
api.set_port_callback("input", execute)
