import ev3dev.ev3 as ev3
import time
from robot import Robot

# based on line_follow_holo2.py
# more object-oriented

# to use this just:

# from line_follow_tank2 import LineFollower
# lf = LineFollower()
# lf.run()

class LineFollower():
    def __init__(self):
        self.robot = Robot()
        self.motortime = 1000
        self.speed = 5
        self.turning_direction = 1 #1 = left, 2 = right

    def forward(self):
        for i in range(int(self.motortime / 100)):
            if self.robot.way_blocked():
                self.robot.stop()
                time.sleep(0.2)
                i = i - 1
            else:
                self.robot.straight_line_moving(-self.speed * 100, duration = 120)

    def left_turn(self, speed, t):
        self.robot.rotate_left(speed * 100, duration = t)

    def right_turn(self, speed, t):
        self.robot.rotate_right(speed * 100, duration = t)
    
    def turn(self):
        # Turn for 0.1s and a bit more for smoothness
        if (self.turning_direction == 1):
            self.left_turn(self.speed, 160)
        else:
            self.right_turn(self.speed, 160)
    
    def change_turn_direction(self):
        if (self.turning_direction == 1):
            self.turning_direction = 2
        else:
            self.turning_direction = 1

    def find_line(self, iterations = 5):
        # If first attempt, set iteration to 3 for minor changes on a straight line
        
        # Turn one way first
        for i in range(iterations):
            while self.robot.way_blocked():
                self.robot.stop()
            if (self.robot.line_detected()):
                return
            self.turn()
            time.sleep(0.1)
        
        # Turn opposite direction, past original angle
        self.change_turn_direction()
        
        for i in range(iterations * 2):
            while self.robot.way_blocked():
                self.robot.stop()
            if (self.robot.line_detected()):
                return
            self.turn()
            time.sleep(0.1)
        
        # Back to original angle
        self.change_turn_direction()
        
        for i in range(iterations):
            while self.robot.way_blocked():
                self.robot.stop()
            if (self.robot.line_detected()):
                return
            self.turn()
            time.sleep(0.1)

        # Increase search space
        self.find_line(iterations + 10)


    def run(self):
        while True:
            try:
                if (not self.robot.line_detected()):
                    self.find_line()
                self.forward()

            except Exception as e:
                print(e)
                pass

lineFollower = LineFollower()
lineFollower.run()
