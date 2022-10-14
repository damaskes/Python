import json
import sys


class Data:
    def __init__(self):
        try:
            with open('data.json', 'r') as fn:
                self.data = json.load(fn)
            self.current_id = 0
        except FileNotFoundError:
            print('Create "data.json" file first by running "quest_writer.py" program')
            sys.exit()

    def get_current_data(self):
        return self.data[self.current_id]

    def set_data_id(self, data_id):
        self.current_id = int(data_id)
