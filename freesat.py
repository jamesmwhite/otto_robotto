import time
from datetime import datetime
import requests
import json

channels = {
        '600':'bbc2hd',
        '505':'bbc1hd',
        '10005':'itvhd',
        '1540':'channel4hd',
        '1547':'channel5',
        '1520':'film4'
        
    }

listings_dict = {}

def get_tv_listings():
    listings_dict.clear()
    chanstring = ''
    for chan in channels:
        if len(chanstring)==0:
            chanstring = '?channel={}'.format(chan)
        else:
            chanstring = '{}&channel={}'.format(chanstring, chan)
    # print chanstring
    req_string = 'https://www.freesat.co.uk/whats/tv-guide/api/0/{}'.format(chanstring)
    req_string_tomorrow = 'https://www.freesat.co.uk/whats/tv-guide/api/01/{}'.format(chanstring)
    print req_string

    r = requests.get(req_string)
    content = r.content
    j_today = json.loads(content.encode('utf-8'))

    r = requests.get(req_string_tomorrow)
    content = r.content
    j_tomorrow = json.loads(content.encode('utf-8'))

    now = datetime.now()
    listings = []
    try:
        for channel in j_today:
            listings.append(parse_channels(channel, now))
        for channel in j_tomorrow:
            listings.append(parse_channels(channel, now))
            
    except Exception as e:
        print e

    # return listings
    return_list = []
    channel_keys = listings_dict.keys()
    channel_keys.sort()
    for item in channel_keys:
        new_str = '-- {} --'.format(item)
        single_chan_dict = listings_dict[item]
        last_str = ''
        time_listings = single_chan_dict.keys()
        time_listings.sort()
        for aitem in time_listings:
            # if aitem == last_str:
            #     continue
            next_item = single_chan_dict[aitem]
            new_str = '{}\n{}'.format(new_str, next_item)
            # last_str = next_item
        return_list.append(new_str)
        
    return return_list

def parse_channels(channel, now):
    chanlistings = ''.encode('utf-8')
    chanid = channel['channelid']
    channame = channels[str(chanid)]
    if channame in listings_dict:
        single_chan_dict = listings_dict[channame]
    else:
        single_chan_dict = {}
    for event in channel['event']:
        name = event['name']
        start = time.strftime("%H:%M", time.localtime(event['startTime']))
        start_day = time.strftime("%d", time.localtime(event['startTime']))
        now_day = time.strftime("%d", time.localtime(time.time()))
        duration = event['duration']
        endtime = datetime.fromtimestamp(int(event['startTime']) + (int(duration)))
        if start_day == now_day:
            if endtime > now:
                encoded_name = name.encode('utf-8', errors='')
                start = start.encode('utf-8')
                chanlistings = '{}\n{} {}'.format(chanlistings, start, encoded_name)
                single_chan_dict[start] = '{} {}'.format(start, encoded_name)
    listings_dict[channame] = single_chan_dict
    return chanlistings

for l in get_tv_listings():
    print l