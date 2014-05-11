__author__ = 'shabib'


from sklearn import cluster

class SubCluster:
    def __init__(self,points,clusters):
        self.dataTM = points
        self.knnTM = cluster.KMeans(clusters)
        self.waypoints =  self.knnTM.fit_predict(self.dataTM)


    def get_datapoints(self, cluster_no):
        results = []
        for i in range(len(self.waypoints)):
            if self.waypoints[i] == cluster_no:
                results.append(self.dataTM[i])
        return results


