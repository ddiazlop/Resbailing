
# PyPDF2

```python
def show_load(self, *args):  
    print('Loading dialog')  
    path = filechooser.open_file(title='Selecciona tu documento PDF', filters=[('PDF files', '*.pdf')])  
    pdfFileObj = open(path[0], 'rb')  
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
    i = 0
```

Tras obtener el path, podemos hacer algo de debugging para ver cuáles son los contenidos del PDF tras leerlo.

Parece que no es necesario _pdfFileObj_

```python
print('Loading dialog')  
path = filechooser.open_file(title='Selecciona tu documento PDF', filters=[('PDF files', '*.pdf')])  
print('Reading PDF')  
pdf_reader = PyPDF2.PdfReader(path[0])  
i = 0
```

En la última versiónd e PyPDF2 prob solo hace falta pdf_reader.

## Extraer la información
Esto es una tarea difícil porque se deben de realizar muchas operaciones si queremos que la lectura del pdf sea general. Para ello vamos a crear el primer archivo del "backend" de nuestra app.

He pensado que lo mejor es crear una clase DocumentData en la que pueda almacenar todos los datos del documento, ya sean tablas o lo que sea. 

### Extraer el título

```python
class DocumentData:  
    def __init__(self, path):  
        self.path = path  
        pdf = PyPDF2.PdfReader(self.path)  
        self.pages = pdf.pages  
  
        # Data  
        self.title = self.extract_title()  
        i = 0  
  
    def extract_title(self):  
        def visitor_title(text, cm, tm, fontDict, fontSize):  
            # TODO: Visitante que pueda extraer el título.  
        first_page = self.pages[1]
```

Según la documentación de la de PyPDF2 la única forma de filtrar el texto es según sus cm, tamaño, posición... y demás. Así que hay que crear un _visitante_ que permita extrear el texto que yo necesito.

> [!attention]
> PyPDF2 parece un lío así que vamos a probar una solución más sencilla.
> 

# Tika
Tika parece ser un lector más cómodo, no es necesario uso de llamadas ni nada, simplemente obtiene el texto en plano para tratarlo más adelante. Vamos a convertir este texto a markdown para tratarlo más adelante.

> [!fail]
> No permite extraer imágenes y es un lío para el tema de las tablas tiene pinta.
> 

# PdfPlumber

```embed
title: 'GitHub - jsvine/pdfplumber: Plumb a PDF for detailed information about each char, rectangle, line, et cetera — and easily extract text and tables.'
image: 'https://opengraph.githubassets.com/85321dfa8f708f831ed88b82407b57c002eebcdb6310735ef6adc7c67782563d/jsvine/pdfplumber'
description: 'Plumb a PDF for detailed information about each char, rectangle, line, et cetera — and easily extract text and tables. - GitHub - jsvine/pdfplumber: Plumb a PDF for detailed information about each ...'
url: 'https://github.com/jsvine/pdfplumber'
```

Este promete, permite extraer cosas como el tamaño del texto, la fuente... Funciona mejor con pdf's generados a máquina pero vamos a ver qué tal cuela este.

## Análisis del PDF
- [[05_Analizar PDF]]


# Extraer PDF a markdown
Quizá es más lento, pero si existe una librería ya creada por otro sería mucho más sencillo sacar cosas como los títulos y demás debido a las características del lenguaje de marcado. 

> [!faq] ¿Debería de optarse por lo más sencillo?
> Trabajar con pdfs es un verdadero quebradero de cabeza, así que vamos a intentar cambiarlo a markdown

## Librerías ya hechas

### Aspose-words
Son una serie de herramientas que permiten tratar con textos pero parece ser de pago.

### pdf-to-markdown
En el README de la librería dice que no es un conversor de propósito múltiple sino uno hecho específicamente para documentos de planificación urbana en Taiwán.

> [!missing]
> No parece que exista ninguna herramienta que convierta pdf a markdown de python que no sea de pago. 
