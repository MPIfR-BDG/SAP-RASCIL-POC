import pickle

log = api.logger
log.info("Starting image comparison operator")

def execute(image1_pickle, image2_pickle):
    log.debug("Executing image comparison")
    image1 = pickle.loads(image1_pickle)
    image2 = pickle.loads(image1_pickle)
    api.send("output", pickle.dumps({"comparison": None}))

api.add_shutdown_handler(lambda: log.info(
    "Shutting down image comparison operator"))
api.set_port_callback(["image1", "image2"], execute)
