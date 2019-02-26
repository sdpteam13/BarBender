import ev3dev.ev3 as ev3
import time

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

    #def forward(self):
    #    # not used for now, remove?
    #    for i in range(int(self.motortime / 100)):
    #        if self.robot.way_blocked():
    #            self.robot.stop()
    #            time.sleep(0.2)
    #            i = i - 1
    #        else:
    #            self.robot.straight_line_moving(self.speed * 100, duration = 120)

    def left_turn(self, speed, t):
        self.robot.rotate_left(speed * 100, duration = t)

    def right_turn(self, speed, t):
        self.robot.rotate_right(speed * 100, duration = t)

    def turn(self, speed):
        # Turn for 0.1s and a bit more for smoothness
        if (self.turning_direction == 1):
            self.left_turn(speed, 100)
        else:
            self.right_turn(speed, 100)

    def change_turn_direction(self):
        if (self.turning_direction == 1):
            self.turning_direction = 2
        else:
            self.turning_direction = 1

    def target_sensed(self, intersectionColor = "green"):
        return self.robot.line_detected() or self.robot.color_detected(intersectionColor)
        #return self.robot.line_detected();

    def find_line(self, iterations = 3, intersectionColor = "green"):
        # If first attempt, set iteration to 3 for minor changes on a straight line

        # Turn one way first
        for i in range(iterations):
            while self.robot.way_blocked():
                self.robot.stop()
            if self.target_sensed(intersectionColor):
                return
            self.turn(self.speed)
            time.sleep(0.1)

        # Turn opposite direction, past original angle
        self.change_turn_direction()

        for i in range(iterations * 2):
            while self.robot.way_blocked():
                self.robot.stop()
            if self.target_sensed(intersectionColor):
                return
            self.turn(self.speed)
            time.sleep(0.1)

        # Back to original angle
        self.change_turn_direction()

        for i in range(iterations):
            while self.robot.way_blocked():
                self.robot.stop()
            if self.target_sensed(intersectionColor):
                return
            self.turn(self.speed)
            time.sleep(0.1)

        # Increase search space
        self.find_line(iterations + 2)

    def iteration(self):
        if (self.robot.way_blocked()):
            self.robot.stop()
            return

        detected_R = self.robot.line_detected_right()
        detected_M = self.robot.line_detected_middle()
        detected_L = self.robot.line_detected_left()

        if (not (detected_R or detected_M or detected_L)):
            self.offline = self.offline + 1
            print("unfind", self.offline)
            self.find_line()

        # else:
        #     print(self.robot.gy.angle)
        #     self.robot.steer_by_degree(degrees = -self.robot.gy.angle)
        elif (detected_L):
            self.left_adjust = self.left_adjust + 1
            print("left adjust", self.left_adjust)
            #self.robot.rotate_left(80)
            self.robot.steer_left(300)
        elif (detected_R):
            self.right_adjust = self.right_adjust + 1
            print("right adjust", self.right_adjust)
            #self.robot.rotate_right(80)
            self.robot.steer_right(300)
        elif (detected_M):
            self.robot.straight_line_moving()

        else:
            # shouldn't be triggered
            pass
        
    def iteration_backwards(self, speed = 150):
        if (self.robot.way_blocked()):
            self.robot.stop()
            return

        detected_R = self.robot.line_detected_right()
        detected_M = self.robot.line_detected_middle()
        detected_L = self.robot.line_detected_left()

        if (not (detected_R or detected_M or detected_L)):
            self.offline = self.offline + 1
            print("unfind", self.offline)
            self.find_line()

        elif (detected_L):
            self.left_adjust = self.left_adjust + 1
            print("left adjust", self.left_adjust)
            self.robot.steer_left(-150)
        elif (detected_R):
            self.right_adjust = self.right_adjust + 1
            print("right adjust", self.right_adjust)
            self.robot.steer_right(-150)
        elif (detected_M):
            self.robot.straight_line_moving_backwards(speed)
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

#lf = LineFollower()
#lf.run()
