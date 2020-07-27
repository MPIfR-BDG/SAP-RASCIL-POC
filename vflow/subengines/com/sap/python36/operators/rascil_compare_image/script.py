import pickle
import codecs

def wrapper(api):
    log = api.logger
    log.info("Starting image comparison operator")

    def execute(image1_pickle, image2_pickle):
        log.debug("Executing image comparison")
        image1 = pickle.loads(codecs.decode(image1_pickle.encode(), "base64"))
        image2 = pickle.loads(codecs.decode(image2_pickle.encode(), "base64"))
        pickled = codecs.encode(pickle.dumps({"comparison": None}), "base64").decode()
        api.send("output", pickled)

    api.add_shutdown_handler(lambda: log.info(
        "Shutting down image comparison operator"))
    api.set_port_callback(["image1", "image2"], execute)


# ////////////////////////////////////////////////////////

try:
    api
except NameError:
    if __name__ == "__main__":
        print("Error: No api object found")
else:
    wrapper(api)
