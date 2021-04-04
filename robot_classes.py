import board
import busio
import adafruit_apds9960.apds9960
from gpiozero import Motor


class Vehicle(BasicVehicle):
    def __init__(self, type):
        self.type = type
        # TODO add stuff for different types 

    def __sensor_to_motor_logic(self):
        pass

class BasicVehicle():
    def __init__(self):
        self.time_interval = 0.2  #s
        self.logic_running = False
        self.robot = LowLevelRobot()

    def start(self):
        self.logic_running = True
        self.__evaluate()


    def stop(self):
        self.logic_running = False
        self.__evaluate()

    def __evaluate(self):
        while self.logic_running:
            self.robot.read()
            left_value, right_value = self.__sensor_to_motor_logic()  # not sure whether it would be better to save these values?
            self.robot.set(left_value, right_value)
            time.sleep(self.time_interval)

    def __sensor_to_motor_logic(self):
        # currently: go forward slowly
        return 0.4, 0.4
        # this is specific for each vehicle! i.e. subclass needs to over-write this


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

    def read(self):
        self.proximity = self.sensor.proximity  # very close is 255, far away is 0, and it's not at all linear
        r, g, b, c = self.sensor.color_data
        self.r, self.g, self.b, self.c = self._convert_color(r,g,b,c)
        # brightness: 0 is dark, the brighter the higher

    def print_sensor_values(self):
        print(f'proximity: {self.proximity}, brightness: {self.c}')
    
    def set(self, left_value, right_value):
        self.left_motor.forward(left_value)
        self.right_motor.forward(right_value)
        # also possible: backward, reverse, stop
    
    def _convert_color(self, rLSB, gLSB, bLSB, cLSB):
        #convert the color readings from 2-byte values to 2⁸ for RGB
        #and percentage for brightness

        rRGB = rLSB>>8
        gRGB = gLSB>>8
        bRGB = bLSB>>8
        cPercent = cLSB / 2**16 *100

        return rRGB, gRGB, bRGB, cPercent
