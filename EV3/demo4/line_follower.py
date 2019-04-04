import time
from environment import Environment
env = Environment()
# based on line_follow_holo2.py
# more object-oriented

# to use this just:

# from line_follow_tank2 import LineFollower
# lf = LineFollower()
# lf.run()

class LineFollower():
    def __init__(self, robot):
        self.robot = robot
        self.motortime = 1000
        self.speed = 2.5
        self.turning_direction = 1 #1 = left, 2 = right
        self.flag = True
        self.offline = 0
        self.left_adjust = 0
        self.right_adjust = 0
    
    def change_turn_direction(self):
        if (self.turning_direction == 1):
            self.turning_direction = 2
        else:
            self.turning_direction = 1
    
    def turn(self, speed):
        # Turn for 0.1s and a bit more for smoothness
        if (self.turning_direction == 1):
            self.robot.rotate_left(speed * 100, duration = 100)
        else:
            self.robot.rotate_right(speed * 100, duration = 100)

    def target_sensed(self):
        return self.robot.line_detected() or self.robot.color_detected()
        #return self.robot.line_detected();

    def find_line(self, iterations = 3):
        # If first attempt, set iteration to 3 for minor changes on a straight line

        # Turn one way first
        for i in range(iterations):
            while self.robot.way_blocked():
                self.robot.stop()
            if self.target_sensed():
                return
            self.turn(self.speed)
            time.sleep(0.1)

        # Turn opposite direction, past original angle
        self.change_turn_direction()

        for i in range(iterations * 2):
            while self.robot.way_blocked():
                self.robot.stop()
            if self.target_sensed():
                return
            self.turn(self.speed)
            time.sleep(0.1)

        # Back to original angle
        self.change_turn_direction()

        for i in range(iterations):
            while self.robot.way_blocked():
                self.robot.stop()
            if self.target_sensed():
                return
            self.turn(self.speed)
            time.sleep(0.1)

        # Increase search space
        self.find_line(iterations + 2)

    def iteration(self, a_speed = env.moving_speed_slow, steer_rate = env.steer_rate_normal):
        # if (self.robot.way_blocked()):
        #     self.robot.stop()
        #     return
        
        detected_R = self.robot.line_detected_right()
        detected_M = self.robot.line_detected_middle()
        detected_L = self.robot.line_detected_left()

        if (not (detected_R or detected_M or detected_L)):
            self.offline = self.offline + 1
            #print("unfind", self.offline)
            self.find_line()
        elif (detected_L):
            #self.left_adjust = self.left_adjust + 1
            #print("left adjust", self.left_adjust)
            self.robot.steer_left(speed = a_speed, steer_rate = steer_rate)
        elif (detected_R):
            #self.right_adjust = self.right_adjust + 1
            #print("right adjust", self.right_adjust)
            self.robot.steer_right(speed = a_speed, steer_rate = steer_rate)
        elif (detected_M):
            self.robot.straight_line_moving(speed = a_speed)
        else:
            # shouldn't be triggered
            pass

    def run(self):
        while True:
            try:
                self.iteration()
            except Exception as e:
                print(e)
                pass