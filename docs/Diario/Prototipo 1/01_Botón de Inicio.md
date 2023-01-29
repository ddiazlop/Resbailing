# Crear un botón en inicio

![[Pasted image 20221231113547.png]]
Es súper complicado meter ese botón ahí, quizá renta que el botón sea solo una imagen. Ahora mismo el archivo con los gráficos es así:

```kv
<MainScreen>  
    FloatLayout:  
        orientation: 'vertical'  
        canvas.before:  
            Rectangle:  
                pos: self.pos  
                size: self.size  
                source: 'images/tobonaranja.png'  
  
        Button:  
            text: 'Crear una presentación'  
            size_hint: 0.4, 0.2  
            pos_hint: {'left': 1, 'top': 0.8, 'right': 0.6, 'bottom': 1}  
            font_size: self.height * 0.15  
            padding: 20, 0  
            background_normal: 'images/button1.png'  
            valign: 'middle'
```

Esto mola mucho porque lo hace todo automático sin que yo le tenga que decir nada realmente.

El probelma está en el texto, que hay que posicionarlo arriba a la izq. He descubierto cómo hacer en plan guay el tamaño:

```kv
font_size: self.height * 0.15  
```

Que como se puede ver, pillaría el tamaño del botón, y se basaría en dicho tamaño para hacer el resto. Es lo mismo que donde se hace _hint_ ya que eso lo que hace es multiplicar el _self.height_ por la altura de donde está contenido.

## Intentos
### Cambiar el Padding ❌
Cambiar el padding no parece hacer nada útil, porque el "padding" se corresponde al padding del botón y no del texto. Así que mejor quito el padding que no está haciendo nada.

### Usar una etiqueta dentro del botón
No tengo ni idea, pero siguiento la forma en la que se estructura el fichero .kv podría funcionar algo del estilo:

```kv
Button:  
    size_hint: 0.4, 0.2  
    pos_hint: {'left': 1, 'top': 0.8, 'right': 0.6, 'bottom': 1}  
    font_size: self.height * 0.15  
    background_normal: 'images/button1.png'  
    valign: 'middle'  
    Label:  
        text: 'Button 1'  
        font_size: self.height * 0.15  
        valign: 'middle'  
        halign: 'center'
```

No se ve nada.
![[Pasted image 20221231114816.png]]


### Cambiar imagen del botón y añadirle tamaño
Lo que mejor está dando resultado es añadirle un tamaño al texto del botón y alinearlo:

```kv
Button:  
    text: 'Crear una presentación'  
    size_hint: 0.4, 0.2  
    pos_hint: {'top': 0.8, 'right': 0.6}  
    font_size: self.height * 0.2  
    text_size: 0.6 * self.width, 1 * self.height  
    valign: 'middle'  
    halign: 'center'  
    background_normal: 'images/button1.png'
```

Y cambiar el botón en sí para que tenga algo de zona vacía encima suya, esto es un poco trusquis pero ha funcionado.

![[Pasted image 20221231121809.png]]

Lo mismo podría hacerse si amplío un poco en la imagen la zona "muerta" en la izquierda.

![[Pasted image 20221231122233.png]]

Es mejorable,pero no voy a perder más tiempo en esto.

- [x] Saltar a la siguiente página donde insertar un archivo PDF (En principio) que se va a tratar ⏫ ✅ 2022-12-31

