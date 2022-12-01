import logging
import asyncio
import aiohttp
import bs4

from aiohttp_requests import requests

ROOT = 'https://www.nutanix.com'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

log = logging.getLogger()

def main(loop):
    result = asyncio.run_coroutine_threadsafe(get_links(ROOT), loop)
    print(result.result())

async def get_links(url):
    response = await requests.get(url)
    return response
    print(dir(response))
    text = await response.text()
    print(text)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()    
    main(loop)
#     loop.run_until_complete(main())    
