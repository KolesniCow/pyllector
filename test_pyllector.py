from pyllector import ApiCollector

import asyncio


async def main():
    collector = ApiCollector('https://vk.com')
    print(await collector.push(cookies={}))


if __name__ == '__main__':
    asyncio.run(main())