# MAIN.PY FILE FOR INTERACTIVE CHURCH GUIDE MAP

# IMPORTED LIBRARIES
import numpy as np
import pandas as pd
import folium
import geopandas as gpd
# PANDAS WARNING THAT DOESN'T ALLOW CHAINED ASSIGNEMENTS TURNED OFF
pd.options.mode.chained_assignment = None  # default='warn'

# BRINGING IN EXCEL DATA INTO PROGRAM
countyReligious_data = pd.read_excel ("2020_USRC_Group_Detail1.xlsx", sheet_name = '2020 Group by County')
countyReligious_summary = pd.read_excel ("2020_USRC_Summaries.xlsx", sheet_name = "2020 County Summary")

# MY ATTEMPT AT BRINGING IN DEMOGRAPHIC DATA (THIS PART WORKS)
'''countyDemographic_data = pd.read_excel ("cc-est2022-all1.xlsm")
countyDemographic_data_refined1 = countyDemographic_data[countyDemographic_data['YEAR'] == 1]
countyDemographic_data_refined2 = countyDemographic_data_refined1[countyDemographic_data_refined1['AGE GROUP'] == 0]

countyDemographic_data_final = countyDemographic_data_refined2[['GEOID', 'YEAR', 'AGE GROUP', 'TOTAL POPULATION', 'TOTAL MALE', 'TOTAL FEMALE', 'WHITE ALONE MALE', 
                                                        'WHITE ALONE FEMALE', 'BLACK ALONE MALE', 'BLACK ALONE FEMALE', 
                                                        'AMERICAN INDIAN AND ALASKIAN NATIVE ALONE MALE', 'AMERICAN INDIAN AND ALASKIAN NATIVE ALONE FEMALE',
                                                        'ASIAN ALONE MALE', 'ASIAN ALONE FEMALE', 'NATIVE HAWIAN OR OTHER PACIFIC ISLANDER ALONE MALE'
                                                        , 'NATIVE HAWIAN OR OTHER PACIFIC ISLANDER ALONE FEMALE']]
#print(countyDemographic_data_refined_final)'''

# TESTING TO MAKE SURE EXCEL DATA GOT INTO THE PROGRAM
'''print(countyReligious_data)

#print(countyReligious_data.head(5))'''

# TESTING OF DATA FRAMES WITH ARRAYS TO CHECK DATA
'''county_percent = np.array(countyReligious_data["Adherents as % of Total Population"])
state_name = np.array(countyReligious_data["State Name"])
county_name = np.array(countyReligious_data["County Name"])
county_pop = countyReligious_summary[["State Name", "County Name", "2020 Population"]]'''

# TESTING THE FOLIUM MAP LIBRARY
'''JacksonMS_map = folium.Map(tiles = "CartoDB positron", location = (32.29, -90.1), zoom_start= 10)

JacksonMS_map.save('map.html')'''

# READING SHAPE FILE FOR MAP AND STORING AS A GEOGRAPHICAL DATA FRAME
gdf_counties = gpd.read_file("cb_2018_us_county_500k/cb_2018_us_county_500k.shp")

# REFINGING AND MERGING GEOGRAPHICAL AND STATISTICAL DATA FROM THE DIFFERENT DATAFRAMES
CountyReligious_data_refined_southernbaptist = countyReligious_data[countyReligious_data['Group Name'] == 'Southern Baptist Convention']
gdf_merged = gdf_counties.merge(CountyReligious_data_refined_southernbaptist, on='GEOID', how = 'outer')

# MY ATTEMPT AT BRINGING IN DEMOGRAPHCIAL DATA, THE GEOID NUMBER WAS READING AS AN INT INSTEAD OF AN OBJECT AND THEREFORE DIDN'T MERGE CORRECTLY
'''gdf_merged = gdf_merged.merge(countyDemographic_data_final, on = 'GEOID')'''

