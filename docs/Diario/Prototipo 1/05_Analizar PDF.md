| Descripción | Prioridad | Etiqueta       |
| ----------- | --------- | -------------- |
| Estudiar un archivo pdf para encontrar la información que necesitamos para realizar el resumen del texto.      | Alta      | #dev #pdf #resumen| 

# Subtareas

-  [[05.1_Pantalla  Cargando]]

# Archivo Markdown
Para analizar el pdf se van a ir teniendo en cuenta una serie de suposiciones en primera instancia y se irá montando un archivo en markdown según los datos encontrados que corresponderá a la presentación más adelante. Este archivo en markdown tendrá la siguiente estructura:

```md
--- % divisor de diapositiva.
# TITULO DE LA DIAPOSITIVA
Contenido de la diapositiva.
| Tabla | Column1 |
| Row2  | Row2    |
---
```

Si un mismo apartado de un documento PDF contiene más de un apartado se creará una diapositiva de tipo "Índice" donde simplemente se mostrarán los títulos en una lista de todos los subtítulos de la misma.

```md
---
# Titulo de la diapositiva
- Titulo2
- Titulo3
- Titulo4
- ...
---
```

Puede darse el caso a su vez que en un documento exista un subtítulo para un título por lo tanto:

```md
---
# Título de la diapositiva
## Título2
Contenido
---
```

# Creación del documento .md
Se van a generar 
## Primera diapositiva
Supongamos que en la primera página del doc se encuentra el título del documento. (Lo raro sería que no estuviese allí). De esta forma, el título suele ser un elemento del pdf  cuyo propósito es llamar la atención del lector y por ende, suele ser de _mayor tamaño_ que el resto del texto. O por lo contrario, se suele poner en negrita, cursiva... Y lo que es más importante, al principio del texto.

[[02_Extraer datos del PDF#PdfPlumber]] ofrece una opción para no solo extraer las palabras de una página sino además, permite ver la "_bounding box_" del mismo, por lo que el título muy probablemente tenga una bounding box de mayor tamaño. O mejor aún, podemos obtener la altura de esa bounding box y comparar únicamente eso, ya que una palabra con mayor tamaño de fuente es una palabra con mayor altura.

> [!failure]
> No parece funcionar, tiene pinta de que la bounding box no se corresponde exactamente con el tamaño de la fuente del texto, probablemente se refiera a la distancia hasta el siguiente objeto en el pdf
> 

- [x] Seguir con el tema de sacar la info del pdf. ✅ 2023-01-28
- [x] Desactualizar python (ya lo instalé) ✅ 2023-01-27

### Subtítulos.
En documentos con portada puede existir un subtítulo. Este subtítulo, siguiendo la lógica del tamaño de la fuente del texto, será el segundo con mayor tamaño. (_Otras consideraciones se podrían realizar más adelante_).


# Generar la Presentación
Ya conocemos como sacar el título y el subtítulo.
- [ ] Estudiar como sacar el texto del resto del documento.

## Problema 1 - índices
Muchos documentos suelen tener índices en su inicio. Cómo trabajamos alrededor de ellos?

### Buscar palabra índice.
No hay que dejarse confundir por esto ya que, cuántas formas existen de poner un índice?? Tabla de contenidos, Índice, index...

### Probar a resumir el índice a ver qué pasa.

```embed
title: 'mrm8488/bert2bert_shared-spanish-finetuned-summarization · Hugging Face'
image: 'https://thumbnails.huggingface.co/social-thumbnails/models/mrm8488/bert2bert_shared-spanish-finetuned-summarization.png'
description: 'We’re on a journey to advance and democratize artificial intelligence through open source and open science.'
url: 'https://huggingface.co/mrm8488/bert2bert_shared-spanish-finetuned-summarization'
```

Tiene pinta que esta librería permite resumir un texto en español, veamos si no explota.

```python
import torch
from transformers import BertTokenizerFast, EncoderDecoderModel
device = 'cuda' if torch.cuda.is_available() else 'cpu'
ckpt = 'mrm8488/bert2bert_shared-spanish-finetuned-summarization'
tokenizer = BertTokenizerFast.from_pretrained(ckpt)
model = EncoderDecoderModel.from_pretrained(ckpt).to(device)

def generate_summary(text):

   inputs = tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
   input_ids = inputs.input_ids.to(device)
   attention_mask = inputs.attention_mask.to(device)
   output = model.generate(input_ids, attention_mask=attention_mask)
   return tokenizer.decode(output[0], skip_special_tokens=True)
   
text = "Your text here..."
generate_summary(text)
```

- [x] Probarlo ✅ 2023-01-29

> [!error] module 'ntpath' has no attribute 'sep'
> Ocurre este error intentando descargar el modelo, también ocurre intentando descargar imágenes. Toca solucionarlo a full.


