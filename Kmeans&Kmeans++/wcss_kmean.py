import random
import math
import csv
import sys
import matplotlib.pyplot as plt

f = open('2d_1.csv', 'r')
reader = csv.reader(f)
SAMPLES = list()

for row in reader:
    example = list()
    example.append(float(row[1]))
    example.append(float(row[2]))
    example.append(float(row[0]))
    SAMPLES.append(example)

f.close()

SAMPLE_POINT = list()
NUM_CLUSTERS = 1
TOTAL_DATA = len(SAMPLES)
wcss_value = list()

BIG_NUMBER = math.pow(10, 10)

# SAMPLES = [[1.0, 1.0], [1.5, 2.0], [3.0, 4.0], [5.0, 7.0], [3.5, 5.0], [4.5, 5.0], [3.5, 4.5]]

data = []
centroids = []


class DataPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    def set_cluster(self, clusterNumber):
        self.clusterNumber = clusterNumber

    def get_cluster(self):
        return self.clusterNumber


class Centroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y


def initialize_centroids():

    i = 0
    if NUM_CLUSTERS == 1:
        centroids.append(Centroid(SAMPLES[SAMPLE_POINT[0]][0], SAMPLES[SAMPLE_POINT[0]][1]))
    else:
        for i in range(NUM_CLUSTERS):
            centroids.append(Centroid(SAMPLES[SAMPLE_POINT[i]][0], SAMPLES[SAMPLE_POINT[i]][1]))

    return


def initialize_datapoints():

    for i in range(TOTAL_DATA):
        newPoint = DataPoint(SAMPLES[i][0], SAMPLES[i][1])

        for j in range(NUM_CLUSTERS):
            if i == SAMPLE_POINT[j]:
                newPoint.set_cluster(j)
            else:
                newPoint.set_cluster(None)
        data.append(newPoint)

    return


def get_distance(dataPointX, dataPointY, centroidX, centroidY):
    # Calculate Euclidean distance.
    return math.sqrt(math.pow((centroidY - dataPointY), 2) + math.pow((centroidX - dataPointX), 2))


def recalculate_centroids():
    totalX = 0
    totalY = 0
    totalInCluster = 0
    convergence = 100

    for j in range(NUM_CLUSTERS):
        for k in range(len(data)):
            if data[k].get_cluster() == j:
                totalX += data[k].get_x()
                totalY += data[k].get_y()
                totalInCluster += 1

        if totalInCluster > 0:
            old_x = centroids[j].get_x()
            old_y = centroids[j].get_y()
            centroids[j].set_x(totalX / totalInCluster)
            centroids[j].set_y(totalY / totalInCluster)
            convergence = old_x - centroids[j].get_x() + old_y - centroids[j].get_y()
        totalInCluster = 0
        totalX = 0
        totalY = 0

    return convergence


def update_clusters():

    for i in range(TOTAL_DATA):
        bestMinimum = BIG_NUMBER
        currentCluster = 0

        for j in range(NUM_CLUSTERS):
            distance = get_distance(data[i].get_x(), data[i].get_y(), centroids[j].get_x(), centroids[j].get_y())
            if distance < bestMinimum:
                bestMinimum = distance
                currentCluster = j

        data[i].set_cluster(currentCluster)

        if data[i].get_cluster() is None or data[i].get_cluster() != currentCluster:
            data[i].set_cluster(currentCluster)
            print("Something is Wrong!")

    return


def perform_kmeans():
    cnt = 1
    convergence = recalculate_centroids()
    update_clusters()
    convergence = 100

    while convergence > 0.01:
        convergence = recalculate_centroids()
        update_clusters()
        cnt += 1

    return


def get_wcss():
    sum = 0
    for i in range(NUM_CLUSTERS):
        for j in range(TOTAL_DATA):
            if data[j].get_cluster() == i:
                distance = get_distance(data[j].get_x(),data[j].get_y(),centroids[i].get_x(),centroids[i].get_y())
                sum += math.pow(distance, 2)
    wcss_value.append(sum)


if __name__ == "__main__":
    plt.xlabel('x axis ->')
    plt.ylabel('WCSS ->')

    for x in range(11):
        SAMPLE_POINT.clear()
        data.clear()
        centroids.clear()
        NUM_CLUSTERS = x + 1
        for i in range(NUM_CLUSTERS):
            SAMPLE_POINT.append(random.randint(1, 99))
        initialize_centroids()
        initialize_datapoints()
        perform_kmeans()
        get_wcss()
        print("FOR K =", x + 1, " WCSS Value is: ", wcss_value[x])

    for i in range(11):
        plt.plot(i, wcss_value[i], 'ro')

    plt.show()