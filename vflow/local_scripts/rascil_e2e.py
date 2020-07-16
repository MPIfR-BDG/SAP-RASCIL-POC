import json
import pickle
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from rascil.processing_components.visibility import (
    convert_blockvisibility_to_visibility as convert_bvis_to_vis)
from rascil.workflows.serial.simulation.simulation_serial import (
    simulate_list_serial_workflow)
from rascil.processing_components.imaging import advise_wide_field
from rascil.data_models.polarisation import PolarisationFrame
from rascil.processing_components.simulation import (
    create_low_test_image_from_gleam)
from rascil.workflows.serial.imaging.imaging_serial import (
    predict_list_serial_workflow)
from rascil.workflows.serial.imaging.imaging_serial import invert_list_serial_workflow
from rascil.data_models.polarisation import PolarisationFrame
from rascil.processing_components.imaging import create_image_from_visibility
from rascil.workflows.serial.simulation.simulation_serial import (
    corrupt_list_serial_workflow)
from rascil.workflows.serial.imaging.imaging_serial import deconvolve_list_serial_workflow

def pickle_to_file(obj, filename):
    f = open(filename, "wb")
    pickle.dump(obj, f)
    f.close()

antenna_configuration = "LOWBD2"
frequency_hi_hz = 120000000
frequency_low_hz = 100000000
max_radius = 300
n_frequency_windows = 7
n_time_steps = 5
phasecentre_dec_deg = -60
phasecentre_epoch = "J2000"
phasecentre_frame = "icrs"
phasecentre_ra_deg = 30

frequency = np.linspace(
    frequency_low_hz,
    frequency_hi_hz,
    n_frequency_windows)
bw = (frequency[1] - frequency[0])
channel_bandwidth = np.ones(n_frequency_windows) * bw
times = np.linspace(-np.pi / 3.0, np.pi / 3.0, n_time_steps)
phasecentre = SkyCoord(
    ra=phasecentre_ra_deg * u.deg,
    dec=phasecentre_dec_deg * u.deg,
    frame=phasecentre_frame,
    equinox=phasecentre_epoch)
bvis_list = simulate_list_serial_workflow(
    antenna_configuration,
    frequency=frequency,
    channel_bandwidth=channel_bandwidth,
    times=times,
    phasecentre=phasecentre,
    order="frequency",
    rmax=max_radius,
    format="blockvis")
vis_list = [convert_bvis_to_vis(bv) for bv in bvis_list]

##### artifact 1: serialized vis_list #########
pickle_to_file(vis_list,"vislist.pickle")
###############################################

delA = 0.02
guard_band_image = 8
wprojection_planes = 1

wprojection_planes = wprojection_planes
advice_low = advise_wide_field(
    vis_list[0],
    guard_band_image=guard_band_image,
    delA=delA,
    wprojection_planes=wprojection_planes)
advice_high = advise_wide_field(
    vis_list[-1],
    guard_band_image=guard_band_image,
    delA=delA,
    wprojection_planes=wprojection_planes)
advice = {
    "vis_slices": advice_low['vis_slices'],
    "npixel": advice_high['npixels2'],
    "cellsize": min(advice_low['cellsize'], advice_high['cellsize'])
}

##### artifact 2: serialized advice ###########
pickle_to_file(advice,"advice.pickle")
###############################################

flux_limit = 1

vis_slices = advice['vis_slices']
npixel = advice['npixel']
cellsize = advice['cellsize']
gleam_model_list = []
for vis in vis_list:
    gleam_model_list.append(
        create_low_test_image_from_gleam(
            npixel=npixel,
            frequency=[vis.frequency[0]],
            channel_bandwidth=[vis.channel_bandwidth[0]],
            cellsize=cellsize,
            phasecentre=vis.phasecentre,
            polarisation_frame=PolarisationFrame("stokesI"),
            flux_limit=flux_limit,
            applybeam=True))

##### artifact 3: serialized gleam model list #####
pickle_to_file(gleam_model_list,"gleam_model_list.pickle")
###################################################


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

##### artifact 4: serialized model list #####
pickle_to_file(model_list,"model_list.pickle")
############################################################


predicted_vislist = predict_list_serial_workflow(
    vis_list,
    gleam_model_list,
    context='wstack',
    vis_slices=advice["vis_slices"])

##### artifact 5: serialized predicted visibility list #####
pickle_to_file(predicted_vislist,"predicted_vislist.pickle")
############################################################


dopsf=False
image_list = invert_list_serial_workflow(
    predicted_vislist,
    model_list,
    context='wstack',
    vis_slices=advice["vis_slices"],
    dopsf=dopsf)

##### artifact 6: serialized image list #####
pickle_to_file(image_list,"image_list.pickle")
############################################################


dopsf=True
psf_list = invert_list_serial_workflow(
    predicted_vislist,
    model_list,
    context='wstack',
    vis_slices=advice["vis_slices"],
    dopsf=dopsf)

##### artifact 7: serialized psf list #####
pickle_to_file(psf_list,"psf_list.pickle")
############################################################

phase_error=1
corrupted_vislist = corrupt_list_serial_workflow(
    predicted_vislist,
    phase_error=phase_error)

##### artifact 8: serialized corrupted vis list #####
pickle_to_file(corrupted_vislist,"corrupted_vislist.pickle")
############################################################


dopsf=False
corrupted_image_list = invert_list_serial_workflow(
    corrupted_vislist,
    model_list,
    context='wstack',
    vis_slices=advice["vis_slices"],
    dopsf=dopsf)

##### artifact 9: serialized corrupted image list ##########
pickle_to_file(corrupted_image_list,"corrupted_image_list.pickle")
############################################################


algorithm = "msclean"
deconvolve_facets = 8
deconvolve_overlap = 16
deconvolve_taper = "tukey"
fractional_threshold = 0.1
gain = 0.1
niter = 1000
psf_support = 64
scales = [0,3,10]
threshold = 0.1

deconvolved_image_list = deconvolve_list_serial_workflow(
    dirty_list=image_list,
    psf_list=psf_list,
    model_imagelist=model_list,
    deconvolve_facets=deconvolve_facets,
    deconvolve_overlap=deconvolve_overlap,
    deconvolve_taper=deconvolve_taper,
    scales=scales,
    algorithm=algorithm,
    niter=niter,
    fractional_threshold=fractional_threshold,
    threshold=threshold,
    gain=gain,
    psf_support=psf_support)

##### artifact 10: serialized deconvolved image list ##########
pickle_to_file(deconvolved_image_list,"deconvolved_image_list.pickle")
############################################################


deconvolved_corrupted_image_list = deconvolve_list_serial_workflow(
    dirty_list=corrupted_image_list,
    psf_list=psf_list,
    model_imagelist=model_list,
    deconvolve_facets=deconvolve_facets,
    deconvolve_overlap=deconvolve_overlap,
    deconvolve_taper=deconvolve_taper,
    scales=scales,
    algorithm=algorithm,
    niter=niter,
    fractional_threshold=fractional_threshold,
    threshold=threshold,
    gain=gain,
    psf_support=psf_support)

##### artifact 11: serialized deconvolved corrupted image list ##########
pickle_to_file(deconvolved_corrupted_image_list,"deconvolved_corrupted_image_list.pickle")
#########################################################################
