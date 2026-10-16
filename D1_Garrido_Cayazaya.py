"""
D1_Garrido_Cayazaya.py
Desafío 1 · Tema 1.3 · Regla de la cadena:  (f∘g)'(x) = f'(g(x)) · g'(x)
Matemática Aplicada II (IBM121S) · Ingeniería Civil en Biomedicina · UDD · 2026

IDEA GENERAL
Un video es una secuencia de imágenes (cuadros): 30 por segundo.
Este programa tiene una función, cuadro_en(t), que dibuja con Matplotlib la imagen
que corresponde al segundo t del video. MoviePy le pide los cuadros uno por uno,
les agrega la narración y guarda el MP4. Los subtítulos y el archivo .srt salen
de la misma lista de tiempos (el GUION), por eso no se desfasan.

USO (en la terminal, dentro de la carpeta del proyecto):
    python D1_Garrido_Cayazaya.py            -> video final 1080x1920
    python D1_Garrido_Cayazaya.py --rapido   -> prueba rápida 540x960
"""

# ════════════════════════════════════════════════════════════════════════════
# 1. LIBRERÍAS  (import: traer herramientas que otros ya programaron)
# ════════════════════════════════════════════════════════════════════════════
import os                                   # revisar si existen archivos
import sys                                  # leer opciones de la terminal y detener el programa
import numpy as np                          # cálculos con números y vectores
import matplotlib                           # dibujar
matplotlib.use("Agg")                       # dibujar sin abrir ventanas
import matplotlib.pyplot as plt
matplotlib.rcParams["mathtext.fontset"] = "cm"   # fórmulas con letra matemática (sin instalar LaTeX)
from matplotlib.patches import FancyBboxPatch
from moviepy import VideoClip, AudioFileClip  # armar el video


# ════════════════════════════════════════════════════════════════════════════
# 2. PARÁMETROS EDITABLES  (variables: cambiar aquí y volver a ejecutar)
# ════════════════════════════════════════════════════════════════════════════

# --- Ejemplo matemático: y = f(g(x)) ---
# Si cambian el ejemplo, deben cambiar las 4 funciones y sus textos (formato LaTeX
# simple de Matplotlib, va entre $...$). El programa verifica las derivadas solo.
def g(x):               # función interna  u = g(x)
    return x**2 + 1


def dg(x):              # su derivada g'(x)
    return 2 * x


def f(u):               # función externa  y = f(u)
    return np.sin(u)


def df(u):              # su derivada f'(u)
    return np.cos(u)


TEXTO_G = r"x^2+1"                       # g(x)
TEXTO_F = r"\mathrm{sen}\,u"             # f(u)
TEXTO_Y = r"\mathrm{sen}(x^2+1)"         # f(g(x))
TEXTO_DG = r"2x"                         # g'(x)
TEXTO_DF = r"\cos\,u"                    # f'(u)
TEXTO_DFG = r"\cos(x^2+1)"               # f'(g(x))
TEXTO_RESULTADO = r"2x\,\cos(x^2+1)"     # derivada final simplificada

X0 = 1.0                # punto donde se estudia la derivada
DX_INICIAL = 0.6        # Δx que se muestra al principio
DX_FINAL = 0.002        # Δx al final de la animación del límite
H_INICIAL = 1.2         # h inicial de la secante
H_FINAL = 0.002         # h final de la secante
X_MIN, X_MAX = -2.0, 2.5  # ventana del gráfico de y = f(g(x))

# --- Aplicación: farmacodinamia ---
C0 = 10.0               # mg/L   concentración inicial del fármaco
K = 0.2                 # 1/h    constante de eliminación
EMAX = 100.0            # %      efecto máximo
EC50 = 5.0              # mg/L   concentración que produce el 50 % del efecto
T_EVAL = 2.0            # h      instante en que evaluamos

# --- Créditos ---
AUTORES = ["Benjamín Garrido", "Joaquín Cayazaya"]
RELATOR = "Nombre Apellido"          # quien graba la voz
DOCENTE = "Prof. Gustavo Castro P."
ASIGNATURA = "Matemática Aplicada II (IBM121S)"
ANIO = 2026
RECURSOS = ["Logos: Facultad de Ingeniería y", "Facultad de Medicina CAS-UDD (Canvas)", "Música: sin música",
            "Gráficos: Matplotlib · Montaje: MoviePy"]

# --- Archivos ---
NOMBRE = "D1_Garrido_Cayazaya"
AUDIO = "narracion.wav"
ETIQUETAS = "etiquetas.txt"
LOGO_FACULTAD = "assets/logo_facultad.png"   # Facultad de Ingeniería
LOGO_CARRERA = "assets/logo_carrera.png"     # Facultad de Medicina CAS-UDD

# --- Video ---
FPS = 30
DUR_CREDITOS = 7.0      # segundos
MODO_RAPIDO = "--rapido" in sys.argv     # True si escribimos --rapido en la terminal
if MODO_RAPIDO:
    DPI = 50            # 540 x 960
else:
    DPI = 100           # 1080 x 1920

# --- Colores: interna SIEMPRE azul, externa SIEMPRE naranja ---
FONDO = "#0E1117"
AZUL = "#4FC3F7"
NARANJA = "#FFB74D"
VERDE = "#81C784"
ROJO = "#FF6E6E"
GRIS = "#9AA0A6"
BLANCO = "#F1F3F4"

