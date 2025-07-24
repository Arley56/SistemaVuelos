import sys
from PyQt6.QtWidgets import QApplication
#from app.vistaVuelos import VistaVuelos
from app.login import Login

app = QApplication(sys.argv)
ventana = Login()
#window = VistaVuelos()

ventana.show()
#window.show()
sys.exit(app.exec())
#try 1