import numpy as np
import math
from matplotlib.pyplot import plot, show, quiver
import matplotlib.pyplot as plt

def samplePoints(equations, pointList, sampleRate):
    sampledTimes = []
    sampledXPoints = []
    sampledYPoints = []
    sampledThetaPoints = []

    pointTimeList = []

    for i in range(0, len(pointList)):
        pointTimeList.append(pointList[i][0])

    # print("TIMES: ", pointTimeList)

    xEquations = equations[0]
    yEquations = equations[1]
    thetaEquations = equations[2]

    currentEquationIndex = 0

    for i in range(sampleRate * pointList[-1][0]):
        time = (i)/(sampleRate)

        for i in range(0, len(pointTimeList) - 1):
            if(time >= pointTimeList[i] and time <= pointTimeList[i+1]):
                currentEquationIndex = i
                break

        currentXEquation = xEquations[i * 6: (i * 6) + 6]
        currentYEquation = yEquations[i * 6: (i * 6) + 6]
        currentThetaEquation = thetaEquations[i * 6: (i * 6) + 6]

        sampledX = currentXEquation[0] + (currentXEquation[1] * time) + (currentXEquation[2] * (time ** 2)) + (currentXEquation[3] * (time ** 3)) + (currentXEquation[4] * (time ** 4)) + (currentXEquation[5] * (time ** 5))
        sampledY = currentYEquation[0] + (currentYEquation[1] * time) + (currentYEquation[2] * (time ** 2)) + (currentYEquation[3] * (time ** 3)) + (currentYEquation[4] * (time ** 4)) + (currentYEquation[5] * (time ** 5))
        sampledTheta = currentThetaEquation[0] + (currentThetaEquation[1] * time) + (currentThetaEquation[2] * (time ** 2)) + (currentThetaEquation[3] * (time ** 3)) + (currentThetaEquation[4] * (time ** 4)) + (currentThetaEquation[5] * (time ** 5))

        sampledXPoints.append(sampledX)
        sampledYPoints.append(sampledY)
        sampledThetaPoints.append(sampledTheta)

        sampledTimes.append(time)

    sampledXVelocities = [0]
    sampledYVelocities = [0]

    for i in range(1, len(sampledXPoints)):
        sampledXVelocities.append((sampledXPoints[i] - sampledXPoints[i - 1])/(1/sampleRate))
        sampledYVelocities.append((sampledYPoints[i] - sampledYPoints[i - 1])/(1/sampleRate))

    print("TIMES: ", sampledTimes)
    print("X: ", sampledXPoints)
    print("Y: ", sampledYPoints)
    print("Theta: ", sampledThetaPoints)

    # plot(sampledXPoints, sampledYPoints)
    print(len(sampledXPoints))
    print(len(sampledYPoints))
    print(len(sampledXVelocities))
    print(len(sampledYVelocities))

    sampledXArray = np.array(sampledXPoints)
    sampledYArray = np.array(sampledYPoints)

    # totalPoints = []

    # for x, y in zip(sampledXPoints, sampledYPoints):
    #     totalPoints.append([x, y])

    # print("TOTAL POINTS: ", totalPoints)

    print("XVEL: ", sampledXVelocities)

    plot(sampledXArray, sampledYArray)
    # quiver(sampledXArray, sampledYArray, sampledXVelocities, sampledYVelocities)
    plt.xlim([-20, 20])
    plt.ylim([-20, 20])
    show()

def generateSplineCurves(points):
    overallSysEqArray = []
    xArray = []
    yArray = []
    thetaArray = []
    overallOutputArray = []

    size = (len(points) - 1) * 6
    print(size)
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
    print(overallSysEqArray)
    print("XMATRIX: ", xArray)
    # print("Y LENGTH: ", len(yArray))

    overallSysEqArray = np.array(overallSysEqArray)

    xMatrix = np.array(xArray)
    yMatrix = np.array(yArray)
    thetaMatrix = np.array(thetaArray)

    M = np.linalg.inv(overallSysEqArray)

    xCoefficients = np.matmul(M, xMatrix)
    yCoefficients = np.matmul(M, yMatrix)
    thetaCoefficients = np.matmul(M, thetaMatrix)

    print("X COEF:", xCoefficients)

    samplePoints([xCoefficients, yCoefficients, thetaCoefficients], pointList, 50)

# list is as follows [time, x, y, theta, xVel, yVel, thetaVel, xAccel, yAccel, thetaAccel]
pointList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, math.pi/4, 3, 1.5, math.pi/4, 0, 0, 0], [2, 6, 3, math.pi/2, 3.5, -0.75, 0, 0, 0, 0], [3, 8, 0, (3/4) * math.pi, 2, 4.5, 0, 0, 0, 0], [4, 10, 12, (3/4) * math.pi, 2, 5, 0, 0, 0, 0], [5, 10, 10, (3/4) * math.pi, 0, 0, 0, 0, 0, 0]]
generateSplineCurves(pointList)
