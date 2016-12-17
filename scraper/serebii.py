from bs4 import BeautifulSoup
import lxml
import requests



def pokeRequest(name):
    name = name.replace(' ', '-').lower()
    res = requests.get('http://bulbahandbook.bulbagarden.net/pokemonsunmoon/pokemon/' + name)
    return BeautifulSoup(res.text, 'lxml')


def pokeScrape(soup):
    stats = {
        'types': [],
        'base': {
            'hitpoints': 0,
            'attack': 0,
            'sAttack': 0,
            'defense': 0,
            'sDefense': 0,
            'speed': 0
        },
        'abilities': [],
        'hiddenAbilities': '',
        'locations': [],
        'attackSets': {
            'learn': [],
            'tm': [],
            'breed': [],
            'tutoring': []
        },
        'levelingRate': '',
        'hatchTime': '',
        'evolutions': []
    }

    for li in soup.find(class_='poke-card__types'):
        stats['types'].append(li.span.text)

    print(stats['types'])

    stats['base']['hitpoints'] = soup.find(class_='poke-card__stats__hp').span.text
    stats['base']['attack'] = soup.find(class_='poke-card__stats__atk').span.text
    stats['base']['sAttack'] = soup.find(class_='poke-card__stats__sp-atk').span.text
    stats['base']['defense'] = soup.find(class_='poke-card__stats__def').span.text
    stats['base']['sDefense'] = soup.find(class_='poke-card__stats__sp-def').span.text
    stats['base']['speed'] = soup.find(class_='poke-card__stats__spd').span.text
    print(stats['base'])

    abilities_info = soup.find("h2", text="Abilities" ).next_sibling()
    abilities_filtered = ([dd for dd in abilities_info if BeautifulSoup(str(dd), 'xml').dd])
    abilities_soup = abilities_filtered[0]
    stats['abilities'] = [a.text for a in abilities_soup.find_all("a")]
    print(stats['abilities'])

    hidden_soup = abilities_filtered[1]
    stats['hiddenAbilities'] = [a.text for a in hidden_soup.find_all("a")]
    print(stats['hiddenAbilities'])

    #stats['abilities'] = [a for a in abilities_info[1]]
    #print(stats['abilities'][0])
    

pokeScrape(pokeRequest('Alolan Rattata'))
