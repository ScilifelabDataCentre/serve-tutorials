import numpy as np
import gradio as gr

def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

demo = gr.Interface(fn=sepia, inputs=gr.Image(label="Your image"), outputs=gr.Image(label="Sepia filtered image"))

demo.launch(server_name="0.0.0.0", server_port=8080)