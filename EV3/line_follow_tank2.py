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
        self.speed = 2.2

    def forward(self):
        for i in range(int(self.motortime / 100)):
            if self.robot.way_blocked():
                self.robot.stop()
                time.sleep(0.2)
                i = i - 1
            else:
                self.robot.straight_line_moving(speed = self.speed * 100,duration = 120)

    def left_turn(self, speed, t):
        self.robot.rotate_left(speed = speed * 100, duration = t)

    def right_turn(self, speed, t):
        self.robot.rotate_right(speed = speed * 100, duration = t)

    def find_line(self, attempts = 0):
        # Determine iteration number
        # If first attempt, set iteration to 3
        # for minor changes on a straight line
        if attempts == 0:
            iterations = 3
            attempts = 0.5
        else:
            iterations = int(attempts * 10)

        # Turn left first
        for i in range(iterations):
            while self.robot.way_blocked():
                self.robot.stop()
            if (self.robot.line_detected()):
                self.motortime = 1000
                return
            self.left_turn(self.speed + 2 * attempts, 120)
            time.sleep(0.1)

        # Back to original angle and then turn right
        for i in range(iterations * 2):
            while self.robot.way_blocked():
                self.robot.stop()
            if (self.robot.line_detected()):
                self.motortime = 1000
                return
            self.right_turn(self.speed + 2 * attempts, 120)
            time.sleep(0.1)

        # Back to original angle
        for i in range(iterations):
            while self.robot.way_blocked():
                self.robot.stop()
            if (self.robot.line_detected()):
                self.motortime = 1000
                return
            self.left_turn(self.speed + 2 * attempts, 120)
            time.sleep(0.1)

        # Increase search space
        self.find_line(attempts + 0.5)


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
