import gradio as gr
import time

def my_function(x, progress=gr.Progress()):
    progress(0, desc="Starting...")
    time.sleep(1)
    for i in progress.tqdm(range(100)):
        time.sleep(0.1)
    return x

demo = gr.Interface(fn=my_function, inputs=gr.Textbox(), outputs=gr.Textbox())

demo.queue().launch(server_name="0.0.0.0", server_port=8080)
