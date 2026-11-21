# Análisis críticos de los arquetipos de la serie «Un país que cambia»
# Un PDF por arquetipo, con la paleta de su historia. Textos en primera persona (la autora).
import os
from fpdf import FPDF

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "pdf")
ND = "/usr/share/fonts/truetype/noto"

def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

class AnalisisPDF(FPDF):
    def __init__(self, cfg):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.cfg = cfg
        self.set_margins(18, 14, 18)
        self.set_auto_page_break(True, margin=16)
        self.add_font("serif", "", os.path.join(ND, "NotoSerif-Regular.ttf"))
        self.add_font("serif", "B", os.path.join(ND, "NotoSerif-Bold.ttf"))
        self.add_font("serif", "I", os.path.join(ND, "NotoSerif-Italic.ttf"))
        self.add_font("sans", "", os.path.join(ND, "NotoSans-Regular.ttf"))
        self.add_font("sans", "B", os.path.join(ND, "NotoSans-Bold.ttf"))
        self.add_font("sans", "I", os.path.join(ND, "NotoSans-Italic.ttf"))

    def footer(self):
        c = self.cfg
        self.set_y(-13)
        self.set_draw_color(*hx(c["accent"]))
        self.set_line_width(0.4)
        self.line(18, self.get_y(), 198, self.get_y())
        self.ln(1.6)
        self.set_font("sans", "", 7.5)
        self.set_text_color(*hx("#666666"))
        self.cell(90, 4, f"Un país que cambia · Análisis crítico {c['num']} de 5 · {c['arq']}")
        self.cell(0, 4, f"Página {self.page_no()}", align="R")

    def header_band(self):
        c = self.cfg
        self.set_fill_color(*hx(c["dark"]))
        self.rect(0, 0, 216, 50, "F")
        self.set_fill_color(*hx(c["accent"]))
        self.rect(0, 50, 216, 1.6, "F")
        self.set_y(8)
        self.set_font("sans", "B", 8.5)
        self.set_text_color(*hx(c["light"]))
        self.cell(0, 5, c["eyebrow"].upper(), align="C")
        self.ln(6.5)
        self.set_font("serif", "B", 19.5)
        self.set_text_color(*hx("#FFFFFF"))
        self.cell(0, 9.5, c["title"], align="C")
        self.ln(10.5)
        self.set_font("sans", "I", 9.3)
        self.set_text_color(*hx(c["light"]))
        self.multi_cell(0, 4.6, c["deck"], align="C")
        self.set_y(53.2)
        self.set_font("sans", "", 8)
        self.set_text_color(*hx("#666666"))
        self.cell(0, 4, "Por Dagmary Pérez Aguiar · La Habana, noviembre de 2026", align="R")
        self.set_y(60)

    def ficha_box(self, ficha):
        c = self.cfg
        self.ln(2)
        rows = [("Audiencia", ficha["audiencia"]),
                ("Método", ficha["metodo"]),
                ("Lo que el dato no permite afirmar", ficha["limite"]),
                ("Y ahora, ¿qué?", ficha["accion"])]
        self.set_font("sans", "", 8.3)
        total = 6.6
        rendered = []
        for label, text in rows:
            full = f"{label}: {text}"
            lines = self.multi_cell(172, 3.85, full, align="L", dry_run=True, output="LINES")
            rendered.append((label, full, len(lines)))
            total += len(lines) * 3.85 + 0.7
        if self.get_y() + total > 262:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*hx(c["chip_bg"]))
        self.rect(18, y, 180, total, "F")
        self.set_fill_color(*hx(c["dark"]))
        self.rect(18, y, 180, 6.4, "F")
        self.set_xy(22, y + 1.2)
        self.set_font("sans", "B", 8.6)
        self.set_text_color(*hx("#FFFFFF"))
        self.cell(0, 4, "FICHA DEL PRODUCTO · MODELO: AUDIENCIA · MENSAJE · EVIDENCIA · FORMATO · MEDIO · ACCIÓN")
        yy = y + 8.3
        for label, full, n in rendered:
            self.set_xy(22, yy)
            self.set_font("sans", "", 8.3)
            self.set_text_color(*hx("#333333"))
            self.multi_cell(172, 3.85, full, align="L")
            yy += n * 3.85 + 0.7
        self.set_y(y + total + 2)

    def tabla_producto(self, ficha):
        c = self.cfg
        self.ln(2)
        rows = [("Audiencia", ficha["audiencia"]),
                ("Método", ficha["metodo"]),
                ("Lo que el dato no permite afirmar", ficha["limite"])]
        lw, cw = 42, 138
        self.set_font("sans", "", 8.6)
        medidas = []
        total = 7.5
        for label, text in rows:
            cl = self.multi_cell(cw - 4, 4.1, text, align="L", dry_run=True, output="LINES")
            self.set_font("sans", "B", 8.6)
            ll = self.multi_cell(lw - 4, 4.1, label, align="L", dry_run=True, output="LINES")
            self.set_font("sans", "", 8.6)
            h = max(len(cl), len(ll)) * 4.1 + 2.6
            medidas.append((label, text, h))
            total += h
        if self.get_y() + total > 262:
            self.add_page()
        y = self.get_y()
        # fila de cabecera
        self.set_fill_color(*hx(c["dark"]))
        self.rect(18, y, 180, 7.5, "F")
        self.set_xy(20, y + 1.8)
        self.set_font("sans", "B", 8.6)
        self.set_text_color(*hx("#FFFFFF"))
        self.cell(lw - 2, 4, "Elemento")
        self.set_xy(18 + lw + 2, y + 1.8)
        self.cell(cw - 2, 4, "Contenido")
        yy = y + 7.5
        for label, text, h in medidas:
            self.set_fill_color(*hx(c["chip_bg"]))
            self.rect(18, yy, lw, h, "F")
            self.set_xy(20, yy + 1.3)
            self.set_font("sans", "B", 8.6)
            self.set_text_color(*hx(c["dark"]))
            self.multi_cell(lw - 4, 4.1, label, align="L")
            self.set_xy(18 + lw + 2, yy + 1.3)
            self.set_font("sans", "", 8.6)
            self.set_text_color(*hx("#333333"))
            self.multi_cell(cw - 4, 4.1, text, align="L")
            self.set_draw_color(*hx(c["accent"]))
            self.set_line_width(0.3)
            self.line(18, yy + h, 198, yy + h)
            yy += h
        self.set_y(yy + 2.5)

    def refs(self, text):
        self.ln(0.5)
        self.set_font("sans", "", 8.3)
        self.set_text_color(*hx("#555555"))
        self.multi_cell(0, 4.1, text, align="L")

    def subhead(self, text):
        c = self.cfg
        self.ln(1.6)
        self.set_font("sans", "B", 11)
        self.set_text_color(*hx(c["dark"]))
        self.cell(0, 5.6, text)
        self.ln(5.9)

    def para(self, text):
        self.set_font("serif", "", 11)
        self.set_text_color(*hx("#2B2B2B"))
        self.multi_cell(0, 5.7, text, align="L")
        self.ln(1.1)

