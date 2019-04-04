from cup_server import cup_dispenser

cp = cup_dispenser()

print("Started")

cp.initialise()
cp.grab_open_more()

while True:
    input()
    cp.grab_close_more()
    cp.grab_and_down()
    cp.grab_open_more()
