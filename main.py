import argparse
import glob
import logging
import os
import shutil
from threading import Thread, Semaphore


logging.basicConfig(filename='history.log', level=logging.DEBUG)


def copy(src, dst):
    if '.' in src:
        if '*' in src:
            aster = src.find('*')
            file_filter = src[aster:]
            src_dir = src.rfind('/')
            for filename in glob.glob(os.path.join(src[:src_dir], file_filter)):
                t = Thread(target=shutil.copy(filename, dst), args=(s,))
                t.start()
                logging.info(filename + " is copied")
        else:
            shutil.copy(src, dst)
            logging.info("file is copied")
    else:
        shutil.copytree(src, dst)
        logging.info("directory is copied")


def move(src, dst):
    if '*' in src:
        aster = src.find('*')
        file_filter = src[aster:]
        src_dir = src.rfind('/')
        for filename in glob.glob(os.path.join(src[:src_dir], file_filter)):
            t = Thread(target=shutil.move(filename, dst), args=(s,))
            t.start()
            logging.info(filename + " is moved")
    else:
        shutil.move(src, dst)
        logging.info("directory is moved")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--operation", action="store", help="copy or move")
    parser.add_argument("--src", type=str, action="store", help="source directory or file")
    parser.add_argument("--dst", type=str, action="store", help="destination directory or file")
    parser.add_argument("--threads", action="store", help="amount of threads", default=1)
    args = parser.parse_args()
    s = Semaphore(args.threads)
    if args.operation == 'copy':
        copy(args.src, args.dst)
    elif args.operation == 'move':
        move(args.src, args.dst)
    else:
        logging.error("Incorrect operation")