ANALISIS = []

# ---- 1 · El Héroe
ANALISIS.append(dict(
    num=1, arq="El Héroe", slug="analisis-1-el-heroe",
    eyebrow="Serie Un país que cambia · Análisis crítico 1 de 5",
    title="Análisis crítico: El Héroe",
    deck="El arquetipo puesto a prueba contra «La ciencia cubana tiene nombre de mujer», la historia de las investigadoras cubanas.",
    dark="#583B59", accent="#F1607D", light="#FBD9CF",
    blocks=[
        ("h", "El arquetipo"),
        ("p", "En la tradición que fijó Christopher Vogler en El viaje del escritor (1992), a partir de los mitos que estudió Joseph Campbell, el héroe es quien sale de su mundo, supera pruebas y regresa con algo para su comunidad. Es un arquetipo de recorrido: hay una meta, hay obstáculos y hay un avance que se puede contar paso a paso. Su fuerza está en que el lector siempre sabe hacia dónde va la historia."),
        ("h", "Cómo lo usé"),
        ("p", "Mi historia altera el arquetipo en su base: la heroína no es una persona, son miles. Quedó escrito desde el primer párrafo, y el recorrido tampoco es un viaje, es una escalera. La proporción de mujeres en la Academia de Ciencias de Cuba sube del 25,9 % en 1998-2002 al 34 % en 2018-2023 y al 39 % en 2024-2029, y el texto se organiza como ese ascenso, con la cima todavía sin alcanzar. El cierre devuelve la imagen al cuento: la heroína de los cuentos suele llevar capa y espada; aquí lleva bata blanca, microscopio y una paciencia de décadas."),
        ("h", "Lo que aporta al dato"),
        ("p", "El arquetipo le da dirección a las cifras. Un porcentaje suelto se olvida al cerrar la página; una escalera que se sube se recuerda, y cada dato nuevo se coloca solo en el peldaño que le toca. También coloca al lector en un sitio concreto, al lado de la protagonista, y hace que lea la comparación con el mundo (33 % de investigadoras en el planeta, 49 % en Cuba, según la UNESCO) como un avance propio. Para un tema donde el país sale bien en la comparación, el héroe permite decirlo con emoción sin inventar nada."),
        ("h", "Lo que deforma o esconde"),
        ("p", "Tres cosas, y ninguna es menor. Primero, el relato heroico tiende al triunfalismo: si la protagonista ya demostró de sobra que puede, el lector puede cerrar el texto creyendo que el problema está resuelto, cuando la propia historia muestra que la presencia femenina cae justo donde se decide, y que la Academia sigue en 39 %. Segundo, la gesta borra las causas. Las mujeres no llegaron a los laboratorios por heroísmo, llegaron por décadas de educación pública y de políticas de empleo; el arquetipo convierte un resultado institucional en mérito personal, aunque sea colectivo. Tercero, una heroína sin rostro puede volverse abstracta: en mi historia no habla ninguna investigadora con nombre, y eso es una pérdida real de verdad."),
        ("h", "Qué haría distinto"),
        ("p", "Probaría la misma historia con una protagonista individual y verificable: una investigadora concreta, con su laboratorio y su tema, y dejaría que las cifras nacionales entraran como el contexto de su caso. Se perdería la amplitud del retrato colectivo y se ganaría lo que el héroe clásico tiene y mi versión no: una persona a la que el lector puede mirar a los ojos."),
        ("h", "Veredicto"),
        ("p", "Volvería a usar el héroe para datos de logro colectivo con comparación internacional, porque ordena, emociona y no necesita falsear nada. No lo usaría cuando el dato central sea una desigualdad vigente: ahí el tono heroico maquilla lo que debería incomodar, y el análisis se convierte en celebración."),
    ],
))

