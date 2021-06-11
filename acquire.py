##### IMPORTS #####
import pandas as pd
import os

from env import host, username, password

##### DB CONNECTION #####
def get_db_url(db, username=username, host=host, password=password):
    
    return f'mysql+pymysql://{username}:{password}@{host}/{db}'

##### ACQUIRE ZILLOW #####
def new_zillow_data():
    '''
    gets zillow information from CodeUp db using SQL query
    and creates a dataframe
    '''

    # SQL query
    zillow_query = '''SELECT parcelid, bathroomcnt, bedroomcnt, calculatedfinishedsquarefeet, 
                    fips, yearbuilt, taxvaluedollarcnt, taxamount
                    FROM properties_2017
                    JOIN predictions_2017 USING (parcelid)
                    WHERE transactiondate BETWEEN "2017-05-01" AND "2017-08-31"
                    AND propertylandusetypeid BETWEEN 260 AND 264
                    '''
    
    # reads SQL query into a DataFrame            
    df = pd.read_sql(zillow_query, get_db_url('zillow'))
    
    return df

def get_zillow_data():
    '''
    checks for existing csv file
    loads csv file if present
    if there is no csv file, calls new_zillow_data
    '''
    
    if os.path.isfile('zillow.csv'):
        
        df = pd.read_csv('zillow.csv', index_col=0)
        
    else:
        
        df = new_zillow_data()
        
        df.to_csv('zillow.csv')
    
    return df