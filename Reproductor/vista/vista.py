from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, QDockWidget,
                             QStatusBar, QTabWidget, QWidget, QHBoxLayout,
                             QVBoxLayout, QListWidget, QListWidgetItem, QSlider, QGroupBox, QSpinBox)
from PyQt6.QtGui import QPixmap, QAction, QKeySequence
from PyQt6.QtCore import Qt
from PyQt6.QtMultimediaWidgets import QVideoWidget

class VistaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initialize_ui()
        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        with open('Reproductor/estilos.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)
        self.mp3_volumen_slider.setValue(50)
        self.mp4_volumen_slider.setValue(50)

    def initialize_ui(self):
        self.setGeometry(100,100,800,500)
        self.setWindowTitle("Reproductor Multimedia")
        self.montar_panel_lateral_con_lista()
        self.generar_pestanyas()
        self.definir_acciones_menu_superior()
        self.montar_menu_superior()
        self.show()

    def generar_pestanyas(self):
        self.tab_bar = QTabWidget(self)
        self.tab_bar.currentChanged.connect(self.cambio_pestanya)
        self.reproductorMP3_container = QWidget()
        self.reproductorMP4_container = QWidget()
        self.galeria_container = QWidget()
        self.tab_bar.addTab(self.reproductorMP3_container, "Reproductor MP3")
        self.tab_bar.addTab(self.reproductorMP4_container, "Reproductor MP4")
        self.tab_bar.addTab(self.galeria_container, "Galería")

        self.construir_pestanya_MP3()
        self.construir_pestanya_MP4()
        self.construir_pestanya_galeria()

        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(self.tab_bar)

        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)

    def construir_pestanya_MP3(self):
        main_v_box = QVBoxLayout()
        buttons_h_box = QHBoxLayout()

        song_image = QLabel()
        pixmap = QPixmap("Reproductor/imagenes/fondo2.png").scaled(512, 300)
        song_image.setPixmap(pixmap)
        song_image.setScaledContents(True)

        self.mp3_botton_before = QPushButton()
        self.mp3_botton_before.setObjectName("botonBefore")
        self.mp3_botton_play = QPushButton()
        self.mp3_botton_play.setObjectName("botonPlay")
        self.mp3_botton_next = QPushButton()
        self.mp3_botton_next.setObjectName("botonNext")

        # Slider de progreso

        self.mp3_slider = QSlider(Qt.Orientation.Horizontal)
        self.mp3_slider.setRange(0, 0)

        # Slider de volumen
        
        self.mp3_volumen_slider = QSlider(Qt.Orientation.Vertical)
        self.mp3_volumen_slider.setRange(0, 100)

        self.mp3_botton_before.setFixedSize(40, 40)
        self.mp3_botton_play.setFixedSize(50, 50)
        self.mp3_botton_next.setFixedSize(40, 40)

        buttons_h_box.addWidget(self.mp3_botton_before)
        buttons_h_box.addWidget(self.mp3_botton_play)
        buttons_h_box.addWidget(self.mp3_botton_next)
        buttons_h_box.addWidget(self.mp3_volumen_slider)

        buttons_container = QWidget()
        buttons_container.setLayout(buttons_h_box)

        main_v_box.addWidget(song_image)
        main_v_box.addWidget(self.mp3_slider)
        main_v_box.addWidget(buttons_container)

        self.reproductorMP3_container.setLayout(main_v_box)

    def construir_pestanya_MP4(self):
        main_v_box = QVBoxLayout()
        buttons_h_box = QHBoxLayout()

        self.imagen_widget = QVideoWidget()
        self.imagen_widget.setMinimumSize(512, 300)

        self.mp4_botton_before = QPushButton()
        self.mp4_botton_before.setObjectName("botonBefore")
        self.mp4_botton_play = QPushButton()
        self.mp4_botton_play.setObjectName("botonPlay")
        self.mp4_botton_next = QPushButton()
        self.mp4_botton_next.setObjectName("botonNext")

        # Slider de progreso

        self.mp4_slider = QSlider(Qt.Orientation.Horizontal)
        self.mp4_slider.setRange(0,0)

        # Slider de volumen
        
        self.mp4_volumen_slider = QSlider(Qt.Orientation.Vertical)
        self.mp4_volumen_slider.setRange(0, 100)

        self.mp4_botton_before.setFixedSize(40, 40)
        self.mp4_botton_play.setFixedSize(50, 50)
        self.mp4_botton_next.setFixedSize(40, 40)

        buttons_h_box.addWidget(self.mp4_botton_before)
        buttons_h_box.addWidget(self.mp4_botton_play)
        buttons_h_box.addWidget(self.mp4_botton_next)
        buttons_h_box.addWidget(self.mp4_volumen_slider)

        buttons_container = QWidget()
        buttons_container.setLayout(buttons_h_box)

        main_v_box.addWidget(self.imagen_widget)
        main_v_box.addWidget(self.mp4_slider)
        main_v_box.addWidget(buttons_container)

        self.reproductorMP4_container.setLayout(main_v_box)

    def construir_pestanya_galeria(self):
        main_v_box = QVBoxLayout()
        buttons_h_box = QHBoxLayout()

        self.image = QLabel()
        pixmap = QPixmap("Reproductor/imagenes/fondo2.png").scaled(300, 150)
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)

        self.botton_before = QPushButton()
        self.botton_before.setObjectName("botonBefore")
        self.botton_next = QPushButton()
        self.botton_next.setObjectName("botonNext")

        self.botton_before.setFixedSize(40, 40)
        self.botton_next.setFixedSize(40, 40)

        buttons_h_box.addWidget(self.botton_before)
        buttons_h_box.addWidget(self.botton_next)

        buttons_container = QWidget()
        buttons_container.setLayout(buttons_h_box)

        # Conversor JPG-PNG

        conversor_grupo = QGroupBox("Convertir JPG a PNG")
        conversor_h_box = QHBoxLayout()

        self.galeria_botton_convertir = QPushButton("Convertir imagen a PNG")
        self.galeria_label_resultado_conversion = QLabel("Sin convertir")

        conversor_h_box.addWidget(self.galeria_botton_convertir)
        conversor_h_box.addWidget(self.galeria_label_resultado_conversion)
        conversor_grupo.setLayout(conversor_h_box)

        # Escalado

        escalar_grupo = QGroupBox("Escalar imagen")
        escalar_h_box = QHBoxLayout()

        self.label_ancho = QLabel("Ancho:")
        self.ancho_input = QSpinBox()
        self.ancho_input.setRange(1, 9999)
        self.ancho_input.setValue(512)

        self.label_alto = QLabel("Alto:")
        self.alto_input = QSpinBox()
        self.alto_input.setRange(1, 9999)
        self.alto_input.setValue(300)

        self.botton_escalar = QPushButton("Escalar")

        escalar_h_box.addWidget(self.label_ancho)
        escalar_h_box.addWidget(self.ancho_input)
        escalar_h_box.addWidget(self.label_alto)
        escalar_h_box.addWidget(self.alto_input)
        escalar_h_box.addWidget(self.botton_escalar)
        escalar_grupo.setLayout(escalar_h_box)

        # Agregar contenido al contenedor principa

        main_v_box.addWidget(self.image)
        main_v_box.addWidget(buttons_container)
        main_v_box.addWidget(conversor_grupo)
        main_v_box.addWidget(escalar_grupo)

        self.galeria_container.setLayout(main_v_box)

    def montar_menu_superior(self):
        self.menuBar()
        menu_file = self.menuBar().addMenu("Archivo")
        menu_view = self.menuBar().addMenu("Ver")

        menu_file.addAction(self.abrir_carpeta_action)
        menu_view.addAction(self.listar_action)

    def definir_acciones_menu_superior(self):

        # TODO: Ajustarlo para que muestre canciones, videos e imagenes dinamicamente

        self.listar_action = QAction('Listar música', self, checkable=True)
        self.listar_action.setShortcut(QKeySequence("Ctrl+L"))
        self.listar_action.setStatusTip("Selecciona una lista de canciones a reproducir")
        self.listar_action.setChecked(True)

        self.abrir_carpeta_action = QAction('Abrir carpeta', self)
        self.abrir_carpeta_action.setShortcut(QKeySequence("Ctrl+O"))
        self.abrir_carpeta_action.setStatusTip("Abrir carpeta de archivos")

    def montar_panel_lateral_con_lista(self):
        self.dock = QDockWidget()
        self.lista = QListWidget()

        self.dock.setWindowTitle("Lista de canciones")
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea
        )

        self.dock.setWidget(self.lista)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

    def actualizar_boton_play(self, reproduciendo):
        boton = self.mp3_botton_play if self.pestanya_actual() == 0 else self.mp4_botton_play
        if reproduciendo:
            self.mp3_botton_play.setStyleSheet("image: url('Reproductor/imagenes/play.png');")
        else:
            self.mp3_botton_play.setStyleSheet("image: url('Reproductor/imagenes/pause.png');")

    def pestanya_actual(self):
        return self.tab_bar.currentIndex()

    def cambio_pestanya(self):
        self.lista.clear()

    def mostrar_imagen(self, ruta):
        pixmap = QPixmap(ruta).scaled(512, 300)
        self.image.setPixmap(pixmap)

    def cargar_lista(self, lista, icono):
        self.lista.clear()
        for elemento in lista:
            item = QListWidgetItem(elemento)
            item.setIcon(icono)
            self.lista.addItem(item)