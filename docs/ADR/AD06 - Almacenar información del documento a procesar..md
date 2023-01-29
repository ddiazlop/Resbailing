# Almacenar información del documento a procesar.

## Problema
Es necesario pensar en una forma en la que recoger los datos que vamos a analizar para que el proceso sea más modular. No tiene sentido que se vaya generando una presentacións sobre la marcha directamente en Google Drive sin dar opción a que se pueda modificar siquiera antes de convertirla. 

## Decisión
Ir almacenando los datos extraídos en un fichero de texto enriquecido al estilo de los archivos _markdown_.

| --        | --    |
| --------- | ----- |
| __Estado__          |  En evaluación     |
| __Grupo__ | Procesamiento |

### Suposiciones
- Se piensa en un futuro que el contenido del texto sea editable antes de generar la presentación por si alguno de los datos no es correcto.
- Utilizar un archivo markdown permite visualizar una vista previa de la presentación sin necesidad de exportar el documento a una presentación.
- Sería de gran utilidad poder comparar el texto original con el resumido.

### Restricciones
Ninguna aparantemente.

## Alternativas
### Crear una Clase donde almacenar los datos.
En un principio pensé en crear una clase donde ir almacenando los datos como "título", "autor"... El problema viene cuando empezamos a tratar el propio texto del documento. 

Dicho texto supone que habría que guardar en una clase no persistente una cantidad de datos que puede ser excesiva y diferente de modificar. Por ejemplo, si quisiera guardar en una clase los datos correspondientes al texto original y el resultado resumido,  ¿cómo se almacenaría? Existen varias opciones:
- **Crear atributos por cada fragmento de texto.**
	- La clase podría llegar a tener demasiados atributos
	- Realmente no existe forma óptima de hacer esto en python.
- **Un diccionario con todo lo que quiero comparar/analizar**
	- Podría suponer una carga en memoria demasiado grande.
	- Baja modularidad y mantenibilidad.
- **Listas de atributos**
	- Opción incluso peor que un diccionario ya que no podría siquiera identificar los distintos elementos de la lista de una forma intuitiva.


## Motivo de la Decisión
Si creamos un texto enriquecido, no solo tendremos un medio con el que comparar el texto enriquecido original resultado del análisis del documento, sino que además tendremos un formato de archivo fácilmente modificable por el que el usuario puede en un futuro modificar los valores que así vea necesarios a través de una segunda interfaz.

Además permite que sea posible hacer una vista previa del resultado en la propia app.

## Impacto de la Decisión
- Creada tarea [[05_Analizar PDF]]
- Creada tarea [[02_Tablero#^k3kwt0|Vista previa documento procesado]]
- Añadida carpeta "sessions" a la estructura del proyecto donde se guardarán los archivos .md resultado de los distintos procesos.
	- Los archivos estarán almacenados en una carpeta con el día de hoy codificado como _yyy-mm-dd_
	- El nombre del archivo dependerá de lo que se considere como el título de la diapositiva.

## Decisiones Relacionadas
_Intencionalmente en blanco_

## Requisitos Relacionados
- [[05_Analizar PDF]]
- [[02_Extraer datos del PDF]]
- [[02_Tablero#^q1ooiy|Generar Presentación sin Imágenes]]
- [[02_Tablero#^p9hfat|Interfaz de Usuario]]
- [[03_Resumir PDF]]

## Artefactos Relacionados
_Intencionalmente en blanco_

## Principios Relacionados
_Intencionalmente en blanco_

## Notas
_Intencionalmente en blanco_