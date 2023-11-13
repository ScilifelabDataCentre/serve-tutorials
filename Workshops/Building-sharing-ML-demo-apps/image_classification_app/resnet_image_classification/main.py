import gradio as gr
import torch
import requests
from PIL import Image
from torchvision import transforms
import torchvision.models as models

checkpoint = torch.load('data/image_classification_resnet18.pth')
model = models.resnet18()
model.load_state_dict(checkpoint)
model.eval()
# Download human-readable labels for ImageNet.
response = requests.get("https://git.io/JJkYN")
labels = response.text.split("\n")

def predict(inp):
  inp = transforms.ToTensor()(inp).unsqueeze(0)
  with torch.no_grad():
    prediction = torch.nn.functional.softmax(model(inp)[0], dim=0)
    confidences = {labels[i]: float(prediction[i]) for i in range(1000)}
  return confidences

def greet(name):
   return "Hello " + name + "!"

interface = gr.Interface(fn=predict,
             inputs=gr.Image(type="pil"),
             outputs=gr.Label(num_top_classes=3),
             examples=["data/lion.jpg", "data/cheetah.jpg"])

interface.launch(server_name="0.0.0.0", server_port=8080)
