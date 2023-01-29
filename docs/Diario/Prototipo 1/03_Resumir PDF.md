Ahora hay que resumir este pdf, veamos primero si existe alguna herramienta en python para conseguir ese pdf. Para ello vamos a usar un documento de PGPI.
![[Acta_de_Constitución.CIT@MEDICA.24-10-2022.v0.7.pdf]]

Esta es el acta de constitución que tiene varios elementos que pueden dar problemas a la hora de intentar reducir este documento a una presentación que podría usarse como presentación de un proyecto:

- Tabla de versionado
- Información en tablas.
- Descripciones
- Listas
- Listas en tablas
- Datos relativos al presupuesto.
- Y otras tablas bastante irregulares en general.

Para una persona sería cuestión de tiempo consolidar toda esta información, pero algorítmicamente puede no ser tan sencillo.

Veamos primero cómo extraemos la información del pdf.
- [[02_Extraer datos del PDF]]