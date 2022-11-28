from pyllector import ApiCollector

import asyncio


async def main():
    collector = ApiCollector('https://vk.com')
    print(await collector.push())


if __name__ == '__main__':
    asyncio.run(main())