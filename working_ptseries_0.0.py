import os
import pandas as pd

folder_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/H2001/L/'
count_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/H2001/L/Markov_Full_count.txt'
sum_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/H2001/L/Markov_Full_sum.txt'
average_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/H2001/L/Markov_Full_Average.txt'
ROI_path = 'Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/ROIs_TxtFiles/Markov_ROIs.txt'

sum_df = pd.read_table(sum_path, sep='\t', header=None)
count_df = pd.read_table(count_path, sep='\t', header=None)
average_df = pd.read_table(average_path, sep='\t', header=None)
ROI_df = pd.read_table(ROI_path, sep='\t', header=None)

ROI_df = ROI_df.iloc[::2]
ROI_df = ROI_df.reset_index(drop=True)

# #print ROI_df
# ROI_df.to_csv('Y:/Projects/Allen-HumanAdult-OHSU/dtseries_Files/ROIs_TxtFiles/Trim_Markov_ROIs.csv', index=False, header=False)

count_df = pd.concat([ROI_df, count_df], axis=1)
columns = list(range(16907))
columns = map(str, columns)
count_df.columns = columns
count_df = count_df.set_index('0')


print count_df.T['L_PO_M132']

# use this to get the rows in the right hemisphere with data
# count_non0 = count_df[(count_df.T !=0).any()]
# print count_non0

#print count_df
count_df = count_df.T
count_df['RL_23_M132'] = count_df['R_23_M132'] + count_df['L_23_M132']
count_df['RL_24d_M132'] = count_df['R_24d_M132'] + count_df['L_24d_M132']
count_df['RL_2_M132'] = count_df['R_2_M132'] + count_df['L_2_M132']
count_df['RL_3_M132'] = count_df['R_3_M132'] + count_df['L_3_M132']
count_df['RL_Subiculum_M132'] = count_df['R_Subiculum_M132'] + count_df['L_Subiculum_M132']
count_df['RL_V2_M132'] = count_df['R_V2_M132'] + count_df['L_V2_M132']
#
# # turn off when doing average calculation
# # count_df = count_df.T

#print count_df


sum_df = pd.concat([ROI_df, sum_df], axis=1)
columns = list(range(16907))
columns = map(str, columns)
sum_df.columns = columns
sum_df = sum_df.set_index('0')

use this to get the rows in the right hemisphere with data
sum_non0 = sum_df[(sum_df.T !=0).any()]
print sum_non0

print sum_df
sum_df = sum_df.T
sum_df['RL_23_M132'] = sum_df['R_23_M132'] + sum_df['L_23_M132']
sum_df['RL_24d_M132'] = sum_df['R_24d_M132'] + sum_df['L_24d_M132']
sum_df['RL_2_M132'] = sum_df['R_2_M132'] + sum_df['L_2_M132']
sum_df['RL_3_M132'] = sum_df['R_3_M132'] + sum_df['L_3_M132']
sum_df['RL_Subiculum_M132'] = sum_df['R_Subiculum_M132'] + sum_df['L_Subiculum_M132']
sum_df['RL_V2_M132'] = sum_df['R_V2_M132'] + sum_df['L_V2_M132']

# turn off when doing average calculation
# sum_df = sum_df.T

# print sum_df

average_df = pd.concat([ROI_df, average_df], axis=1)
columns = list(range(16907))
columns = map(str, columns)
average_df.columns = columns
average_df = average_df.set_index('0')

# print average_df
average_df = average_df.T
average_df['L_23_M132'] = sum_df['RL_23_M132'] / count_df['RL_23_M132']
average_df['L_24d_M132'] = sum_df['RL_24d_M132'] / count_df['RL_24d_M132']
average_df['L_2_M132'] = sum_df['RL_2_M132'] / count_df['RL_2_M132']
average_df['L_3_M132'] = sum_df['RL_3_M132'] / count_df['RL_3_M132']
average_df['L_Subiculum_M132'] = sum_df['RL_Subiculum_M132'] / count_df['RL_Subiculum_M132']
average_df['L_V2_M132'] = sum_df['RL_V2_M132'] / count_df['RL_V2_M132']


# Replace the right hemisphere values with 0s
average_df.loc[average_df['R_23_M132'] > 0, 'R_23_M132'] = 0.000000
average_df.loc[average_df['R_24d_M132'] > 0, 'R_24d_M132'] = 0.000000
average_df.loc[average_df['R_2_M132'] > 0, 'R_2_M132'] = 0.000000
average_df.loc[average_df['R_3_M132'] > 0, 'R_3_M132'] = 0.000000
average_df.loc[average_df['R_Subiculum_M132'] > 0, 'R_Subiculum_M132'] = 0.000000
average_df.loc[average_df['R_V2_M132'] > 0, 'R_V2_M132'] = 0.000000

average_df = average_df.fillna(0)

average_df = average_df.T

sum_df = sum_df.T
# print sum_df
count_df = count_df.T
# print count_df

print average_df

average_df.to_csv(os.path.join(folder_path,'Indexed_Sym_RisNA_Markov_Average.csv'),header=False)
average_df.to_csv(os.path.join(folder_path,'Sym_RisNA_Markov_Average.txt'),header=None, index=None, sep=' ')