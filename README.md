# Final Assignment

### Status

Once you are finished with the final assignment, edit this readme and add "x" to the correct box:

* [x] Submitted

* [ ] I'm still working on my final assignment. 


## Green areas, land use and population growth
#### Population growth, land use and green areas
Green areas in cities area important to the well being of the people living there. In the notebook, I present tools that will give insight on how the green areas are distributed around the city using postal code area data with the land use data provided by cities. This notebook uses Helsinki as an example, but the tools area applicable to other cities in Finland too. Tools also include analytics for the population growth and land use distribution. The notebook also includes visualization functionalities, that will create an interactive map of the chosen area and a tool for visualizing the land use distribution in a given postal code area.

### Structure of this repository:
#### Readme: 
README.md
#### Notebook with example usage.
Green_areas_land_use_and_population_growth.ipynb
#### Functions-file with the raw tool codes.
functions.py
#### Example files: 
pop_growth_and_land_use_map.html


### Input data:
#### Postal code area statistics (Paavo-database) from the Statistics Finland.
http://www.stat.fi/org/avoindata/paikkatietoaineistot/paavo.html

WFS addresses:
http://geo.stat.fi/geoserver/postialue/wfs?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=postialue:pno_tilasto_2020&outputformat=JSON
http://geo.stat.fi/geoserver/postialue/wfs?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=postialue:pno_tilasto_2015&outputformat=JSON


#### Land usage polygons for the city that is analyzed. 
This example utilizes the data distributed by the Helsinki Region Infoshare.
https://hri.fi/data/fi/dataset/seutukartta

WFS addresses: 
https://kartta.hel.fi/ws/geoserver/avoindata/wfs?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=avoindata:Seutukartta_maankaytto_viheralueet&outputformat=JSON
https://kartta.hel.fi/ws/geoserver/avoindata/wfs?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=avoindata:Seutukartta_maankaytto_teollisuusalueet&outputformat=JSON
https://kartta.hel.fi/ws/geoserver/avoindata/wfs?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=avoindata:Seutukartta_maankaytto_rakennetut_alueet&outputformat=JSON


### Analysis steps:
#### Data fetching
The analysis starts with data fetching. These tools utilize any land usage polygon data and the Paavo-database data from Finland.

#### Data analysis
This part will create statistics into an variable that can be visualized. More detailed information can be found in the Notebook and in the function files.

### Results:
Results are displayed in the interactive map and in with the postal code land usage Visualizer. These can also be found in the Notebook. 