# --- Guion: lista de tuplas (id, inicio_s, fin_s, texto del subtítulo) ---
# Tiempos provisorios: si existe etiquetas.txt (Audacity), se usan los reales.
GUION = [
    ("gancho",       0.0,   2.9, "Si una función vive dentro de otra, ¿cómo se deriva?"),
    ("maquinas",     3.2,   7.8, "Una composición encadena dos máquinas: primero g y luego f."),
    ("notacion",     8.0,  12.4, "Entra x; g entrega u = g(x) y f entrega y = f(u)."),
    ("ejemplo",     12.6,  16.8, "En el ejemplo, g es la función interna y f, la externa."),
    ("pregunta",    17.0,  21.8, "Si x cambia un poco, ¿cuánto cambia y?"),
    ("delta_u",     22.0,  27.8, "Un cambio Δx en x produce en u un cambio Δu ≈ g'(x)·Δx."),
    ("delta_y",     28.0,  33.8, "Ese Δu, a su vez, produce en y un cambio Δy ≈ f'(u)·Δu."),
    ("encadenar",   34.0,  39.8, "Encadenando, Δy ≈ f'(u)·g'(x)·Δx: las razones se multiplican."),
    ("cociente",    40.0,  45.8, "Con rigor: Δy/Δx es igual a Δy/Δu por Δu/Δx."),
    ("limite",      46.0,  51.8, "Como g es continua, si Δx tiende a cero, Δu también."),
    ("formula",     52.0,  57.8, "En el límite, la derivada es f'(g(x)) por g'(x)."),
    ("receta1",     58.0,  62.3, "Receta: deriva la externa y evalúala en la interna..."),
    ("receta2",     62.5,  66.8, "...y multiplica por la derivada de la interna."),
    ("grafica",     67.0,  72.3, "Comprobémoslo con la secante a y = f(g(x))."),
    ("converge",    72.5,  77.8, "Si h tiende a cero, su pendiente converge al valor de la regla."),
    ("farmaco",     78.0,  82.8, "Aplicación: un fármaco se elimina según C(t) = C₀·e^(−kt)."),
    ("efecto",      83.0,  87.8, "Su efecto depende de la concentración: modelo Emax."),
    ("cadena_app",  88.0,  93.8, "E depende de t a través de C: dE/dt = dE/dC · dC/dt."),
    ("evaluar",     94.0,  97.8, "Evaluamos cada factor en el instante elegido, con unidades."),
    ("interpretar", 98.0, 101.8, "El signo negativo indica que el efecto va disminuyendo."),
    ("sintesis",   102.0, 109.5, "En resumen: en una composición, las razones se multiplican."),
]