# ---- 2 · El Detective
ANALISIS.append(dict(
    num=3, arq="El Detective", slug="analisis-3-el-detective",
    eyebrow="Serie Un país que cambia · Análisis crítico 3 de 5",
    title="Análisis crítico: El Detective",
    deck="El arquetipo puesto a prueba contra «El caso de los millones que faltan», la historia de la caída de la población cubana.",
    dark="#28441E", accent="#6A1A35", light="#C8D0B8",
    blocks=[
        ("h", "El arquetipo"),
        ("p", "El detective nace en la novela policial del siglo XIX y se fija con personajes como Sherlock Holmes, creado por Arthur Conan Doyle en 1887. Llega a una escena incompleta, recoge indicios en un orden deliberado y reconstruye lo que pasó. Su promesa al lector es doble: existe una explicación y se puede llegar a ella siguiendo el razonamiento, paso a paso, sin trampas."),
        ("h", "Cómo lo usé"),
        ("p", "Convertí la caída de la población en un misterio por resolver: el resumen lo anuncia («Vamos a resolver este misterio con las pistas que los datos nos dejaron») y la historia abre con dos cifras, un país de 11.239.224 habitantes en 2016 que en 2024 cuenta 9.748.007. El resto avanza por descarte: primero comprueba que no es un error de conteo, después presenta el saldo migratorio como la pista que señala al aeropuerto, descompone 2024 en sus componentes (nacimientos, defunciones y migración neta) y cierra con el escenario, sin un solo culpable. Los dos gráficos funcionan dentro del texto como las pruebas de esa cadena, y los subtítulos «Pista uno» y «Pista dos» marcan los pasos de la deducción."),
        ("h", "Lo que aporta al dato"),
        ("p", "El detective le presta a la demografía su mejor virtud: el orden de la deducción. Antes de señalar la migración, el texto descarta la explicación falsa, que es lo mismo que hace un análisis serio y lo que casi ningún lector haría solo frente a una tabla de la ONEI. El lector llega así a la cifra del saldo, -251.221 personas en 2024, como a una conclusión propia y no como a un titular que hay que creer. Además, ese orden justifica la selección de datos: cada cifra entra porque responde a la pregunta anterior."),
        ("h", "Lo que deforma o esconde"),
        ("p", "El precio es alto y conviene decirlo sin rodeos. La emigración es un duelo para quien se va y para quien se queda, y el arquetipo lo convierte en un juego de ingenio: la frialdad del procedimiento puede leerse como distancia ante el dolor ajeno. Las personas quedan reducidas a pistas, saldos y componentes; nadie que haya emigrado habla en la historia. Hay además una tensión de fondo: la forma policial promete un culpable y un cierre, y estos datos no tienen ninguno de los dos. Mi propio texto admite que no hay un solo culpable, pero la estructura sigue empujando hacia una resolución que la realidad no ofrece. La tabla del producto lo reconoce a su manera: el saldo migratorio es una diferencia neta, no el conteo de quienes se fueron ni el mapa de a dónde fueron."),
        ("h", "Qué haría distinto"),
        ("p", "El mismo tema admite el arquetipo del Testigo: alguien que cuenta desde dentro, la madre que despide a un hijo o el recién llegado que escribe a su familia, con las cifras oficiales como telón de fondo. Se perdería la claridad de la deducción y se ganaría lo que al detective le falta, una voz humana que el lector pueda verificar y recordar."),
        ("h", "Veredicto"),
        ("p", "Lo usaría de nuevo cuando la historia sea, en rigor, una descomposición: una cifra grande que se explica por partes y donde el orden de las pruebas cambia la conclusión. No lo usaría cuando el centro del tema sea la experiencia de las personas, porque el procedimiento las convierte en evidencia y el dato gana a costa de ellas."),
    ],
))

