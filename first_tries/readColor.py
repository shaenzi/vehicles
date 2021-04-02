import board
import busio
import adafruit_apds9960.apds9960
import time

i2c = busio.I2C(board.SCL, board.SDA)

i2c.init(board.SCL, board.SDA, 400000) #last argument is frequency

#i2c.scan returns 57, which is 0x39, which is the address of the sensor on the bus

sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

sensor.enable_color = True

def convert_color(rLSB, gLSB, bLSB, cLSB):
    #convert the color readings from 2-byte values to 2⁸ for RGB
    #and percentage for brightness

    rRGB = rLSB>>8
    gRGB = gLSB>>8
    bRGB = bLSB>>8
    cPercent = cLSB / 2**16 *100

    return rRGB, gRGB, bRGB, cPercent

#wait until sensor is ready
time.sleep(2)

i = 0
while (i<10):
    r, g, b, c = sensor.color_data
    r,g,b,c = convert_color(r,g,b,c)
    print('Red: {0}, Green: {1}, Blue: {2}, Clear: {3}'.format(r, g, b, c))
    i +=1
    time.sleep(2)
