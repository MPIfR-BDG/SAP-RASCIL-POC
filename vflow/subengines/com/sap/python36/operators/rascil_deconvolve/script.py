import pickle
from rascil.workflows.serial.imaging.imaging_serial import deconvolve_list_serial_workflow

log = api.logger
log.info("Starting deconvolution operator")

def execute(vis_data_pickle, psf_pickle):
    log.debug("Executing deconvolution")
    data = pickle.loads(vis_data_pickle)
    psf_list = pickle.loads(psf_pickle)
    deconvolved = deconvolve_list_serial_workflow(
        data["vis_list"], 
        psf_list, 
        model_imagelist=data["model_list"], 
        deconvolve_facets=8, 
        deconvolve_overlap=16, 
        deconvolve_taper='tukey',
        scales=[0, 3, 10],
        algorithm='msclean', 
        niter=1000, 
        fractional_threshold=0.1,
        threshold=0.1, 
        gain=0.1, 
        psf_support=64)
    api.send("output", pickle.dumps(deconvolved))

api.add_shutdown_handler(lambda: log.info(
    "Shutting down deconvolution operator"))
api.set_port_callback(["input_vis", "input_psf"], execute)