# ---- 3 · La Sombra
ANALISIS.append(dict(
    num=5, arq="La Sombra", slug="analisis-5-la-sombra",
    eyebrow="Serie Un país que cambia · Análisis crítico 5 de 5",
    title="Análisis crítico: La Sombra",
    deck="El arquetipo puesto a prueba contra «Las playas que se quedaron esperando», la historia del turismo que no vuelve.",
    dark="#074461", accent="#FDD503", light="#BFE3F2",
    blocks=[
        ("h", "El arquetipo"),
        ("p", "En la psicología de Carl Gustav Jung, la sombra es la parte de uno mismo que no se quiere mirar y que, aun así, actúa. La narrativa la tomó después como la amenaza latente: aquello que no aparece en escena pero condiciona todo lo que ocurre. No es un villano con nombre y apellido; es una presencia que se conoce por sus efectos, y por eso exige un lector atento a lo que falta."),
        ("h", "Cómo lo usé"),
        ("p", "Mi historia trata de una ausencia, y la sombra era el arquetipo que mejor la nombraba. El texto abre con hoteles con la mitad de las luces encendidas y tumbonas alineadas frente a un mar perfecto sin nadie tumbado en ellas, y presenta el turismo como el motor más visible de la economía, un motor que hoy tose. Los datos entran como efectos de esa presencia: 4,6 millones de visitantes en 2018, 2,2 millones en 2024, la recuperación que se intenta en 2023 y se interrumpe. La sombra me permitió además enlazar con el tema de la emigración: los cubanos residentes en el exterior que dejaron de visitar la isla, un 17,8 % menos, son la parte más íntima de lo que falta."),
        ("h", "Lo que aporta al dato"),
        ("p", "Representar lo que no está es el problema clásico de cualquier historia de caída, y la sombra lo resuelve en el plano del lenguaje: convierte una resta en una atmósfera que el lector puede ver antes de leer una sola cifra. También sostiene la advertencia sin necesidad de inventar un culpable. La sombra no acusa a nadie, anuncia consecuencias, y eso encaja con unos datos que miden llegadas de visitantes y no los motivos de quienes dejaron de venir. Cuando el dato es una ausencia, el arquetipo le da cuerpo sin falsearlo."),
        ("h", "Lo que deforma o esconde"),
        ("p", "La sombra cobra dos precios. El primero es el fatalismo: contra una sombra no se discute ni se negocia, y el lector puede salir del texto con la sensación de que la caída es un destino, cuando detrás hay decisiones concretas y discutibles, de mercados, de políticas y de una crisis energética que sí tiene responsables. El segundo precio es que el sector queda como una entidad sin rostro: las personas que viven del turismo aparecen tarde y como una lista de afectados, no como protagonistas de su propia historia. Y hay una pregunta que el arquetipo me impidió hacer: si depender de un solo mercado para casi 4 de cada 10 visitantes ya era una fragilidad antes de la caída. La sombra llora lo perdido; no examina si lo perdido era sólido."),
        ("h", "Qué haría distinto"),
        ("p", "Contaría la misma caída desde el arquetipo del Anfitrión: la dueña de una casa particular, el taxista, la artesana que vende en el malecón, cada uno con su cuenta del año, y las cifras nacionales entrando como el clima que rodea sus decisiones. La ausencia se seguiría viendo, pero tendría nombres, y el lector podría juzgar por sí mismo qué parte es destino y qué parte es decisión."),
        ("h", "Veredicto"),
        ("p", "La sombra sirve para historias de pérdida difusa, donde el dato es una ausencia y no existe un responsable único que las cifras puedan señalar. Deja de servir cuando el análisis necesita responsables y decisiones concretas, porque su atmósfera los disuelve y termina protegiendo a quien debería responder."),
    ],
))

