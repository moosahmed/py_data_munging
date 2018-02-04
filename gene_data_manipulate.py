## Goal for this script is to use Ontology_tel_di_L.csv to trim MicroarrayExpression_StrucID.csv, then use that to trim SampleAnnot.csv

#imports

import os.path
import pandas as pd
#import numpy as np
#import csv

# SET PATHS
# Paths are both in my local drive format and AIRC format. REMEMBER to select accordingly.

#For microarray_path USE the StrucID file which has the sample IDs manually added to the microarrayexpression file

#AIRC PATHS

#folder_path = '/group_shares/FAIR_HCP/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/'
#sample_annot_path = '/group_shares/FAIR_HCP/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/SampleAnnot.csv'
#microarray_path = '/group_shares/FAIR_HCP/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/MicroarrayExpression_StrucID.csv'
#ontology_path = '/group_shares/FAIR_HCP/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/Ontology_tel_di_L.csv'

#My Local Drive PATHS

folder_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/'
sample_annot_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/SampleAnnot.csv'
microarray_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/MicroarrayExpression_Full_StrucID.csv'
ontology_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/Ontology.csv'
probe_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15697/Probes.csv'
probe_list = 'Y:/Projects/Allen-HumanAdult-OHSU/Science_paper/probe_list.csv'

#Check paths

print os.path.isfile(sample_annot_path)
print os.path.isfile(microarray_path)
print os.path.isfile(ontology_path)
print os.path.isdir(folder_path)
print os.path.isfile(probe_path)
print os.path.isfile(probe_list)

# Take Ontology.csv file and make Ontology_tel_di_L.csv or any other variation
ont = pd.read_csv(ontology_path)

# Take out Rs. Not for 15697 & 09861
ont = ont[ont.hemisphere !="R"]

# Pick ONE of the next 3 variations depending on what file you want. Name output accordingly.

# 1) CORTEX ONLY Take out everything except cortex (4008) also take out hippocampal regions - 4249
ont = ont[ont.structure_id_path.str.contains("4008")]
ont = ont[ont.structure_id_path.str.contains("4249") == False]

# # 2) SUBCORTICAL and HIPPOCAMPUS Take out everything but Diencephalon (4391) and Telencephalon (4007) #Take out cortex (4008) leaving 4249
# ont = ont[ont.structure_id_path.str.contains("4007|4391")]
# # Take out cortex (4008) leaving hippocamous (4249)
# ont = ont[ont.structure_id_path.str.contains("4008")==False | ont.structure_id_path.str.contains("4249")]
#
# #3) ALL tel and di
# ont = ont[ont.structure_id_path.str.contains("4007|4391")]
#
# Create the ontology csv
# ont.to_csv(os.path.join(folder_path,'Ontology_cortex.csv'), index=False)

# # Load the ontology csv file and make a list of all the IDs
ontology_ID = ont['id'].dropna().astype(int).tolist()
# print len(ontology_ID)
# print ontology_ID

# # Load sample_annot file and trim it using the ontology IDs left
sampleannot_df = pd.read_csv(sample_annot_path)
sampleannot_df = sampleannot_df.T
sampleannot_df = sampleannot_df.loc[:,sampleannot_df.loc['structure_id'].isin(ontology_ID)]
sampleannot_df = sampleannot_df.T
sampleannot_df.to_csv(os.path.join(folder_path,'trimd_SampleAnnot_Full_cortex.csv'), index=False)

# # Load Science Probe list and make a list of the probe IDs
p_list = pd.read_csv(probe_list)
p_id = p_list['probe_id'].tolist()
# print p_id
# print len(p_id)

# # Load Probe data and filter using science probe list
probes_df = pd.read_csv(probe_path)
probes_df = probes_df.T
probes_df = probes_df.loc[:,probes_df.loc['probe_name'].isin(p_id)]
probes_df = probes_df.T
probes = probes_df['probe_id'].astype(str).tolist()
#print probes
#probes_df.to_csv(os.path.join(folder_path,'science_trimd_Probes.csv'))

# # load the microarray file and filter using the ontology ID
microarray_df = pd.read_csv(microarray_path,header=None,index_col=0,low_memory=False)
microarray_df = microarray_df.loc[:,microarray_df.loc['structure_id'].isin(ontology_ID)]

# # Filter using Science probes data set
microarray_df = microarray_df.reset_index(level=['0'])
microarray_df = microarray_df.T
microarray_df = microarray_df.set_index([0])
microarray_df = microarray_df.loc[:,microarray_df.loc['structure_id'].isin(probes)]
microarray_df = microarray_df.T
# print microarray_df

# # Change title and save trimmed microarray file to csv
microarray_df.to_csv(os.path.join(folder_path,'Science_trimd_MicroarrayExpression_Full_cortex_Struc.csv'),header=False, index=False)
print microarray_df
