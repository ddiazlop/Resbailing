### Tasks
- [x] Buscar más opciones que no sean Stable Diffusion, pero no creo que existan ✅ 2022-12-31
---
# Stable Diffusion v1.5

<iframe src="https://huggingface.co/runwayml/stable-diffusion-v1-5" allow="fullscreen" allowfullscreen="" style="height:100%;width:100%; aspect-ratio: 16 / 9; "></iframe>

## Por qué usar este
Stable Diffusion es el único generador de imágenes con licencia de uso libre que da unos resultados óptimos ante la [[Generación de Imágenes]].

la versión 1.5 intenta salirse de la [[Generación de Imágenes]] clasificando el texto y prefiere hacerlo sin clasificar. La guía píxel a píxel de una imagen no necesita del "clasificador" usual tal y como se describe en el paper: [[Difusión sin Clasificador.pdf]].

## Implementación
_Proporcionada en la Model Card de Huggingface_

```python
from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16")
pipe = pipe.to("cuda")

prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt).images[0]  
    
image.save("astronaut_rides_horse.png")
```

# Stable Diffusion + Dreambooth


<iframe src="https://bytexd.com/how-to-use-dreambooth-to-fine-tune-stable-diffusion-colab/" allow="fullscreen" allowfullscreen="" style="height: 100%; width: 100%; aspect-ratio: 4 / 3;"></iframe>

## Por qué usar este
Podría ser útil entrenar mis propios pesos de stable diffusion con imágenes típicas de presentaciones, estilo voxel art o cosas así evitando lo _wacky_ que puede llegar a ser generar imágenes

## Implementación

### [Colab con el código para entrenarlo](https://colab.research.google.com/github/TheLastBen/fast-stable-diffusion/blob/main/fast-DreamBooth.ipynb#scrollTo=iAZGngFcI8hq)


