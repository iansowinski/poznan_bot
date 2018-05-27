import redis
import json
import prm

client = redis.StrictRedis(host='redis', port=6379, db=0)

while True:
    location_to_process = client.rpop('rowery')
    if location_to_process != None:
        message = json.loads(location_to_process.decode("utf-8"))
        data = prm.stations_from_coords('Poznan', [message['lat'], message['lng']], 5)

        response = '🚲 *Najbliższe stacje od Ciebie o* ' + str(data[0]['time']) +'*: *  \n\n'
        cond = ['2', '3', '4']

        for item in data:
            if item['bikes'] == '1':
                grammar_message_bike = ' rower'
            elif item['bikes'] in cond:
                grammar_message_bike = ' rowery'
            else:
                grammar_message_bike = ' rowerów'

            if item['free_racks'] == '1':
                grammar_message_racks = ' wolny zamek'
            elif item['free_racks'] in cond:
                grammar_message_racks = ' wolne zamki'
            else:
                grammar_message_racks = ' wolnych zamków'

            response = str(response) + str(item['label']) + ' - ' + str(item['distance']) + ' m' + ':' + '\n   ' + str(item['bikes']) + grammar_message_bike + ' _(' + str(item['free_racks']) + '/' + str(item['bike_racks']) + grammar_message_racks + ')_' + '\n'

        client.set(message['id'], response)