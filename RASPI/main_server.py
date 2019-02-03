from flask import Flask
from flask import request
import time
import test_client as tc
app = Flask(__name__)

# the queue holds multiple orders
queue = []

# a queue structure holding the next instructions for the robot
commands = []

# get commands from file and load into commands
def get_commands(n):
    f = open('commands')
    lines = f.readlines()
    f.close()

    line = lines[n]
    data = line.split(',')
    commands = data    
    
# send a message to the robot depending on the command
def move_robot(c):
    if c == 'f':
        tc.send_message('follow_line_until_intersection')
    if c == 'r':
        tc.send_message('turn_right')
    if c == 'l':
        tc.send_message('turn_left')
    if c == 't':
        tc.send_message('turn_around')

# :)
@app.route('/')
def hello_world():
   return 'This is group 13\'s web server for the their robot, no touchy touchy'


# Endpoint for the connection from the app
@app.route('/APP/', methods=['POST'])
def APP():
   data = request.form.get('seat')

   # verify data is of type int
   try:
    data = int(data)
   except:
    data = 0

   # don't give invalid seat values
   data = data % 6

   # verify data is not Nonetype (already check but just to be safe)
   if data is not None:

      # add seat to queue
      queue.append(data)

      # if there are no commands in the command queue get the next set of commands
      if len(commands) == 0:
        get_commands(data)
      return "success!"
   return "failure!"

# Endpoint for connections from the EV3
@app.route('/EV3/', methods=['POST'])# finishes an action
def EV3():
   # Check the command queue is non-empty
   if len(commands) > 0:
    move_robot(command[0])
    commands.pop(0)
   else:
    # when debugging stops crash if queue is empty
    try:
        queue.pop(0)
        if len(queue) > 0:
            get_commands(queue[0])
    except:
        return "failure"
    
   return "received"

# run the flask app
if __name__ == '__main__':
   app.run('0.0.0.0', port=80)
