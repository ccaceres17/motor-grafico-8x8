"""
EDITOR DE SPRITES 8x8 - Motor grafico binario de 64 bits
Proyecto de Electronica Digital.

Compatible con Flet 0.86.5 / Python 3.12.

Doble direccion de conversion:
    1) HEXADECIMAL -> BINARIO(64 bits) -> MATRIZ 8x8
    2) MATRIZ 8x8  -> BINARIO(64 bits) -> HEXADECIMAL

Ejecutar en modo web:
    python main.py
o bien:
    flet run --web main.py
"""

import flet as ft

# ---------------------------------------------------------------
# CONSTANTES
# ---------------------------------------------------------------
TOTAL_LEDS = 64          # 8 x 8 = 64 bits
LADO = 8                 # matriz 8x8

COLOR_ON = ft.Colors.GREEN        # LED encendida (bit 1)
COLOR_OFF = ft.Colors.GREY_800    # LED apagada   (bit 0)
COLOR_HOVER = ft.Colors.BLACK     # LED bajo el cursor (temporal)
COLOR_BORDE = ft.Colors.GREY_700


def main(page: ft.Page):
    page.title = "Editor de Sprites 8x8"
    page.bgcolor = ft.Colors.GREY_900
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.padding = ft.Padding.all(24)

    # -----------------------------------------------------------
    # ESTADO LOGICO: 64 booleanos (False = apagada, True = encendida)
    # leds[i] es el Container visual correspondiente al bit i.
    # -----------------------------------------------------------
    estados = [False] * TOTAL_LEDS
    leds = []

    # -----------------------------------------------------------
    # OUTPUT (16 caracteres hex, mayusculas, con ceros a la izquierda)
    # -----------------------------------------------------------
    output_hex = ft.Text(
        value="0000000000000000",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN,
        font_family="monospace",
    )

    # -----------------------------------------------------------
    # HELPERS
    # -----------------------------------------------------------
    def pintar_led(i: int):
        """Aplica al Container el color segun su estado logico."""
        leds[i].bgcolor = COLOR_ON if estados[i] else COLOR_OFF

    def actualizar_output():
        """MATRIZ -> BINARIO(64) -> ENTERO -> HEX(16)."""
        binaria = "".join("1" if estados[i] else "0" for i in range(TOTAL_LEDS))
        numero = int(binaria, 2)
        output_hex.value = format(numero, "016X")

    # -----------------------------------------------------------
    # EVENTO: CLICK sobre una LED  (0 -> 1  /  1 -> 0)
    # -----------------------------------------------------------
    def on_led_click(indice: int):
        def handler(e):
            estados[indice] = not estados[indice]
            # El cursor sigue encima, se mantiene el color hover;
            # al salir el cursor se pintara con el nuevo estado.
            leds[indice].bgcolor = COLOR_HOVER
            actualizar_output()
            page.update()
        return handler

    # -----------------------------------------------------------
    # EVENTO: HOVER (no cambia el estado logico, solo el color)
    # e.data == "true"  -> el cursor entra  -> negro
    # e.data == "false" -> el cursor sale   -> color real del estado
    # -----------------------------------------------------------
    def on_led_hover(indice: int):
        def handler(e):
            if e.data == "true":
                leds[indice].bgcolor = COLOR_HOVER
            else:
                pintar_led(indice)
            page.update()
        return handler

    # -----------------------------------------------------------
    # CONSTRUCCION DE LAS 64 LEDS
    # -----------------------------------------------------------
    for i in range(TOTAL_LEDS):
        led = ft.Container(
            width=42,
            height=42,
            bgcolor=COLOR_OFF,
            border=ft.Border.all(1, COLOR_BORDE),
            border_radius=6,
            on_click=on_led_click(i),
            on_hover=on_led_hover(i),
        )
        leds.append(led)

    # Distribuir las LEDs en 8 filas de 8 columnas
    filas = []
    for r in range(LADO):
        fila = ft.Row(
            controls=[leds[r * LADO + c] for c in range(LADO)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        )
        filas.append(fila)

    matriz = ft.Column(
        controls=filas,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
    )

    # -----------------------------------------------------------
    # INPUT HEX  (maximo 16 caracteres, solo 0-9 y A-F)
    # -----------------------------------------------------------
    input_hex = ft.TextField(
        label="INPUT HEX",
        hint_text="Ej: F  /  FF  /  00000000000000FF  /  1234567890ABCDEF",
        max_length=16,
        width=420,
        text_size=16,
        keyboard_type=ft.KeyboardType.TEXT,
        # Filtra en vivo: solo permite digitos hexadecimales
        input_filter=ft.InputFilter(
            regex_string=r"[0-9a-fA-F]*",
            allow=True,
            replacement_string="",
        ),
    )

    # -----------------------------------------------------------
    # EVENTO: CARGAR HEX -> BINARIO(64) -> LEDS
    # -----------------------------------------------------------
    def cargar_hex(e):
        texto = (input_hex.value or "").strip().upper()

        # Validacion: vacio
        if texto == "":
            input_hex.error = "Ingrese un valor hexadecimal."
            page.update()
            return

        # Validacion: maximo 16 caracteres
        if len(texto) > 16:
            input_hex.error = "Maximo 16 caracteres hexadecimales."
            page.update()
            return

        # Validacion: solo caracteres hexadecimales
        try:
            numero = int(texto, 16)
        except ValueError:
            input_hex.error = "Solo se permiten caracteres 0-9 y A-F."
            page.update()
            return

        # Sin errores
        input_hex.error = None

        # HEX -> BINARIO de EXACTAMENTE 64 bits (conserva ceros a la izquierda)
        binario = format(numero, "064b")

        # BINARIO -> LEDS
        for i in range(TOTAL_LEDS):
            estados[i] = binario[i] == "1"
            pintar_led(i)

        # Refleja tambien el valor normalizado en el OUTPUT
        output_hex.value = format(numero, "016X")

        page.update()

    input_hex.on_submit = cargar_hex  # Enter tambien carga

    boton_cargar = ft.Button(
        content="CARGAR HEX",
        on_click=cargar_hex,
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        height=52,
    )

    # -----------------------------------------------------------
    # LAYOUT
    # -----------------------------------------------------------
    titulo = ft.Text("EDITOR DE SPRITES 8x8", size=30, weight=ft.FontWeight.BOLD,
                     color=ft.Colors.WHITE)
    subtitulo = ft.Text("Motor grafico binario de 64 bits", size=15,
                        color=ft.Colors.GREY_400)

    fila_input = ft.Row(
        controls=[input_hex, boton_cargar],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=12,
    )

    caja_output = ft.Container(
        content=output_hex,
        bgcolor=ft.Colors.BLACK,
        border=ft.Border.all(1, COLOR_BORDE),
        border_radius=8,
        padding=ft.Padding.all(14),
        alignment=ft.Alignment.CENTER,
    )

    page.add(
        ft.Column(
            controls=[
                titulo,
                subtitulo,
                ft.Container(height=10),
                ft.Text("INPUT HEX", size=16, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_300),
                fila_input,
                ft.Container(height=16),
                ft.Text("MATRIZ 8x8", size=16, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_300),
                matriz,
                ft.Container(height=16),
                ft.Text("OUTPUT HEXADECIMAL", size=16, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_300),
                caja_output,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        )
    )


# ---------------------------------------------------------------
# EJECUCION EN MODO WEB
# ---------------------------------------------------------------
if __name__ == "__main__":
    ft.app(main, view=ft.AppView.WEB_BROWSER, port=8550)