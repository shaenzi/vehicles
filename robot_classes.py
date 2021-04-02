import board
import busio
import adafruit_apds9960.apds9960
import time

class BasicVehicle(self):
    def __init__():
        pass
        # TODO: have a robot class here, evaluate it at regular intervals

    def start_timer():
        pass

    def stop_timer():
        pass

class Vehicle(BasicVehicle):
    def __init__(type):
        self.type = type
        # TODO add stuff for different types 

    def stop():
        pass

    def start():
        pass

    def quit():
        pass

class Robot:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.i2c.init(board.SCL, board.SDA, 400000) #last argument is frequency
        #i2c.scan returns 57, which is 0x39, which is the address of the sensor on the bus
        self.sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
        self.sensor.enable_color = True
        self.sensor.enable_proximity = True


    def read():
        self.proximity = self.sensor.proximity
        r, g, b, c = self.sensor.color_data
        self.r, self.g, self.b, self.c = self._convert_color(r,g,b,c)

    def print_values():
        print(f'proximity: {self.proximity}, brightness: {self.c}')
    
    def set():
        pass
        # TODO: set motor speeds
    
    def _convert_color(rLSB, gLSB, bLSB, cLSB):
        #convert the color readings from 2-byte values to 2⁸ for RGB
        #and percentage for brightness

        rRGB = rLSB>>8
        gRGB = gLSB>>8
        bRGB = bLSB>>8
        cPercent = cLSB / 2**16 *100

        return rRGB, gRGB, bRGB, cPercent
