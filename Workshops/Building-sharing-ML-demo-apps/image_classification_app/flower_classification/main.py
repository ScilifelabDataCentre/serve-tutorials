import gradio as gr
import torch
from PIL import Image
from torchvision import transforms
import torchvision.models as models

model = torch.load('data/flower_model_vgg19.pth')
model.eval()
# Download human-readable labels for ImageNet.
with open('data/flower_dataset_labels.txt', 'r') as f:
    labels=f.readlines()

def predict(inp):
  inp = transforms.ToTensor()(inp).unsqueeze(0)
  with torch.no_grad():
    prediction = torch.nn.functional.softmax(model(inp)[0], dim=0)
    confidences = {labels[i]: float(prediction[i]) for i in range(102)}
  return confidences

interface = gr.Interface(fn=predict,
             inputs=gr.Image(type="pil"),
             outputs=gr.Label(num_top_classes=3))

interface.launch(server_name="0.0.0.0", server_port=8080, debug=True)