# MORE REFINEMENT OF DATA
gdf_merged_refined = gdf_merged[['GEOID', 'State Name', 'County Name', 'NAME', 'Group Code', 'Group Name',
                                 'Congregations', 'Adherents', 'Adherents as % of Total Adherents', 'Adherents as % of Total Population', 
                                 'ALAND', 'AWATER', 'geometry']]
gdf_merged_refined[['State Name', 'County Name', 'Group Code',]] = gdf_merged_refined[['State Name', 'County Name', 'Group Code',]].fillna('Not Available')
gdf_merged_refined['Group Name'] = gdf_merged_refined['Group Name'].fillna('Southern Baptist Convention')
gdf_merged_refined[['Congregations', 'Adherents', 'Adherents as % of Total Adherents', 'Adherents as % of Total Population']] = gdf_merged_refined[['Congregations', 
'Adherents', 'Adherents as % of Total Adherents', 'Adherents as % of Total Population',]].fillna(0)
gdf_merged_refined = gdf_merged_refined.drop(3233)

# NOTES FROM PAST SELF
''' Refine the Religious data first then merge with the counties'''

# TESTING OF DATA 
'''print(gdf_merged_refined)
print(gdf_merged_refined.columns)

print(gdf_merged_refined.isnull().sum())'''

# TEST OF GEOGRAPHICAL DATA FRAME
'''gdf_merged_refined.to_excel('gpd.xlsx')
#USCounties_map = gdf_counties.explore()
#USCounties_southernbaptist_map = gdf_merged_refined.explore(column = "Adherents as % of Total Adherents", name = "Need Based Upon Adherents as % of Total Population")

#USCounties_map.save('map1.html')
#USCounties_southernbaptist_map.save('Southern_Baptist_Convention_Map.html')'''

# FOLIUM MAP
USCounties_southernbaptist_map1 = folium.Map(location = [44, -103], tiles = 'CartoDB positron', zoom_start = 4)

# TOOLTIP FOR MAP
tooltip = folium.features.GeoJsonTooltip(fields =['GEOID', 'State Name', 'County Name', 'NAME', 'Group Code', 'Group Name',
                                 'Congregations', 'Adherents', 'Adherents as % of Total Adherents', 'Adherents as % of Total Population', 
                                 'ALAND', 'AWATER'],
                                 labels = True,
                                 stick = False)
# ADD TILE LAYER FOR OPENSTREET MAP
folium.TileLayer("openstreetmap").add_to(USCounties_southernbaptist_map1)

# MAP CHOROPLETH
cpleth = folium.Choropleth(gdf_merged_refined, data = gdf_merged_refined, key_on = "feature.properties.NAME",
                           #DECLARING WHAT DATA TO BASE THE CHOROPLETH OFF OF 
                           columns = ['NAME', 'Adherents as % of Total Adherents'], 
                           fill_color = "RdYlGn",
                           legend_name = "Adherents as % of Total Adherents",
                           name = "Southern Baptist Convention Church Guide")
cpleth.geojson.add_child(tooltip)

# ADDIONG CHOROPLETH TO FOLIUM MAP WITH LAYER CONTROL
cpleth.add_to(USCounties_southernbaptist_map1)
folium.LayerControl().add_to(USCounties_southernbaptist_map1)

# ATTEMPT AT UTILIZING MARKERS FOR DIFFERENT DATA (TOO BUSY AND TOO MUCH DATA)
'''folium.Marker([-89.18136899999999, 37.046305],
              popup = '<strong>Location</strong>',
              tooltip = 'Hello World Test').add_to(USCounties_southernbaptist_map1)'''

# SAVING FOLIUM MAP AS AN HTML FILE
USCounties_southernbaptist_map1.save('Southern Baptist Convention Map1.html')

# NOTES FROM PAST SELF
'''FOr Loop to iterate and create markers and add data?

## Add Demographic data to Geo dataframe
## take out unneccesary data when hovering over
## Adjust zoom level? Or Starting cords'''