from fastapi import FastAPI

from subscriber import mq_subscriber

app = FastAPI()

# Add the routes

@app.on_event("startup")
async def startup():
    mq_subscriber.consume_mq_queue(
        queue_name='notifications',
        app=app,
        no_ack=False
    )