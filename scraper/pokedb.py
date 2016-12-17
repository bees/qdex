from bs4 import BeautifulSoup
import lxml
import requests
import re
import pprint
import json
import time
import ipdb

from tokenize import tokenize

TMAP = {
    'evYield': 'EV yield',
    'catchRate': 'Catch rate',
    'happiness': 'Base Happiness',
    'exp': 'Base EXP',
    'levelingRate': 'Growth Rate'
}

BMAP = {
    'hp': 'HP',
    'atk': 'Attack',
    'def': 'Defense',
    'spAtk': 'Sp. Atk',
    'spDef': 'Sp. Def',
    'spd': 'Speed'
}

def poke_request(name):
    name = name.replace(' ', '-').lower()
    res = requests.get('http://pokemondb.net/pokedex/' + name)
    return BeautifulSoup(res.text, 'lxml')

def poke_moves_request(name):
    name = name.replace(' ', '-').lower()
    res = requests.get('http://pokemondb.net/pokedex/' + name + '/moves/7')
    return BeautifulSoup(res.text, 'lxml')


def poke_scrape(soup, name):
    try:
        info = {
            'name': name,
            'types': [],
            'stats': {
                'hp': {},
                'atk': {},
                'def': {},
                'spAtk': {},
                'spDef': {},
                'spd': {}
            },
            'abilities': {
                'normal': [],
                'hidden': []
            },
            'training': {
                'evYield': '',
                'catchRate': 0,
                'exp': 0,
                'happiness': 0,
                'levelingRate': ''
            },
            'breeding': {
                'eggGroups': [],
                'cycles': 0,
                'male': 0,
                'female': 0
            },
            'locations': [],
            'attackSets': {
                'learn': [],
                'tm': [],
                'evolution': [],
                'tutor': [],
                'breed': []
            },
            'typeDefenses': [],
            'evolutions': []
        }


        info['types'] = [a.text for a in soup.find('th', text='Type').parent.td.find_all('a')]

        for key in BMAP:
            stats_list = [stat for stat in soup.find('th', text=BMAP[key]).parent.find_all('td')]
            info['stats'][key]['base'] = int(stats_list[0].text)
            info['stats'][key]['min'] = int(stats_list[2].text)
            info['stats'][key]['max'] = int(stats_list[3].text)

        for key in TMAP:
            stats_list = [stat for stat in soup.find('th', text=TMAP[key]).parent.find_all('td')]
            if (key == 'catchRate' or key == 'exp' or key == 'happiness'):
                val = re.sub(r'\(.*?\)', '', str(stats_list[0].text))
                info['training'][key] = int(val)
            else:
                val = re.sub('[^A-Za-z0-9 ]+', '', stats_list[0].text)
                info['training'][key] = val

        info['breeding']['eggGroups'] = [a.text for a in soup.find('th', text='Egg Groups').parent.td.find_all('a')]
        info['breeding']['male'] = int(re.sub("[^0-9]", "", soup.find('span', class_='gender-male').text))
        info['breeding']['female'] = int(re.sub("[^0-9]", "", soup.find('span', class_='gender-female').text))
        info['breeding']['cycles'] = int(re.sub('[^A-Za-z0-9 ]+', '', re.sub(r'\(.*?\)', '', soup.find('th', text='Egg cycles').parent.find_all('td')[0].text))) 


        ability_list = [ability for ability in soup.find('th', text='Abilities').parent.find_all('td')[0].find_all('a')]
        info['abilities']['normal'] = [a.text for a in ability_list if a.parent.name != 'small']
        info['abilities']['hidden'] = [a.text for a in ability_list if a.text not in info['abilities']['normal']]




        parentDict = {}

        for table in soup.find_all('table', class_='type-table'):
            #TODO: this should be doable with a condition, see why 'in' doesn't work with table.parent
            try:
                parent_id = table.parent['id']
                if parent_id not in parentDict:
                    #TODO: remove 'ability'
                    parentDict[parent_id] = soup.find('a', href='#' + parent_id).text.replace(' ability', '')
                    info['typeDefenses'].append({'ability': parentDict[parent_id], 'types': {}})
            except:
                pass


            if parentDict:
                statSet = [stat for stat in info['typeDefenses'] if parentDict[parent_id] in stat['ability']][0]
                for td in table.parent.find_all('td'):
                    statSet['types'][td['title'].split()[0].lower()] = td.text
            else:
                if len(info['typeDefenses']) == 0:
                    info['typeDefenses'].append({'ability': 'default', 'types': {}})

                for td in table.parent.find_all('td'):
                    info['typeDefenses'][0]['types'][td['title'].split()[0].lower()] = td.text


        ths = soup.find_all('th')
        info['locations'] = [th for th in ths if 'Sun' in th.text][1].parent.td.text.split(', ')

        moup = poke_moves_request(name)
        tables = moup.find_all('table')

        for table in moup.select('h3 ~ .colset'):
            
            moves = table.find_all('td')
            h3 = table.parent.find_all('h3')[0]
            h3.extract()

            if h3.text == 'Moves learnt by level up':
                for i in range(0, len(moves), 6):
                    info['attackSets']['learn'].append({
                        'level': moves[i].text,
                        'name': moves[i+1].text,
                        'type': moves[i+2].text,
                        'category': moves[i+3]['data-filter-val'],
                        'power': moves[i+4].text,
                        'accuracy': moves[i+5].text
                    })

            elif h3.text == 'Egg moves':
                for i in range(0, len(moves), 5):
                    info['attackSets']['breed'].append({
                        'name': moves[i+0].text,
                        'type': moves[i+1].text,
                        'category': moves[i+2]['data-filter-val'],
                        'power': moves[i+3].text,
                        'accuracy': moves[i+4].text
                    })

            elif h3.text == 'Moves learnt on evolution':
                for i in range(0, len(moves), 5):
                    info['attackSets']['evolution'].append({
                        'name': moves[i+0].text,
                        'type': moves[i+1].text,
                        'category': moves[i+2]['data-filter-val'],
                        'power': moves[i+3].text,
                        'accuracy': moves[i+4].text
                    })

            elif h3.text == 'Move Tutor moves':
                for i in range(0, len(moves), 5):
                    info['attackSets']['tutor'].append({
                        'name': moves[i+0].text,
                        'type': moves[i+1].text,
                        'category': moves[i+2]['data-filter-val'],
                        'power': moves[i+3].text,
                        'accuracy': moves[i+4].text
                    })

            elif h3.text == 'Moves learnt by TM':
                for i in range(0, len(moves), 6):
                    info['attackSets']['tm'].append({
                        'tm': moves[i].text,
                        'name': moves[i+1].text,
                        'type': moves[i+2].text,
                        'category': moves[i+3]['data-filter-val'],
                        'power': moves[i+4].text,
                        'accuracy': moves[i+5].text
                    })


        with open(name + '.json', 'w') as f:
            json.dump(info, f)
    except:
        print(name)
        pass


def get_pokes():
    res = requests.get('http://pokemondb.net/pokedex/game/sun-moon')
    soup = BeautifulSoup(res.text, 'lxml')

    for poke in soup.select('li#island0 a.ent-name'):
        poke_scrape(poke_request(poke.text), poke.text) 
        time.sleep(.5)


if __name__ == '__main__':
    get_pokes()
    #poke_scrape(poke_request('Metapod'), 'Metapod') 
