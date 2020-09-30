#!/usr/bin/env python
import numpy as np
from scipy.linalg import norm


def flatten(data_list, list_element_type=int):
	"""
	flatten a list containg inner lists
	Input
	=====
				data_list : list containing inner list
				list_element_type : element dtype in the (inner) list (int, float, str)
	Return
	======
				a flattened list
	>>> lst = [ [0, [3,4],[5,6,7]], 1, [2,9]]
	>>> print (flatten(lst))
	>>> [0,3,4,5,6,7,1,2,9]
	>>> lst = [['BA', ['NA','RM']],'FI',['MI','TO']]
	>>> print(flatten(lst, str))
	>>> ['BA', 'NA', 'RM', 'FI', 'MI', 'TO']
	"""

	lst = []
	#check if the list contains inner lists. If not then return the original list
	if all([isinstance(elt, ist_element_type) for elt in data_list])== True:
		return data_list
	else:
		for elt in data_list:
			#append to the list if elt not a list (int, float)
			if isinstance(elt, ist_element_type) == True:
				lst.append(elt)
			else:
				#loop through the inner list
				inner_list = elt
				for inner_elt in inner_list:
					#append to the list if inner elt not a list
					if isinstance(inner_elt, ist_element_type) == True:
						lst.append(inner_elt)
					else:
						#loop through the inner inner list and append its element to the lst
						for inner_inner_elt in inner_elt:
							lst.append(inner_inner_elt)
    			
	return lst
    
                     
def fclusters(labels, clusters):
	"""
	Return the cluster for which the label belongs to.
	Here labels are mapped to integers from 0 to lenght of the labels
	Input
	=====
		labels : list containing labels
		clusters : list containing clusters represented by integers
	>>> clusters = [[0, [3, 4]], 1, [2, 5]] # [['BA', ['NA','RM']],'FI',['MI','TO']]
	>>> labels = ['BA', 'FI', 'MI', 'NA', 'RM', 'TO']
	>>> print(fclusters(labels, clusters))
	>>> [1. 2. 3. 1. 1. 3.]
	"""
	m = len(clusters)
	n = len(labels)
	if m>n:
		raise ValueError("cluster length can not be greater than label lenght")
	label_indices = np.zeros(n)
	for i in range(m):
		tmp_data = []
		tmp_data.append(clusters[i])
		clusters_i = flatten(tmp_data)
		label_indices[clusters_i] = i+1
	return label_indices

def hac(data, labels, kclusters):
	"""
	This is an O(n^2) hierarchical agglomerative cluster algorithm using single-linkage, i.e the minimum distance between elements in the clusters.
	Input
	=====
		data : a n by n symmetric matrix, e.g., representing distances
		labels : The initial set of clusters, i.e, it contains n clustres (each point considered as its own cluster)		
		kclusters : number of clusters <= n.
	Return
	======
		labels/clusters obtained after kclusters iterations 
		
	"""
	while len(labels) > kclusters:
		#find the minimum distance of two clusters
		val = np.min( data[ np.nonzero(data) ] )
		#locate indices of the best two clusters 
		indices = np.where( data==val )
		#select positions of the two clusters
		indx1, indx2 = indices[0][0], indices[1][0]
		#compute the minimum distance (single-linkage) between elements of the new merged cluster and the other remaining old ones.This includes the distances between the elements in the new cluster
		mergedist = np.min( data[ [indx1, indx2] ], axis=0 )
		#remove one the distance between elements of the new cluster.This is usually zero at mergedist[indx2] or mergedist[indx1]
		mergedist = np.delete( mergedist, indx2 )
		#remove row and column associated with one of the chosen cluster
		reduced = np.delete( np.delete(data, indx2, axis=0), indx2, axis=1)
		#update the distance matrix by inserting the new computed distances between elements in the new cluster and the old clusters	
		reduced[indx1] = mergedist
		reduced[:, indx1] = mergedist
		data = reduced
		#merging clusters as one clusters and delete one of them.
		labels[indx1] = [labels[indx1]] + [labels[indx2]]
		#print indx1, indx2				#(labels[indx1],) + (labels[indx2],)
		del labels[indx2]
		
	return labels
if __name__=='__main__':
	
	ItalyDistances = [
		[  0, 662, 877, 255, 412, 996],
		[662,   0, 295, 468, 268, 400],
		[877, 295,   0, 754, 564, 138],
		[255, 468, 754,   0, 219, 869],
		[412, 268, 564, 219,   0, 669],
		[996, 400, 138, 869, 669,   0]]
	mat_dist = np.array(ItalyDistances)
	#labels = ['BA','FI','MI','NA','RM','TO']
	labels = list(range(6))
	kclusters = 3
	oldlabels = np.copy(labels)
	clusters = hac(mat_dist, labels, kclusters)
	print ('hierarchical agglomerative clustering', clusters)
	print ('find clusters', fclusters(, clusters))
	
	

