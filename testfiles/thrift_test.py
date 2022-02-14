import sys

import requests
import os
import subprocess
import urllib.request
import time
import csv

"""
fileDir = "../warehouse_logfiles/warehouse_"

filepath = (fileDir + str(sys.argv[1]) + ".data")
filepath2 = (fileDir + str(sys.argv[2]) + ".data")

first_log = []
second_log = []

for line in reversed(list(open(filepath))):
    first_log.append(line)

for line in reversed(list(open(filepath2))):
    second_log.append(line)

if first_log[0][0] == second_log[0][0]:
    print("something went wrong")
elif first_log[0][-2] == second_log[0][-2]:
    print("something went wrong")
else:
    print("your sent process with thrift was successful")
    print("\n\n\n\n")
"""


def load_data(warehouse_id: int) -> list:
    try:
        file = open(
            #"D:\\UNI\\Aktuelles_Semester\\Verteilte_Systeme_WS21\\VS_Python\\warehouse_logfiles\\warehouse_"
            "C:\\PyghonProgramms\\warehouse_logfiles\\warehouse_"
            + str(warehouse_id) + ".data", "r+")
    except:
        file = open(
            #"D:\\UNI\\Aktuelles_Semester\\Verteilte_Systeme_WS21\\VS_Python\\warehouse_logfiles\\warehouse_"
            "C:\\PyghonProgramms\\warehouse_logfiles\\warehouse_"
            + str(warehouse_id) + ".data", "x")
        return list()
    csv_reader = csv.reader(file, delimiter="|")
    data = list(csv_reader)
    return data


list1 = load_data(int(sys.argv[1]))
list2 = load_data(int(sys.argv[2]))
list1_reversed = list1[::-1]
list2_reversed = list2[::-1]


amount_identical = False
ip_different = False

if list1_reversed[0][3] == list2_reversed[0][3] and list1_reversed[0][4] != list2_reversed[0][4] and list1_reversed[0][0] != list2_reversed[0][0]:
    amount_identical = True
    ip_different = True
else:
    print("something went wrong")


if amount_identical and ip_different:
    print("sending from a warehouse to another was successful !")
else:
    print("something went wrong")
