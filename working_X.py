#imports

import os.path
import pandas as pd

folder_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/Funcgii/H1012'
probe_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/Probes.csv'
#X_path = 'Y:/Projects/Allen-HumanAdult-OHSU/maybrain/Gordon_Xmatrix_2017_04_cs.csv'
X_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/Funcgii/H1012/H1012.average_Gene_Gordon.txt'
microarray_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/Science_mean_trimd_MicroarrayExpression.csv'
gene_list = 'Y:/Projects/Allen-HumanAdult-OHSU/Science_paper/probe_list.csv'
roi_list = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/ROIs_TxtFiles/Trim_Gordon_ROIs.csv'

print os.path.isdir(folder_path)
print os.path.isfile(X_path)
print os.path.isfile(gene_list)
print os.path.isfile(probe_path)
print os.path.isfile(microarray_path)
print os.path.isfile(roi_list)

## Read in the mean trimmed microarray file to pull the trimmed probe list
micro_df = pd.read_csv(microarray_path, header=None)
trimd_probe_list = micro_df[0].astype(int).tolist()
print trimd_probe_list
print len(trimd_probe_list)
#print micro_df


## trim the probes_df to get a trimmed down list of gene names.
probes_df = pd.read_csv(probe_path)
probes_df = probes_df.T
probes_df = probes_df.loc[:,probes_df.loc['probe_id'].isin(trimd_probe_list)]
probes_df = probes_df.T
probes = probes_df['gene_symbol'].astype(str).tolist()

print probes
print len(probes)

#X_df = pd.read_csv(X_path)
#print X_df

X_df = pd.read_table(X_path, sep='\t', header=None)
#print X_df
print len(X_df)


genes_df = pd.read_csv(gene_list)
genes = genes_df['gene_symbol'].astype(str).tolist()
print genes
print len(genes)

## Only for My Gene Matrices to add the GENE names to the matrix, Then we filter by the science mean trimmed gene list.
X_df.loc['Gene'] = genes
print X_df
X_df = X_df.loc[:,X_df.loc['Gene'].isin(probes)]
X_df = X_df.sort_index()
print X_df


## This is for the X matrices; check which list filtering you want to use.
# X_df = X_df.T
# # X_df = X_df.loc[:,X_df.loc['Gene'].isin(genes)]
# X_df = X_df.loc[:,X_df.loc['Gene'].isin(probes)]
# X_df = X_df.T
# print X_df

X_df.to_csv(os.path.join(folder_path,'Science_FullMean_trimd_H1012.average_Gene_Gordon.csv'),index=False)

## For My Matrices
X_genes = X_df.loc['Gene'].tolist()

print X_genes
## For X
#X_genes = X_df['Gene'].tolist()

## Save Gene Names
x_genes_file = open(os.path.join(folder_path,'Science_FULLmean_trimd_H1012.average_Gene_Gordon_genes.txt'), 'w')

for item in X_genes:
    x_genes_file.write("%s\n" % item)

##For Mine
X_values = X_df.drop('Gene')


##For X
# X_values = X_df.drop('Gene', axis=1)

X_values = X_values.fillna('nan')
print X_values

X_values.to_csv(os.path.join(folder_path,'Science_FULLmean_trimd_H1012.average_Gene_Gordon_values.csv'),index=False, header=False)

## Add ROI list to X_values

ROI_df = pd.read_csv(roi_list, names=["ROI"])
X_ROI_df = X_values.join(ROI_df)
X_ROI_df = X_ROI_df.set_index(["ROI"])

## remove NAN ROIs
X_ROI_df = X_ROI_df.dropna(axis=0)
print X_ROI_df

## Save the ROI Trimmed csv
X_ROI_df.to_csv(os.path.join(folder_path, 'Science_FULLmean_NaN_ROI_trimd_H1012.average_Gene_Gordon.csv'), header=False)

## Save the trimmed ROI list
X_ROIs = X_ROI_df.index.values
print X_ROIs
trimd_roi_file = open(os.path.join(folder_path, 'Science_FULLmean_NaN_ROI_trimd_H1012.average_Gene_Gordon_ROIs.txt'), 'w')

for item in X_ROIs:
     trimd_roi_file.write("%s\n" % item)

X_ROI_df.to_csv(os.path.join(folder_path, 'Science_FULLmean_NaN_ROI_trimd_H1012.average_Gene_Gordon_VALUES.csv'), index=False, header=False)