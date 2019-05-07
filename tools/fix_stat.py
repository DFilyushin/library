import re
import bson
from wiring import Wiring


def fix_stat():
    wiring = Wiring()
    cnt = 0
    stats = wiring.stat.collection.find({'resource': {"$regex": "/books/[a-z0-9]*/content$"}})
    for item in stats:
        resource = item['resource']
        id = str(item['_id'])
        find = re.findall(r'/books/([a-z0-9]*)/content$', resource)
        id_new = find[0]
        wiring.stat.collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'resource': id_new, 'action': 'bd'}})
        cnt += 1
    print('Book download: ' + str(cnt))

    cnt = 0
    stats = wiring.stat.collection.find({'resource': {"$regex": "/books/[a-z0-9]*$"}})
    for item in stats:
        resource = item['resource']
        id = str(item['_id'])
        find = re.findall(r'/books/([a-z0-9]*)$', resource)
        id_new = find[0]
        wiring.stat.collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'resource': id_new, 'action': 'bv'}})
        cnt += 1
    print('Book view: ' + str(cnt))

    cnt = 0
    stats = wiring.stat.collection.find({'resource': {"$regex": "/books/by_author/[a-z0-9]*$"}})
    for item in stats:
        resource = item['resource']
        id = str(item['_id'])
        find = re.findall(r'/books/by_author/([a-z0-9]*)$', resource)
        id_new = find[0]
        wiring.stat.collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'resource': id_new, 'action': 'av'}})
        cnt += 1
    print('Author view: ' + str(cnt))

    cnt = 0
    stats = wiring.stat.collection.find({'resource': {"$regex": "/books/by_genre/[a-z0-9]*$"}})
    for item in stats:
        resource = item['resource']
        id = str(item['_id'])
        find = re.findall(r'/books/by_genre/([a-z0-9]*)$', resource)
        id_new = find[0]
        wiring.stat.collection.update_one({'_id': bson.ObjectId(id)}, {'$set': {'resource': id_new, 'action': 'gv'}})
        cnt += 1
    print('Genres view: ' + str(cnt))
