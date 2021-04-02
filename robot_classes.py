import board
import busio
import adafruit_apds9960.apds9960
from gpiozero import Robot


class BasicVehicle():
    def __init__(self):
        pass
        # TODO: have a robot class here, evaluate it at regular intervals

    def start_timer(self):
        pass

    def stop_timer(self):
        pass

class Vehicle(BasicVehicle):
    def __init__(self, type):
        self.type = type
        # TODO add stuff for different types 

    def stop(self):
        pass

    def start(self):
        pass

    def quit(self):
        pass

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
        self.motors = Robot(left=(7,8), right=(9,10))


    def read(self):
        self.proximity = self.sensor.proximity  # very close is 255, far away is 0, and it's not at all linear
        r, g, b, c = self.sensor.color_data
        self.r, self.g, self.b, self.c = self._convert_color(r,g,b,c)
        # brightness: 0 is dark, the brighter the higher

    def print_sensor_values(self):
        print(f'proximity: {self.proximity}, brightness: {self.c}')
    
    def set(self):
        pass
        # TODO: set motor speeds
    
    def _convert_color(self, rLSB, gLSB, bLSB, cLSB):
        #convert the color readings from 2-byte values to 2⁸ for RGB
        #and percentage for brightness

        rRGB = rLSB>>8
        gRGB = gLSB>>8
        bRGB = bLSB>>8
        cPercent = cLSB / 2**16 *100

        return rRGB, gRGB, bRGB, cPercent
