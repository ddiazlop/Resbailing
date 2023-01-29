---
banner: "https://www.simplilearn.com/ice9/free_resources_article_thumb/Best-Programming-Languages-to-Start-Learning-Today.jpg"
banner_y: 0.51333
---
# AD03: Entorno de Desarrollo

## Problema
Hay que decidir el entorno en el que se desarrollará la aplicación

## Decisión
Desarrollar la aplicación enteramente en __Python__ usando algún framwork para desarrollo de aplicaciones o desarrollo web.

| --        | --    |
| --------- | ----- |
| __Estado__          |  Implementado     |
| __Grupo__ | Desarrollo |

### Suposiciones
- La mayor parte de las librerías que se necesitan para [[Generación de Imágenes]] y [[Resumen de Textos]] se encuentan desarrolladas en Python. 

### Restricciones
No se espera que suponga ninguna restricción para el proyecto.

## Alternativas
### Usar Elixir + Python
Elixir es un lenguaje de programación usado por empresas como Discord para reducir la carga sobre sistemas que necesiten de llamadas muy frecuentes a otros subservicios o APIs. 

Esto sería útil ya que las librerías de [[Generación de Imágenes]] y [[Resumen de Textos]] suponen una carga bastante grande sobre la mayoría de procesadores, así que reducir la carga al menos en la Interfaz de Usuario puede resultar de utilidad.

Si utilizamos Elixir para realizar el back-end tendríamos al mismo tiempo que desplegar una API en Python a la que poder realizarle peticiones.

## Motivo de la Decisión
Desarrollar la aplicación en Elixir supondría aprender un nuevo lenguaje de programación además de necesitar de forma obligatoria desarrollar una API en Python que suministre a la aplicación en Elixir de toda la funcionalidad.

Por cuestión de complejidad, resulta más cómodo desarrollar toda la aplicación en Python ya que las librerías que se van a usar se encuentran allí y no es necesario aprender otro lenguaje ni implementar una API.

## Impacto de la Decisión
Es necesario decidir si implementar la aplicación como una app web o de escritorio y elegir un framework que ayude a hacerlo.

## Decisiones Relacionadas
- D01
- D02

## Requisitos Relacionados
- Decidir el Entorno de Desarrollo

## Artefactos Relacionados
_Intencionalmente en blanco_

## Principios Relacionados
_Intencionalmente en blanco_

## Notas
_Intencionalmente en blanco_

