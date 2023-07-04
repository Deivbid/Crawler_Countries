import pandas as pd
import numpy as np

#Remember to put the name of the file
df = pd.read_excel('markets.xlsx')

# Replace NaN values with zeros
df = df.fillna(0)

# Get the last row (total)
last_row = df.iloc[-1]

# Divide each row of the "Approx Legacy MV" column by the last row value, also the column won't be named that, it will be named exp pf
df['Approx Legacy MV'] /= last_row['Approx Legacy MV']
# AMMEND IN BOTH CASES FOR WHEN THE TOTAL ON ONE OF THEM IS 0, SO IT DOES NOT DIVIDE BY 0
# Divide each row of the "Approx Target MV" column by the last row value, also the column won't be named that, it will be named exp bench
df['Approx Target MV'] /= last_row['Approx Target MV']

# Add a new column based on the condition
condition = ((df['Approx Legacy MV'] > 0.05) | (df['Approx Target MV'] > 0.05)) & (df['Market'] != 'USD Cash') & (df['Market'] != 'GLOBAL') & (df['Market'] != 'YANKEE')  
df['Is it in scope? (5%)'] = np.where(condition, 'YES', 'NO')

#INSTEAD OF SAYING 'TRUE' OR 'FALSE', MAKE IT SAY 'YES' OR 'NO' FOR TRUE AND FOR FALSE, RESPECTIVELY

# Save the modified dataframe to a new Excel file
df.to_excel('markets_in_scope.xlsx', index=False)