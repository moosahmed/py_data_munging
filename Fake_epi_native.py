# IMPORTS

import os.path
import numpy as np
import nibabel
import csv

# SET PATHS
# Make sure you edit the file names to represent what you need and your output file name

#AIRC PATHS
# sample_annot_path = '/group_shares/FAIR_HCP/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor12876/SampleAnnot.csv'
# microarray_path = '/group_shares/FAIR_HCP/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor12876/MicroarrayExpression_136.csv'
# Native_path = '/group_shares/FAIR_HCP/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/Allen_Processed/H0351.1009/mri/orig/001.nii.gz'
# ROI_segmentation_path = '/group_shares/FAIR_HCP/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/fakeEPIs/H0351.1009_ROI_segmentation_136_mnionorig.nii.gz'

#WINDOWS PATHS; FAIR_HCP being Y:
sample_annot_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15496/trimd_SampleAnnot_cortex.csv'
microarray_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/normalized_microarray_donor15496/trimd_MicroarrayExpression_cortex.csv'
Native_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/Allen_Processed/H0351.1015/mri/orig/001.nii.gz'
ROI_segmentation_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/fakeEPIs/H0351.1015_ROI_segmentation_cortex.nii.gz'

#FOR 10021/H2002
# Native_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/WithT2/10021/T1.nii.gz'
# ROI_segmentation_path = 'Y:/Projects/Allen-HumanAdult-OHSU/scratch_TEMP_NO_BACKUP/fakeEPIs/H0351.2002_ROI_segmentation_tel_di_only.nii.gz'
# Check paths
#import os.path

print os.path.isfile(sample_annot_path)
print os.path.isfile(microarray_path)
print os.path.isfile(Native_path)
print os.path.isfile(ROI_segmentation_path)

# Load the Native brain atlas
img = nibabel.load(Native_path)
print img.shape
print img.get_data_dtype()

# Load the annotation csv file and transfer it into its own array

csvfile = open(sample_annot_path)
csvreader = csv.DictReader(csvfile)

sample_annot = []
for row in csvreader:
    sample_annot.append(row)
csvfile.close()

print len(sample_annot)
#print len(sample_annot[0])
#print sample_annot[0]
print np.shape(sample_annot)
#print type(sample_annot)
#print sample_annot[0].keys()
#print sample_annot[0]

# Open the genetics file and transfer it into its own array

csvfile = open(microarray_path)
csvreader = csv.reader(csvfile,dialect=csv.excel_tab)

sample_genetics_header = []
for row in csvreader:
    sample_genetics_header.append([float(element) for element in row[0].split(',')])
csvfile.close()

# Transpose the genetics array
trans_sample_genetics = np.transpose(sample_genetics_header)
print np.shape(trans_sample_genetics)
print len(trans_sample_genetics[0])


#print len(sample_genetics_header)
#print len(sample_genetics_header[0])
#print sample_genetics_header[1][1]
#print np.shape(sample_genetics_header)
#print sample_genetics_header[0].keys()
#print type(sample_genetics_header)

# Create genetics timecourse
native_affine = img.get_affine()
inv_native_affine = np.linalg.inv(native_affine)

genetic_tc = np.zeros((182,218,182,2), dtype='float32')
#genetic_tc = np.zeros((185,180,192,2), dtype='float32')
print "genetic tc shape:", genetic_tc.shape
print "genetic tc datatype:", genetic_tc.dtype

# from copy import deepcopy

for i in range(len(sample_annot)):
    coord_native = np.array(
        [float(sample_annot[i]['mni_x']), float(sample_annot[i]['mni_y']), float(sample_annot[i]['mni_z'])])
    coord_vox = tuple([int(round(vox)) for vox in nibabel.affines.apply_affine(inv_native_affine, coord_native)])
    # genetic_tc[coord_vox] = i+1
    timecourse = trans_sample_genetics[i]
    genetic_tc[coord_vox] = timecourse

genetic_ROIs = nibabel.Nifti1Image(genetic_tc, native_affine)
print "genetic ROIs shape:", genetic_ROIs.shape
print "genetic ROIs datatype:", genetic_ROIs.get_data_dtype()

# Save fake epi file
nibabel.save(genetic_ROIs, ROI_segmentation_path)

# Check out the fake epi file
fakeepi = nibabel.load(ROI_segmentation_path)
print fakeepi.shape
print fakeepi.get_data_dtype()