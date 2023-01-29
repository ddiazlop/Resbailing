Intentando hacer varias pantallas, teóricamente hay que usar ScreenManager.

# Mantener el fondo
Quiero mantener el fondo y no lo consigo, es una rayada.

## Clase dinámica ❌
La idea es crear una clase dinámica para así poder ir importanto o no las cosas:

```kv
<Tobofondo@Rectangle>:  
    pos: self.pos  
    size: self.size  
    source: 'images/tobonaranja.png'  
  
<MainScreen>:  
    FloatLayout:  
        orientation: 'vertical'  
        canvas.before:  
            Tobofondo:
```

No obstante, _tobofondo_ no quiere colaborar. Y sale la pantalla entera en negro.

## No hacer nada y volverlo a escribir ✔
Obviamente funciona, pero para nada es ideal claro. JAJAJAJAJAJ

# Botón de Upload
La idea es que haya un botón translúcido blanco que al pulsarlo muestre una barra de progreso debajo que se vaya relleando según se vaya resumiendo el texto en pdf.

- [x] Toca crear el botón de subir un archivo y hacer el mondongo. 🔼 🛫 2023-01-01 ✅ 2023-01-03

El botón ya está listo.
![[Pasted image 20230103112028.png]]

No obstante, la implementación de Kivy para seleccionar un archivo es bastante fea y poco intuitiva. No usa el explorador del sistema como es costumbre en cualquier app o incluso webapp.

![[Pasted image 20230103112214.png]]


## Plyer 2.1.0
Plyer parece solucionar este problema ya que implementa varias API bastante útiles para gestionar un sistema.

![[Pasted image 20230103112610.png]]

Esto sí me gusta más. Ahora ya puedo tener el path de un  pdf y por tanto su contenido.
![[Pasted image 20230103113632.png]]

Ahora viene el mondongo.
[[03_Resumir PDF]]

