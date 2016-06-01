from randval import randgen
# import serial

# ser = serial.Serial(port='dev/ttyACM0', baudrate=9600, timeout=1)


class UART:
    # the initializer
    def __init__(self):
        self.battempq1 = []
        self.battempq2 = []
        self.battempq3 = []
        self.battempq4 = []
        self.sensID = ['a', 'b', 'c', 'd']

    def readr(self):
        # x = ser.read()
        x = randgen()

        if x == '':
            return 'x'

        else:
            return x

    def checkr(self, value):
        if value[0] == 'a':
            self.battempq1.append(value[1:])

        elif value[0] == 'b':
            self.battempq2.append(value[1:])

        elif value[0] == 'c':
            self.battempq3.append(value[1:])

        else:
            self.battempq4.append(value[1:])


if __name__ == "__main__":
    x = UART()
    for y in range(0, 20):
        x.checkr(x.readr())
    print 'quad 1' + str(x.battempq1)
    print 'quad 2' + str(x.battempq2)
    print 'quad 3' + str(x.battempq3)
    print 'quad 4' + str(x.battempq4)
