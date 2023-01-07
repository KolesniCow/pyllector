from pyllector.sync.client import ApiCollector

import asyncio


def main():
    collector = ApiCollector('https://vk.com')
    print(collector.push())


if __name__ == '__main__':
    main()