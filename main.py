import threading
from parsers.iz_parser import iz_parser
from parsers.ria_parser import ria_parser
from parsers.sport_parser import sport_parser


def main():
    thread1 = threading.Thread(target=iz_parser)
    thread2 = threading.Thread(target=ria_parser)
    thread3 = threading.Thread(target=sport_parser)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()


if __name__ == "__main__":
    main()
