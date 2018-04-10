import random
import math
import csv
import sys

f = open('Iris.csv', 'r')
reader = csv.reader(f)
SAMPLES = list()
firstline = False

for row in reader:
    if firstline:
        example = list()
        example.append(float(row[1]))
        example.append(float(row[2]))
        example.append(float(row[3]))
        example.append(float(row[4]))
        example.append(row[5])
        SAMPLES.append(example)

    if not firstline:
        firstline = True

f.close()

SAMPLE_POINT = list()
NUM_CLUSTERS = 3
TOTAL_DATA = len(SAMPLES)
for i in range(NUM_CLUSTERS):
    SAMPLE_POINT.append(random.randint(1,150))

BIG_NUMBER = math.pow(10, 10)

# SAMPLES = [[1.0, 1.0], [1.5, 2.0], [3.0, 4.0], [5.0, 7.0], [3.5, 5.0], [4.5, 5.0], [3.5, 4.5]]

data = []
data2 = []
centroids = []


class DataPoint:
    def __init__(self, x, y, z, q):
        self.x = x
        self.y = y
        self.z = z
        self.q = q

    def set_q(self, q):
        self.q = q

    def get_q(self):
        return self.q

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def set_z(self, z):
        self.z = z

    def get_z(self):
        return self.z

    def set_cluster(self, clusterNumber):
        self.clusterNumber = clusterNumber

    def get_cluster(self):
        return self.clusterNumber


class Centroid:
    def __init__(self, x, y, z, q):
        self.x = x
        self.y = y
        self.z = z
        self.q = q

    def set_q(self, q):
        self.q = q

    def get_q(self):
        return self.q


    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def set_z(self, z):
        self.z = z

    def get_z(self):
        return self.z

def initialize_centroids():
    # Set the centoid coordinates to match the data points furthest from each other.
    print("Centroids initialized at:")
    for i in range(NUM_CLUSTERS):
        centroids.append(Centroid(SAMPLES[SAMPLE_POINT[i]][0], SAMPLES[SAMPLE_POINT[i]][1], SAMPLES[SAMPLE_POINT[i]][2], SAMPLES[SAMPLE_POINT[i]][3]))
        print("(",SAMPLES[i], ")")
    print("After centroids are initialized")
    print()
    return


def initialize_datapoints():
    for i in range(TOTAL_DATA):
        newPoint = DataPoint(SAMPLES[i][0], SAMPLES[i][1], SAMPLES[i][2], SAMPLES[i][3])

        for j in range(NUM_CLUSTERS):
            if i == SAMPLE_POINT[j]:
                newPoint.set_cluster(j)
            else:
                newPoint.set_cluster(None)
        data.append(newPoint)

    return


def get_orig_cluster():
    for i in range(TOTAL_DATA):
        newPoint = DataPoint(SAMPLES[i][0], SAMPLES[i][1], SAMPLES[i][2],SAMPLES[i][3])

        if SAMPLES[i][4] == 'Iris-setosa':
            newPoint.set_cluster(0)
        elif SAMPLES[i][4] == 'Iris-versicolor':
            newPoint.set_cluster(1)
        elif SAMPLES[i][4] == 'Iris-virginica':
            newPoint.set_cluster(2)
        else:
            newPoint.set_cluster(None)
        data2.append(newPoint)

    return


def get_distance(dataPointX, dataPointY, dataPointZ, dataPointQ, centroidX, centroidY, centroidZ, centroidQ):
    # Calculate Euclidean distance.
    return math.sqrt(math.pow((centroidY - dataPointY), 2) + math.pow((centroidX - dataPointX), 2) + math.pow((centroidZ - dataPointZ), 2)  + math.pow((centroidQ - dataPointQ), 2))


