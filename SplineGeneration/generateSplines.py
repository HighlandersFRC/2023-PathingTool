import numpy as np
import math
from matplotlib.pyplot import plot, show, quiver
import matplotlib.pyplot as plt
import time

class SplineGenerator:
    def __init__(self):
        self.xCoefficients = []
        self.yCoefficients = []
        self.thetaCoefficients = []

        self.xVelCoefficients = []
        self.yVelCoefficients = []
        self.thetaVelCoefficients = []

        self.xAccelCoefficients = []
        self.yAccelCoefficients = []
        self.thetaAccelCoefficients = []

    def sample(self, pointList, sample_time):
        pointTimeList = []

        for i in range(0, len(pointList)):
            pointTimeList.append(pointList[i].time)
        
        index = 0
        for j in range(0, len(pointTimeList) - 1):
            if(sample_time >= pointTimeList[j] and sample_time <= pointTimeList[j + 1]):
                index = j
                break

        currentXEquation = self.xCoefficients[index * 6: (index * 6) + 6]
        currentYEquation = self.yCoefficients[index * 6: (index * 6) + 6]
        currentThetaEquation = self.thetaCoefficients[index * 6: (index * 6) + 6]

        sampledX = currentXEquation[0] + (currentXEquation[1] * sample_time) + (currentXEquation[2] * (sample_time ** 2)) + (currentXEquation[3] * (sample_time ** 3)) + (currentXEquation[4] * (sample_time ** 4)) + (currentXEquation[5] * (sample_time ** 5))
        sampledY = currentYEquation[0] + (currentYEquation[1] * sample_time) + (currentYEquation[2] * (sample_time ** 2)) + (currentYEquation[3] * (sample_time ** 3)) + (currentYEquation[4] * (sample_time ** 4)) + (currentYEquation[5] * (sample_time ** 5))
        sampledTheta = currentThetaEquation[0] + (currentThetaEquation[1] * sample_time) + (currentThetaEquation[2] * (sample_time ** 2)) + (currentThetaEquation[3] * (sample_time ** 3)) + (currentThetaEquation[4] * (sample_time ** 4)) + (currentThetaEquation[5] * (sample_time ** 5))

        # # plot(sampledXPoints, sampledYPoints)
        # print(len(sampledXPoints))
        # print(len(sampledYPoints))
        # print(len(sampledXVelocities))
        # print(len(sampledYVelocities))

        # totalPoints = []

        # for x, y in zip(sampledXPoints, sampledYPoints):
        #     totalPoints.append([x, y])

        # print("TOTAL POINTS: ", totalPoints)

        # print("XVEL: ", sampledXVelocities)

        # show()
        return [sampledX, sampledY, sampledTheta]

    # def get_exceeded_max_intervals(self, key_points, max_lin_vel, max_lin_accel, max_ang_vel, max_ang_accel):
    #     lin_vel_coefficients = np.polyadd(np.polymul(self.xVelCoefficients, self.xVelCoefficients), np.polymul(self.yVelCoefficients, self.yVelCoefficients))
    #     lin_accel_coefficients = np.polyadd(np.polymul(self.xAccelCoefficients, self.xAccelCoefficients), np.polymul(self.yAccelCoefficients, self.yAccelCoefficients))
    #     lin_vel_coefficients[0] -= max_lin_vel ** 2
    #     lin_accel_coefficients[0] -= max_lin_accel ** 2
    #     lin_vel_roots = list(np.roots(lin_vel_coefficients))
    #     lin_accel_roots = list(np.roots(lin_accel_coefficients))
    #     lin_vel_roots = [float(r) for r in lin_vel_roots if np.isreal(r)]
    #     lin_accel_roots = [float(r) for r in lin_accel_roots if np.isreal(r)]

    def sample_lin_vel(self, key_points: list, time: float):
        index = 0
        for i in range(len(key_points) - 1):
            if time >= key_points[i].time and time <= key_points[i + 1].time:
                index = i
                break
        y_vel_coefficients = np.flip(self.yVelCoefficients[index * 6: index * 6 + 6])
        x_vel_coefficients = np.flip(self.xVelCoefficients[index * 6: index * 6 + 6])
        lin_vel_coefficients = np.polyadd(np.polymul(x_vel_coefficients, x_vel_coefficients), np.polymul(y_vel_coefficients, y_vel_coefficients))
        return math.sqrt(float(np.polyval(lin_vel_coefficients, time)))

    def generateSplineCurves(self, points):
        overallSysEqArray = []
        xArray = []
        yArray = []
        thetaArray = []
        overallOutputArray = []

        size = (len(points) - 1) * 6
        # print(size)
        # print(overallSysEqArray)
        for i in range(len(points) - 1):
            currentPoint = points[i]
            nextPoint = points[i+1]
            
            startPad = [0 for j in range(0, i * 6)]

            # if(i == len(points) - 2):
            firstPointEq = startPad + [1, currentPoint[0], currentPoint[0] ** 2, currentPoint[0] ** 3, currentPoint[0] ** 4, currentPoint[0] ** 5]
            secondPointEq = startPad + [1, nextPoint[0], nextPoint[0] ** 2, nextPoint[0] ** 3, nextPoint[0] ** 4, nextPoint[0] ** 5]
            firstVelEq = startPad + [0, 1,  2 * currentPoint[0], 3 * (currentPoint[0] ** 2), 4 * (currentPoint[0] ** 3), 5 * (currentPoint[0] ** 4)]
            secondVelEq = startPad + [0, 1,  2 * nextPoint[0], 3 * (nextPoint[0] ** 2), 4 * (nextPoint[0] ** 3), 5 * (nextPoint[0] ** 4)]
            firstAccelEq = startPad + [0, 0, 0, 6, 24 * currentPoint[0], 60 * (currentPoint[0] ** 2)]
            secondAccelEq = startPad + [0, 0, 0, 6, 24 * nextPoint[0], 60 * (nextPoint[0] ** 2)]

            firstEndPad = [0 for j in range(0, size - len(firstPointEq))]
            secondEndPad = [0 for j in range(0, size - len(secondPointEq))]
            firstVelEndPad = [0 for j in range(0, size - len(firstVelEq))]
            secondVelEndPad = [0 for j in range(0, size - len(secondVelEq))]
            firstAcelEndPad = [0 for j in range(0, size - len(firstAccelEq))]
            secondAcelEndPad = [0 for j in range(0, size - len(secondAccelEq))]

            overallSysEqArray.append(firstPointEq + firstEndPad)
            overallSysEqArray.append(secondPointEq + secondEndPad)
            overallSysEqArray.append(firstVelEq + firstVelEndPad)
            overallSysEqArray.append(secondVelEq + secondVelEndPad)
            overallSysEqArray.append(firstAccelEq + firstAcelEndPad)
            overallSysEqArray.append(secondAccelEq + secondAcelEndPad)
            
            xArray.append(currentPoint[1])
            xArray.append(nextPoint[1])
            xArray.append(currentPoint[4])
            xArray.append(nextPoint[4])
            xArray.append(currentPoint[7])
            xArray.append(nextPoint[7])

            yArray.append(currentPoint[2])
            yArray.append(nextPoint[2])
            yArray.append(currentPoint[5])
            yArray.append(nextPoint[5])
            yArray.append(currentPoint[8])
            yArray.append(nextPoint[8])

            thetaArray.append(currentPoint[3])
            thetaArray.append(nextPoint[3])
            thetaArray.append(currentPoint[6])
            thetaArray.append(nextPoint[6])
            thetaArray.append(currentPoint[9])
            thetaArray.append(nextPoint[9])

            # if(i <= len(points) - 3):
            #     snapEndPad = [0 for j in range(0, size - len(secondAccelEq))]
            #     overallSysEqArray.append(secondAccelEq + snapEndPad)
            #     # print("SNAP: ", len(secondAccelEq + snapEndPad))
            #     print("SNAP: ", secondAccelEq + snapEndPad)
            #     xArray.append(0)
            #     yArray.append(0)
            #     thetaArray.append(0)

        # print(len(overallSysEqArray))
        # print(overallSysEqArray)
        # print("XMATRIX: ", xArray)
        # print("Y LENGTH: ", len(yArray))

        overallSysEqArray = np.array(overallSysEqArray)

        xMatrix = np.array(xArray)
        yMatrix = np.array(yArray)
        thetaMatrix = np.array(thetaArray)

        M = np.linalg.inv(overallSysEqArray)

        xCoefficients = np.matmul(M, xMatrix)
        yCoefficients = np.matmul(M, yMatrix)
        thetaCoefficients = np.matmul(M, thetaMatrix)

        # print("X COEF:", xCoefficients)

        
        # # define the time interval
        # time_interval = np.linspace(0, 1, num=50)

        # # calculate the x velocities
        # x_velocities = np.polyval(self.xCoefficients[1:], time_interval)

        # # print the results
        # print("X velocities: ", x_velocities)

        # sampledPoints = samplePoints([xCoefficients, yCoefficients, thetaCoefficients], points, 50)

        # return sampledPoints
        self.xCoefficients = xCoefficients
        self.yCoefficients = yCoefficients
        self.thetaCoefficients = thetaCoefficients

        xCoefficients = np.flip(xCoefficients)
        yCoefficients = np.flip(yCoefficients)
        thetaCoefficients = np.flip(thetaCoefficients)

        self.xVelCoefficients = np.polyder(xCoefficients)
        self.yVelCoefficients = np.polyder(yCoefficients)
        self.thetaVelCoefficients = np.polyder(thetaCoefficients)

        self.xAccelCoefficients = np.polyder(self.xVelCoefficients)
        self.yAccelCoefficients = np.polyder(self.yVelCoefficients)
        self.thetaAccelCoefficients = np.polyder(self.thetaVelCoefficients)

        self.xVelCoefficients = np.flip(self.xVelCoefficients)
        self.yVelCoefficients = np.flip(self.yVelCoefficients)
        self.thetaVelCoefficients = np.flip(self.thetaVelCoefficients)

        self.xAccelCoefficients = np.flip(self.xAccelCoefficients)
        self.yAccelCoefficients = np.flip(self.yAccelCoefficients)
        self.thetaAccelCoefficients = np.flip(self.thetaAccelCoefficients)

        # plt.plot([i / 100 for i in range(100)], [float(np.polyval(np.flip(self.xCoefficients), i / 100)) for i in range(100)], color = (1, 0, 0, 1))
        # plt.plot([i / 100 for i in range(100)], [float(np.polyval(np.flip(self.xVelCoefficients), i / 100)) for i in range(100)], color = (0, 1, 0, 1))
        # plt.plot([i / 100 for i in range(100)], [float(np.polyval(np.flip(self.xAccelCoefficients), i / 100)) for i in range(100)], color = (0, 0, 1, 1))
        # plt.show()

    # # list is as follows [sample_time, x, y, theta, xVel, yVel, thetaVel, xAccel, yAccel, thetaAccel]
    # pointList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, math.pi/4, 3, 1.5, math.pi/4, 0, 0, 0], [2, 6, 3, math.pi/2, 3.5, -0.75, 0, 0, 0, 0], [3, 8, 0, (3/4) * math.pi, 2, 4.5, 0, 0, 0, 0], [4, 10, 12, (3/4) * math.pi, 2, 5, 0, 0, 0, 0], [5, 10, 10, (3/4) * math.pi, 0, 0, 0, 0, 0, 0]]
    # pointList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, -1, 0, 1, 1, 0, 0, 0, 0], [2, 4, 8, 0, 2, 2, 0, 0, 0, 0], [3, 6, 2, 0, 1, 1, 0, 0, 0, 0]]
    # generateSplineCurves(pointList)
