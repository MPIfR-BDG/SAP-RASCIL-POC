import pickle
from rascil.data_models.polarisation import PolarisationFrame
from rascil.processing_components.imaging import  create_image_from_visibility


log = api.logger
log.info("Starting model creation operator")


def execute(rascil_pickle):
    log.debug("Executing model creation")
    data = pickle.loads(rascil_pickle)
    vis_list = data["visibilities"]
    model_list = []
    for vis in vis_list:
        model_list.append(
            create_image_from_visibility(
                vis,
                npixel=npixel,
                frequency=[vis.frequency[0]],
                channel_bandwidth=[vis.channel_bandwidth[0]],
                cellsize=data["cellsize"],
                phasecentre=vis.phasecentre,
                polarisation_frame=PolarisationFrame("stokesI")
            )
        )
    message = {
        "metadata": {},
        "images": model_list,
        "visibilities": vis_list
    }
    api.send("output", pickle.dumps(data))

api.add_shutdown_handler(lambda: log.info(
    "Shutting down model creation operator"))
api.set_port_callback("input", execute)
