"""Tests json output file
"""
import unittest
import json

import logging

logging.basicConfig(level=logging.DEBUG)


class TestJsonOutput(unittest.TestCase):

    def setUp(self):
        filename = 'apps/exam_api/iom-new/set-7.csv-json.json'
        json_data = open(filename).read()
        self.data = json.loads(json_data)
        self.NUMBER_OF_QUESTIONS = 100
        self.EXAM_TYPE = 'MEDICAL'
        self.EXAM_CODE = self.data[0]['exam_code']
        self.SUBJECT = {
            'physics': range(0, 20),
            'chemistry': range(20, 50),
            'botany': range(50, 70),
            'zoology': range(70, 100)
        }

    def test_overall_json(self):
        """total questions 100, all items are dicts"""
        assert len(self.data) == self.NUMBER_OF_QUESTIONS
        for item in self.data:
            assert isinstance(item, (dict))

    def test_single_structure(self):
        """ The  """
        test_data = ['subject', 'marks', 'question',
                     'exam_code', 'answer', 'exam_type']
        for item in self.data:
            assert sorted(item.keys()) == sorted(test_data)
            assert isinstance(item['marks'], int)
            assert isinstance(item['exam_code'], int)
            assert item['exam_type'] == self.EXAM_TYPE

    def test_question(self):
        """test each of the question ignoring the options"""
        log = logging.getLogger('test_question')
        for item in self.data:
            log.debug(item)
            assert 'question' in item
            assert 'text' in item['question']
            assert len(item['question']['text'].strip()) > 0
            # $ is closed in latex
            assert item['question']['text'].count('$') % 2 == 0
            # assert item['question']['text'] == item['question']['text'].strip()

    def test_options(self):
        """test options in each of the questions"""
        log = logging.getLogger('test_options')
        for item in self.data:
            assert 'answer' in item
            # ensue that all 4 options and correct are in dict
            assert len(item['answer']) == 5

            options = ['a', 'b', 'c', 'd', 'correct']
            # print(item)
            for each_option in options:
                # log.debug(item)
                # ensure option is in the list
                assert each_option in item['answer']
                # check value of each option
                if each_option != 'correct':
                    # log.debug(item)
                    # $ is closed in latex
                    assert item['answer'][each_option]['text'].count('$') % 2 == 0
                    assert 'text' in item['answer'][each_option]
                    option_text = item['answer'][each_option]['text']
                    assert len(option_text) > 0
                    # assert option_text.strip() == option_text

                else:
                    log.debug(item)
                    # ensure that the correct value is one of a, b, c or d.
                    assert item['answer'][each_option] in options[:4]

    def test_subject(self):
        """test options in subject of each question"""
        for count, item in enumerate(self.data):
            subject_lower = item['subject'].lower()
            assert subject_lower in self.SUBJECT
            assert count in self.SUBJECT[subject_lower]

    def test_exam_code_uniformity(self):
        """test option for each exam code to be same"""
        for item in self.data:
            assert item['exam_code'] == self.EXAM_CODE


if __name__ == '__main__':
    unittest.main()
