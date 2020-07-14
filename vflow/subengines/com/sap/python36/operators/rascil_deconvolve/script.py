import pickle
from rascil.workflows.serial.imaging.imaging_serial import deconvolve_list_serial_workflow

log = api.logger
log.info("Starting deconvolution operator")

def execute(rascil_vis_pickle, rasicl_psf_pickle, rasicl_model_pickle):
    log.debug("Executing deconvolution")
    vis_data = pickle.loads(rascil_vis_pickle)
    psf_data = pickle.loads(rasicl_psf_pickle)
    model_data = pickle.loads(rasicl_model_pickle)
    deconvolved = deconvolve_list_serial_workflow(
        vis_data["visibilities"], 
        psf_data["images"], 
        model_imagelist=model_data["images"], 
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
    message = {
        "metadata": {},
        "images": deconvolved
    }
    api.send("output", pickle.dumps(message))

api.add_shutdown_handler(lambda: log.info(
    "Shutting down deconvolution operator"))
api.set_port_callback(["input_vis", "input_psf", "input_model"], execute)
