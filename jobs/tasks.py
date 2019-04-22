import time
import json
import logging

from celery import shared_task
from .models import Job
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


log = logging.getLogger(__name__)


@shared_task()
def sec3(job_id, reply_channel):
    # time sleep represent some long running process
    time.sleep(3)
    # Change task status to completed
    job = Job.objects.get(pk=job_id)
    log.debug("Running job_name=%s", job.name)

    job.status = "completed"
    job.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        "reply_channel",
        {
            "text": json.dumps(
                {
                    "action": "completed",
                    "job_id": job.id,
                    "job_name": job.name,
                    "job_status": job.status,
                }
            )
        },
    )
    # Old Fashion
    # Send status update back to browser client
    # if reply_channel is not None:
    #     Channel(reply_channel).send(
    #         {
    #             "text": json.dumps(
    #                 {
    #                     "action": "completed",
    #                     "job_id": job.id,
    #                     "job_name": job.name,
    #                     "job_status": job.status,
    #                 }
    #             )
    #         }
    #     )
