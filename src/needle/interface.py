from typing import List, Optional, TypedDict

import gradio as gr

from needle import CSS_PATH


class MetaData(TypedDict):
    title: Optional[str]


class Message(TypedDict):
    """
    Gradio message chatbot representation

    Args:
    ----
        role (str): User or chatbot
        content (str): Message content
        metadata (MetaData): Additional message information

    Returns:
    -------
        Message: Gradio message chatbot representation

    """

    role: str
    content: str
    metadata: MetaData


def echo(message: str, history: List[Message]) -> str:
    """
    Get the assistant response message

    Args:
    ----
        message (str): User message
        history (List[Message]): Chatbot history

    Returns:
    -------
        str: Chatbot response message

    """
    return message


def vote(data: gr.LikeData) -> None:
    """
    Get the user vote response

    Args:
    ----
        data (gr.LikeData): User vote data

    Returns:
    -------
        None: Print the user vote response

    """
    if data.liked:
        print("You upvoted this response: ", data.value)
    else:
        print("You downvoted this response: ", data.value)


def undo(list_messages: List[Message]) -> gr.update:
    """
    Gradio pipeline to undo the last message

    Args:
    ----
        list_messages (List[Message]): Chatbot history

    Returns:
    -------
        List[Message]: Chatbot history without the last message

    """
    if len(list_messages) >= 2:
        return gr.update(value=list_messages[:-2])

    gr.Warning("History haven't enough messages to undo")
    return gr.update(value=list_messages)


def clear():
    """
    Gradio pipeline to clear the chatbot history

    Returns
    -------
        List[Message]: Empty chatbot history

    """
    return gr.update(value=[])


def retry(list_messages: List[Message]):
    """
    Gradio pipeline to retry the last user message

    Args:
    ----
        list_messages (List[Message]): Chatbot history

    Returns:
    -------
        List[Message]: Chatbot history with the last user message

    """
    if len(list_messages) < 2:
        gr.Warning("History haven't enough messages to retry")
        return gr.update(value=list_messages)

    # Get the last user message
    message = list_messages[-2]["content"]

    # Remove user and chatbot messages
    list_messages = list_messages[:-1]

    # Add user message to the list
    response = echo(message, list_messages)
    list_messages.append({"role": "assistant", "content": response, "metadata": {"title": None}})

    return gr.update(value=list_messages)


css = CSS_PATH.read_text()


with gr.Blocks(css=css) as blocks:
    chatbot = gr.Chatbot(
        placeholder="<h1 style='text-align: center;'>Chatbot</h1><strong>Enter any ask or say something</strong>",
        type="messages",
        height=575,
    )

    with gr.Row():
        with gr.Column(scale=10):
            gr.ChatInterface(fn=echo, type="messages", chatbot=chatbot)

        with gr.Column(min_width=0):
            button_undo = gr.Button(value="↩️")
            button_undo.click(undo, inputs=[chatbot], outputs=[chatbot], show_api=False)

        with gr.Column(min_width=0):
            button_retry = gr.Button(value="🔄")
            button_retry.click(retry, inputs=[chatbot], outputs=[chatbot], show_api=False)

        with gr.Column(min_width=0):
            button_clear = gr.Button(value="❌")
            button_clear.click(clear, outputs=[chatbot], show_api=False)

    chatbot.like(vote, show_api=False)

if __name__ == "__main__":
    blocks.launch()
