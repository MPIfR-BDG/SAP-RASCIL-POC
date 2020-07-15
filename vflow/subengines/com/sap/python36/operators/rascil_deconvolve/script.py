import pickle
from rascil.workflows.serial.imaging.imaging_serial import deconvolve_list_serial_workflow

log = api.logger
log.info("Starting deconvolution operator")

def execute(vis_pickle, psf_pickle, model_pickle):
    log.debug("Executing deconvolution")
    vis_list = pickle.loads(vis_pickle)
    psf_list = pickle.loads(psf_pickle)
    model_list = pickle.loads(model_pickle)
    deconvolved = deconvolve_list_serial_workflow(
        vis_list, 
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
api.set_port_callback(["inputvis", "inputpsf", "inputmodel"], execute)
