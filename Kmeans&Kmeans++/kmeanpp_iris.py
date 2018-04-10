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

NUM_CLUSTERS = 3
TOTAL_DATA = len(SAMPLES)
BIG_NUMBER = math.pow(10, 10)
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

def get_distance(dataPointX, dataPointY, dataPointZ, dataPointQ, centroidX, centroidY, centroidZ, centroidQ):
    # Calculate Euclidean distance.
    return math.sqrt(math.pow((centroidY - dataPointY), 2) + math.pow((centroidX - dataPointX), 2) + math.pow(
        (centroidZ - dataPointZ), 2) + math.pow((centroidQ - dataPointQ), 2))


def set_points_first_kpp():
    cent_list = list()
    centOne = SAMPLES[148]
    centroids.append(Centroid(centOne[0], centOne[1], centOne[2], centOne[3]))
    cent_list.append(centOne)
    dist = list()
    sum_dist = 0
    cum_dist = list()
    k = 0
    for j in range(len(SAMPLES)):
        distance = math.pow(get_distance(SAMPLES[j][0], SAMPLES[j][1], SAMPLES[j][2],
                                         SAMPLES[j][3], cent_list[0][0], cent_list[0][1],
                                         cent_list[0][2], cent_list[0][3]), 2)
        dist.append(distance)
        sum_dist += distance
        cum_dist.append(sum_dist)

    rand_num = random.uniform(0, sum_dist)
    for j, p in enumerate(cum_dist):
        if rand_num < p:
            k = j
            break
    cent_list.append(SAMPLES[k])
    centroids.append(Centroid(cent_list[1][0], cent_list[1][1], cent_list[1][2], cent_list[1][3]))
    print("Centroid List: ", cent_list)

    return cent_list


def set_points_two_kpp(cent):

    cent_list = cent
    dist = list()
    sum_dist = 0
    cum_dist = list()
    for j in range(len(SAMPLES)):
        distance = list()
        min_distance = 0
        for s in range(2):
            pata_nahi = get_distance(SAMPLES[j][0], SAMPLES[j][1], SAMPLES[j][2], SAMPLES[j][3],
                                     cent_list[s][0], cent_list[s][1], cent_list[s][2], cent_list[s][3])
            distance.append(math.pow(pata_nahi, 2))

        for s in range(2):
            if s == 0:
                a = 0
            elif distance[s] < distance[s - 1]:
                min_distance = distance[s]
            else:
                min_distance = distance[s - 1]
        dist.append(min_distance)
        sum_dist += min_distance
        cum_dist.append(sum_dist)

    rand_num = random.uniform(0, sum_dist)
    for j, p in enumerate(cum_dist):
        if rand_num < p:
            k = j
            break

    print("THIS IS Centroid 3 added: ", SAMPLES[k])
    cent_list.append(SAMPLES[k])
    centroids.append(Centroid(cent_list[2][0], cent_list[2][1], cent_list[2][2], cent_list[2][3]))
    return


def initialize_datapoints():
    for row in SAMPLES:
        newPoint = DataPoint(row[0],row[1],row[2],row[3])
        if row == centroids[0]:
            newPoint.set_cluster(0)
        elif row == centroids[1]:
            newPoint.set_cluster(1)
        elif row == centroids[2]:
            newPoint.set_cluster(2)
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


def recalculate_centroids():
    totalX = 0
    totalY = 0
    totalZ = 0
    totalQ = 0
    totalInCluster = 0
    convergence = 0

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
            example_pat = old_x - centroids[j].get_x() + old_y - centroids[j].get_y() + old_z - centroids[j].get_z() + old_q - centroids[j].get_q()
            example_pat = abs(example_pat)
            convergence += example_pat
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
            distance = get_distance(data[i].get_x(), data[i].get_y(), data[i].get_z(), data[i].get_q(),centroids[j].get_x(), centroids[j].get_y(), centroids[j].get_z(),centroids[j].get_q())
            if (distance < bestMinimum):
                bestMinimum = distance
                currentCluster = j

        data[i].set_cluster(currentCluster)

        if (data[i].get_cluster() is None or data[i].get_cluster() != currentCluster):
            data[i].set_cluster(currentCluster)
            print("Exception!")

    return

def perform_kmeans():
    cnt = 1
    initialize_datapoints()
    convergence = recalculate_centroids()
    update_clusters()
    convergence=100

    while convergence > 0.0000000001:
        convergence = recalculate_centroids()
        update_clusters()
        cnt += 1
    print("For Convergence the centroid was shifted ", cnt, " Times.")
    return


def print_results():
    for i in range(NUM_CLUSTERS):
        count = 0
        print("Cluster ",i, " includes:")

        for j in range(TOTAL_DATA):
            if data[j].get_cluster() == i:
                count += 1
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
                print()
        print()
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


if __name__ == "__main__":
    cent_list = set_points_first_kpp()
    set_points_two_kpp(cent_list)
    perform_kmeans()
    print_results()
    get_orig_cluster()
    compare_results()
    print()
