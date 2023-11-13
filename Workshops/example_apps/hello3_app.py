import gradio as gr

def greet(name, is_morning, temperature_F):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature_F} degrees today"
    celsius = (temperature_F - 32) * 5 / 9
    return greeting, round(celsius, 2)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "checkbox", gr.Slider(0, 100)],
    outputs=["text", "number"],
    examples=[["David", True, 55], ["Ash", False, 70]]
)

demo.launch(server_name="0.0.0.0", server_port=8080)