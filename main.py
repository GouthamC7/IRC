# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
three_tenths = 0.7999849293604264
almost_three_tenths = 0.9

are_close = math.isclose(three_tenths, almost_three_tenths, abs_tol=0.1)

comparision = []
comparision.append(True)
comparision.append(False)

print(are_close)
print(all(comparision))

a = [0.1, 0.2]
b = [0.0001, 0.002]
for x,y in zip(a,b):
    print(x,y)