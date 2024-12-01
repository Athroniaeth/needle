import time
from dataclasses import dataclass
from typing import List

import gradio as gr


@dataclass
class Message:
    role: str
    title: str
    content: str

    @classmethod
    def from_gradio_dict(cls, data: dict):
        return cls(role=data["role"], title=data['metadata']['title'], content=data['content'])


def yes(message: str, history: List[dict]):
    history = [Message.from_gradio_dict(x) for x in history]
    print(type(message), type(history))
    print(history)
    time.sleep(5)
    return "yes"


def vote(data: gr.LikeData):
    if data.liked:
        print("You upvoted this response: ", data.value)
    else:
        print("You downvoted this response: ", data.value)


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        placeholder="<h1 style='text-align: center;'>Chatbot</h1><strong>Enter any ask or say something</strong>",
        type="messages"
    )

    chatbot.like(vote)
    gr.ChatInterface(fn=yes, type="messages", chatbot=chatbot)

demo.launch()
