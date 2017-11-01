##Goal of this script is to process the genes to select the ones with high variance

# IMPORTS

import os.path
import numpy as np
import nibabel
import csv
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')



# SET PATHS
# Paths are both in my local drive format and AIRC format. REMEMBER to select accordingly.

#AIRC PATHS

#folder_path = '/group_shares/FAIR_HCP/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor12876/'

#My Local Drive PATHS

#folder_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/'
folder_path = 'Y:/Projects/Allen-HumanAdult-OHSU/maybrain'
X_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/Funcgii/H1012/H1012.average_Gene_HCP.txt'
#X_path = 'Y:/Projects/Allen-HumanAdult-OHSU/maybrain/Science_trimd_Gordon_Xmatrix_2017_04_cs.csv'


#Check paths

print os.path.isdir(folder_path)
print os.path.isfile(X_path)

## load Genes

# X_df = pd.read_csv(X_path,index_col='Gene',low_memory=False)
X_df = pd.read_table(X_path,header=None,low_memory=False)
print X_df

#Stats

## Take The Mean for every gene along rows and add mean column at the end.

mean = X_df.mean(axis=1)
#mean = microarray_df.mean(axis=1)
print mean

X_df['mean'] = X_df.mean(axis=1)
print X_df
print len(X_df)

X_df = X_df.drop('mean',axis=1)

# mean2 = mean.mean(axis=0)
# print mean2

## Compute fold change across genes for each ROI

fold_change = X_df.divide(mean,axis=0)
# fold_change = microarray_df.divide(mean,axis=0)
# fold_change = fold_change.loc[:, (fold_change !=0).any(axis=0)]

print fold_change

log = fold_change.apply(np.log)
print log

## Compute stats on fold change

var = log.var(axis=1)
print var
print var.max()

std = log.std(axis=1)
print std
print std.max()

# #cut_std = std[std > 0.15]
# #print cut_std
# #print cut_std.shape

#Plot
plt.scatter(mean,std)
plt.show()


plt.hist(mean,100)
plt.axis([0,10,0,1000])
plt.show()