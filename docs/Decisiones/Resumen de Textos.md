### Tasks 📄
- [x] TODO: Más ventajas ✅ 2022-12-31
- [x] Más desventajas ✅ 2022-12-31
- [x] Investigar sobre más opciones y contrastarlas. ✅ 2022-12-31
---
# Facebook - BART Model

```embed
title: 'facebook/bart-large-cnn · Hugging Face'
image: 'https://huggingface.co/front/thumbnails/facebook.png'
description: 'We’re on a journey to advance and democratize artificial intelligence through open source and open science.'
url: 'https://huggingface.co/facebook/bart-large-cnn'
```

## Por qué usar este
No he investigado mucho pero tiene pinta de que como está refinado con artículos de la CNN, para presentaciones debería de identificar bien el tema que se habla.

### Ventajas
- Parace ser útil para resumir textos con cierta rigurosidad. 

### Desventajas
- Tiene un límite de índices de 1024 que parece que no se puede solventar así que no se le puden meter textos demasiado largos.
	- Posibles soluciones:
		1. Dividir los textos cada 3 párrafos o cada cierto número de caracteres, sin cortar el número de
	

## Implementación 

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

ARTICLE = """
According to the American Society for the Prevention of Cruelty to Animals (ASPCA), an estimated 78 million dogs are owned as pets in the United States.

  

It is unclear when dogs were first domesticated, but a studyTrusted Source published last year claims that, at least in Europe, dogs were tamed 20,000–40,000 years ago.

  

It is likely that humans and dogs have shared a special bond of friendship and mutual support ever since at least the Neolithic period — but why has this bond been so long-lasting?

  

Of course, these cousins of the wolves have historically been great at keeping us and our dwellings safe, guarding our houses, our cattle, and our various material goods. Throughout history, humans have also trained dogs to assist them with hunting, or they have bred numerous quirky-looking species for their cuteness or elegance.

  

However, dogs are also — and might have always been — truly valued companions, famed for their loyalty and seemingly constant willingness to put a smile on their owners’ faces.
"""

text = summarizer(ARTICLE, max_length=15, min_length=1, do_sample=False)

text = text[0]['summary_text']

print(text)
```
