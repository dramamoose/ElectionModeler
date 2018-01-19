from collections import defaultdict
from everypolitician import EveryPolitician


def getlegislators():
    housecounts = defaultdict(lambda:0)
    senatecounts = defaultdict(lambda: 0)
    nonvoting = ['American Samoa', 'District of Columbia', 'Guam', 'Northern Mariana Islands', 'Puerto Rico',
                 'US Virgin Islands']
    ep = EveryPolitician()
    epusa = ep.country('United-States-of-America')
    epussenate = epusa.legislature('Senate')
    epushouse = epusa.legislature('House')
    housedata = epushouse.latest_legislative_period().csv()
    senatedata = epussenate.latest_legislative_period().csv()
    housedata[:] = [entry for entry in housedata if entry.get('end_date') == '' and entry.get('area') not in nonvoting]
    senatedata[:] = [entry for entry in senatedata if entry.get('end_date') == '']
    for entry in housedata:
        housecounts[entry['group']] = housecounts[entry['group']] + 1
    for entry in senatedata:
        senatecounts[entry['group']] = senatecounts[entry['group']] + 1
    housecounts = dict(housecounts)
    senatecounts = dict(senatecounts)
    return housedata, senatedata, housecounts, senatecounts
currenthousemembers, currentsenatemembers, currenthousecounts, currentsenatecounts = getlegislators()

