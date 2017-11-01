## This computes the correlation of two time courses.

import os.path
import pandas as pd

ROI_path = 'T:/Projects/FAIR_HORAK/FLING_process/Mat_data/ROI_ADT_ASNR2.csv'

ROI_df = pd.read_csv(ROI_path,index_col=0)
ROI_df = ROI_df.set_index(['session'], append=True)
ROI_df = ROI_df.set_index(['side'], append=True)
ROI_df = ROI_df.set_index(['ROI'], append=True)

# print ROI_df

corr_df = ROI_df.loc[(ROI_df.index.get_level_values('subjnum') == 349) & (ROI_df.index.get_level_values('session') == '_BL') & (ROI_df.index.get_level_values('side') == 'L')]

print corr_df
#
# print corr_df.T.corr()