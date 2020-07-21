import pickle
from rascil.data_models.polarisation import PolarisationFrame
from rascil.processing_components.imaging import create_image_from_visibility


def wrapper(api):

    log = api.logger
    log.info("Starting model creation operator")


    def execute(vis_pickle, advice_pickle):
        log.debug("Executing model creation")
        vis_list = pickle.loads(vis_pickle)
        advice = pickle.loads(advice_pickle)
        vis_slices = advice['vis_slices']
        npixel = advice['npixel']
        cellsize = advice['cellsize']
        model_list = []
        for vis in vis_list:
            model_list.append(
                create_image_from_visibility(
                    vis,
                    npixel=npixel,
                    frequency=[vis.frequency[0]],
                    channel_bandwidth=[vis.channel_bandwidth[0]],
                    cellsize=cellsize,
                    phasecentre=vis.phasecentre,
                    polarisation_frame=PolarisationFrame("stokesI")
                )
            )
        api.send("output", pickle.dumps(model_list))


    api.add_shutdown_handler(lambda: log.info(
        "Shutting down model creation operator"))
    api.set_port_callback(["inputvis", "inputadvice"], execute)


# ////////////////////////////////////////////////////////

try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)
