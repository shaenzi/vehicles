from gpiozero import Robot
import time
import numpy as np

robby = Robot(left=(7,8), right=(9,10))

min_speed = 0.4
time_to_go_straight = 1
time_to_turn = 0.4

for n in np.arange(3):
    robby.forward(min_speed)
    time.sleep(time_to_go_straight)
    robby.right(min_speed)
    time.sleep(time_to_turn)

robby.stop()