# ════════════════════════════════════════════════════════════════════════════
# 3. LEER EL GUION Y LOS TIEMPOS  (archivos + listas + diccionarios)
# ════════════════════════════════════════════════════════════════════════════
def leer_etiquetas():
    """Si existe etiquetas.txt (exportado desde Audacity), reemplaza los tiempos
    provisorios por los reales. Cada línea del archivo es: inicio<TAB>fin<TAB>texto."""
    if not os.path.exists(ETIQUETAS):
        print("[guion] sin etiquetas.txt: se usan tiempos provisorios")
        return GUION
    filas = []
    with open(ETIQUETAS, encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split("\t")
            if len(partes) >= 2 and not partes[0].startswith("\\"):
                filas.append(partes)
    if len(filas) != len(GUION):
        print(f"[ERROR] {ETIQUETAS} tiene {len(filas)} etiquetas y el guion {len(GUION)} frases.")
        sys.exit()
    nuevo = []
    for i in range(len(GUION)):
        id_frase, _, _, texto = GUION[i]
        inicio = float(filas[i][0].replace(",", "."))
        fin = float(filas[i][1].replace(",", "."))
        if len(filas[i]) > 2 and filas[i][2] != "":
            texto = filas[i][2]          # si cambiaron la frase al grabar, se usa la nueva
        nuevo.append((id_frase, inicio, fin, texto))
    print(f"[guion] tiempos tomados de {ETIQUETAS}")
    return nuevo


GUION = leer_etiquetas()

# Diccionarios para buscar rápido cuándo empieza y termina cada frase: INICIO["limite"] -> 46.0
INICIO = {}
FIN = {}
for id_frase, inicio, fin, texto in GUION:
    INICIO[id_frase] = inicio
    FIN[id_frase] = fin

for id_frase, inicio, fin, texto_frase in GUION:      # pauta: subtítulos de máximo 2 líneas
    if len(texto_frase) > 66:
        print(f"[aviso] el subtítulo '{id_frase}' es largo: podría ocupar más de 2 líneas")

FIN_CORTINA = min(3.0, INICIO["maquinas"])        # la cortina dura máximo 3 s
INICIO_CREDITOS = FIN["sintesis"] + 0.4
DURACION = INICIO_CREDITOS + DUR_CREDITOS
if DURACION > 120:
    print(f"[ERROR] El video dura {DURACION:.1f} s y el máximo es 120 s.")
    sys.exit()


# ════════════════════════════════════════════════════════════════════════════
# 4. MATEMÁTICA  (valores en x0 y verificación de las derivadas)
# ════════════════════════════════════════════════════════════════════════════
def y(x):
    """La composición y = f(g(x))."""
    return f(g(x))


U0 = g(X0)              # u0 = g(x0)
Y0 = f(U0)              # y0 = f(u0)
DG0 = dg(X0)            # g'(x0)
DF0 = df(U0)            # f'(u0)
PENDIENTE = DF0 * DG0   # lo que predice la regla de la cadena


def derivada_numerica(funcion, x, h=1e-6):
    """Cociente incremental centrado: aproxima la derivada sin fórmulas."""
    return (funcion(x + h) - funcion(x - h)) / (2 * h)


def verificar():
    """Compara las derivadas escritas a mano con la derivada numérica en varios puntos.
    Si alguien escribe mal una derivada, el programa avisa y se detiene."""
    for x in [-1.5, -0.5, 0.3, 1.0, 1.7]:
        if abs(dg(x) - derivada_numerica(g, x)) > 1e-4:
            print(f"[ERROR] dg(x) no es la derivada de g(x) (falla en x = {x})")
            sys.exit()
        if abs(df(x) - derivada_numerica(f, x)) > 1e-4:
            print(f"[ERROR] df(u) no es la derivada de f(u) (falla en u = {x})")
            sys.exit()
        regla = df(g(x)) * dg(x)
        if abs(regla - derivada_numerica(y, x)) > 1e-4:
            print(f"[ERROR] la regla de la cadena no coincide en x = {x}")
            sys.exit()
    print(f"[mate] verificado: g'(x0) = {DG0:.4f}, f'(u0) = {DF0:.4f}, (f∘g)'(x0) = {PENDIENTE:.4f}")


# Aplicación: C(t) = C0·e^(−kt)  y  E(C) = Emax·C / (EC50 + C)
C_T = C0 * np.exp(-K * T_EVAL)                 # mg/L
DC_DT = -K * C_T                               # mg/(L·h)
DE_DC = EMAX * EC50 / (EC50 + C_T) ** 2        # % por mg/L
DE_DT = DE_DC * DC_DT                          # %/h   <- regla de la cadena


def efecto_en_el_tiempo(t):
    c = C0 * np.exp(-K * t)
    return EMAX * c / (EC50 + c)


# ════════════════════════════════════════════════════════════════════════════
# 5. HERRAMIENTAS DE DIBUJO  (funciones pequeñas que se reutilizan)
#    El "lienzo" ocupa toda la imagen: (0, 0) es la esquina inferior izquierda
#    y (1, 1) la superior derecha. Bajo y = 0.27 van los subtítulos.
# ════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(10.8, 19.2), dpi=DPI, facecolor=FONDO)
lienzo = None           # se crea de nuevo en cada cuadro
ANCHOS = {}             # memoria de anchos ya medidos (para no medir dos veces)
ESCALA = 1.25           # agranda todos los textos a la vez


def coma(valor, decimales=2):
    """3.14159 -> '3,14' (coma decimal, como en Chile)."""
    return f"{valor:.{decimales}f}".replace(".", ",")


def igual_o_aprox(valor, decimales=2):
    """'= 2' si el valor es exacto; '≈ 0,91' si hubo que redondear (formato LaTeX)."""
    if abs(valor - round(valor)) < 1e-9:              # entero exacto: 2
        return "=" + str(int(round(valor)))
    if abs(valor - round(valor, decimales)) < 1e-9:   # decimal exacto: 0,5
        return "=" + coma(valor, decimales).rstrip("0")
    return r"\approx " + coma(valor, decimales)


def opacidad(id_frase, t, retraso=0.0):
    """0 antes de que empiece la frase (+retraso); sube a 1 en medio segundo."""
    segundos = t - INICIO[id_frase] - retraso
    if segundos <= 0:
        return 0.0
    if segundos >= 0.5:
        return 1.0
    return segundos / 0.5


def progreso(id_frase, t, retraso=0.0, duracion=1.0):
    """Avance de una animación: 0 al empezar, 1 al terminar (con frenado suave)."""
    p = (t - INICIO[id_frase] - retraso) / duracion
    if p < 0:
        p = 0.0
    if p > 1:
        p = 1.0
    return 3 * p**2 - 2 * p**3      # curva suave: parte lento, acelera y frena


def texto(x, y_, contenido, tam=30, color=BLANCO, alfa=1.0, negrita=False, alinear="center"):
    if alfa > 0:
        grosor = "bold" if negrita else "normal"
        lienzo.text(x, y_, contenido, fontsize=tam * ESCALA, color=color, alpha=alfa,
                    ha=alinear, va="center", fontweight=grosor)


def ancho_de(contenido, tam):
    """Mide qué fracción del ancho de la imagen ocupa un texto."""
    clave = (contenido, tam)
    if clave not in ANCHOS:
        t = lienzo.text(0, 0, contenido, fontsize=tam * ESCALA)
        caja_px = t.get_window_extent(renderer=fig.canvas.get_renderer())
        ANCHOS[clave] = caja_px.width / fig.bbox.width
        t.remove()
    return ANCHOS[clave]


def formula(partes, y_, tam=34, alfa=1.0, x_centro=0.5, separacion=0.008):
    """Dibuja una fórmula con partes de distintos colores, centrada.
    partes = lista de (texto, color). Devuelve el ancho total (para enmarcarla)."""
    total = 0
    for contenido, color in partes:
        total = total + ancho_de(contenido, tam) + separacion
    total = total - separacion
    x = x_centro - total / 2
    for contenido, color in partes:
        if alfa > 0:
            lienzo.text(x, y_, contenido, fontsize=tam * ESCALA, color=color, alpha=alfa,
                        ha="left", va="center")
        x = x + ancho_de(contenido, tam) + separacion
    return total


def recuadro(x, y_, ancho, alto, color, alfa=1.0, relleno=0.0):
    if alfa > 0:
        lienzo.add_patch(FancyBboxPatch((x - ancho / 2, y_ - alto / 2), ancho, alto,
                                        boxstyle="round,pad=0.004,rounding_size=0.012",
                                        edgecolor=color, facecolor=color, lw=3,
                                        alpha=alfa, fill=False))
        if relleno > 0:
            lienzo.add_patch(FancyBboxPatch((x - ancho / 2, y_ - alto / 2), ancho, alto,
                                            boxstyle="round,pad=0.004,rounding_size=0.012",
                                            facecolor=color, edgecolor="none", alpha=relleno * alfa))


def flecha(x1, y1, x2, y2, color=GRIS, alfa=1.0):
    if alfa > 0:
        lienzo.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=3, alpha=alfa,
                                        mutation_scale=25))


