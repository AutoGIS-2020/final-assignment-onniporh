import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import shapely.speedups
import seaborn as sns
import pandas as pd

########

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

########

def precentage(value_1, value_2):
    result = value_2 / value_1 * 100
    return result.round(1)

########

def fetch_postal_area_data(url, municipality_code):
    # creating a variable for postal code area demographic statistics for 2020
    pca_data = gpd.read_file(url)

    # changing the CRS to ETRS-GK25 FIN
    pca_data = pca_data.to_crs(epsg=3879)
    
    # selecting the data from the given municipality
    pca_data = pca_data[pca_data['kunta'].str.match(municipality_code)]
    
    return pca_data

########

def green_areas(ga_data, pca_data):
    '''
    Calculates green area shares for postal code areas in a given dataframe.
    Both dataframes have to be geodataframes. 
    
    
    ---Returns---
    A geodataframe with green areas and postal code areas calculated in new columns.
    '''
    
    # Calculating areas for the postal code areas
    pca_data['total_area_km2'] = pca_data.area / 1000000
    
    # Fixing the potential errors with self-intersecting polygons
    ga_data['geometry'] = ga_data['geometry'].buffer(0)
    
    # Overlaying the green_areas with the pca_statistics with intersection
    pca_ga_data = gpd.overlay(pca_data, ga_data, how='intersection')
    
    # Calculating areas for green areas and postal code areas
    pca_ga_data['green_area_km2'] = pca_ga_data.area / 1000000
    pca_ga_data = pca_ga_data[['postal_code', 'green_area_km2']]
    
    # Aggregating by summing the green areas in a new dataframe
    aggregation_functions = {'green_area_km2': 'sum'}
    pca_ga_data = pca_ga_data.groupby(pca_ga_data['postal_code']).aggregate(aggregation_functions)
    
    # Concat the industrial area data into the statistics dataframe
    pca_data = pca_data.merge(pca_ga_data, on='postal_code', how='left')
    
    # Green area precentage calcultion
    pca_data['green_area_precentage'] = precentage(pca_data['total_area_km2'], pca_data['green_area_km2'])
    
    # Green area per capita calculation
    pca_data['green_area_pc_2020_m2'] = ((pca_data['green_area_km2'] * 1000000) / pca_data['pop_2020']).round(1)
    pca_data['green_area_pc_2020_m2'] = pca_data['green_area_pc_2020_m2'].replace([np.inf, -np.inf], np.nan)
    
    return pca_data

#######

def industrial_areas(ia_data, pca_data):
    '''
    Calculates industrial area shares for postal code areas in a given dataframe.
    Both dataframes have to be geodataframes. 
    
    
    ---Returns---
    A geodataframe with industrial areas and postal code areas calculated in new columns.
    '''
    
    # Calculating areas for the postal code areas
    pca_data['total_area_km2'] = pca_data.area / 1000000
    
    # Fixing the potential errors with self-intersecting polygons
    ia_data['geometry'] = ia_data['geometry'].buffer(0)
    
    # Overlaying the industrial areas with the pca_statistics with intersection
    pca_ia_data = gpd.overlay(pca_data, ia_data, how='intersection')
    
    # Calculating areas for industrial areas and postal code areas
    pca_ia_data['industrial_area_km2'] = pca_ia_data.area / 1000000
    pca_ia_data = pca_ia_data[['postal_code', 'industrial_area_km2']]
    
    # Aggregating by summing the industrial areas in a new dataframe
    aggregation_functions = {'industrial_area_km2': 'sum'}
    pca_ia_data = pca_ia_data.groupby(pca_ia_data['postal_code']).aggregate(aggregation_functions)
    
    # Concat the industrial area data into the statistics dataframe
    pca_data = pca_data.merge(pca_ia_data, on='postal_code', how='left')
    pca_data = pca_data.fillna(0)
    
    # industrial area precentage calcultion
    pca_data['industrial_area_precentage'] = precentage(pca_data['total_area_km2'], pca_data['industrial_area_km2'])
    
    return pca_data

########

def other_built_areas(ba_data, pca_data):
    '''
    Calculates built up area shares for postal code areas in a given dataframe. Other areas
    consists mainly of residential and commercial areas.
    Both dataframes have to be geodataframes. 
    
    
    ---Returns---
    A geodataframe with residential areas and postal code areas calculated in new columns.
    '''
    
    # Calculating areas for the postal code areas
    pca_data['total_area_km2'] = pca_data.area / 1000000
    
    # Fixing the potential errors with self-intersecting polygons
    ba_data['geometry'] = ba_data['geometry'].buffer(0)
    
    # Overlaying the industrial areas with the pca_statistics with intersection
    pca_ba_data = gpd.overlay(pca_data, ba_data, how='intersection')
    
    # Calculating areas for industrial areas and postal code areas
    pca_ba_data['other_area_km2'] = pca_ba_data.area / 1000000
    pca_ba_data = pca_ba_data[['postal_code', 'other_area_km2']]
    
    # Aggregating by summing the industrial areas in a new dataframe
    aggregation_functions = {'other_area_km2': 'sum'}
    pca_ba_data = pca_ba_data.groupby(pca_ba_data['postal_code']).aggregate(aggregation_functions)
    
    # Concat the industrial area data into the statistics dataframe
    pca_data = pca_data.merge(pca_ba_data, on='postal_code', how='left')
    pca_data = pca_data.fillna(0)
    
    # industrial area precentage calcultion
    pca_data['other_area_precentage'] = precentage(pca_data['total_area_km2'], pca_data['other_area_km2'])
    
    return pca_data

########

def dominant_land_use(land_use_data):
    '''
    Calculates dominant land land use types i
    '''
    land_use_data = land_use_data.fillna(0)
    land_use_copy = land_use_data
    land_use_copy = land_use_data[['other_area_precentage', 'industrial_area_precentage', 'green_area_precentage',]]
    land_use_copy = land_use_copy.rename(columns = {'other_area_precentage':'Residential or commercial', 
                                                    'industrial_area_precentage':'Industrial', 
                                                    'green_area_precentage':'Green area'}) 
    
    land_use_copy['dominant_land_use'] = land_use_copy.idxmax(axis=1)
    land_use_copy = land_use_copy[['dominant_land_use']]
    land_use_data = land_use_data.join(land_use_copy)

    return land_use_data
    
########

def visualize_land_use(data, postal_code, save):
    '''
    Plot land use data from the data made with the other tools in this file. 
    
    Does not return a variable.
    Saves the plot as a png if save variable is defined as a string 'yes'.
    '''
    # Make new dataframe to process
    plot_data = data[['postal_code', 'name', 'green_area_precentage', 'industrial_area_precentage', 'other_area_precentage']]
    plot_row = plot_data[plot_data['postal_code'] == postal_code] 
    
    # Define names and values from the selected data
    names = ['Green area', 'Industrial area', 'Other land use']
    values = [plot_row.iloc[0]['green_area_precentage'], plot_row.iloc[0]['industrial_area_precentage'], plot_row.iloc[0]['other_area_precentage']]

    # Plot
    plt.bar(names, values, color='#6dc296')
    plt.suptitle('Land use precentages in ' + plot_row.iloc[0]['name'], color='#383838')
    
    if save == True:
        plt.savefig('land_use_in_' + postal_code + '.png', dpi=600)
    
    else:
        plt.show()