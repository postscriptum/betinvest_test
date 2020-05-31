import asyncio
import aiohttp
import datetime
import redis


now = round(datetime.datetime.now().timestamp())
req = {
    'url': 'https://clientsapi31.bkfon-resource.ru/results/results.json.php',
    'params': {
        'locale': 'en',
        'lastUpdate': 0,
        '_': now,
    }
}
redis_events = redis.Redis(host='localhost', port=6379, db=1)
redis_sections = redis.Redis(host='localhost', port=6379, db=2)


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(req['url'], params=req['params']) as response:
            results = await response.json()
            # store events to redis
            for event in results['events']:
                event_id = event['id']
                del event['id']
                redis_events.hmset(event_id, event)
            # store sections to redis
            for section in results['sections']:
                section_name = section['name']
                redis_sections.delete(section_name)
                redis_sections.rpush(section_name, *section['events'])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
