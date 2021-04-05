import time
import board
import busio
import adafruit_apds9960.apds9960
from gpiozero import Motor


from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        # self.start()  # do not want it to start automatically

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class BasicVehicle():
    def __init__(self):
        self.time_interval = 0.2  #s
        self.rt = RepeatedTimer(self.time_interval, self.__evaluate)
        self.robot = LowLevelRobot()

    def start(self):
        self.rt.start()

    def stop(self):
        self.rt.stop()
        self.robot.stop()  # otherwise robot continues with last values set

    def __evaluate(self):
        self.robot.read()
        left_value, right_value = self.__sensor_to_motor_logic()  # not sure whether it would be better to save these values?
        self.robot.set(left_value, right_value)

    def __sensor_to_motor_logic(self):
        # currently: go forward slowly
        return 0.4, 0.4
        # this is specific for each vehicle! i.e. subclass needs to over-write this


class VehicleX(BasicVehicle):
    # first try at having sensor logic: stop if too close or dark

    def __sensor_to_motor_logic(self):
        if (self.robot.proximity > 150) or (self.robot.c < 5):
            return 0, 0
        else:
            return 0.4, 0.4


class LowLevelRobot:
    # do not call the class Robot as the 
    def __init__(self):
        # initialise i2c and sensor
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.i2c.init(board.SCL, board.SDA, 400000) #last argument is frequency
        #i2c.scan returns 57, which is 0x39, which is the address of the sensor on the bus
        self.sensor = adafruit_apds9960.apds9960.APDS9960(self.i2c)
        self.sensor.enable_color = True
        self.sensor.enable_proximity = True

        # initialise robot
        self.left_motor = Motor(9, 10)
        self.right_motor = Motor(7, 8)
        self.left_value = 0
        self.right_value = 0

    def read(self):
        self.proximity = self.sensor.proximity  # very close is 255, far away is 0, and it's not at all linear
        r, g, b, c = self.sensor.color_data
        self.r, self.g, self.b, self.c = self._convert_color(r,g,b,c)
        # brightness: 0 is dark, the brighter the higher

    def print_sensor_values(self):
        print(f'proximity: {self.proximity}, brightness: {self.c}')
    
    def set(self, left_value, right_value):
        self.left_value = left_value
        self.right_value = right_value
        self.left_motor.forward(left_value)
        self.right_motor.forward(right_value)
        # theoretically, values between 0 and 1 are possible, but wheel does not turn below 0.4
        # also possible: backward, reverse, stop

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def start(self):
        self.set(self.left_value, self.right_value)
    
    def _convert_color(self, rLSB, gLSB, bLSB, cLSB):
        #convert the color readings from 2-byte values to 2⁸ for RGB
        #and percentage for brightness

        rRGB = rLSB>>8
        gRGB = gLSB>>8
        bRGB = bLSB>>8
        cPercent = cLSB / 2**16 *100

        return rRGB, gRGB, bRGB, cPercent
