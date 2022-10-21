import numpy as np

def generateSplineCurves(points):
    # overallSysEqArray = np.zeros(((len(points) - 1) * 4, (len(points) - 1) * 4))
    overallSysEqArray = []
    yArray = []
    size = (len(points) - 1) * 4
    # print(overallSysEqArray)
    for i in range(len(points) - 1):
        currentPoint = points[i]
        nextPoint = points[i+1]
        if(i == 0):
            yArray.append(0)
            startPad = [0 for j in range(0, i * 4)]
            eq = startPad + [0, 1, 2 * currentPoint[0], 3 * (currentPoint[0] ** 2)]
            firstEndPad = [0 for j in range(0, ((len(points) - 1) * 4) - len(eq))]
            overallSysEqArray.append(eq + firstEndPad)
            # overallSysEqArray[((i) * 4)][(i) * 4:((i) * 4)+4] = eq
        
        startPad = [0 for j in range(0, i * 4)]

        firstEq = startPad + [1, currentPoint[0], currentPoint[0] ** 2, currentPoint[0] ** 3]
        secondEq = startPad + [1, nextPoint[0], nextPoint[0] ** 2, nextPoint[0] ** 3]
        if(i == len(points) - 2):
            thirdEq = startPad + [0, 1,  2 * nextPoint[0], 3 * (nextPoint[0] ** 2)]
            print("THIRD EQ: ", thirdEq)
        else:
            thirdEq = startPad + [0 , 1, 2 * nextPoint[0], 3 * (nextPoint[0] ** 2), 0, -1, -2 * nextPoint[0], -3 * (nextPoint[0] ** 2)]
        fourthEq = [0, 0, 2, 6 * nextPoint[0], 0, 0, -2, -6 * nextPoint[0]]

        firstEndPad = [0 for j in range(0, size - len(firstEq))]
        thirdEndPad = [0 for j in range(0, size - len(thirdEq))]
        fourthEndPad = [0 for j in range(0, size - len(fourthEq))]

        overallSysEqArray.append(firstEq + firstEndPad)
        overallSysEqArray.append(secondEq + firstEndPad)
        overallSysEqArray.append(thirdEq + thirdEndPad)

        # print("FIRST: ", firstEq + firstEndPad)
        # print("SECOND: ", secondEq + firstEndPad)
        # print("THIRD: ", thirdEq + thirdEndPad)

        print("FIRST: ", len(firstEq + firstEndPad))
        print("SECOND: ", len(secondEq + firstEndPad))
        print("THIRD: ", len(thirdEq + thirdEndPad))

        yArray.append(currentPoint[1])
        yArray.append(nextPoint[1])
        yArray.append(0)

        if(i <= len(points) - 3):
            yArray.append(0)
            fourthEq = startPad + fourthEq
            fourthEndPad = [0 for j in range(0, size - len(fourthEq))]
            if(i != len(points) - 3):
                fourthEq = fourthEq + fourthEndPad
            overallSysEqArray.append(fourthEq)
            # print("FOURTH: ", fourthEq)
            print("FOURTH: ", len(fourthEq))

    print("OVERALL: " + str(overallSysEqArray) + " LENGTH: ", len(overallSysEqArray))
    print("Y MATRIX: " + str(yArray))

    overallSysEqArray = np.array(overallSysEqArray)

    yMatrix = np.array(yArray)

    # sysEqMatrix = np.array(overallSysEqArray)

    M = np.linalg.inv(overallSysEqArray)

    coefficientMatrix = np.matmul(M, yMatrix)

    print("COEFFICIENTS ", coefficientMatrix)

# pointList = [[0,0], [-10,-8], [7.68,5], [3,15], [-4, -2.743]]
# pointList = [[0,0], [1, 1], [10, 12], [17,18]]
pointList = [[0,1], [2, 2], [5, 0], [8, 0]]

generateSplineCurves(pointList)