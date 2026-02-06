import gradio as gr

def greet(name):
   return "Hello " + name + "!"


title = "Demo app"
description = (
  "<center>"
  "Text, images, etc. can be added here with HTML or markdown formatting."
  "</center>"
)
ref = "This app is related to the following article: [Article title](#). The code can be found here: [GitHub](#)"

demo = gr.Interface(fn=greet, 
                    inputs="text", 
                    outputs="text", 
                    title=title, 
                    description=description, 
                    article=ref)

demo.launch(server_name="0.0.0.0", server_port=7860)