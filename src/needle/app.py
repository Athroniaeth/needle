import gradio as gr
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from needle.exception import http_exception_handler

from needle.interface import blocks

app = FastAPI()


# Exceptions handlers
app.add_exception_handler(HTTPException, http_exception_handler)


@app.get(path="/hello")
def hello():
    return {"hello": "world"}


"""
Don't use '/' for path, gradio prevents prometheus 
from retrieving information as gradio modifies routes.
Routes defined as /metrics are hidden by the Gradio application mounted on '/'.
"""
app = gr.mount_gradio_app(
    app=app,
    path="/app",
    blocks=blocks,
)

# Initialize and configure the Prometheus instrument
Instrumentator().instrument(app).expose(app)
