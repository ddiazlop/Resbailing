---
banner: "https://www.datocms-assets.com/14946/1633281680-ux-vs-ui-cover-edited.png?auto=format&fit=max&w=1200"
banner_y: 0.50333
---
# AD04: Framework de Python

## Problema
Debe elegirse un framework para desarrollar la aplicación. 

## Decisión
- Utilizar el Framework **Kivy** para desarrollo de aplicaciones en Python y desarrollar una aplicación de escritorio. 
- Separar las responsabilidades del front-end y el back-end por si en un futuro se quiere crear un front-end web. Dando pie a una posible y futura API solo con la funcionalidad.

| --        | --    |
| --------- | ----- |
| __Estado__          |  Aprobado     |
| __Grupo__ | Desarrollo |

### Suposiciones
- Aplicación enteramente en Python
- Puede accederse a las librerías de forma modular e integrarlas en la aplicación.
- Puede crearse un paquete ejecutable a la hora de entregar prototipos o el producto final.
- Permite estilizar la interfaz de usuario.

### Restricciones
- Framework desconocido, por lo que se requiere de aprendizaje.
- Quizá la aplicación final supone mucha caraga para el ordenador de un usuario.
- No se puede desplegar como servicio web.

## Alternativas
### Web Framework
#### Django
- Conocido, no requiere de aprendizaje y permite que la carga del trabajo de la [[Generación de Imágenes]] la realice el servidor web, quitándosela al dispositivo del usuario.
- Posibilidad de usar CSS para estilizar la aplicación.

No obstante, requiere de que la aplicación esté desplegada en un servicio web, lo que supondría un coste adicional debido a que se necesitaría alquilar un servidor con la potencia suficiente como para mantener el servicio. Si fuesen varios usuarios simultáneos del mismo servicio podría suponer una carga excesiva.

#### Flask
Mismos motivos que Django, pero puede llegar a consumir menos recursos y ofrece soporte para API, lo que podría estar muy bien si en un futuro se decide implementar el front-end con Elixir.

#### Anvil
- Ofrece una interfaz gráfica para desarrollar la página arrastrando los elementos.
- Sencillez a la hora de diseñar la interfaz.
- También es un servicio de web-hosting y editor de código.

Es una solución orientada hacia usuarios poco experimentados y que realmente no da mucho lugar a la diversidad o a la personalización de la aplicación. Podría ser la forma más rápida de implementar y poner a funcionar el front-end pero quizá tenga limitaciones a la hora de usar librerías externas o necesitar descargar paquetes y librerías dentro de la aplicación.

Además resulta más cómodo usar un IDE con facilidades como la predicción de texto, debugging... Que Anvil no ofrece como servicio.

### App Framework
#### Electron
- Implementación para conectar un front-end en __React.js__ con un back-end en python. 
- Da como resultado adicional una API de python sobre la que el front-end en __React.js__ realiza las peticiones.

El aprendizaje de este framework se le debe sumar el aprendizaje de __React.js__, es demasiado complejo teniendo en cuenta el alcance de este proyecto.

### App & Web Framework
#### Flet
[[Flet]] es muy interesante ya que permite desarrollar una aplicación a partir de widgets como lo haría __Kivy__ pero permite adicionalmente presentar esa misma aplicación tanto como aplicación web como aplicación de escritorio. Esto significa que al desarrollar una app con Flet, estaría desarrollando con python simultáneamente una versión de escritorio y web.

No obstante, este framework se encuentra en fases de desarrollo aún muy temprana lo que siginifica que presenta una gran limitación a la hora de personalizar las diferentes widgets y adaptar la aplicación resultado. Adicionalmente, debido a su temprana edad existen pocas guías y ejemplos del mismo en acción.

## Motivo de la Decisión
__Kivy__ ofrece un framework robusto con el que crear una aplicación de escritorio con __Python__ por medio de Widgets tal y como lo hace __Flet__ pero no permite su despliegue web. No obstante, __Kivy__ ya es un framework con cierta madurez e incluso existen librerías adicionales para el mismo ya que es de código abierto.

## Impacto de la Decisión
- Ya se puede empezar a desarrollar la aplicación.

## Decisiones Relacionadas
- [[AD03 - Entorno de Desarrollo]]

## Requisitos Relacionados
- [[02_Tablero#^g2ultw]]: Elegir un framework

## Artefactos Relacionados
_Intencionalmente en blanco_

## Principios Relacionados
_Intencionalmente en blanco_

## Notas
No debe de descartarse la opción de terminar implementado el producto final como una API sobre la que se puedan hacer peticiones, incluso si no tiene un front-end como tal. Así, desligamos front-end de back-end y resulta en menos carga para el ususario.