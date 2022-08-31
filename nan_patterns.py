"""
Program importing Titanic data and visualising to see patterns to fill NaNs

"""
# Importing libraries 

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Reading data files:
    
df = pd.read_csv('train.csv')
df2 = pd.read_csv('test.csv')

# Declaring functions used for splitting cabin data:
    
    
def split_cabin_data (df):
    df['Cabin'] = df['Cabin'].astype(str)
    df['DeckNo'] = df['Cabin'].apply(lambda x: x[0] if x !='nan' else np.NaN)
    df['CabinNo'] = df['Cabin'].apply(
        lambda x: x[2:-2] if x !='nan' else np.NaN)
    df['Port'] = df['Cabin'].apply(lambda x: x[-1] if x !='nan' else np.NaN)
    df.drop(columns = 'Cabin', inplace = True)
    return df

def add_group_number (df):
    df['Group'] = df['PassengerId'].apply(lambda x: x[:4])
    return df


# Splitting 'Cabin' number into 'Deck', 'Number' and 'Side'
df = split_cabin_data(df)
df = add_group_number(df)
df2 = split_cabin_data(df2)
df2 = add_group_number(df2)

homeplanet_group = df.loc[ 
    :,['Group', 'HomePlanet']].dropna().drop_duplicates(subset=['Group'])

homeplanet_group2 = df2.loc[
    :,['Group', 'HomePlanet']].dropna().drop_duplicates(subset=['Group'])

homeplanet_group = pd.concat([homeplanet_group, homeplanet_group2])

# Declaring functions used for filling HomePlanet NaNs based on Group


def fill_HomePlanet_by_group (df):
    for index, row in df.iterrows():
        group = row['Group']
        group_list = homeplanet_group['Group'].to_list()
        if group in group_list:
            new_home_planet = homeplanet_group.loc[
                homeplanet_group['Group'] == group].iloc[0]['HomePlanet']
            df.at[index, 'HomePlanet'] = new_home_planet
        else:
            continue
    return df


# Filling HomePlanet NaNs:

df_homeplanet_na = df.loc[df['HomePlanet'].isna()]
df.loc[df['HomePlanet'].isna()] = fill_HomePlanet_by_group(df_homeplanet_na)


df2_homeplanet_na = df2.loc[df2['HomePlanet'].isna()]
df2.loc[df2['HomePlanet'].isna()] = fill_HomePlanet_by_group(df2_homeplanet_na)

# Removing columns related to money spending:

column_names = list(df.columns.values)
columns_set_to_plot = set()
col_to_remove = ['PassengerId', 'RoomService', 'FoodCourt', 'ShoppingMall', 
                 'Spa', 'VRDeck', 'Name', 'Group', 'CabinNo']

for i in col_to_remove:
    column_names.remove(i)

for col1 in column_names:
    for col2 in column_names:
        if col1 == col2:
            continue
        else:
            column_pair_to_add = tuple(sorted((col1, col2)))
            columns_set_to_plot.add(column_pair_to_add)
            
            
            
# Plotting values to see if there are more realtionships between data:
    
col1, col2 = 'DeckNo', 'Destination'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")
plt.show()

col1, col1 = 'Destination', 'HomePlanet'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")

col1, col2 = 'HomePlanet', 'Port'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = 'Age', 'Port'
sns.catplot(x=col2, y=col1, data=df)
plt.show()

col1, col2 = 'CryoSleep', 'Port'
sns.histplot(
    binwidth=0.5, x=col2, hue=col1, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = 'DeckNo', 'HomePlanet'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = 'Age', 'CryoSleep'
sns.catplot(x=col2, y=col1, data=df)
plt.show()

col1, col2 = 'HomePlanet', 'VIP'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = 'HomePlanet', 'Transported'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = 'Transported', 'VIP'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = "Age" , 'VIP'
sns.catplot(x=col2, y=col1, data=df)
plt.show()

col1, col2 = 'Destination', 'Port'
sns.histplot(
    binwidth=0.5, x=col2, hue=col1, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = 'CryoSleep', "VIP"
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = 'Age', 'Transported'
sns.catplot(
    x=col2, y=col1, data=df)
plt.show()

col1, col2 = 'CryoSleep', 'Transported'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = 'DeckNo', 'Port'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat="count", multiple="stack")
plt.show()

col1, col2 = 'Destination', 'VIP'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat='count', multiple='stack')
plt.show()

col1, col2 = 'Destination', 'Transported'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat='count', multiple='stack')
plt.show()

col1, col2 = 'Age', 'Destination'
sns.catplot(x=col2, y=col1, data=df)
plt.show()

col1, col2 = 'CryoSleep', 'Destination'
sns.histplot(
    binwidth=0.5, x=col2, hue=col1, data=df, stat='count', multiple='stack')
plt.show()

col1, col2 = 'Port', 'Transported'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat='count', multiple='stack')
plt.show()

col1, col2 = 'DeckNo', 'VIP'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat='count', multiple='stack')
plt.show()

col1, col2 = 'DeckNo', 'Transported'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat='count', multiple='stack')
plt.show()

col1, col2 = 'Port', 'VIP'
sns.histplot(
    binwidth=0.5, x=col1, hue=col2, data=df, stat='count', multiple='stack')
plt.show()

col1, col2 = 'CryoSleep', 'HomePlanet'
sns.histplot(
    binwidth=0.5, x=col2, hue=col1, data=df, stat='count', multiple='stack')
plt.show()

col1, col2 = 'Age', 'DeckNo'
sns.catplot(x=col2, y=col1, data=df)
plt.show()

col1, col2 = 'CryoSleep', 'DeckNo'
sns.histplot(
    binwidth=0.5, x=col2, hue=col1, data=df, stat='count', multiple='stack')
plt.show()

col1, col2 = 'Age', 'HomePlanet'
sns.catplot(x=col2, y=col1, data=df)
plt.show()




# Meaningful patterns from plots:
    # all passengers in DeckNo 'A', 'B', 'C', 'T' are from Europa
    # most passengers from DeckNo 'E', 'F', 'G' are from Earth
    # most passengers from  DeckNo 'D' are from Mars
    # most passengers are not VIP
    # passengers not in CryoSleep are more likely to be trasported
    # passengers in CryoSleep are less likely to be trasported
    # tranposrted people are more likely to be in Port 'S'
    # most passengers are travelling to Trappist-1e
    # passengers from Earth most likely to be in DeckNo G
    # passengers from Europa Most likely to be in DeckNo B
    # passengers from Mars most likely to be in DeckNo F
