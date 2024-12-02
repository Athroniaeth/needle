import time
from dataclasses import dataclass, field
from typing import List, Optional

import gradio as gr


@dataclass
class Message:
    role: str
    content: str
    title: Optional[str] = field(default=None)

    @classmethod
    def from_gradio_dict(cls, data: dict):
        return cls(role=data["role"], title=data['metadata']['title'], content=data['content'])


def yes(message: str, history: List[dict]):
    history = [Message.from_gradio_dict(x) for x in history]
    print(type(message), type(history))
    print(history)
    return "yes"


def vote(data: gr.LikeData):
    if data.liked:
        print("You upvoted this response: ", data.value)
    else:
        print("You downvoted this response: ", data.value)


with (gr.Blocks() as demo):
    chatbot = gr.Chatbot(
        placeholder="<h1 style='text-align: center;'>Chatbot</h1><strong>Enter any ask or say something</strong>",
        type="messages",
        height=550,
    )

    with gr.Row():
        with gr.Column(scale=10):
            gr.ChatInterface(fn=yes, type="messages", chatbot=chatbot)

        with gr.Column(min_width=0):
            button_undo = gr.Button(value="↩️")

            def undo(list_messages):
                if len(list_messages) >= 2:
                    return gr.update(value=list_messages[:-2])

                gr.Warning("History haven't enough messages to undo")
                return gr.update(value=list_messages)

            button_undo.click(undo, inputs=[chatbot], outputs=[chatbot])

        with gr.Column(min_width=0):
            button_retry = gr.Button(value="🔄")

            def retry(list_messages):

                if len(list_messages) < 2:
                    gr.Warning("History haven't enough messages to retry")
                    return gr.update(value=list_messages)

                # Get the last user message
                message = list_messages[-2]

                # Remove user and chatbot messages
                list_messages = list_messages[:-1]

                # Add user message to the list
                response = yes(message, list_messages)
                list_messages.append({"role": "assistant", "content": response, "metadata": {"title": None}})

                return gr.update(value=list_messages)

            button_retry.click(retry, inputs=[chatbot], outputs=[chatbot])

        with gr.Column(min_width=0):
            button_clear = gr.Button(value="❌")

            def clear():
                return gr.update(value=[])

            button_clear.click(clear, outputs=[chatbot])

    chatbot.like(vote)

if __name__ == "__main__":
    demo.launch()
