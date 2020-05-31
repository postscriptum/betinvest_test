from aiohttp import web
import aiohttp_jinja2
import jinja2
import redis
import datetime


redis_events = redis.Redis(host='localhost', port=6379, db=1)
redis_sections = redis.Redis(host='localhost', port=6379, db=2)
status_codes = {
    b'2': 'Live',
    b'3': 'Completed',
    b'4': 'Canceled',
}


@aiohttp_jinja2.template('results.html')
def handle(request):
    results = []
    begin_str = request.match_info.get('begin_str')
    for section_name in redis_sections.scan_iter():
        section = {
            'name': section_name.decode(),
            'events': [],        
        }
        event_ids = redis_sections.lrange(section_name, 0, -1)
        for event_id in event_ids:
            event = redis_events.hgetall(event_id)
            event_name = event[b'name'].decode()
            if begin_str is None or event_name.startswith(begin_str):
                section['events'].append({
                    'name': event_name,
                    'score': event[b'score'].decode(),
                    'start_time': datetime.datetime.fromtimestamp(
                        int(event[b'startTime'].decode())).strftime(
                        '%d %b %Y at %H:%M'),
                    'status': status_codes.get(event[b'status'], ''),
                    'comment': event[b'comment1'].decode() +
                               event[b'comment2'].decode() +
                               event[b'comment3'].decode(),
                })
        if section['events']:
            results.append(section)
    return {'results': results}


app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('./templates'))
app.add_routes([web.get('/', handle),
                web.get('/{begin_str}', handle)])


if __name__ == '__main__':
    web.run_app(app)