def recalculate_centroids():
    totalX = 0
    totalY = 0
    totalZ = 0
    totalQ = 0
    totalInCluster = 0
    convergence=100

    for j in range(NUM_CLUSTERS):
        for k in range(len(data)):
            if (data[k].get_cluster() == j):
                totalX += data[k].get_x()
                totalY += data[k].get_y()
                totalZ += data[k].get_z()
                totalQ += data[k].get_q()
                totalInCluster += 1

        if (totalInCluster > 0):
            old_x = centroids[j].get_x()
            old_y = centroids[j].get_y()
            old_z = centroids[j].get_z()
            old_q = centroids[j].get_q()
            centroids[j].set_x(totalX / totalInCluster)
            centroids[j].set_y(totalY / totalInCluster)
            centroids[j].set_z(totalZ / totalInCluster)
            centroids[j].set_q(totalQ / totalInCluster)
            convergence = old_x - centroids[j].get_x() + old_y - centroids[j].get_y() + old_z - centroids[j].get_z() + old_q - centroids[j].get_q()

        totalInCluster = 0
        totalX = 0
        totalY = 0
        totalZ = 0
        totalQ = 0

    return convergence


def update_clusters():

    for i in range(TOTAL_DATA):
        bestMinimum = BIG_NUMBER
        currentCluster = 0

        for j in range(NUM_CLUSTERS):
            distance = get_distance(data[i].get_x(), data[i].get_y(), data[i].get_z(), data[i].get_q(), centroids[j].get_x(), centroids[j].get_y(),centroids[j].get_z(),centroids[j].get_q())
            if distance < bestMinimum:
                bestMinimum = distance
                currentCluster = j

        data[i].set_cluster(currentCluster)

        if data[i].get_cluster() is None or data[i].get_cluster() != currentCluster:
            data[i].set_cluster(currentCluster)
            print("Something is Wrong!")
    return


def perform_kmeans():
    cnt =1
    initialize_centroids()
    initialize_datapoints()
    convergence = recalculate_centroids()
    update_clusters()
    convergence=100

    while convergence > 0.000001:
        convergence = recalculate_centroids()
        update_clusters()
        cnt +=1
    print("For Convergence the centroid was shifted ", cnt, " Times.")
    return


def print_results():
    for i in range(NUM_CLUSTERS):
        count = 0
        print("Cluster includes :")
        print(i)
        for j in range(TOTAL_DATA):
            if data[j].get_cluster() == i:
                print("(", data[j].get_x(), ", ", data[j].get_y(),  ", ", data[j].get_z(),  ", ", data[j].get_q(), ")")
                count += 1
            else:
                flag = 1
        print(count)
    return


def print_orig_results():
    for i in range(NUM_CLUSTERS):
        count = 0
        print("Cluster includes :")
        print(i)
        j = 0
        for j in range(TOTAL_DATA):
            if data2[j].get_cluster() == i:
                print("(", data2[j].get_x(), ", ", data2[j].get_y(), ", ", data2[j].get_z(), ", ", data2[j].get_q(), ")")
                count += 1
            else:
                a = 0
        a = 0
        print(count)
    return


def compare_results():

    misclassified = 0
    total = 0
    edge1 = 0
    edge2 = 0
    for i in range(TOTAL_DATA):
        for j in range(i):
            if i == j:
                a = 0
            else:
                if data[i].get_cluster() == data[j].get_cluster():
                    edge1 = 1
                else:
                    edge1 = 0
                if data2[i].get_cluster() == data2[j].get_cluster():
                    edge2 = 1
                else:
                    edge2 = 0
            if edge1 == edge2:
                total += 1
            else:
                total += 1
                misclassified +=1

    error_rate = misclassified/total
    error_rate = error_rate * 100
    print("Misclassified : ", misclassified, "Total Edges : ", total)
    print("Error by Hamming Distance for Clustering Algorithm is: ", error_rate)
    return


if __name__== "__main__":
    perform_kmeans()
    print_results()
    get_orig_cluster()
    print_orig_results()
    compare_results()