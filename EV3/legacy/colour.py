import ev3dev.ev3 as ev3
import time

c = ev3.ColorSensor('in2')
#c.mode = 'COL-COLOR' #light up all LEDs
#c.mode = 'COL-REFLECT' #LEDs off

colours = ["none", "black", "blue", "green",
		"yellow", "red", "white", "brown"]

while True:
	print(colours[c.color])
	time.sleep(0.2)
	print(c.reflected_light_intensity)
	time.sleep(0.2)
