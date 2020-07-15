import pickle
from rascil.processing_components.imaging import advise_wide_field

log = api.logger
log.info("Starting advise wide field operator")

def execute(vis_pickle):
    log.debug("Executing advise wide field")
    vis_list = pickle.loads(vis_pickle)
    
    wprojection_planes = api.config.wprojection_planes
    advice_low = advise_wide_field(
        vis_list[0], 
        guard_band_image=api.config.guard_band_image, 
        delA=api.config.delA,
        wprojection_planes=wprojection_planes)
    advice_high = advise_wide_field(
        vis_list[-1], 
        guard_band_image=api.config.guard_band_image, 
        delA=api.config.delA,
        wprojection_planes=wprojection_planes)
    advice = {
        "low": advice_low,
        "high": advice_high,
        "vis_slices": advice_low['vis_slices'],
        "npixel": advice_high['npixels2'],
        "cellsize": min(advice_low['cellsize'], advice_high['cellsize'])
    }
    api.send("output", pickle.dumps(advice))

api.add_shutdown_handler(lambda: log.info(
    "Shutting down advise wide field operator"))
api.set_port_callback("input", execute)