def titulo(contenido):
    texto(0.5, 0.945, contenido, tam=34, negrita=True)


def maquinas(y_, nombres, colores, alfa=1.0):
    """Diagrama: entrada -> [caja] -> intermedio -> [caja] -> salida.
    nombres y colores son listas de 5 elementos; las posiciones 1 y 3 son cajas."""
    posiciones = [0.08, 0.29, 0.50, 0.71, 0.92]
    medio_ancho = [0.03, 0.075, 0.03, 0.075, 0.03]     # mitad del ancho de cada elemento
    for i in range(5):
        if i == 1 or i == 3:
            recuadro(posiciones[i], y_, 0.15, 0.045, colores[i], alfa, relleno=0.12)
        texto(posiciones[i], y_, "$" + nombres[i] + "$", tam=30, color=colores[i], alfa=alfa)
    for i in range(4):                                  # flechas entre elementos vecinos
        inicio = posiciones[i] + medio_ancho[i] + 0.01
        final = posiciones[i + 1] - medio_ancho[i + 1] - 0.01
        flecha(inicio, y_, final, y_, GRIS, alfa)


def logo(ruta, x, y_, alto, rotulo):
    """Muestra un logo; si el archivo no existe, dibuja un recuadro de reemplazo."""
    if os.path.exists(ruta):
        imagen = plt.imread(ruta)
        if imagen.shape[2] == 4:                     # PNG con transparencia: recortar bordes vacíos
            filas, columnas = np.where(imagen[:, :, 3] > 0)
            imagen = imagen[filas.min():filas.max() + 1, columnas.min():columnas.max() + 1]
        proporcion = imagen.shape[1] / imagen.shape[0]          # ancho / alto
        ancho = alto * proporcion * (19.2 / 10.8)
        ejes = fig.add_axes([x - ancho / 2, y_ - alto / 2, ancho, alto])
        ejes.imshow(imagen)
        ejes.axis("off")
    else:
        recuadro(x, y_, 0.26, alto, GRIS)
        texto(x, y_, rotulo, tam=14, color=GRIS)


def franja_logos(y_, alto):
    """Franja blanca con los dos logos: sus letras son oscuras y no se verían sobre el fondo negro."""
    recuadro(0.5, y_, 0.88, alto + 0.02, BLANCO, relleno=1.0)
    logo(LOGO_FACULTAD, 0.30, y_, alto, "Logo Facultad")
    logo(LOGO_CARRERA, 0.74, y_, alto, "Logo Carrera")


def partir_en_lineas(frase, max_caracteres=33):
    """Divide un subtítulo en líneas de máximo ~33 caracteres, sin cortar palabras."""
    lineas = []
    actual = ""
    for palabra in frase.split(" "):
        if actual == "":
            actual = palabra
        elif len(actual) + 1 + len(palabra) <= max_caracteres:
            actual = actual + " " + palabra
        else:
            lineas.append(actual)
            actual = palabra
    lineas.append(actual)
    return lineas


def subtitulo(t):
    """Busca qué frase se está diciendo en el segundo t y la dibuja abajo."""
    for id_frase, inicio, fin, frase in GUION:
        if inicio <= t < fin:
            lineas = partir_en_lineas(frase)
            lienzo.text(0.5, 0.20, "\n".join(lineas), fontsize=32, color="white",
                        ha="center", va="center", linespacing=1.3,
                        bbox=dict(facecolor="black", edgecolor="none", pad=10))


# ════════════════════════════════════════════════════════════════════════════
# 6. ESCENAS  (una función por cada parte del video; reciben el segundo t)
# ════════════════════════════════════════════════════════════════════════════
def escena_cortina(t):
    franja_logos(0.92, 0.05)
    texto(0.5, 0.865, "Matemática Aplicada II · Desafío 1", tam=18, color=GRIS)
    texto(0.5, 0.835, "1.3  Regla de la cadena", tam=26, negrita=True)
    texto(0.5, 0.66, "Si una función vive\ndentro de otra,\n¿cómo se deriva?", tam=40,
          negrita=True, alfa=opacidad("gancho", t))
    formula([("$f($", NARANJA), ("$g(x)$", AZUL), ("$)$", NARANJA)], 0.48, tam=80,
            alfa=opacidad("gancho", t, 0.9))


