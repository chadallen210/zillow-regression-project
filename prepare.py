##### IMPORTS #####
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import sklearn.preprocessing

##### PREPARE FUNCTIONS #####

def miss_dup_values(df):
    '''
    this function takes a dataframe as input and will output metrics for missing values and duplicated rows, 
    and the percent of that column that has missing values and duplicated rows
    '''
        # Total missing values
    mis_val = df.isnull().sum()
        # Percentage of missing values
    mis_val_percent = 100 * df.isnull().sum() / len(df)
        #total of duplicated
    dup = df.duplicated().sum()  
        # Percentage of missing values
    dup_percent = 100 * dup / len(df)
        # Make a table with the results
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        # Rename the columns
    mis_val_table_ren_columns = mis_val_table.rename(columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        # Sort the table by percentage of missing descending
    mis_val_table_ren_columns = mis_val_table_ren_columns[
    mis_val_table_ren_columns.iloc[:,1] != 0].sort_values('% of Total Values', ascending=False).round(1)
        # Print some summary information
    print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
           "There are " + str(mis_val_table_ren_columns.shape[0]) +
           " columns that have missing values.")
    print( "  ")
    print (f"** There are {dup} duplicate rows that represents {round(dup_percent, 2)}% of total Values**")
        # Return the dataframe with missing information
    return mis_val_table_ren_columns

def wrangle_zillow():
    '''
    checks for existing zillow csv file and loads if present,
    otherwise runs new_zillow_data function to acquire data
    '''
    
    # drop any duplicates (removed 25 records)
    df.drop_duplicates(inplace=True)

    # replace symbols, etc with NaN's
    df = df.replace(r'^\s*$', np.nan, regex=True)
    
    # drop nulls (removed 95 records)
    df = df.dropna()
    
    # set index to parcelid (no statistical value)
    df.set_index('parcelid', drop=True, inplace=True)
    
    # rename columns for easier identification
    df = df.rename(columns={'parcelid': 'parcel_id', 'bathroomcnt': 'bathrooms', 'bedroomcnt': 'bedrooms',
                       'calculatedfinishedsquarefeet': 'square_feet', 'fips': 'county_code',
                       'yearbuilt': 'age', 'taxvaluedollarcnt': 'appraised_value', 'taxamount': 'taxes'})
    
    # convert year built into age, age is better for evaluation
    df.age = 2017 - df.age
    
    # change data types from float to int
    df.bathrooms = df.bathrooms.astype('int')
    df.bedrooms = df.bedrooms.astype('int')
    df.square_feet = df.square_feet.astype('int')
    df.county_code = df.county_code.astype('int')
    df.age = df.age.astype('int')
    df.appraised_value = df.appraised_value.astype('int')
    
    # calculate upper and lower bounds for square_feet
    q1sf, q3sf = df.square_feet.quantile([0.25, 0.75])
    iqrsf = q3sf - q1sf
    uppersf = q3sf + (1.5 * iqrsf)
    lowersf = q1sf - (1.5 * iqrsf)
    
    # remove outliers if below or above the bounds (removed 1194 records)
    df = df[df.square_feet > lowersf]
    df = df[df.square_feet < uppersf]
    
    # calculate upper and lower bounds for appraised_value
    q1av, q3av = df.appraised_value.quantile([0.25, 0.75])
    iqrav = q3av - q1av
    upperav = q3av + (1.5 * iqrav)
    lowerav = q1av - (1.5 * iqrav)
    
    # remove outliers if below or above the bounds (removed 1226 records)
    df = df[df.appraised_value > lowerav]
    df = df[df.appraised_value < upperav]
    
    # calculate upper and lower bounds for bathrooms
    q1bth, q3bth = df.bathrooms.quantile([0.25, 0.75])
    iqrbth = q3bth - q1bth
    upperbth = q3bth + (1.5 * iqrbth)
    lowerbth = q1bth - (1.5 * iqrbth)
    
    # remove outliers if below or above the bounds (removed 143 records)
    df = df[df.bathrooms > lowerbth]
    df = df[df.bathrooms < upperbth]
    
    # calculate upper and lower bounds for bedrooms
    q1bd, q3bd = df.bedrooms.quantile([0.25, 0.75])
    iqrbd = q3bd - q1bd
    upperbd = q3bd + (1.5 * iqrbd)
    lowerbd = q1bd - (1.5 * iqrbd)
    
    # remove outliers if below or above the bounds (removed 487 records)
    df = df[df.bedrooms > lowerbd]
    df = df[df.bedrooms < upperbd]
        
    return df

def split_zillow(df, target):
    '''
    this function takes in the zillow dataframe
    splits into train, validate and test subsets
    then splits for X (features) and y (target)
    '''
    
    # split df into 20% test, 80% train_validate
    train_validate, test = train_test_split(df, test_size=0.2, random_state=1234)
    
    # split train_validate into 30% validate, 70% train
    train, validate = train_test_split(train_validate, test_size=0.3, random_state=1234)
    
    # Split with X and y
    X_train = train.drop(columns=[target])
    y_train = train[target]
    
    X_validate = validate.drop(columns=[target])
    y_validate = validate[target]
    
    X_test = test.drop(columns=[target])
    y_test = test[target]
    
    return train, validate, test, X_train, y_train, X_validate, y_validate, X_test, y_test

def Min_Max_Scaler(X_train, X_validate, X_test):
    """
    Takes in X_train, X_validate and X_test dfs with numeric values only
    Returns scaler, X_train_scaled, X_validate_scaled, X_test_scaled dfs 
    """
    scaler = sklearn.preprocessing.MinMaxScaler().fit(X_train)
    X_train_scaled = pd.DataFrame(scaler.transform(X_train), index = X_train.index, columns = X_train.columns)
    X_validate_scaled = pd.DataFrame(scaler.transform(X_validate), index = X_validate.index, columns = X_validate.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), index = X_test.index, columns = X_test.columns)
    
    return scaler, X_train_scaled, X_validate_scaled, X_test_scaled

