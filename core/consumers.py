import json

from channels.generic.websocket import WebsocketConsumer
# from .models import Job


class JobConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        # close connection
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        job = text_data_json["job"]
        # print("Job", job)
        self.send(text_data=json.dumps({"message": job}))
