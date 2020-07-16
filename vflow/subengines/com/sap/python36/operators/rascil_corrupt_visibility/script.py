import pickle
from rascil.workflows.serial.simulation.simulation_serial import (
    corrupt_list_serial_workflow)


def wrapper(api):
    log = api.logger
    log.info("Starting visibility corruption operator")

    def execute(vis_pickle):
        log.debug("Executing visibility corruption")
        vis_list = pickle.loads(vis_pickle)
        corrupted_vislist = corrupt_list_serial_workflow(
            vis_list,
            phase_error=api.config.phase_error)
        api.send("output", pickle.dumps(corrupted_vislist))

    #api.add_shutdown_handler(lambda: log.info(
        #"Shutting down visibility corruption operator"))

    api.set_port_callback("input", execute)

# ////////////////////////////////////////////////////////

try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)
