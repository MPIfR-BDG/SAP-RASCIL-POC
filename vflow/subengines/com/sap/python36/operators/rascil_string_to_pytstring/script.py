def on_input(data):
    api.send("output", str(data))

api.set_port_callback("input", on_input)