def escena_maquinas(t):
    titulo("Regla de la cadena")
    # 1) La composición como dos máquinas en serie
    maquinas(0.84, ["x", "g", "u", "f", "y"], [BLANCO, AZUL, AZUL, NARANJA, NARANJA],
             opacidad("maquinas", t))
    # 2) Notación
    texto(0.32, 0.75, "$u=g(x)$", tam=30, color=AZUL, alfa=opacidad("notacion", t))
    texto(0.68, 0.75, "$y=f(u)$", tam=30, color=NARANJA, alfa=opacidad("notacion", t))
    formula([("$y=$", NARANJA), ("$f($", NARANJA), ("$g(x)$", AZUL), ("$)$", NARANJA)],
            0.67, tam=50, alfa=opacidad("notacion", t, 2.0))
    # 3) El ejemplo concreto
    a = opacidad("ejemplo", t)
    formula([("$g(x)=" + TEXTO_G + "$", AZUL), ("interna", AZUL)], 0.56, tam=30, alfa=a, separacion=0.04)
    b = opacidad("ejemplo", t, 1.3)
    formula([("$f(u)=" + TEXTO_F + "$", NARANJA), ("externa", NARANJA)], 0.50, tam=30, alfa=b, separacion=0.04)
    formula([("$y=" + TEXTO_Y + "$", BLANCO)], 0.43, tam=34, alfa=opacidad("ejemplo", t, 2.6))


# --- Rectas numéricas x, u, y (misma escala en las tres) ---
RANGO = 1.25 * max(DX_INICIAL, abs(g(X0 + DX_INICIAL) - U0), abs(y(X0 + DX_INICIAL) - Y0))


def posicion(valor, centro):
    """Convierte un número en una posición horizontal sobre la recta."""
    return 0.55 + (valor - centro) / RANGO * 0.37


def recta(y_, centro, nombre, color, rotulo, alfa):
    if alfa <= 0:
        return
    lienzo.plot([0.18, 0.92], [y_, y_], color=GRIS, lw=2, alpha=alfa)
    for k in range(-4, 5):                                   # marcas cada RANGO/4
        xm = posicion(centro + k * RANGO / 4, centro)
        lienzo.plot([xm, xm], [y_ - 0.004, y_ + 0.004], color=GRIS, lw=2, alpha=alfa)
    texto(0.10, y_, "$" + nombre + "$", tam=34, color=color, alfa=alfa)
    lienzo.plot([posicion(centro, centro)], [y_], "o", color=color, ms=10, alpha=alfa)
    texto(posicion(centro, centro), y_ - 0.022, rotulo, tam=18, color=color, alfa=alfa)


def segmento(y_, base, delta, centro, color, nombre, alfa):
    if alfa <= 0 or delta == 0:
        return
    x1 = posicion(base, centro)
    x2 = posicion(base + delta, centro)
    lienzo.plot([x1, x2], [y_ + 0.008, y_ + 0.008], color=color, lw=9, alpha=alfa,
                solid_capstyle="butt")
    texto((x1 + x2) / 2, y_ + 0.024, "$" + nombre + "$", tam=20, color=color, alfa=alfa)


def delta_x_actual(t):
    """Valor de Δx en el segundo t: crece en 'delta_u' y se achica en 'limite'."""
    if t < INICIO["limite"]:
        return DX_INICIAL * progreso("delta_u", t, 0, 2.0)
    p = progreso("limite", t, 0.2, 3.8)
    return DX_INICIAL * (DX_FINAL / DX_INICIAL) ** p        # se achica de forma pareja


