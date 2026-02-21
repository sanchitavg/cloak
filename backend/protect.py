import torch
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from io import BytesIO

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def protect_image(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        # Just test embedding without using it
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            _ = model.get_image_features(**inputs)

        # Add simple pixel noise
        image_array = np.array(image).astype(np.float32)
        pixel_noise = np.random.normal(0, 2, image_array.shape)
        image_array = np.clip(image_array + pixel_noise, 0, 255)

        protected_image = Image.fromarray(image_array.astype(np.uint8))

        output = BytesIO()
        protected_image.save(output, format="PNG")
        return output.getvalue()

    except Exception as e:
        print("ERROR:", e)
        raise e