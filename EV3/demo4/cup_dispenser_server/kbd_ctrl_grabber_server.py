from server import cup_dispenser

cp = cup_dispenser()

print("Started")

cp.initialise()

while True:
    input()
    cp.grab_and_down()