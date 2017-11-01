## Goal for this script is to compare different structural connectivity aquisitions. conn1 and conn3 and euclidean distance matrix

## import
import os.path
import pandas as pd
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

## Upload files
conn_folder_path = 'Y:/Projects/Allen-HumanAdult-OHSU/from_david/STRUCTURE_AND_FUNCTIONAL_CONNECTIVITY_ALLEN/HUMAN'

conn1 = sio.loadmat(os.path.join(conn_folder_path,'NBSprep/30connectome_conn1_HCPParc_reslice.mat'))
conn3 = sio.loadmat(os.path.join(conn_folder_path,'NBSprep/31connectome_HCPParc_reslice.mat'))
dist = sio.loadmat(os.path.join(conn_folder_path,'distmat_HCP.mat'))

conn1_mat = conn1['subject_array_3D']
conn3_mat = conn3['subject_array_3D']
dist_mat = dist['distmat']

## Delete extra subject

conn3_mat = np.delete(conn3_mat,7,2)

## Average across subjects

conn1_mat = np.mean(conn1_mat,2)
conn3_mat = np.mean(conn3_mat,2)

## Vectorize upper triangle
dist_utri_arr = dist_mat[np.triu_indices(360,k =1)]
conn1_utri_arr = conn1_mat[np.triu_indices(360,k =1)]
conn3_utri_arr = conn3_mat[np.triu_indices(360,k =1)]

## Analyze

diff = np.subtract(conn3_utri_arr,conn1_utri_arr)

print np.corrcoef(conn1_utri_arr,conn3_utri_arr)

# print conn1_utri_arr
# print conn3_utri_arr
# print conn1_utri_arr.shape
# print conn3_utri_arr.shape

plt.scatter(dist_utri_arr,diff)
plt.show()