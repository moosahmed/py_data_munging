import os
import pandas as pd

folder_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/H2001/L/'
count_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/H2001/L/Markov_Full_count.txt'
sum_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/H2001/L/Markov_Full_sum.txt'
# average_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/H1016/L/Markov_Full_Average.txt'
ROI_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/ROIs_TxtFiles/Gordon_ROIs.txt'

sum_df = pd.read_table(sum_path, sep='\t', header=None)
count_df = pd.read_table(count_path, sep='\t', header=None)
# average_df = pd.read_table(average_path, sep='\t', header=None)
# ROI_df = pd.read_table(ROI_path, sep='\t', header=None)


#TODO: Do this for every New ROI
# ROI_df = ROI_df.iloc[::2]
# ROI_df = ROI_df.reset_index(drop=True)
# print ROI_df
# ROI_df.to_csv('Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/ROIs_TxtFiles/Trim_Gordon_ROIs.csv', index=False, header=False)

for s in range(0,93):
    sum_df.iloc[s] = sum_df.iloc[s] + sum_df.iloc[s+93]
    sum_df.iloc[s+93] = 0.000000
    count_df.iloc[s] = count_df.iloc[s] + count_df.iloc[s+93]
    count_df.iloc[s+93] = 0.000000

average_df = sum_df.div(count_df)
average_df = average_df.fillna(0)

print average_df

average_df.to_csv(os.path.join(folder_path,'Sym_L_only_Markov_Average.txt'),header=None, index=None, sep=' ')