def escena_rectas(t):
    titulo("Regla de la cadena")
    texto(0.36, 0.905, "$u=g(x)$", tam=22, color=AZUL)
    texto(0.64, 0.905, "$y=f(u)$", tam=22, color=NARANJA)
    a = opacidad("pregunta", t, 0.5)
    recta(0.83, X0, "x", BLANCO, "$x_0" + igual_o_aprox(X0) + "$", a)
    recta(0.74, U0, "u", AZUL, "$u_0=g(x_0)" + igual_o_aprox(U0) + "$", opacidad("pregunta", t, 0.9))
    recta(0.65, Y0, "y", NARANJA, "$y_0=f(u_0)" + igual_o_aprox(Y0) + "$", opacidad("pregunta", t, 1.3))
    flecha(0.10, 0.815, 0.10, 0.757, AZUL, a)
    flecha(0.10, 0.725, 0.10, 0.667, NARANJA, a)
    texto(0.07, 0.785, "$g$", tam=20, color=AZUL, alfa=a)
    texto(0.07, 0.695, "$f$", tam=20, color=NARANJA, alfa=a)

    # Los tres cambios: Δx, Δu = g(x0+Δx) − g(x0), Δy = f(g(x0+Δx)) − f(g(x0))
    dx = delta_x_actual(t)
    du = g(X0 + dx) - U0
    dy = y(X0 + dx) - Y0
    segmento(0.83, X0, dx, X0, ROJO, r"\Delta x", opacidad("delta_u", t))
    segmento(0.74, U0, du, U0, AZUL, r"\Delta u", opacidad("delta_u", t))
    segmento(0.65, Y0, dy, Y0, NARANJA, r"\Delta y", opacidad("delta_y", t))

    # La fórmula de abajo cambia según la frase que se está diciendo
    if t < INICIO["delta_y"]:
        formula([(r"$\Delta u$", AZUL), (r"$\approx$", BLANCO), ("$g'(x)$", AZUL),
                 (r"$\cdot$", BLANCO), (r"$\Delta x$", ROJO)], 0.555, tam=36, alfa=opacidad("delta_u", t, 2.6))
    elif t < INICIO["encadenar"]:
        formula([(r"$\Delta y$", NARANJA), (r"$\approx$", BLANCO), ("$f'(u)$", NARANJA),
                 (r"$\cdot$", BLANCO), (r"$\Delta u$", AZUL)], 0.555, tam=36, alfa=opacidad("delta_y", t, 2.0))
    elif t < INICIO["cociente"]:
        formula([(r"$\Delta y$", NARANJA), (r"$\approx$", BLANCO), ("$f'(u)$", NARANJA),
                 (r"$\cdot$", BLANCO), ("$g'(x)$", AZUL), (r"$\cdot$", BLANCO), (r"$\Delta x$", ROJO)], 0.555, tam=36)
        texto(0.5, 0.505, "las razones se multiplican", tam=22, color=VERDE,
              alfa=opacidad("encadenar", t, 2.8))
    else:
        formula([(r"$\dfrac{\Delta y}{\Delta x}=$", BLANCO), (r"$\dfrac{\Delta y}{\Delta u}$", NARANJA),
                 (r"$\cdot$", BLANCO), (r"$\dfrac{\Delta u}{\Delta x}$", AZUL)], 0.555, tam=38)
        # Valores en vivo de los tres cocientes
        b = opacidad("cociente", t, 2.0)
        texto(0.92, 0.86, r"$\Delta x=$" + coma(dx, 3), tam=18, color=ROJO, alfa=b, alinear="right")
        filas = [(r"$\dfrac{\Delta u}{\Delta x}=$", du / dx, AZUL, "$g'(x_0)=" + coma(DG0, 3) + "$"),
                 (r"$\dfrac{\Delta y}{\Delta u}=$", dy / du, NARANJA, "$f'(u_0)=" + coma(DF0, 3) + "$"),
                 (r"$\dfrac{\Delta y}{\Delta x}=$", dy / dx, VERDE, coma(PENDIENTE, 3))]
        for i in range(3):
            etiqueta, valor, color, meta = filas[i]
            altura = 0.47 - i * 0.055
            texto(0.30, altura, etiqueta + " " + coma(valor, 3), tam=28, color=color, alfa=b,
                  alinear="left")
            texto(0.66, altura, r"$\rightarrow$ " + meta, tam=22, color=color,
                  alfa=opacidad("limite", t, 4.1 + 0.3 * i), alinear="left")
        texto(0.5, 0.305, "g continua: si Δx → 0, entonces Δu → 0", tam=17, color=GRIS,
              alfa=opacidad("limite", t, 0.2))


def escena_regla(t):
    titulo("Regla de la cadena")
    a = opacidad("formula", t, 0.6)
    ancho = formula([(r"$(f\circ g)'(x)=$", BLANCO), (r"$f'(g(x))$", NARANJA), (r"$\cdot$", BLANCO),
                     ("$g'(x)$", AZUL)], 0.85, tam=40, alfa=a)
    recuadro(0.5, 0.85, ancho + 0.06, 0.06, VERDE, a)
    formula([(r"$\dfrac{dy}{dx}=$", BLANCO), (r"$\dfrac{dy}{du}$", NARANJA), (r"$\cdot$", BLANCO),
             (r"$\dfrac{du}{dx}$", AZUL)], 0.75, tam=40, alfa=opacidad("formula", t, 3.2))
    # Receta aplicada al ejemplo
    formula([("$f'(u)=" + TEXTO_DF + "$", NARANJA)], 0.64, tam=30, alfa=opacidad("receta1", t))
    formula([("$f'(g(x))=" + TEXTO_DFG + "$", NARANJA)], 0.58, tam=30, alfa=opacidad("receta1", t, 1.6))
    formula([("$g'(x)=" + TEXTO_DG + "$", AZUL)], 0.51, tam=30, alfa=opacidad("receta2", t))
    formula([("$y'=$", BLANCO), ("$" + TEXTO_DFG + "$", NARANJA), (r"$\cdot$", BLANCO),
             ("$(" + TEXTO_DG + ")$", AZUL)], 0.44, tam=30, alfa=opacidad("receta2", t, 1.3))
    formula([("$=" + TEXTO_RESULTADO + "$", VERDE)], 0.38, tam=34, alfa=opacidad("receta2", t, 2.9))


