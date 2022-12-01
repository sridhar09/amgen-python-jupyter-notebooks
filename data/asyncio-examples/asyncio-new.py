import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

log = logging.getLogger()

def main():
    loop = asyncio.get_event_loop()    
    loop.run_until_complete(asyncio.gather(coroutine_1(), coroutine_2()))
    
    
async def coroutine_1():
    log.info('coroutine_1 is active on the event loop')

    log.info('coroutine_1 yielding control. Going to be blocked for 4 seconds')
    value = await asyncio.sleep(4)

    log.info('coroutine_1 resumed. coroutine_1 exiting with %s', value)
    

async def coroutine_2():
    log.info('coroutine_2 is active on the event loop')

    log.info('coroutine_2 yielding control. Going to be blocked for 5 seconds')
    await asyncio.sleep(5)

    log.info('coroutine_2 resumed. coroutine_2 exiting')
    

if __name__ == '__main__':
    main()
