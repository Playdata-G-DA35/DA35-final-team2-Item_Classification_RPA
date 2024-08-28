# category.py
import torch
from torchvision import transforms
from PIL import Image
import torchvision.models as models
import torch.nn as nn

class ImageEmbeddingModel:
    def __init__(self, weight_path, class_num, img_path):
        self.img_width, self.img_height, self.img_channel = 224, 224, 3
        self.emb_model = self.create_model(weight_path, class_num, embedding=True)
        self.csf_model = self.create_model(weight_path, class_num, embedding=False)
        self.img_tensor = self.preprocess_image(img_path)

    def create_model(self, weight_file, class_num, embedding):
        base_model = models.resnet50(weights=None)
        base_model.fc = nn.Linear(2048, class_num)
        base_model.load_state_dict(torch.load(weight_file, map_location='cpu'))
        base_model.eval()

        if embedding:
            base_model = torch.nn.Sequential(*(list(base_model.children())[:-1]))

        return base_model

    def preprocess_image(self, img_path):
        img = Image.open(img_path).convert('RGB')
        preprocess = transforms.Compose([
            transforms.Resize((self.img_width, self.img_height)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        img_tensor = preprocess(img)
        img_tensor = img_tensor.unsqueeze(0)
        return img_tensor

    def get_category(self):
        with torch.no_grad():
            category = self.csf_model(self.img_tensor)
        return category