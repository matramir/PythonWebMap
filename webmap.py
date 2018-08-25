import folium, pandas as pd,numpy as np

data = pd.read_csv('volcano_db.csv', encoding = "ISO-8859-1")
map = folium.Map(location =[-37.721037, -72.209377], zoom_start=6)

def color_producer(elevation):
    if elevation < 0:
        return 'blue'
    elif 0 <= elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

for column_value in ("Number", "Region", "Country", "Type", "Status", "Last Known"):
    data = data.drop(column_value, 1)

fg_geo = folium.FeatureGroup(name="Population")

fg_geo.add_child(folium.GeoJson(data=open("world.json", "r", encoding='utf-8-sig').read(),
style_function=lambda x: {'fillOpacity': 0.1, 'line_opacity' :0.1,'color':'gray','fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fg_geo)

intervals = np.arange(0, data.index.max(), 50)
fg = folium.FeatureGroup(name="Volcanoes")
for value in intervals:
    if value == intervals[-1]:
        a = value
        b = data.index.max()
    else:
        a = value
        b = value+50

    data_slice = data[a:b]
    lat=list(data_slice["Latitude"].round(3))
    lon=list(data_slice["Longitude"].round(3))
    ele=list(data_slice["Elev"])
    name=list(data_slice["Volcano Name"].str.replace("'",""))



    for lt, ln, el, nm in zip(lat, lon, ele, name):
        fg.add_child(folium.CircleMarker(location=[lt,ln],radius = 6, popup=nm+"\n Elevation: "+str(el)+" m.", fill_color=color_producer(el), fill=True,  color = 'grey', fill_opacity=0.7))

map.add_child(fg)
map.add_child(folium.LayerControl())


map.save("MapVol.html")