def escena_secante(t):
    titulo("Regla de la cadena")
    a = opacidad("grafica", t, 0.3)
    if a <= 0:
        return
    # h: se mantiene en H_INICIAL y en 'converge' se achica hasta H_FINAL
    p = progreso("converge", t, 0, 3.6)
    h = H_INICIAL * (H_FINAL / H_INICIAL) ** p
    pendiente_secante = (y(X0 + h) - Y0) / h

    ejes = fig.add_axes([0.10, 0.50, 0.84, 0.36])
    ejes.set_facecolor("none")
    xs = np.linspace(X_MIN, X_MAX, 500)
    ejes.plot(xs, y(xs), color=BLANCO, lw=3, alpha=a)
    # Recta secante por P = (x0, y0) y Q = (x0+h, y(x0+h))
    ejes.plot(xs, Y0 + pendiente_secante * (xs - X0), color=ROJO, lw=2.5,
              alpha=opacidad("grafica", t, 2.4))
    ejes.plot([X0 + h], [y(X0 + h)], "o", color=ROJO, ms=11, alpha=opacidad("grafica", t, 2.4))
    ejes.plot([X0], [Y0], "o", color=NARANJA, ms=11, alpha=a)
    # Tangente (pendiente de la regla), al final
    ejes.plot(xs, Y0 + PENDIENTE * (xs - X0), "--", color=VERDE, lw=2.5,
              alpha=opacidad("converge", t, 3.8))
    minimo = min(y(xs))
    maximo = max(y(xs))
    margen = 0.15 * (maximo - minimo)
    ejes.set_ylim(minimo - margen, maximo + margen)
    ejes.set_xlim(X_MIN, X_MAX)
    for borde in ["top", "right"]:
        ejes.spines[borde].set_visible(False)
    for borde in ["left", "bottom"]:
        ejes.spines[borde].set_color(GRIS)
    ejes.tick_params(colors=GRIS, labelsize=14)
    texto(0.12, 0.88, "$y=" + TEXTO_Y + "$", tam=22, alfa=a, alinear="left")

    b = opacidad("grafica", t, 2.4)
    texto(0.5, 0.43, "$h=$ " + coma(h, 3), tam=28, alfa=b)
    texto(0.5, 0.375, r"$m_{sec}=\dfrac{y(x_0+h)-y(x_0)}{h}=$ " + coma(pendiente_secante, 3),
          tam=26, color=ROJO, alfa=b)
    texto(0.5, 0.32, r"$f'(g(x_0))\,g'(x_0)\approx$ " + coma(PENDIENTE, 3), tam=26, color=VERDE,
          alfa=opacidad("converge", t))


def escena_aplicacion(t):
    titulo("Aplicación: farmacodinamia")
    maquinas(0.875, ["t", "C(t)", "C", "E(C)", "E"], [BLANCO, AZUL, AZUL, NARANJA, NARANJA],
             opacidad("farmaco", t))
    texto(0.5, 0.835, "t en h  ·  C en mg/L  ·  E en %", tam=18, color=GRIS, alfa=opacidad("farmaco", t))
    texto(0.5, 0.785, r"$C(t)=C_0\,e^{-kt}$", tam=32, color=AZUL, alfa=opacidad("farmaco", t, 1.4))
    texto(0.5, 0.75, f"C₀ = {coma(C0, 0)} mg/L,   k = {coma(K, 1)} 1/h", tam=21, color=AZUL,
          alfa=opacidad("farmaco", t, 1.4))
    texto(0.5, 0.70, r"$E(C)=\dfrac{E_{max}\,C}{EC_{50}+C}$", tam=32, color=NARANJA,
          alfa=opacidad("efecto", t, 1.2))
    texto(0.5, 0.655, f"Emax = {coma(EMAX, 0)} %,   EC50 = {coma(EC50, 0)} mg/L", tam=21, color=NARANJA,
          alfa=opacidad("efecto", t, 1.2))
    a = opacidad("cadena_app", t)
    ancho = formula([(r"$\dfrac{dE}{dt}=$", BLANCO), (r"$\dfrac{dE}{dC}$", NARANJA), (r"$\cdot$", BLANCO),
                     (r"$\dfrac{dC}{dt}$", AZUL)], 0.585, tam=36, alfa=a)
    recuadro(0.5, 0.585, ancho + 0.06, 0.065, VERDE, opacidad("cadena_app", t, 2.2))
    te = coma(T_EVAL, 0)
    texto(0.5, 0.515, f"C({te}) = {coma(C0, 0)}·e^(−{coma(K * T_EVAL, 1)}) ≈ {coma(C_T)} mg/L", tam=22,
          color=AZUL, alfa=opacidad("evaluar", t))
    texto(0.5, 0.475, f"dC/dt = −k·C ≈ {coma(DC_DT)} mg/(L·h)", tam=22, color=AZUL,
          alfa=opacidad("evaluar", t, 0.8))
    texto(0.5, 0.435, f"dE/dC = Emax·EC50/(EC50+C)² ≈ {coma(DE_DC)} % por mg/L", tam=21, color=NARANJA,
          alfa=opacidad("evaluar", t, 1.6))
    b = opacidad("interpretar", t)
    texto(0.5, 0.375, f"dE/dt ≈ {coma(DE_DC)} · ({coma(DC_DT)}) ≈ {coma(DE_DT)} %/h", tam=24,
          color=VERDE, alfa=b, negrita=True)
    recuadro(0.5, 0.375, 0.86, 0.045, VERDE, b)
    if DE_DT < 0:
        tendencia = "disminuye"
    else:
        tendencia = "aumenta"
    texto(0.5, 0.325, f"A las {te} h, el efecto {tendencia} ≈ {coma(abs(DE_DT), 1)} puntos % por hora",
          tam=19, alfa=opacidad("interpretar", t, 1.8))


