import pandas as pd
import urllib
import os



def download_data():
        
    url_to_nivo_data = 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Nivo/'


    list_month = ['0'+str(i) for i in range(1,10)] + [str(i) for i in range(10,13)]

    for ayear in np.arange(2010,2019,1) :
        for amonth in list_month :
            print(str(ayear)+amonth)
            urllib.request.urlretrieve(url_to_nivo_data+'Archive/nivo.'+str(ayear)+amonth+'.csv.gz',
                                   'data/'+str(ayear)+amonth+'.gz')
            try :
                _ = pd.read_csv('data/'+str(ayear)+amonth+'.gz',delimiter=';')
            except Exception:
                print('no data available for '+str(ayear)+amonth)
                os.remove('data/'+str(ayear)+amonth+'.gz')
