# coding=utf-8
from twython import Twython
from difflib import get_close_matches
from collections import OrderedDict
import json
import arrow

APP_KEY = '***'
APP_SECRET = '***'
twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens()
OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']


bezirke = ['CharlottenburgNord', 'Malchow', 'Altglienicke', 'Adlershof', 'Dahlem', 'Tiergarten', 'Hansaviertel', 'FalkenhagenerFeld', 'Wilhelmstadt', 'Rahnsdorf', 'Tegel', 'Rosenthal', 'Britz', 'AltTreptow', 'Charlottenburg', 'Heiligensee', 'Mitte', 'Buckow', 'Kreuzberg', 'Zehlendorf', 'Gesundbrunnen', 'Wannsee', 'Nikolassee', 'Luebars', 'Haselhorst', 'Koepenick', 'Buckow2', 'Baumschulenweg', 'Wedding', 'Gruenau', 'Blankenburg', 'Lichtenberg', 'Karlshorst', 'PrenzlauerBerg', 'Pankow', 'Bohnsdorf', 'Hermsdorf', 'Lankwitz', 'Wartenberg', 'Plaenterwald', 'Neukoelln', 'Wilmersdorf', 'Moabit', 'Hakenfelde', 'Rudow', 'Marienfelde', 'Wittenau', 'Reinickendorf', 'Kladow', 'Grunewald', 'Niederschoeneweide', 'Karow', 'Friedrichshain', 'FranzoesischBuchholz', 'Frohnau', 'Mueggelheim', 'Niederschoenhausen', 'Oberschoeneweide', 'Lichterfelde', 'Mariendorf', 'Wilhelmsruh', 'Konradshoehe', 'Biesdorf', 'Rummelsburg', 'Lichtenrade', 'Westend', 'Waidmannslust', 'Halensee', 'Friedrichshagen', 'Buch', 'MaerkischesViertel', 'Falkenberg', 'Fennpfuhl', 'Gropiusstadt', 'Tempelhof', 'NeuHohenschoenhausen', 'Blankenfelde', 'Johannisthal', 'Friedenau', 'Heinersdorf', 'Gatow', 'Mahlsdorf', 'Hellersdorf', 'Kaulsdorf', 'Marzahn', 'Friedrichsfelde', 'AltHohenschoenhausen', 'Weissensee', 'Steglitz', 'Spandau', 'Staaken', 'Schmoeckwitz', 'Schoeneberg', 'Schmargendorf', 'Siemensstadt' ]
tweets = list()
all_hashtags = dict()
all_bezirke = dict()
done_ids = list()

for p in range(1000):
    results = twitter.get_user_timeline(screen_name='PolizeiBerlin_E', count=200, page=p)
    if len(results) == 0: break

    for tweet in results:
        hash_tags = list()
        for h in tweet['entities']['hashtags']:
            hash_tags.append(h['text'])

        if '24hPolizei' in hash_tags:# and not tweet['in_reply_to_screen_name']:
            t = OrderedDict()
            t['bezirk']     = ''
            t['text']       = tweet['text']
            t['hashtags']   = hash_tags
            t['time']       = arrow.get(tweet['created_at'], 'ddd MMM DD HH:mm:ss Z YYYY').format('YYYYMMDDHHmmss')
            t['id']         = tweet['id']
            t['url']        = 'https://twitter.com/{}/status/{}'.format( 'PolizeiBerlin_E', tweet['id'] )

            if int(t['time'][:4]) < 2015:
                continue

            for h in hash_tags:

                if not h in ['24hPolizei',]:
                    b = get_close_matches(h, bezirke, n=1)
                    if len(b) == 1:
                        t['bezirk']= b[0]
                        if b[0] in all_bezirke:
                            all_bezirke[b[0]] += 1
                        else:
                            all_bezirke[b[0]] = 1

                if h in all_hashtags:
                    all_hashtags[h] += 1
                else:
                    all_hashtags[h] = 1


            if t['id'] not in done_ids:
                tweets.append(t)
                done_ids.append(t['id'])
                t['hashtags'] = ';'.join(t['hashtags'])
            # else:
            #     print('duplicate:', t)

json.dump(tweets, open('24hPolizei_2015.json', 'w'), indent=2, ensure_ascii=False, sort_keys=False)