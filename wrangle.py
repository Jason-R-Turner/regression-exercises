#!/usr/bin/env python
# coding: utf-8

# 2. Using your acquired Zillow data, walk through the summarization and cleaning steps in your wrangle.ipynb file like we did above. You may handle the missing values however you feel is appropriate and meaninful; remember to document your process and decisions using markdown and code commenting where helpful.


# import modules for acquire and prep stages
import pandas as pd
import env
import os
from sklearn.model_selection import train_test_split


# The below function will be what we use to access the database holding our Zillow data



def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    Function allows user to access Codeup database using their own 
    credentials stored in  their env.py file
    '''
    
# Returns with correct address/password combinat to access the database
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'



def new_zillow_data():
    '''
    SQL query that joins the customers table with, contract, payment, and \n
    internet service options
    '''
    
# SQL query that joins three other tables to customer table
    sql_query = '''
                SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips FROM properties_2017
                join propertylandusetype using (propertylandusetypeid)
                where propertylandusedesc = "Single Family Residential"
                '''
# Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
# Returns the called dataframe
    return df



def get_zillow_data():
    '''
    Function allows user to access zillow_data from Codeup database and write it\n
    to a csv file then returns the dataframe.
    '''
    
# if statement that checks if there's already a .csv file to use 
    if os.path.isfile('zillow.csv'):
        
# If csv file exists read in data from csv file.
        df = pd.read_csv('zillow.csv', index_col=0)
        
# Alternative if no csv file found then
    else:
        
# Read fresh data from db into a DataFrame
        df = new_zillow_data()
        
# Cache data for local use
        df.to_csv('zillow.csv')

# Returns requested df
    return df


# Since there are relatively few nulls compared to the number of rows of data we have they'll be dropped using the below function


def handle_nulls(df):
    '''
    Gets rid of the rows with any null values and returns a new null-free df
    '''
    
# drops the rows with any null values and returns a new null-free df
    df = df.dropna()
    
    
    return df


# We'll clean up the data by converting it into data types that are easier to work with for our purposes


def float_to_int(df):
    '''
    Converts our fips, bedrooms, calculatedfinishedsquarefeet, taxvaluedollarcnt, and yearbuilt from floats to integers
    '''
# converts our fips, bedrooms, calculatedfinishedsquarefeet, taxvaluedollarcnt, and yearbuilt from floats to integers
    df["fips"] = df["fips"].astype(int)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)
    df["taxvaluedollarcnt"] = df["taxvaluedollarcnt"].astype(int)
    df["calculatedfinishedsquarefeet"] = df["calculatedfinishedsquarefeet"].astype(int)
    
    return df


# In[7]:


def clean_zillow(df):
    '''
    Groups our functions used to clean up our data into a single function for ease of use
    '''
    
    df = handle_nulls(df)
    df = float_to_int(df)
    
    return df




def split_zillow(df):
    '''
    Takes our df and splits it into train, validate, and test dfs for exploration, fitting, validation, and testing
    '''
    
# splits the full data set 60/40 into train and test dataframes stratified 
# around taxvaluedollarcnt, the target variable, using the train_test_split function
    train, test = train_test_split(df, 
                               train_size = 0.75, 
                               stratify = df.fips, 
                               random_state=2468)

# splits the train dataframe 60/40 into the new train and validate dataframes
# they're stratified around taxvaluedollarcnt again using the train_test_split function
    train, validate = train_test_split(train,
                                    train_size = 0.75,
                                    stratify = train.fips,
                                    random_state=2468)
    
# returns the three dataframes we'll use for training, validation, and testing
    return train, validate, test


# 5. Based on the work you've done, choose a scaling method for your dataset. Write a function within your prepare.py (wrangle.py for me) that accepts as input the train, validate, and test data splits, and returns the scaled versions of each. Be sure to only learn the parameters for scaling from your training data!



def scale_zillow(train, validate, test,
                 cols_to_scale = ['bedroomcnt', 'bathroomcnt', 'calculatedfinishedsquarefeet', 'taxvaluedollarcnt']):
    '''
    Accepts train, valide, and test as inputs from split data then returns scaled versions for each one
    '''
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    scaler = MinMaxScaler()
    
    scaler.fit(train[cols_to_scale])
    
    train_scaled[cols_to_scale] = pd.DataFrame(scaler.transform(train[cols_to_scale]), columns=train[cols_to_scale].columns.values).set_index([train.index.values])
                                                  
    validate_scaled[cols_to_scale] = pd.DataFrame(scaler.transform(validate[cols_to_scale]), columns=validate[cols_to_scale].columns.values).set_index([validate.index.values])
    
    test_scaled[cols_to_scale] = pd.DataFrame(scaler.transform(test[cols_to_scale]), columns=test[cols_to_scale].columns.values).set_index([test.index.values])
    
    return train_scaled, validate_scaled, test_scaled


# 3. Store all of the necessary functions to automate your process from acquiring the data to returning a cleaned dataframe witn no missing values in your wrangle.py file. Name your final function wrangle_zillow



def wrangle_zillow():
    '''
    Function that acquires zillow data using the new_zillow_data function and 
    caches it, as a csv file, if there isn't already a local copy
    '''
    df = get_zillow_data()
    df = clean_zillow(df)
    train, validate, test = split_zillow(df)
    
    return train, validate, test


def split_tips(df):
    '''
    Takes our df and splits it into train, validate, and test dfs for exploration, fitting, validation, and testing
    '''
    
# splits the full data set 60/40 into train and test dataframes stratified 
# around taxvaluedollarcnt, the target variable, using the train_test_split function
    train, test = train_test_split(df, 
                               train_size = 0.75, 
                               stratify = df.tip, 
                               random_state=2468)

# splits the train dataframe 60/40 into the new train and validate dataframes
# they're stratified around taxvaluedollarcnt again using the train_test_split function
    train, validate = train_test_split(train,
                                    train_size = 0.75,
                                    stratify = train.tip,
                                    random_state=2468)
    
# returns the three dataframes we'll use for training, validation, and testing
    return train, validate, test

def scale_tips(train, validate, test,
                 cols_to_scale = ['total_bill', 'tip', 'size', 'price_per_person']):
    '''
    Accepts train, validate, and test as inputs from split data then returns scaled versions for each one
    '''
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    scaler = MinMaxScaler()
    
    scaler.fit(train[cols_to_scale])
    
    train_scaled[cols_to_scale] = pd.DataFrame(scaler.transform(train[cols_to_scale]), columns=train[cols_to_scale].columns.values).set_index([train.index.values])
                                                  
    validate_scaled[cols_to_scale] = pd.DataFrame(scaler.transform(validate[cols_to_scale]), columns=validate[cols_to_scale].columns.values).set_index([validate.index.values])
    
    test_scaled[cols_to_scale] = pd.DataFrame(scaler.transform(test[cols_to_scale]), columns=test[cols_to_scale].columns.values).set_index([test.index.values])
    
    return train_scaled, validate_scaled, test_scaled

def wrangle_tips(df):
    '''
    Splits tips data into train, validate, and test, then scales those into scaled versions
    '''
    df = split_tips(df)
    df = scale_tips(df)
    train, validate, test = scale_tips(df)
    
    return train_scaled, validate_scaled, test_scaled