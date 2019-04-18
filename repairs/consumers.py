from channels.generic.websocket import WebsocketConsumer
import json
import os
from django.conf import settings
import repairs.backend.repair as repair

class RepairConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.repair_instance = repair.Repair('data/sample.csv')
        self.proposed = self.repair_instance.run()
        print(self.proposed)
        self.send_proposed()

    def send_proposed(self):
        self.send(json.dumps({
            'type': 'proposal',
            'attributes': self.repair_instance.attributes,
            'data': self.proposed[0]
        }))
        print(self.proposed[0])

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print("receeekiwejraowifjaioewjf ", text_data)
        if text_data == '':
            return
        selection = json.loads(text_data)

        if selection['type'] == 'repair':
            self.repair_instance.replace(self.proposed[0], selection['selection'])

            self.proposed.pop(0)

            if len(self.proposed):
                self.send_proposed()
            else:
                self.send(json.dumps({
                    'type': 'done',
                    'attributes': self.repair_instance.attributes,
                    'tuples': self.repair_instance.tuples
                }))
        # print(selection)