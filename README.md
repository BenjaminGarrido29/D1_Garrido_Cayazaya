# Desafío 1 · Tema 1.3 · Regla de la cadena f(g(x))

Matemática Aplicada II (IBM121S) · Ingeniería Civil en Biomedicina · UDD · 2026

Un solo script de Python (`D1_Garrido_Cayazaya.py`) genera todo el video: cortina, escenas matemáticas, aplicación, subtítulos, audio y créditos. El resultado es un MP4 vertical de 1080×1920 a 30 fps (H.264 + AAC) y su archivo `.srt`.

## Idea central

Un video es una secuencia de imágenes: 30 por segundo. La función `cuadro_en(t)` dibuja con **Matplotlib** la imagen que corresponde al segundo `t`. **MoviePy** le pide esas imágenes una por una, les agrega la narración y guarda el MP4.

## Instalación

1. Instalar Python 3.10 a 3.12. **No se necesita LaTeX.**
2. Instalar las bibliotecas: `pip install -r requirements.txt`
3. Opcional: poner los logos de Canvas en `assets/logo_facultad.png` y `assets/logo_carrera.png`. Si faltan, se dibuja un recuadro en su lugar.

## Uso

```bash
python D1_Garrido_Cayazaya.py --rapido   # prueba en 540x960 (~2 min)
python D1_Garrido_Cayazaya.py            # video final en 1080x1920 (~4 min)
```

## Sincronización con la voz

1. Grabar la narración en Audacity leyendo el `GUION` del script.
2. Importar `etiquetas_plantilla.txt` (Archivo → Importar → Etiquetas) y ajustar cada etiqueta a su frase.
3. Exportar las etiquetas como `etiquetas.txt` y el audio como `narracion.wav`, en la carpeta del script.
4. Ejecutar el script. Las animaciones, los subtítulos y el `.srt` usan los mismos tiempos.

## Estructura del código

| Sección | Qué hace | Conceptos de Python |
|---|---|---|
| 1. Librerías | Importa NumPy, Matplotlib y MoviePy | `import` |
| 2. Parámetros | Funciones del ejemplo, punto x₀, datos del fármaco, créditos y guion | variables, `def`, listas de tuplas |
| 3. Guion | Lee `etiquetas.txt` y arma los diccionarios `INICIO` y `FIN` | archivos, `for`, diccionarios |
| 4. Matemática | Calcula valores en x₀ y **verifica** las derivadas con el cociente incremental | funciones, `if`, `for` |
| 5. Herramientas de dibujo | Texto, fórmulas en colores, flechas, recuadros, logos y subtítulos | funciones con parámetros |
| 6. Escenas | Una función por cada parte del video | `if`, `for`, listas |
| 7. `cuadro_en(t)` | Elige la escena según el segundo `t` | `if` / `elif` |
| 8. Exportar | Escribe el `.srt` y el `.mp4` | archivos |

## Parámetros editables

Para cambiar el ejemplo hay que editar las cuatro funciones (`g`, `dg`, `f`, `df`) y sus textos (`TEXTO_G`, etc.). El programa comprueba que `dg` y `df` sean realmente las derivadas comparándolas con el cociente incremental. Si hay un error, avisa y se detiene.

También se pueden cambiar `X0`, `DX_INICIAL`, `DX_FINAL`, `H_INICIAL`, `H_FINAL` y los datos del fármaco (`C0`, `K`, `EMAX`, `EC50`, `T_EVAL`).

## Aplicación

Eliminación de primer orden C(t) = C₀·e^(−kt) y modelo Emax E(C) = Emax·C/(EC₅₀ + C). Por regla de la cadena:

dE/dt = (dE/dC)·(dC/dt) ≈ −4,89 %/h en t = 2 h

Referencia del modelo: Holford y Sheiner (1981), *Understanding the dose-effect relationship*, Clinical Pharmacokinetics 6, 429–453. Los parámetros son ilustrativos.
