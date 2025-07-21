from codrone_edu.drone import *
import time
import datetime

drone = Drone()
drone.pair()

def log_time(action):
    timestamp = time.time()
    return timestamp

drone.takeoff()
drone.set_trim(-3, 1)
start_time = log_time("start")

for x in range(0, 4, 1):
    drone.set_pitch(40)                       
    drone.move(4)
    drone.set_pitch(0)
    drone.set_roll(-30)
    drone.move(2)
    drone.set_roll(0)
    drone.set_pitch(-40)               
    drone.move(3)
    drone.set_pitch(0)
    drone.set_roll(-30)
    2
    drone.move(2)
    drone.set_roll(0)

drone.land()
end_time = log_time("end")

print(f"flight time: {end_time - start_time:.6f} segundos-")


drone.close()