# ---- 4 · El Sabio
ANALISIS.append(dict(
    num=2, arq="El Sabio", slug="analisis-2-el-sabio",
    eyebrow="Serie Un país que cambia · Análisis crítico 2 de 5",
    title="Análisis crítico: El Sabio",
    deck="El arquetipo puesto a prueba contra «Los que no nacen y los que envejecen», la historia demográfica de la cuna vacía y la vejez creciente.",
    dark="#472C3B", accent="#A43C2F", light="#F5EDBB",
    blocks=[
        ("h", "El arquetipo"),
        ("p", "El sabio es la figura que ya vio pasar el tiempo y por eso habla sin prisa: el anciano de los cuentos, el consejero que matiza y que advierte antes de que el problema estalle. Su autoridad no viene de un cargo, viene de la experiencia acumulada, y su función dentro del relato es poner el presente en una perspectiva larga, donde casi todo lo que parece nuevo ya ocurrió antes de otra forma."),
        ("h", "Cómo lo usé"),
        ("p", "La historia abre con la figura en voz baja («Un sabio no levanta la voz: ha vivido bastante para reconocer una señal cuando la ve») y se cuenta con dos relojes que marchan en sentidos opuestos, el de los nacimientos y el de la vejez. En el momento en que el texto podría caer en el lamento, se detiene en un «Pero hay que matizar» para recordar que envejecer es también una conquista de la salud pública. El dato con más recorrido del texto es una racha: Cuba no alcanza el nivel de reemplazo, los 2,1 hijos por mujer que mantienen estable una población, desde 1978. Esa mirada de medio siglo es el gesto propio del arquetipo, y el cierre lo hace explícito: los datos demográficos no gritan, dan señales con décadas de antelación, y atenderlas a tiempo es la diferencia entre envejecer con dignidad y envejecer por descuido."),
        ("h", "Lo que aporta al dato"),
        ("p", "El envejecimiento se presta al titular catastrofista, y el sabio permite sostener la paradoja completa sin mentir: la gente vive más años, que es un éxito, y eso mismo genera una factura en pensiones y cuidados. Su lentitud también es una forma de respeto por el lector. En vez de soltarle el 25,7 % de población con 60 años o más como un susto, el texto lo lleva por la balanza de nacimientos y defunciones de 2024 y por el mapa de las provincias, hasta que la cifra se entiende y deja de ser solo una cifra."),
        ("h", "Lo que deforma o esconde"),
        ("p", "La serenidad tiene un precio político que mi historia paga. Pensiones que no alcanzan y cuidados que no llegan son urgencias de hoy, y una voz que no levanta la voz puede sonar a resignación: si el fenómeno se veía venir desde 1978, la pregunta incómoda es quién no escuchó, y el texto no la formula. Hay un segundo problema de método: el sabio tradicional transmite verdades que no se discuten, y mi historia descansa en una sola fuente, la ONEI, presentada sin contraste con ninguna otra estimación. Y un tercer problema, de representación: en una historia sobre personas mayores no habla ninguna persona mayor. La sabiduría queda del lado de la narradora y no de los protagonistas."),
        ("h", "Qué haría distinto"),
        ("p", "El arquetipo de la Cuidadora pondría el centro donde el sabio solo pasa de visita: en el trabajo diario de cuidar a una persona mayor, que es donde el envejecimiento se vive de verdad. Las cifras serían las mismas y el mapa no cambiaría; cambiaría quién tiene la palabra y qué cuenta como problema, si la tendencia de un gráfico o la noche sin dormir de quien cuida."),
        ("h", "Veredicto"),
        ("p", "El sabio es el arquetipo correcto para procesos lentos que necesitan contexto, y para evitar un alarmismo que los datos no justifican. Debe usarse con una condición que mi historia cumple solo a medias: que la calma no sustituya a las preguntas por las decisiones tomadas y por las que faltan, y que los protagonistas hablen con su propia voz."),
    ],
))

# ---- 5 · La Transformación
ANALISIS.append(dict(
    num=4, arq="La Transformación", slug="analisis-4-la-transformacion",
    eyebrow="Serie Un país que cambia · Análisis crítico 4 de 5",
    title="Análisis crítico: La Transformación",
    deck="El arquetipo puesto a prueba contra «Los que se quedaron y emprendieron», la historia de las mipymes privadas.",
    dark="#24503C", accent="#E9B44C", light="#F5E3B0",
    blocks=[
        ("h", "El arquetipo"),
        ("p", "La transformación es el arquetipo del cambio de estado: lo que era una cosa pasa a ser otra, como en los cuentos donde nada vuelve a ser lo que fue después de cierto momento. En un relato marca un antes y un después nítidos, casi siempre con una fecha o un acontecimiento que hace de bisagra, y su energía está en el contraste entre los dos momentos."),
        ("h", "Cómo lo usé"),
        ("p", "Mi historia se apoya en una bisagra exacta, septiembre de 2021, cuando las micro, pequeñas y medianas empresas privadas fueron legalizadas en Cuba, y en una escena que se repite, la de una reja que se abre por primera vez, un cartel recién pintado y una población mirando nuevas ofertas. El antes es la prohibición de décadas; el después es un conteo: 9.236 mipymes privadas en diciembre de 2024 y 9.550 en marzo de 2025, según el registro del Ministerio de Economía y Planificación, con 262.000 trabajadores en los nuevos actores económicos. El cierre la coloca como respuesta a las tres anteriores: frente a los que se van, estos son los que se quedan."),
        ("h", "Lo que aporta al dato"),
        ("p", "Ningún otro arquetipo le daría a un registro administrativo un arco tan claro. La transformación convierte una lista de empresas autorizadas en un proceso con dirección, y permite al lector situar el dato dentro de la serie completa: tras dos historias de pérdida seguidas, esta cuenta una construcción. La escena de la reja cumple además una función de escala, porque baja la economía a la esquina del barrio, que es donde estas empresas existen y donde el lector puede comprobar el fenómeno con sus propios ojos."),
        ("h", "Lo que deforma o esconde"),
        ("p", "El arco de la transformación promete un final que los datos no conocen. El registro cuenta empresas en operación en dos fechas; no dice cuántas prosperan, cuánto venden ni cuánto tiempo duran, y la propia tabla del producto lo declara. Al ordenar las cifras como un ascenso, el texto se acerca más de lo debido al discurso promocional: la inflación, los apagones y la escasez quedan fuera del texto, sin medirse como factores. La brecha de género, más del 74 % de los socios son hombres, queda registrada como un contraste curioso con la primera historia, cuando podría ser un problema central del fenómeno. Y la transformación que se celebra es la individual, la de emprender, mientras la pregunta estructural de qué lugar ocuparán estas empresas en la economía del país queda fuera del texto."),
        ("h", "Qué haría distinto"),
        ("p", "El arquetipo del Artesano contaría el mismo fenómeno con menos épica y más oficio: seguir a una sola mipyme real durante un año, con sus cuentas, sus permisos y sus tropiezos, usando el registro nacional como marco y no como argumento. Se perdería amplitud, porque un caso no suma 9.550, y se ganaría la verdad de detalle que el conteo no puede dar."),
        ("h", "Veredicto"),
        ("p", "La transformación funciona cuando el cambio de estado es real y está fechado, como ocurre aquí. Su riesgo es confundir el inicio del cambio con su resultado. Mientras los datos solo midan nacimientos de empresas y no su vida, este arquetipo debe usarse declarando ese límite en el propio texto; si no se declara, el análisis se convierte en propaganda con cifras."),
    ],
))

