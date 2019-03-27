import ev3dev.ev3 as ev3
import time

motor = ev3.LargeMotor('outC')

class drink_dispenser:
    
    def __init__(self):
        self.initialise()
        time.sleep(2)
    
    def initialise(self):
        while not motor.is_stalled:
            motor.run_timed(speed_sp=-200, time_sp=200, stop_action='brake')
    
    def open(self):
        motor.run_timed(speed_sp=250, time_sp=400)
        
    def close(self):
        motor.run_timed(speed_sp=-250, time_sp=420)
    
    def run(self):
        self.open()
        time.sleep(1)
        self.close()
        time.sleep(1)
        
        '''self.open()
        time.sleep(1)
        self.close()
        time.sleep(1)
        
        self.open()
        time.sleep(1)
        self.close()'''

if __name__ == '__main__':
    dd = drink_dispenser()
    dd.run()
