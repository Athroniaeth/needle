import gradio as gr
from fastapi import FastAPI

from needle.interface import blocks

app = FastAPI()

app = gr.mount_gradio_app(
    app=app,
    path="/",
    blocks=blocks,
)
