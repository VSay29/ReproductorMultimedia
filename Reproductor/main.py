import sys
from PyQt6.QtWidgets import QApplication
from vista import vista
from controlador import controlador
from modelo import reproductor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    vista = vista.VistaPrincipal()
    reproductor = reproductor.Reproductor()
    controlador = controlador.Controlador(vista, reproductor)
    vista.show()
    sys.exit(app.exec())