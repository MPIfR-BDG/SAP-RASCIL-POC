import pickle
from rascil.workflows.serial.imaging.imaging_serial import (
    deconvolve_list_serial_workflow)


def wrapper(api):
    log = api.logger
    log.info("Starting deconvolution operator")

    def execute(image_pickle, psf_pickle, model_pickle):
        log.debug("Executing deconvolution")
        image_list = pickle.loads(image_pickle)
        psf_list = pickle.loads(psf_pickle)
        model_list = pickle.loads(model_pickle)
        deconvolved = deconvolve_list_serial_workflow(
            image_list,
            psf_list,
            model_imagelist=model_list,
            deconvolve_facets=api.config.deconvolve_facets,
            deconvolve_overlap=api.config.deconvolve_overlap,
            deconvolve_taper=api.config.deconvolve_taper,
            scales=api.config.scales,
            algorithm=api.config.algorithm,
            niter=api.config.niter,
            fractional_threshold=api.config.fractional_threshold,
            threshold=api.config.threshold,
            gain=api.config.gain,
            psf_support=api.config.psf_support)
        api.send("output", pickle.dumps(deconvolved))

    api.add_shutdown_handler(lambda: log.info(
        "Shutting down deconvolution operator"))
    api.set_port_callback(["inputimage", "inputpsf", "inputmodel"], execute)


try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)