# ---------------------------------------------------------------- ficha y contraste
CHIP_BG = {1: "#FDF1EE", 2: "#F8F3E2", 3: "#EEF2E4", 4: "#EDF4EE", 5: "#EAF6FB"}

FICHAS = {
    1: dict(
        audiencia="público general y, en especial, jóvenes que están eligiendo qué estudiar.",
        metodo="historia construida con datos secundarios ya publicados por UNESCO, la Academia de Ciencias de Cuba y la ONEI; no se recogieron datos nuevos y las cifras se citan tal como las publican las fuentes.",
        limite="En Cuba hay igualdad plena entre mujeres y hombres en la ciencia: los datos muestran paridad de participación, pero la presencia femenina disminuye en los niveles más altos, como la membresía de la Academia.",
        accion="si conoces a una niña o joven que duda de si la ciencia es para ella, cuéntale esta historia con sus cifras: en Cuba, 49 de cada 100 personas que investigan son mujeres."),
    3: dict(
        audiencia="público general, con atención a las familias cubanas que tienen a alguien dentro o fuera de la isla.",
        metodo="historia construida con las series oficiales de población y migración publicadas por la ONEI; las diferencias entre años y el promedio diario son cálculos de la autora a partir de esas cifras.",
        limite="El saldo migratorio de 2024, -251.221 personas, es una diferencia neta entre salidas y entradas: no es el conteo de las personas que emigraron, y tampoco dice a qué países se fueron.",
        accion="antes de compartir cualquier cifra de emigración, comprueba su año y su fuente; y si tienes a alguien lejos, esta historia es un buen pretexto para llamarlo hoy."),
    5: dict(
        audiencia="público general y, en especial, quienes trabajan en el turismo o viven de él.",
        metodo="historia construida con las estadísticas de llegadas publicadas por la ONEI y recogidas por la agencia EFE, y con datos del Ministerio de Turismo sobre mercados emisores; el porcentaje de caída frente a 2019 es cálculo de la autora. Se omiten 2020 y 2021, los años del cierre por la pandemia.",
        limite="El turismo cayó por una sola causa: las cifras miden cuántos visitantes llegaron, no los motivos de quienes dejaron de venir; las causas son varias y estos datos, por sí solos, no las separan.",
        accion="si vives del turismo o conoces a quien vive de él, comparte esta historia con las cifras completas y su fuente: entender la caída, sin exagerarla ni esconderla, es el primer paso para revertirla."),
    2: dict(
        audiencia="público general y, en especial, familias que cuidan o cuidarán a personas mayores.",
        metodo="historia construida con los indicadores demográficos oficiales de la ONEI (nacimientos, defunciones, fecundidad y envejecimiento); la razón entre defunciones y nacimientos es cálculo de la autora.",
        limite="Cuba tendrá una población determinada en 2050: estos datos describen 2024 y una tendencia de décadas, pero no predicen el futuro, que depende también de la migración y de las políticas que se adopten.",
        accion="haz la cuenta en tu propia familia: ¿quiénes tienen más de 60 años y quién los cuida o los cuidará? Conversarlo ahora, con los datos sobre la mesa, es parte de envejecer con dignidad."),
    4: dict(
        audiencia="público general y, en especial, quienes se plantean emprender o ya tienen un negocio pequeño.",
        metodo="historia construida con el registro oficial de mipymes del Ministerio de Economía y Planificación y la distribución sectorial de la ONEI; el aumento trimestral es cálculo de la autora a partir de ambos cortes.",
        limite="Las mipymes están salvando la economía: el registro cuenta empresas en operación, pero no dice cuántas prosperan, cuánto venden ni cuántos empleos generan; eso estos datos no lo miden.",
        accion="la próxima vez que pases frente a un negocio privado nuevo, entra, compra algo si puedes y pregunta cómo empezó: detrás de cada uno de estos 9.550 locales hay una historia que merece ser contada."),
}

