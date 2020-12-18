import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.speedups

def pop_change(df, first_population, second_population):
    '''
    Calculates difference between columns in to a new column called 'pop_change'
    
    ---Parameters---
    df: dataframe
    first_column_name: string
    second_column_name: string
    
    ---Returns---
    Modified input dataframe with the columns 'pop_change', 'pop_change_precentage'.
    '''
    df['pop_change'] = df[second_population] - df[first_population]
    df['pop_change_precentage'] = df['pop_change'] / df[first_population] * 100
    df['pop_change_precentage'] = df['pop_change_precentage'].round(1)
    
    return df
    

def precentage(value_1, value_2):
    result = value_2 / value_1 * 100
    return result

def 
    
    

