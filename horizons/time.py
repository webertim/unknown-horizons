import time

TIME_STEP = 1/8
t = time.time()

def time():
    return t

def step():
    global t
    t += TIME_STEP