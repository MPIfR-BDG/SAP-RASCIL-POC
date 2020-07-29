import time

num_of_vis = 0
counter = 0
time_start = 0

def set_num_of_vis(numofvis):
    global num_of_vis
    global counter
    global time_start
    num_of_vis = numofvis
    counter = 0
    time_start = time.time()

def on_input(vis):
    global num_of_vis
    global counter
    global time_start
    counter += 1
    if counter == num_of_vis:
        time_lapse = time.time() - time_start
        api.send("output","processed {} visibilities in {} seconds".format(num_of_vis,time_lapse))
        
api.set_port_callback("numofvis",set_num_of_vis)
api.set_port_callback("input",on_input)