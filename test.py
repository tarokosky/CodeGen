#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import random
import sqlite3
import time
import os

def test1():
    t1 = time.time()
    time.sleep(1)
    t2 = time.time()
    print("t1 = %d, t2 = %d" % (t1, t2))
    print("Delta = %d" % (t2 - t1))

    t1 = time.monotonic()
    time.sleep(1)
    t2 = time.monotonic()
    print("t1 = %d, t2 = %d" % (t1, t2))
    print("Delta = %d" % (t2 - t1))

    t1 = time.monotonic_ns()
    time.sleep(1)
    t2 = time.monotonic_ns()
    print("t1 = %d, t2 = %d" % (t1, t2))
    print("Delta = %d" % (t2 - t1))

def main():
    test1()

if __name__ == '__main__':
    main()
