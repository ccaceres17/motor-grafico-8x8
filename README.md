# Motor Gráfico Binario 8x8

Proyecto académico desarrollado en Python utilizando Flet.

## Descripción

El proyecto implementa un motor gráfico binario basado en una matriz de 8x8 LEDs.

La matriz representa 64 bits:

8 × 8 = 64 bits

El sistema permite convertir valores hexadecimales de hasta 16 caracteres a una representación binaria de 64 bits y visualizarla mediante la matriz.

También permite modificar individualmente las LEDs y obtener nuevamente el valor hexadecimal correspondiente.

## Funcionalidades

### HEX → BINARIO → MATRIZ

El usuario introduce un valor hexadecimal.

Ejemplo:

F

El sistema lo convierte a:

000000000000000F

Y posteriormente a 64 bits:

00000000000000000000000000000000000000000000000000001111

Los bits se representan en la matriz 8x8.

### MATRIZ → BINARIO → HEX

El usuario puede hacer clic sobre las LEDs para cambiar su estado.

Cada LED representa:

- 0 = apagada
- 1 = encendida

La matriz se convierte nuevamente a una cadena binaria de 64 bits y posteriormente a un valor hexadecimal de 16 caracteres.

## Interacción

Al pasar el cursor sobre una LED, esta cambia temporalmente a color negro.

El hover no modifica el estado lógico de la LED.

Al hacer clic se modifica el estado de la LED.

## Tecnologías

- Python 3.12
- Flet 0.86.5

## Ejecución

Instalar dependencias:

```bash
pip install -r requirements.txt

Ejecutar:

flet run main.py

Ejecutar en modo web:

flet run --web main.py

---

# 3. Ahora vamos a publicar la aplicación 🌐

Y aquí tenemos una ventaja: **tu aplicación es ideal para una publicación estática** porque no utiliza base de datos, archivos externos ni servidor. Flet permite generar el sitio con:

```powershell
flet publish main.py

Esto genera una carpeta:

dist/

con la aplicación web lista para publicar.

Como tienes el ejecutable de Flet fuera del PATH, utiliza nuestro comando completo:

& "C:\Users\usuario_s2\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\flet.exe" publish main.py