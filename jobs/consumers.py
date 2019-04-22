from channels.generic.websocket import WebsocketConsumer
from .models import Job
from .tasks import sec3
import json


class JobConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))



    def start_sec3(self, name,):
        job = Job()
        job.name = name
        job.status = "started"
        job.save()

        sec3_task = sec3.delay(job.id)
        job.celery_id = sec3_task.id
        job.save()

        self.send(
            {
                "text": json.dumps(
                    {
                        "action": "started",
                        "job_id": job.id,
                        "job_name": job.name,
                        "job_status": job.status,
                    }
                )
            }
        )
