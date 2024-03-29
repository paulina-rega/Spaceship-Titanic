
"""
Program importing Titanic, filling NaNs and preparing it for ML algorithm

"""
# Importing libraries 
import pandas as pd
import numpy as np

# Reading train and test files:
df = pd.read_csv('train.csv')            
df2 = pd.read_csv('test.csv')


# Declaring some functions:
def find_common_value(col_name):
    '''
    Fids most common value in Series.

    Parameters
    ----------
    col_name : Series
        Series with categorical data.

    Returns
    -------
    common_value : string
        Most common value in the col_name.

    '''
    common_value = col_name.value_counts().index[0]
    return common_value


def fill_nan_with_common_value(col, common_value):
    '''
    Fills NaNs in given column with given value

    Parameters
    ----------
    col : Series
        Column to fill NaNs.
    common_value : object
        Value to fill column.

    Returns
    -------
    col : Series
        Updated column.

    '''
    col.fillna(common_value, inplace = True)
    return col


def add_column_if_value_is_missed(df, category):
    '''
    Adding column to DataFrame with information if value in some category was 
    missing

    Parameters
    ----------
    df : DataFrame
        DataFrame to update
    category : string
        Name of the column with missing values.

    Returns
    -------
    df : DataFrame
        DataFrame with added column.

    '''
    new_column_name = 'is' + category + 'Known'
    df[new_column_name] = df[category].notnull()
    return df

    
def split_cabin_data (df):
    '''
    Splitting 'Cabin' column into 'Deck', 'Number' and 'Side' and deleting
    'Cabin' column

    Parameters
    ----------
    df : DataFrame
        DataFrame with 'Cabin' column and 'deck/num/side' format.

    Returns
    -------
    df : DataFrame
        DataFrame with new columns.

    '''
    df['Cabin'] = df['Cabin'].astype(str)
    df['DeckNo'] = df['Cabin'].apply(lambda x: x[0] if x !='nan' else np.NaN)
    df['CabinNo'] = df['Cabin'].apply(
        lambda x: x[2:-2] if x !='nan' else np.NaN)
    df['Port'] = df['Cabin'].apply(lambda x: x[-1] if x !='nan' else np.NaN)
    df.drop(columns = 'Cabin', inplace = True)
    return df


def add_group_number (df):
    '''
    Adding group number to DataFrame based on passenger ID

    Parameters
    ----------
    df : DataFrame
        DataFrame with 'PassengerId' column where first 4 characters are group
        number

    Returns
    -------
    df : DataFrame
        DataFrame with added 'Group' column

    '''
    df['Group'] = df['PassengerId'].apply(lambda x: x[:4])
    return df


# Splitting 'Cabin' number into 'Deck', 'Number' and 'Side':

df = split_cabin_data(df)
df = add_group_number(df)
df2 = split_cabin_data(df2)
df2 = add_group_number(df2)




# Filling 'HomePlanet' NaNs with value based on other passengers in
# the same 'Group':
    
homeplanet_group = df.loc[
    :,['Group', 'HomePlanet']].dropna().drop_duplicates(subset=['Group'])

homeplanet_group2 = df2.loc[
    :,['Group', 'HomePlanet']].dropna().drop_duplicates(subset=['Group'])

homeplanet_group = pd.concat([homeplanet_group, homeplanet_group2])


def fill_HomePlanet_by_group (df):
    '''
    Filling 'HomePlanet' NaNs with value based on other passengers in
    the same 'Group':

    Parameters
    ----------
    df : DataFrame
        DataFrame with 'HomePlanet' label

    Returns
    -------
    df : DataFrame
        Updated DataFrame.

    '''
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


df_homeplanet_na = df.loc[df['HomePlanet'].isna()]
df.loc[df['HomePlanet'].isna()] = fill_HomePlanet_by_group(df_homeplanet_na)

df2_homeplanet_na = df2.loc[df2['HomePlanet'].isna()]
df2.loc[df2['HomePlanet'].isna()] = fill_HomePlanet_by_group(df2_homeplanet_na)

# Declaring function filling NaNs in column based on another column meeting
# some criteria:


