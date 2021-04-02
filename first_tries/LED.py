from gpiozero import PWMLED
import time

led = PWMLED(15)

led.value = 0.5
time.sleep(1)
led.value = 1
time.sleep(1)
led.off()

led.pulse()
time.sleep(5)
led.off()

led.blink()
time.sleep(5)
led.off()