CONTRASTES = {
    1: "La tabla declara como audiencia a las jóvenes que están eligiendo qué estudiar, la misma protagonista colectiva del relato. Pero la misma tabla pone el límite que el tono heroico tiende a borrar, porque no permite afirmar que haya igualdad plena cuando la presencia cae en los niveles altos. Ahí está el contraste útil del producto: lo que la escalera celebra, la tabla lo matiza, y la historia es más honesta por esa fricción que por cualquiera de las dos partes por separado.",
    3: "La tabla admite el límite central de la deducción: el saldo migratorio es una diferencia neta que no cuenta personas, ni dice quiénes se fueron ni a qué países. Es decir, la propia tabla declara que el misterio no se resuelve del todo, justo lo contrario de lo que la forma policial promete al lector. Esa tensión no debilita el producto; es su parte más rigurosa. El lector de la historia recibe la deducción completa; quien lee la tabla, además, el inventario de lo que la deducción no puede probar. Las pistas ordenan la evidencia y la tabla impide que ese orden se confunda con certeza.",
    5: "La tabla pone por escrito lo que la atmósfera de la sombra no puede hacer: separar causas. Su límite declarado es que las cifras miden llegadas, no motivos, y que las causas de la caída son varias y estos datos no las separan. También es honesta en el método, porque admite que el porcentaje de caída frente a 2019 es un cálculo propio a partir de la ONEI y de EFE. El contraste queda así: el arquetipo aporta la imagen que se recuerda, la de las playas vacías, y la tabla aporta la advertencia que la imagen no trae, la de que detrás de la sombra hay decisiones y no un destino.",
    2: "La tabla limita la historia por el lado del futuro: los datos describen 2024 y una tendencia de décadas, pero no permiten afirmar cómo será la población en 2050. Es un límite bien puesto, porque el tono del sabio, que habla como quien ya lo ha visto todo, podría hacer pasar una tendencia por un destino cerrado. El cierre de la historia también corrige al arquetipo en su punto débil: baja la demografía a la mesa familiar y pregunta quién cuidará a quién, que es la voz concreta que la narración no incluye.",
    4: "La tabla pone el límite que este arco más necesita: el registro cuenta empresas en operación, pero no dice cuántas prosperan, cuánto venden ni cuántos empleos generan de verdad. Es la frase que impide leer la historia como un parte de victoria: deja claro que se está ante el inicio de un proceso y no ante su resultado. El cierre de la historia está bien elegido para este arquetipo: no pide celebrar el cambio en abstracto, pide entrar en un negocio concreto y preguntar cómo empezó, que es donde la transformación se comprueba.",
}

LITERATURA = {
    1: "Este juicio tiene respaldo en la literatura sobre dramaturgia de datos. Segel y Heer (2010) mostraron que las visualizaciones narrativas que funcionan dosifican el recorrido del lector, y mi escalera es eso, un recorrido guiado peldaño a peldaño. Hullman y Diakopoulos (2011) demostraron que el encuadre y la secuencia no son neutros, que construyen la interpretación: el marco heroico es un encuadre, y por eso puede maquillar el techo que los datos sí muestran. La revisión sistemática de Sorba, Massara y Risi (2025), con 93 estudios, encuentra que los enfoques narrativos y performativos mejoran la memoria y la implicación de quien lee, que es el efecto que la escalera busca, aunque la evidencia sobre cambios de conducta sigue siendo escasa.",
    3: "La estructura de esta historia tiene nombre en la literatura. Weber, Engebretsen y Kennedy (2018) describen el periodismo de datos lineal como una dramaturgia paso a paso, donde el autor ordena las revelaciones y el lector las sigue: mi historia es ese modelo aplicado a la demografía. Segel y Heer (2010) llaman a una de sus formas la copa de martini, un tallo estrecho y guiado que después se abre a la exploración del lector. Mi historia tiene tallo y no tiene copa, porque el lector nunca explora por su cuenta, y la literatura permite nombrar esa limitación con precisión. Hullman y Diakopoulos (2011) añaden que el orden de presentación es un recurso retórico: descartar primero el error de conteo es método y también es persuasión.",
    5: "La literatura ayuda a situar el riesgo de este arquetipo. Hullman y Diakopoulos (2011) sostienen que toda visualización narrativa encuadra, selecciona qué se muestra y qué queda fuera, y que ese encuadre construye la interpretación. La sombra es un encuadre llevado al extremo, porque muestra los efectos y deja las causas fuera de escena. En el debate entre claridad y emoción que recorre el campo, Akten (2015) defiende la dramatización del dato que busca una respuesta empática antes que claridad; mi historia se acerca a esa posición, y el periodismo de datos la mira con sospecha por su cercanía a la manipulación. El campo nombra además el riesgo del lavado dramatúrgico: añadir emoción a un relato sin cambiar las relaciones de poder que el relato debería examinar. El fatalismo que critico en mi texto es ese riesgo con otro nombre.",
    2: "La voz del sabio también tiene lectura en la literatura. La corriente que desciende de Goffman (1959) estudia el dato como performance social: quien presenta datos actúa ante una audiencia y construye autoridad con esa actuación. Cluley (2024) lo documentó en presentaciones de investigación de mercados, donde el dato no solo informa, actúa. La serenidad de mi narradora es una actuación de autoridad en ese sentido, y explica por qué una sola fuente, la ONEI, puede sonar a verdad cerrada. La corriente participativa marca el contraste: Bhargava y otros (2022) y Snyder-Young y otros (2024) usan el teatro de datos para que las personas representadas participen en la interpretación de sus propios datos. Mi historia no les da la palabra a las personas mayores, y esa ausencia, que la crítica señalaba por intuición, la literatura la convierte en una decisión de método discutible.",
    4: "El estado del arte sitúa esta historia en la corriente más criticada del campo. Weber, Engebretsen y Kennedy (2018) describen la dramaturgia paso a paso del periodismo de datos como la más cercana a la comunicación estratégica, y el mapa del campo advierte que esa tradición tiende a dramatizar en detrimento de la precisión. Mi arco de antes y después corre ese riesgo en su versión promocional. Hullman y Diakopoulos (2011) explican el mecanismo: el encuadre inicial y la secuencia de cifras crecientes construyen una interpretación de progreso antes de que el lector pueda juzgarla. La revisión de Sorba, Massara y Risi (2025) señala el vacío que también tiene mi historia: hay evidencia de que estos relatos se recuerdan, pero casi ninguna de que midan resultados. Contar empresas que abren no es medir empresas que viven, en la literatura y en mi texto.",
}

