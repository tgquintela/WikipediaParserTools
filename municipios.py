

import wikipedia
import pandas as pd
import numpy as np
from utils import parse_excel_sheet, write_dataframe_to_excel

### Setting and parsing initial data
wikipedia.set_lang('es')
data = parse_excel_sheet('/home/tono/Documents/municipios-espana_2011.xls')
municipios15 = parse_excel_sheet('/home/tono/Documents/15codmun_table.xls')
municipios15 = list(municipios15['NOMBRE'])

### Uniforming data in order to parse wikipedia
## Observing differences
counts = {'intersect': 0, 'only_coord': 0, 'only_ine': 0}
lists = {'intersect': [], 'only_coord': [], 'only_ine': []}
for i in range(data.shape[0]):
    muni = data['municipio'][i]
    if muni in municipios15:
        counts['intersect'] += 1
        lists['intersect'].append(muni)
    else:
        counts['only_coord'] += 1
        lists['only_coord'].append(muni)

for i in range(len(municipios15)):
    muni_list = list(data['municipio'])
    muni = municipios15[i]
    if muni not in muni_list:
        counts['only_ine'] += 1
        lists['only_ine'].append(muni)

write_dataframe_to_excel(pd.DataFrame(lists['only_ine']),
                         '/home/tono/Documents/ine.xls')
write_dataframe_to_excel(pd.DataFrame(lists['only_coord']),
                         '/home/tono/Documents/coord.xls')

## Preparing and applying a mapping
mapping = parse_excel_sheet('/home/tono/Documents/Mappingdata.xls')
a = data[['municipio']]
b = data[['municipio']]
b.columns = b.columns = ['Nombre oficial']

data2 = pd.concat([a,b,data], axis=1)
munis_map = mapping['coord']
data2.columns = ['municipio', 'Nombre oficial', 'Nombre Wikipedia',
                 'provincia', 'comunidad', 'latitud', 'longitud',
                 'Enlace Google Maps']

for i in range(data2.shape[0]):
    muni = data2['municipio'][i]
    coincidences = np.where(munis_map == muni)[0]
    if coincidences.shape[0] == 1:
        data2['Nombre oficial'][i] = mapping[u'ine'][coincidences[0]]
        data2['Nombre Wikipedia'][i] = mapping[u'new'][coincidences[0]]
    elif coincidences.shape[0] > 1:
        print "Duplicates. "+muni

## Correct manually the rest of the data
data = parse_excel_sheet('/home/tono/Documents/municipios-espana_2014.xls')

extrainfo = []
for i in range(data2.shape[0]):
    results = wikipedia.geosearch(data2['latitud'][i], data2['longitud'][i],
                                  data2['Nombre Wikipedia'])
    infobox = parse_infobox(wikipedia.page(results[0]))
    extrainfo.append(infobox)
