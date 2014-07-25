#!/usr/bin/env python
# encoding: utf-8
# Create your views here.

import json
import csv
import time
import datetime


def convert(csv_file_name):
    with open(csv_file_name, 'r') as csvfile:
    # with codecs.open('IOM-set-1.csv', 'rb') as csvfile:
    # with open('IOM-set-1.csv', 'rb', 'utf-8') as csvfile:
        time_stamp = int(
            time.mktime(
                datetime.datetime.now().timetuple()
            )
        )
        my_data = csv.reader(csvfile, delimiter=',', quotechar='"')
        data_list = []
        count = 0
        for item in my_data:
            if count != 0:
                data_dict = {
                    "question": {
                        "text": item[0],
                        "image": item[7]
                    },
                    "answer": {
                        "a": {
                            "text": item[1],
                            "image": item[8]
                        },
                        "b": {
                            "text": item[2],
                            "image": item[9]
                        },
                        "c": {
                            "text": item[3],
                            "image": item[10]
                        },
                        "d": {
                            "text": item[4],
                            "image": item[11]
                        },
                        "correct": item[5].lower()
                    },
                    "subject": item[6].lower(),
                    "marks": 1,
                    "exam_type": 'MEDICAL',
                    "exam_code": time_stamp
                }
                data_list.append(data_dict)
            count += 1
            if count == 101:
                break

        with open(csv_file_name + "-json.json", 'w') as outfile:
            json.dump(data_list, outfile, ensure_ascii=False)

for i in range(1, 8):
    time.sleep(1)
    convert('apps/exam_api/iom-new/set-' + str(i) + '.csv')
