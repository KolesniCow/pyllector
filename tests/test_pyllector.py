import logging

from pyllector import ApiClient

logging.basicConfig()


def main():
    collector = ApiClient('https://vk.com')
    print(collector.push())


if __name__ == '__main__':
    main()
