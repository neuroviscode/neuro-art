import os
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from logic import vae_models
import torchvision.transforms as transforms


class StyleTransferVAE:
    encoder_dir = Path('assets/models/encoder.pth')
    decoder_dir = Path('assets/models/decoder.pth')
    transform_module_dir = Path('assets/models/transform-module.pth')

    def __init__(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # initialize model modules
        self.encoder = vae_models.encoder4()
        self.decoder = vae_models.decoder4()
        self.transform_module = vae_models.TransformModule(latent_dim=256)

        self.encoder.load_state_dict(torch.load(self.encoder_dir))
        self.decoder.load_state_dict(torch.load(self.decoder_dir))
                if torch.cuda.is_available():
            self.transform_module.load_state_dict(torch.load(self.transform_module_dir))
        else:
            self.transform_module.load_state_dict(torch.load(self.transform_module_dir, map_location=torch.device('cpu')))

        # load models into GPU tensors and set their mode to evaluation
        self.encoder.to(self.device).eval()
        self.decoder.to(self.device).eval()
        self.transform_module.to(self.device).eval()

        self.transform = transforms.Compose([transforms.ToTensor(), ])

    def run_style_transfer(self, content_image: Image, style_image: Image):

        content = self.transform(content_image).unsqueeze(0).to(self.device)
        style = self.transform(style_image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            content_features = self.encoder(content)
            style_features = self.encoder(style)

            feature, _, _ = self.transform_module(content_features['r41'], style_features['r41'])
            prediction = self.decoder(feature)
            prediction = prediction.data[0].cpu().permute(1, 2, 0)

        prediction = prediction * 255.0
        prediction = prediction.clamp(0, 255)

        return Image.fromarray(np.uint8(prediction))


