#!/usr/bin/env python
# encoding: utf-8
# Create your views here.

import json
import csv
import codecs


def convert():
    with codecs.open('IOM-set-1.csv', 'rb') as csvfile:
    # with codecs.open('IOM-set-1.csv', 'rb') as csvfile:
    # with open('IOM-set-1.csv', 'rb', 'utf-8') as csvfile:
        my_data = csv.reader(csvfile, delimiter='\t', quotechar='"')
        data_list = []
        count = 0
        for item in my_data:
            if count != 0:
                data_dict = {
                    "question": {
                        "text": item[0],
                        "image": item[8]
                    },
                    "answer": {
                        "a": {
                            "text": item[1],
                            "image": item[9]
                        },
                        "b": {
                            "text": item[2],
                            "image": item[10]
                        },
                        "c": {
                            "text": item[3],
                            "image": item[11]
                        },
                        "d": {
                            "text": item[4],
                            "image": item[12]
                        },
                        "correct": item[5]
                    },
                    "subject": item[7],
                    "marks": int(item[13]),
                    "exam_code": int(item[6])
                }
                data_list.append(data_dict)
            count += 1
            if count == 101:
                break

        with open('302.json', 'w') as jsonfile:
            json.dump(data_list, jsonfile)

convert()
