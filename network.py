# Authors - Eddie Ozuna, Anthony Campana, Orion Cadri
import random


class NeuralNetwork:

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.correct = 200
        self.random_points = [[0]*n for _ in range(m)]
        self.t_of_h = [[0]*8 for _ in range(m)]
        self.t_of_l = [[0]*8 for _ in range(m)]
        self.createPoints()

    def createPoints(self):
        points = random.sample(range(12), 12)
        l = 0
        k = self.n
        for i in range(self.m):
            self.random_points[i] = points[l:k]
            self.random_points[i].sort()
            l = k
            k += self.n

    def setMatrices(self, array):
        self.s = [[0]*self.n for _ in range(self.m)]
        for i in range(len(self.random_points)):
            points = self.random_points[i]
            for j in range(len(points)):
                self.s[i][j] = array[points[j]]

    def train(self, array):
        self.setMatrices(array[:12])
        if array[12].lower() == 'h':
            for i in range(len(self.s)):
                index = ''.join(str(e) for e in self.s[i])
                self.t_of_h[i][self.binaryToDecimal(index)] += 1
        elif array[12].lower() == 'l':
            for i in range(len(self.s)):
                index = ''.join(str(e) for e in self.s[i])
                self.t_of_l[i][self.binaryToDecimal(index)] += 1

    def binaryToDecimal(self, n):
        return int(n, 2)

    def class_l(self, array):
        self.setMatrices(array)
        self.l_total = 0
        for i in range(len(self.s)):
            index = ''.join(str(e) for e in self.s[i])
            self.l_total += self.t_of_l[i][self.binaryToDecimal(index)]

    def class_h(self, array):
        self.setMatrices(array)
        self.h_total = 0
        for i in range(len(self.s)):
            index = ''.join(str(e) for e in self.s[i])
            self.h_total += self.t_of_h[i][self.binaryToDecimal(index)]

    def belongsTo(self, array):
        self.class_h(array[:12])
        self.class_l(array[:12])
        answer = [None, "Actual Class:", array[12],
                  "Predicted Class:", None, None]
        if self.l_total > self.h_total:
            answer[0] = array
            answer[4] = "L"
        elif self.h_total > self.l_total:
            answer[0] = array
            answer[4] = "H"
        answer[5] = True if answer[2] == answer[4] else False
        if not answer[5]:
            self.correct -= 1
        return answer

    def generateDataSet(self, t, opt):
        a = 0
        up = False
        middle = False
        if opt == 'training':
            f = open("training.txt", "w+")
        elif opt == "testing":
            f = open("testing.txt", "w+")
        k = 0
        for j in range(t):
            if j % 6 == 0:
                k = 0
            training_set = ["1", "0", "0", "1", "0",
                            "0", "1", "0", "0", "1", "1", "1"]
            if j > 6:
                training_set[k] = '0'
                if k < 9:
                    k += 3
                elif k >= 9 and k < 12:
                    k += 1
            f.write("".join(training_set))
            f.write('L')
            f.write("\n")
            if j % 11 == 0:
                a = 0
                up = False
                middle = False
            training_set = ["1", "0", "1", "1", "1",
                            "1", "1", "1", "1", "1", "0", "1"]
            training_set[a] = '0'
            if a < 9 and up != True:
                a += 3
            elif a >= 9 and a < 12 and up != True:
                a += 1
            elif a >= 2 and a <= 11 and middle != True:
                a -= 3
            elif middle == True:
                a += 3
            if a == 11:
                up = True
            if a == 2:
                a = 4
                middle = True
            f.write("".join(training_set))
            f.write('H')
            f.write("\n")
        f.close()


network = NeuralNetwork(3, 4)
# Generating the training daa set for H and L
network.generateDataSet(10, 'training')
# Generates the testing data set for H and L
network.generateDataSet(10, 'testing')
# Training Phase
with open('training.txt') as data:
    for line in data:
        sequence = [None] * (len(line) - 1)
        for i in range(len(line)-2):
            sequence[i] = int(line[i])
        sequence[12] = line[12]
        network.train(sequence)
# Testing Phase
with open('testing.txt') as data:
    for line in data:
        sequence = [None] * (len(line) - 1)
        for i in range(len(line)-2):
            sequence[i] = int(line[i])
        sequence[12] = line[12]
        print(network.belongsTo(sequence), '\n', 'Accuracy',
              (network.correct/200)*100, '%')