def fill_nan_basing_on_other_column(
        df, other_col, val_to_compare, col_to_fill, val_to_fill):
    '''
    Return DataFrame with filled NaN with given value if value in another
    column meets condition
    
    Parameters
    ----------
    df : DataFrame
        DataFrame with columns 'other_col' and 'col_to_fill'.
    other_col : string
        Label of the another column to check parameter.
    val_to_compare : string or list of strings
        Value or list of values of parameter to check in other_col
    col_to_fill : string
        Label of the column to fill NaN in.
    val_to_fill : string
        Value to fill nan with.

    Returns
    -------
    DataFrame

    '''
    print('\n\n {} NaNs before filling  df & df2 based on {}={}:'.format(
         col_to_fill, other_col, val_to_compare))
    print(df.isnull().sum()[col_to_fill])
    

    if isinstance(val_to_compare, list):
        for val in val_to_compare:
            df.update(
                df.loc[(df[other_col]==val)].fillna({col_to_fill:val_to_fill}))
    else: 
        df.update(
            df.loc[(df[other_col]==val_to_compare)].fillna(
                {col_to_fill:val_to_fill}))
    
    print('\n {} NaNs after filling  df & df2 based on {}={}:'.format(
         col_to_fill, other_col, val_to_compare))
    print(df.isnull().sum()[col_to_fill])
    
    return df
    

# Filling 'HomePlanet' NaNs with 'Europe' for passengers from 'DeckNo'
# A, B, C, T:
df = fill_nan_basing_on_other_column(
    df, 'DeckNo', ['A', 'B', 'C', 'T'], 'HomePlanet', 'Europa')
df2 = fill_nan_basing_on_other_column(
    df2, 'DeckNo', ['A', 'B', 'C', 'T'], 'HomePlanet', 'Europa')


# Filling 'HomePlanet' NaNs with 'Earth' for passengers from 'DeckNo' E, F, G:
df = fill_nan_basing_on_other_column(
    df, 'DeckNo', ['E', 'F', 'G'], 'HomePlanet', 'Earth')
df2 = fill_nan_basing_on_other_column(
    df2, 'DeckNo', ['E', 'F', 'G'], 'HomePlanet', 'Earth')

# Filling 'HomePlanet' NaNs with 'Mars' for passengers from 'DeckNo' D:
df = fill_nan_basing_on_other_column(df, 'DeckNo', 'D', 'HomePlanet', 'Mars')
df2 = fill_nan_basing_on_other_column(df2, 'DeckNo', 'D', 'HomePlanet', 'Mars')

# Filling 'Deckno' NaNs with 'G' for passengers from 'HomePlanet' Earth:
df = fill_nan_basing_on_other_column(df, 'HomePlanet', 'Earth', 'DeckNo', 'G')
df2 = fill_nan_basing_on_other_column(
    df2, 'HomePlanet', 'Earth', 'DeckNo', 'G')

# Filling 'Deckno' NaNs with 'B' for passengers from 'HomePlanet' Europa:
df = fill_nan_basing_on_other_column(
    df, 'HomePlanet', 'Europa', 'DeckNo', 'B')
df2 = fill_nan_basing_on_other_column(
    df2, 'HomePlanet', 'Europa', 'DeckNo', 'B')

# Filling 'DeckNo' NaNs with 'F' for passengers from 'HomePlanet' Mars:
df = fill_nan_basing_on_other_column(df, 'HomePlanet', 'Mars', 'DeckNo', 'F')
df2 = fill_nan_basing_on_other_column(df2, 'HomePlanet', 'Mars', 'DeckNo', 'F')

# Filling 'Port' NaNs to unknown: 
df['Port'].fillna('U', inplace=True)
df2['Port'].fillna('U', inplace=True)

# Dropping 'Name', 'CabinNo' columns
columns_to_drop = ['Name', 'CabinNo', 'Group']
df = df.drop(columns = columns_to_drop)
df2 = df2.drop(columns = columns_to_drop)

# Filling remaining 'HomePlanet', 'Destination', 'VIP', 'Age' NaNs with 
# common values:
    
categorical_value_to_fill = [
    'HomePlanet', 'Destination', 'VIP', 'Age', 'DeckNo']

for category in categorical_value_to_fill:
    df = add_column_if_value_is_missed(df, category)
    df2 = add_column_if_value_is_missed(df2, category)
    common_value = find_common_value(df[category])
    df[category] = fill_nan_with_common_value(df[category], common_value)
    df2[category] = fill_nan_with_common_value(df[category], common_value)


