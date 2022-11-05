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

    quiver(sampledXArray, sampledYArray, sampledXVelocities, sampledYVelocities)
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
        if(i == 0):
            xArray.append(0)
            yArray.append(0)
            thetaArray.append(0)
            startPad = [0 for j in range(0, i * 6)]
            # eq = startPad + [0, 1, 2 * currentPoint[0], 3 * (currentPoint[0] ** 2)]
            eq = startPad + [0, 1, 2 * currentPoint[0], 3 * (currentPoint[0] ** 2), 4 * (currentPoint[0] ** 3), 5 * (currentPoint[0] ** 4)]
            # eq = startPad + [0, 1, 0, 0]
            firstEndPad = [0 for j in range(0, (size - len(eq)))]
            overallSysEqArray.append(eq + firstEndPad)
            print("ORIGINAL SLOPE: ", eq + firstEndPad)
            # overallSysEqArray[((i) * 4)][(i) * 4:((i) * 4)+4] = eq
        
        startPad = [0 for j in range(0, i * 6)]

        if(i == len(points) - 2):
            firstEq = startPad + [1, currentPoint[0], currentPoint[0] ** 2, currentPoint[0] ** 3, currentPoint[0] ** 4, currentPoint[0] ** 5]
            secondEq = startPad + [1, nextPoint[0], nextPoint[0] ** 2, nextPoint[0] ** 3, nextPoint[0] ** 4, nextPoint[0] ** 5]
            velocityEq = startPad + [0, 1,  2 * nextPoint[0], 3 * (nextPoint[0] ** 2), 4 * (nextPoint[0] ** 3), 5 * (nextPoint[0] ** 4)]
            accelerationEq = startPad + [0, 0,  2, 6 * (nextPoint[0]), 12 * (nextPoint[0] ** 2), 20 * (nextPoint[0] ** 3)]
            jerkEq = startPad + [0, 0, 0, 6, 24 * nextPoint[0], 60 * (nextPoint[0] ** 2)]
        else:
            firstEq = startPad + [1, currentPoint[0], currentPoint[0] ** 2, currentPoint[0] ** 3, currentPoint[0] ** 4, currentPoint[0] ** 5]
            secondEq = startPad + [1, nextPoint[0], nextPoint[0] ** 2, nextPoint[0] ** 3, nextPoint[0] ** 4, nextPoint[0] ** 5]
            velocityEq = startPad + [0, 1,  2 * nextPoint[0], 3 * (nextPoint[0] ** 2), 4 * (nextPoint[0] ** 3), 5 * (nextPoint[0] ** 4), 0, -1,  -2 * nextPoint[0], -3 * (nextPoint[0] ** 2), -4 * (nextPoint[0] ** 3), -5 * (nextPoint[0] ** 4)]
            accelerationEq = startPad + [0, 0,  2, 6 * (nextPoint[0]), 12 * (nextPoint[0] ** 2), 20 * (nextPoint[0] ** 3), 0, 0,  -2, -6 * (nextPoint[0]), -12 * (nextPoint[0] ** 2), -20 * (nextPoint[0] ** 3)]
            jerkEq = startPad + [0, 0, 0, 6, 24 * nextPoint[0], 60 * (nextPoint[0] ** 2), 0, 0, 0, -6, -24 * nextPoint[0], -60 * (nextPoint[0] ** 2)]
        snapEq = startPad + [0, 0, 0, 0, 24, 120 * nextPoint[0], 0, 0, 0, 0, -24, -120 * nextPoint[0]]

        firstEndPad = [0 for j in range(0, size - len(firstEq))]
        secondEndPad = [0 for j in range(0, size - len(secondEq))]
        velEndPad = [0 for j in range(0, size - len(velocityEq))]
        accEndPad = [0 for j in range(0, size - len(accelerationEq))]
        jerkEndPad = [0 for j in range(0, size - len(jerkEq))]

        overallSysEqArray.append(firstEq + firstEndPad)
        overallSysEqArray.append(secondEq + secondEndPad)
        overallSysEqArray.append(velocityEq + velEndPad)
        overallSysEqArray.append(accelerationEq + accEndPad)
        overallSysEqArray.append(jerkEq + jerkEndPad)
        
        # print("FIRST: ", len(firstEq + firstEndPad))
        # print("SECOND: ", len(secondEq + secondEndPad))
        # print("VEL: ", len(velocityEq + velEndPad))
        # print("ACC: ", len(accelerationEq + accEndPad))
        # print("JERK: ", len(jerkEq + jerkEndPad))
        
        print("FIRST: ", (firstEq + firstEndPad))
        print("SECOND: ", (secondEq + secondEndPad))
        print("VEL EQ: ", velocityEq + velEndPad)
        print("ACC EQ: ", accelerationEq + accEndPad)
        print("JERK EQ: ", jerkEq + jerkEndPad)
        
        xArray.append(currentPoint[1])
        xArray.append(nextPoint[1])
        xArray.append(0)
        xArray.append(0)
        xArray.append(0)

        yArray.append(currentPoint[2])
        yArray.append(nextPoint[2])
        yArray.append(0)
        yArray.append(0)
        yArray.append(0)

        thetaArray.append(currentPoint[3])
        thetaArray.append(nextPoint[3])
        thetaArray.append(0)
        thetaArray.append(0)
        thetaArray.append(0)

        if(i <= len(points) - 3):
            snapEndPad = [0 for j in range(0, size - len(snapEq))]
            overallSysEqArray.append(snapEq + snapEndPad)
            # print("SNAP: ", len(snapEq + snapEndPad))
            print("SNAP: ", snapEq + snapEndPad)
            xArray.append(0)
            yArray.append(0)
            thetaArray.append(0)

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

    samplePoints([xCoefficients, yCoefficients, thetaCoefficients], pointList, 10)

# pointList = [[1, 1, 2, 0], [1.5, 3, 1, math.pi/4], [2, 5, 4, math.pi/2], [3, 8, 0, (3/4) * math.pi]]

pointList = [[0, 0, 0, 0], [1, 1, 1, math.pi/4], [2, 4, 4, math.pi/2]]#, [3, 8, 0, (3/4) * math.pi], [4, 10, 12, (3/4) * math.pi], [5, 10, 10, (3/4) * math.pi], [6, 9, 15, (3/4) * math.pi]]
generateSplineCurves(pointList)