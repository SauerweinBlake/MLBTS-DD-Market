#%%
import requests
import pandas as pd
import datetime

#%%
listings_GET = requests.get("https://mlb23.theshow.com/apis/listings.json?type=mlb_card")
num_pages = listings_GET.json()['total_pages']

listings_all = []

for i in range(1,num_pages+1,1):
    resp = requests.get(f'https://mlb23.theshow.com/apis/listings.json?type=mlb_card&page={i}')
    listing_25 = resp.json()['listings']
    listings_all += listing_25

item_info = [x['item'] for x in listings_all]

#%%
base = pd.DataFrame.from_records(listings_all)
info = pd.DataFrame.from_records(item_info)

#%%
base.drop('item', axis=1, inplace=True)
full = pd.concat([base,info], axis=1)

#%%
full = full[(full['rarity'] == 'Gold') | (full['rarity'] == 'Silver') | (full['rarity'] == 'Diamond')][[
    'listing_name','best_sell_price','best_buy_price','name','rarity','team','ovr','series',
    'display_position','has_augment','augment_end_date','stars','trend','new_rank','has_rank_change','event',
    'set_name','is_live_set']].copy()
full['time'] = pd.to_datetime(datetime.datetime.now())

#%%
full.to_csv('Market_Data.csv',mode='a',header=False,index=False)

#%%