REFERENCIAS = {
    1: "Referencias: Segel, E. y Heer, J. (2010). Narrative Visualization: Telling Stories with Data. IEEE Transactions on Visualization and Computer Graphics, 16(6). · Hullman, J. y Diakopoulos, N. (2011). Visualization Rhetoric: Framing Effects in Narrative Visualization. IEEE Transactions on Visualization and Computer Graphics, 17(12). · Sorba, E., Massara, F. y Risi, E. (2025). Theatre of Statistics: A Systematic Review of Performative Approaches for Enhancing Statistical Literacy. IASE 2025.",
    3: "Referencias: Weber, W., Engebretsen, M. y Kennedy, H. (2018). Data Stories: Rethinking Journalistic Storytelling in the Context of Data Journalism. Studies in Communication Sciences, 18(1). · Segel, E. y Heer, J. (2010). Narrative Visualization: Telling Stories with Data. IEEE Transactions on Visualization and Computer Graphics, 16(6). · Hullman, J. y Diakopoulos, N. (2011). Visualization Rhetoric: Framing Effects in Narrative Visualization. IEEE Transactions on Visualization and Computer Graphics, 17(12).",
    5: "Referencias: Hullman, J. y Diakopoulos, N. (2011). Visualization Rhetoric: Framing Effects in Narrative Visualization. IEEE Transactions on Visualization and Computer Graphics, 17(12). · Akten, M. (2015). Data Dramatization. Medium. · Dramaturgia y comunicación de datos: estado del arte (2006-2026), documento de trabajo, 2026 (debate ético: lavado dramatúrgico).",
    2: "Referencias: Goffman, E. (1959). The Presentation of Self in Everyday Life. · Cluley, R. (2024). Marketing Science Fictions. Bristol University Press. · Bhargava, R. y otros (2022). Data Theatre as an Entry Point to Data Literacy. Educational Technology & Society, 25(4). · Snyder-Young, D. y otros (2024). Viewpoints/Points of View: Building a Transdisciplinary Data Theatre Collaboration. Arts, 13(1).",
    4: "Referencias: Weber, W., Engebretsen, M. y Kennedy, H. (2018). Data Stories: Rethinking Journalistic Storytelling in the Context of Data Journalism. Studies in Communication Sciences, 18(1). · Hullman, J. y Diakopoulos, N. (2011). Visualization Rhetoric: Framing Effects in Narrative Visualization. IEEE Transactions on Visualization and Computer Graphics, 17(12). · Sorba, E., Massara, F. y Risi, E. (2025). Theatre of Statistics: A Systematic Review of Performative Approaches for Enhancing Statistical Literacy. IASE 2025.",
}

# ---------------------------------------------------------------- build
def build(cfg):
    cfg = dict(cfg)
    cfg["chip_bg"] = CHIP_BG[cfg["num"]]
    pdf = AnalisisPDF(cfg)
    pdf.add_page()
    pdf.header_band()
    for kind, text in cfg["blocks"]:
        if kind == "h":
            pdf.subhead(text)
        else:
            pdf.para(text)
    if cfg["num"] in LITERATURA:
        pdf.subhead("Respaldo en la literatura")
        pdf.para(LITERATURA[cfg["num"]])
        pdf.refs(REFERENCIAS[cfg["num"]])
    if cfg["num"] in FICHAS:
        pdf.subhead("El producto en una tabla")
        pdf.tabla_producto(FICHAS[cfg["num"]])
        pdf.para(CONTRASTES[cfg["num"]])
    path = os.path.join(OUT, cfg["slug"] + ".pdf")
    pdf.output(path)
    words = sum(len(t.split()) for k, t in cfg["blocks"] if k == "p")
    print(f"{cfg['slug']}: {pdf.page_no()} páginas, ~{words} palabras")
    return path

if __name__ == "__main__":
    for a in ANALISIS:
        build(a)
