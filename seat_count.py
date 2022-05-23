# %%
import pandas as pd 
import requests
import json 
import datetime 
import pytz
# pd.set_option("display.max_rows", 100)

fillo = 'https://interactive.guim.co.uk/docsdata/11WneZFp0CwnkDiBtQTTH_y-OjSzAlZR4c6rCPrQ_baA.json'
#%%

r = requests.get(fillo)
jsony = json.loads(r.text)

#%%


# records = jsony['sheets']['seat leaders']
records = jsony['sheets']['electorates']

data = pd.DataFrame.from_records(records)

#%%

df = data.copy()
# 'electorate', 'state', 'prediction', ''

# print(p['prediction'].unique().tolist())
# 'NAT', 'LNP', 'LIB', 'KAP', 'IND', 'GRN', 'CA', 'ALP', 
# 'ALP leading', 'LNP leading', 'LIB leading', 'IND leading',
# 'GRN leading ALP', 'NAT leading IND', 'ALP leading GRN'
 
df['Count'] = 1
df.loc[df['prediction'] == '', 'prediction'] = "Too close to call"
df.loc[df['prediction'].isin(['NAT', 'LNP', 'LIB']), 'prediction'] = 'Coalition'
df.loc[df['prediction'].isin(['ALP']), 'prediction'] = 'Labor'


# df.loc[df['prediction'].isin(['NAT leading IND', 'LNP leading', 'LIB leading']), 'prediction'] = 'Coalition leading'

# df.loc[df['prediction'].isin(['ALP leading GRN', 'ALP leading']), 'prediction'] = 'ALP leading'

df.loc[df['prediction'].isin(['KAP', 'IND', 'GRN', 'CA']), 'prediction'] = 'Other/independent'
# df.loc[df['prediction'].isin(['GRN leading ALP', 'IND leading']), 'prediction'] = 'Other leading'


grp = df.groupby(by=['prediction'])['Count'].sum().reset_index()
# grp = grp.loc[grp['prediction'].isin(['Coalition', 'Labor'])]

p = grp

# vchecker = 'gdp_per_capita'
# print(p.loc[p[vchecker].isna()])
print(p)
print(p.columns.tolist())
# print(p['prediction'].unique().tolist())
# print(p['Count'].sum())

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
syd_now = utc_now.astimezone(pytz.timezone("Australia/Sydney"))

syd_now = syd_now.strftime('%I:%M%p %d %b')
print(syd_now)

# %%
grp['Color'] = '#b51800'
grp.loc[grp['prediction'] == 'Coalition', 'Color'] = '#005689'
grp.loc[grp['prediction'] == 'Other/independent', 'Color'] = '#4e0375'
grp.loc[grp['prediction'] == 'Too close to call', 'Color'] = '#7d7569'

final = grp.to_dict(orient='records')

template = [
	{
	"title": "House of representatives results",
	"subtitle": f"Showing the number of seats predicted for each party. 76 seats are required to form government. Last updated {syd_now}",
	"footnote": "",
	"source": "Australian Electoral Commission, Guardian Australia",
	"margin-left": "20",
	"margin-top": "30",
	"margin-bottom": "20",
	"margin-right": "10"
	}
]



from yachtcharter import yachtCharter
# testo = "-testo"
testo = ''
chart_key = f"oz-datablogs-election-results-bars{testo}"
yachtCharter(template=template, 
			data=final,
			chartId=[{"type":"horizontalbar"}],
            options=[{"enableShowMore":"False", "autoSort":"FALSE"}],
			chartName=f"{chart_key}")