import time
from datetime import datetime
import requests
import json

def get_tv_listings():
    channels = {
        '600':'bbc2hd',
        '505':'bbc1hd',
        '10005':'itvhd',
        '1540':'channel4hd',
        '1547':'channel5',
        '1520':'film4'
        
    }
    chanstring = ''
    for chan in channels:
        if len(chanstring)==0:
            chanstring = '?channel={}'.format(chan)
        else:
            chanstring = '{}&channel={}'.format(chanstring, chan)
    # print chanstring
    r = requests.get('https://www.freesat.co.uk/whats/tv-guide/api/0/{}'.format(chanstring))
    content = r.content
    # print 'woooooo'
    # print content
    j = json.loads(content.encode('utf-8'))
    now = datetime.now()
    listings = []
    for channel in j:
        chanlistings = ''
        chanid = channel['channelid']
        channame = channels[str(chanid)]
        chanlistings = '{}\n*************************************'.format(chanlistings)
        chanlistings = '{}\n{}'.format(chanlistings, channame)
        chanlistings = '{}\n*************************************'.format(chanlistings)
        for event in channel['event']:
            name = event['name']
            start = time.strftime("%H:%M", time.localtime(event['startTime']))
            duration = event['duration']
            endtime = datetime.fromtimestamp(int(event['startTime']) + (int(duration)))

            if endtime > now:
                # print '{} {}'.format(name.encode('utf-8'), start)
                chanlistings = '{}\n{} {}'.format(chanlistings, start, name.encode('utf-8'))
        listings.append(chanlistings)
    return listings

for l in get_tv_listings():
    print l