import gradio as gr

with gr.Blocks(theme="default") as blocks:
    text = gr.Textbox(lines=5, label="Input Text")