def escena_sintesis(t):
    titulo("En resumen")
    a = opacidad("sintesis", t)
    texto(0.20, 0.80, "$x$", tam=40, alfa=a)
    flecha(0.24, 0.80, 0.46, 0.80, AZUL, a)
    texto(0.35, 0.83, "$g'(x)$", tam=26, color=AZUL, alfa=a)
    texto(0.50, 0.80, "$u$", tam=40, color=AZUL, alfa=a)
    flecha(0.54, 0.80, 0.76, 0.80, NARANJA, a)
    texto(0.65, 0.83, "$f'(u)$", tam=26, color=NARANJA, alfa=a)
    texto(0.80, 0.80, "$y$", tam=40, color=NARANJA, alfa=a)
    b = opacidad("sintesis", t, 1.4)
    ancho = formula([(r"$\dfrac{dy}{dx}=$", BLANCO), (r"$f'(g(x))$", NARANJA), (r"$\cdot$", BLANCO),
                     ("$g'(x)$", AZUL)], 0.66, tam=44, alfa=b)
    recuadro(0.5, 0.66, ancho + 0.06, 0.075, VERDE, b)
    texto(0.5, 0.50, "En una composición,\nlas razones de cambio\nse multiplican.", tam=32, color=VERDE,
          alfa=opacidad("sintesis", t, 3.6))


def escena_creditos(t):
    a = min(1.0, (t - INICIO_CREDITOS) / 0.8)
    franja_logos(0.90, 0.045)
    bloques = [("Autores", AUTORES),
               ("Relator(a)", [RELATOR, "estudiante de Ing. Civil en Biomedicina"]),
               ("Docente", [DOCENTE]),
               ("Asignatura", [ASIGNATURA, f"Ingeniería Civil en Biomedicina · UDD · {ANIO}"]),
               ("Recursos", RECURSOS)]
    altura = 0.82
    for rotulo, lineas in bloques:
        texto(0.5, altura, rotulo, tam=18, color=GRIS, alfa=a)
        altura = altura - 0.03
        for linea in lineas:
            texto(0.5, altura, linea, tam=25, alfa=a)
            altura = altura - 0.03
        altura = altura - 0.02


# ════════════════════════════════════════════════════════════════════════════
# 7. EL CUADRO DEL SEGUNDO t  (if/elif: qué escena corresponde a cada momento)
# ════════════════════════════════════════════════════════════════════════════
def cuadro_en(t):
    """MoviePy llama a esta función 30 veces por segundo de video.
    Recibe el segundo t y devuelve la imagen (una matriz de píxeles)."""
    global lienzo
    fig.clf()                                         # borrar el cuadro anterior
    lienzo = fig.add_axes([0, 0, 1, 1])
    lienzo.set_xlim(0, 1)
    lienzo.set_ylim(0, 1)
    lienzo.axis("off")

    if t < FIN_CORTINA:
        escena_cortina(t)
    elif t < INICIO["pregunta"]:
        escena_maquinas(t)
    elif t < INICIO["formula"]:
        escena_rectas(t)
    elif t < INICIO["grafica"]:
        escena_regla(t)
    elif t < INICIO["farmaco"]:
        escena_secante(t)
    elif t < INICIO["sintesis"]:
        escena_aplicacion(t)
    elif t < INICIO_CREDITOS:
        escena_sintesis(t)
    else:
        escena_creditos(t)

    subtitulo(t)
    fig.canvas.draw()                                 # dibujar de verdad
    imagen = np.asarray(fig.canvas.buffer_rgba())     # convertir a matriz de píxeles
    return imagen[:, :, :3]                           # quitar la transparencia (RGBA -> RGB)


# ════════════════════════════════════════════════════════════════════════════
# 8. EXPORTAR: subtítulos .srt y video .mp4
# ════════════════════════════════════════════════════════════════════════════
def formato_srt(segundos):
    """62.5 -> '00:01:02,500' (formato de tiempo de los archivos .srt)."""
    horas = int(segundos // 3600)
    minutos = int(segundos % 3600 // 60)
    resto = segundos % 60
    return f"{horas:02}:{minutos:02}:{resto:06.3f}".replace(".", ",")


def escribir_srt():
    with open(NOMBRE + ".srt", "w", encoding="utf-8") as archivo:
        numero = 1
        for id_frase, inicio, fin, frase in GUION:
            archivo.write(f"{numero}\n{formato_srt(inicio)} --> {formato_srt(fin)}\n{frase}\n\n")
            numero = numero + 1
    print(f"[srt] {NOMBRE}.srt")


def crear_video():
    video = VideoClip(frame_function=cuadro_en, duration=DURACION)
    if os.path.exists(AUDIO):
        voz = AudioFileClip(AUDIO)
        if voz.duration > DURACION:
            voz = voz.subclipped(0, DURACION)
        video = video.with_audio(voz)
    else:
        print(f"[aviso] no se encontró {AUDIO}: el video sale sin voz")
    salida = NOMBRE + ("_rapido" if MODO_RAPIDO else "") + ".mp4"
    video.write_videofile(salida, fps=FPS, codec="libx264", audio_codec="aac",
                          ffmpeg_params=["-pix_fmt", "yuv420p"])
    print(f"[ok] {salida} ({DURACION:.1f} s)")


# ════════════════════════════════════════════════════════════════════════════
# 9. PROGRAMA PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[guion] duración total: {DURACION:.1f} s")
    verificar()
    escribir_srt()
    crear_video()