# Creating a list of venues to spend money in
types = df.dtypes
numeric_types = types[types=='float64'].drop('Age').index

# Adding SpendingSum column to df
df['SpendingsSum'] = df[numeric_types].sum(axis = 1)
df2['SpendingsSum'] = df2[numeric_types].sum(axis = 1)

# Filling passengers 'CryoSleep' NaNs Based on spendings 
# (no spendings - 'CryoSllep' is True, some spendings - 'CryoSleep' is False ):
    
df_nan_sleep = df[df['CryoSleep'].isna()]
df_nan_sleep.loc[(df_nan_sleep['SpendingsSum'] > 0), 'CryoSleep'] = False
df_nan_sleep.loc[(df_nan_sleep['SpendingsSum'] <= 0), 'CryoSleep'] = True
df.loc[df_nan_sleep.index, :] = df_nan_sleep[:] 

df2_nan_sleep = df2[df2['CryoSleep'].isna()]
df2_nan_sleep.loc[(df2_nan_sleep['SpendingsSum'] > 0), 'CryoSleep'] = False
df2_nan_sleep.loc[(df2_nan_sleep['SpendingsSum'] <= 0), 'CryoSleep'] = True
df2.loc[df2_nan_sleep.index, :] = df2_nan_sleep[:] 
    
# Filling 'CryoSleep' == True passengers spendings NaNs to zero :
    
df.update(df.loc[(df['CryoSleep']==True), numeric_types].fillna(0))
df2.update(df2.loc[(df2['CryoSleep']==True), numeric_types].fillna(0))

# Creating df of median spendings in venues based on age:
ages = df['Age'].dropna().unique()
ages = np.sort(ages)
ages_expenses = pd.DataFrame({}, index = ages)

for i in numeric_types:
    ages_expenses[i]=0
    df[i] = df[i].astype(float)

# Calculating median spendings for groups based on age:

for current_age in ages:
    df_current_age = df[
        ((df['Age'] == current_age) & (df['CryoSleep'] == False))]
    if df_current_age.empty:
        continue
    for current_num_type in numeric_types:
        if df_current_age[current_num_type].isnull().all():
            # Skip calculating the median if the is no data
            continue
        median_spending = int(df_current_age[current_num_type].median(
            skipna = True))
        ages_expenses.loc[current_age, current_num_type] = median_spending
    
ages_spending_groups = [0, 13, 20, 30, 40, 50, 60, 200]
rows_number = len(ages_spending_groups)
columns_number = len(numeric_types)

df_spending_by_age_groups = pd.DataFrame(
    np.zeros((rows_number, columns_number)), columns = numeric_types, 
    index = ages_spending_groups)

ages_expenses.reset_index(inplace = True)
ages_expenses = ages_expenses.rename(columns = {'index':'Age'})

for i in range(len(ages_spending_groups) - 1):
    beginning_of_age_range = ages_spending_groups[i]
    ending_of_age_range = ages_spending_groups[i+1]
    df_temp_age_range = ages_expenses[
        (ages_expenses['Age'] >= beginning_of_age_range) &
        (ages_expenses['Age'] < ending_of_age_range)]
    for numeric_type in numeric_types: 
        temp_median = df_temp_age_range[numeric_type].median()
        df_spending_by_age_groups.at[
            beginning_of_age_range, numeric_type] = temp_median
        
# Filling remainging NaNs in spending (based on median spending by age grop):
    
num_ranges = len(ages_spending_groups)

for numeric_type in numeric_types:
    df_numeric_type = df.loc[df[numeric_type].isnull()]
    df2_numeric_type = df2.loc[df2[numeric_type].isnull()]
    for age in range(1, num_ranges):
        current_range_max_age = ages_spending_groups[age - 1]
        median_spending = df_spending_by_age_groups.at[
            current_range_max_age, numeric_type]
        df.update(df.loc[
            (df['Age'] >= current_range_max_age), numeric_type].fillna(
                median_spending))
        df2.update(df2.loc[
            (df2['Age'] >= current_range_max_age), numeric_type].fillna(
                median_spending))
                
# Exporting data:
    
df.to_csv('train_set_processed.csv', index = False)
df2.to_csv('test_set_processed.csv', index = False)

