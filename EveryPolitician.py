from collections import defaultdict
from everypolitician import EveryPolitician


def getcurrentlegislators():
    import urllib.request, json
    ep = EveryPolitician()

    epusa = ep.country('United-States-of-America')
    epussenate = epusa.legislature('Senate')
    with urllib.request.urlopen(epussenate.popolo_url) as url:
        senatedata = json.loads(url.read().decode())
    epUSHouse = epusa.legislature('House')
    with urllib.request.urlopen(epUSHouse.popolo_url) as url:
        housedata = json.loads(url.read().decode())

    return housedata, senatedata


def getlegislators(legislaturedata):
    legislatorcount = {}
    legislatormap = {}

    position_by_area = {}
    for position in legislaturedata['memberships']:
        if position['legislative_period_id'] == currentlegislature:
            position_by_area[position['area_id']] = position
    person_by_id = {}
    for person in legislaturedata['persons']:
        person_by_id[person['id']] = person
    organization_by_id = {}
    for organization in legislaturedata['organizations']:
        organization_by_id[organization['id']] = organization['name']
        legislatorcount[organization['name']] = 0
    for state in legislaturedata['areas']:
        legislatormetadata = {}
        print(state['name'])

        try:
            position = position_by_area[state['id']]
            person = person_by_id[position['person_id']]
            legislatormetadata['name'] = person['given_name'] + ' ' + person['family_name']
            legislatormetadata['party'] = organization_by_id[position['on_behalf_of_id']]
            print(person['given_name'], person['family_name'], organization_by_id[position['on_behalf_of_id']])
            legislatorcount[organization_by_id[position['on_behalf_of_id']]] = legislatorcount[organization_by_id[
                position['on_behalf_of_id']]] + 1
            legislatormap[state['name']] = legislatormetadata
        except TypeError:
            print('No Representative')
        except KeyError:
            print('No Representative')
    print(legislatorcount)
    return legislatorcount, legislatormap


housedata, senatedata = getcurrentlegislators()
currentlegislature = housedata['events'][-1]['id']
housecount, housemap = getlegislators(housedata)
senatecount, senatemap = getlegislators(senatedata)
