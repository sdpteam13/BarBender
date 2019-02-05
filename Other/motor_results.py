import matplotlib.pyplot as plt

f = open('motor_results.dat','r')
lines = f.readlines()
f.close()

left = []
right = []
for line in lines:
    line = line.strip()
    l, r = line.split(' ')
    left.append(-int(l))
    right.append(-int(r))
    
time = [(i)/100.0 for i in range(len(left))]
print (left)

plt.plot(time, left,  label='left')
plt.plot(time, right, label='right')
plt.title('sum-left: ' + str(sum(left)) + ' sum-right: ' + str(sum(right)))
plt.legend()
plt.show() 
