"""
Archivo: login.py
Descripción: Este archivo implementa la interfaz gráfica de inicio de sesión para el sistema de vuelos utilizando PyQt6.
Incluye funcionalidades para iniciar sesión, registrar nuevos usuarios y cambiar contraseñas.

Clases:
- Login: Clase principal que representa la ventana de inicio de sesión.
- CambiarContrasena: Clase que representa el diálogo para cambiar la contraseña.

Dependencias:
- PyQt6: Framework para crear interfaces gráficas.
- sqlite3: Biblioteca para interactuar con la base de datos SQLite.
- os: Biblioteca para manejar rutas de archivos.
- Registro: Clase externa para registrar nuevos usuarios.

Base de datos:
- Se utiliza una base de datos SQLite ubicada en la carpeta `db` dentro del proyecto.
"""

# Importación de módulos necesarios
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QCheckBox,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt
import os
import sqlite3

from app.registro import Registro  # Clase para registrar nuevos usuarios
from app.vistaVuelos import VistaVuelos  # Clase para mostrar vuelos disponibles
from app.adminVuelos import AdminVuelos


# Configuración de la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "db", "data_base.db")
conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

class Login(QWidget):
    """
    Clase que representa la ventana de inicio de sesión.

    Métodos:
    - __init__: Inicializa la ventana de inicio de sesión.
    - inicializarUI: Configura la interfaz gráfica y los estilos CSS.
    - password_visibility: Alterna la visibilidad de la contraseña.
    - iniciar_main_window: Verifica las credenciales y abre la ventana principal.
    - registrar_usuario: Abre el formulario de registro de usuarios.
    - cambiar_contrasena: Abre el diálogo para cambiar la contraseña.
    - open_main_window: Método placeholder para abrir la ventana principal.
    """
    def __init__(self):
        super().__init__()
        self.inicializarUI()

    def inicializarUI(self):
        """
        Configura la interfaz gráfica de la ventana de inicio de sesión.
        Incluye el formulario de inicio de sesión y una imagen decorativa.
        """
        
        
        # Configuración general de la ventana
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("Login")
        ruta_icono = os.path.join(BASE_DIR, "assets", "icono_image.ico")
        self.setWindowIcon(QIcon(ruta_icono))

        # Aplicación de estilos CSS
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: #333;
                font-family: 'Segoe UI', Arial;
                font-size: 14px;
            }
            QLabel {
                color: #111;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #f9f9f9;
                border: 2px solid #0056b3;
                border-radius: 6px;
                padding: 6px;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #d32f2f;  /* rojo */
                background-color: #fff;
            }
            QPushButton {
                background-color: #0056b3;  /* azul fuerte */
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976d2;  /* azul más claro */
            }
            QPushButton:pressed {
                background-color: #d32f2f;  /* rojo vibrante */
            }
            QCheckBox {
                spacing: 6px;
                color: #444;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: #d32f2f;
                border: 1px solid #d32f2f;
            }
            QCheckBox::indicator:unchecked {
                background-color: #ccc;
                border: 1px solid #999;
            }
        """)

        # Configuración del layout principal
        main_layout = QHBoxLayout(self)

        # === FORMULARIO ===
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.setContentsMargins(50, 30, 50, 30)

        # Campos del formulario
        
        label_usuario = QLabel("Documento:")
        label_usuario.setFont(QFont("Arial", 12))
        self.user_input = QLineEdit()

        label_password = QLabel("Contraseña:")
        label_password.setFont(QFont("Arial", 12))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.check_view_password = QCheckBox("Ver contraseña")
        self.check_view_password.toggled.connect(self.password_visibility)

        # Botones del formulario
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.iniciar_main_window)

        register_button = QPushButton("Registrate")
        register_button.clicked.connect(self.registrar_usuario)

        change_pass_button = QPushButton("Cambiar contraseña")
        change_pass_button.clicked.connect(self.cambiar_contrasena)

        # Añadir elementos al formulario
        form_layout.addWidget(label_usuario)
        form_layout.addWidget(self.user_input)
        form_layout.addWidget(label_password)
        form_layout.addWidget(self.pass_input)
        form_layout.addWidget(self.check_view_password)
        form_layout.addSpacing(10)
        form_layout.addWidget(login_button)
        form_layout.addWidget(register_button)
        form_layout.addWidget(change_pass_button)
        form_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))




        # === IMAGEN ===
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setScaledContents(True)

        # Cargar imagen decorativa
        image_path = os.path.join(BASE_DIR, "assets", "login_image.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("Imagen no encontrada")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === Layout principal: 50% Formulario | 50% Imagen ===
        main_layout.addWidget(form_widget, 1)
        main_layout.addWidget(image_label, 1)

        self.setLayout(main_layout)
        self.show()

    def password_visibility(self, clicked):
        """
        Alterna la visibilidad de la contraseña en el campo de entrada.
        """
        if clicked:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

    def iniciar_main_window(self):
        usuario = self.user_input.text().strip()
        clave = self.pass_input.text()

        if not usuario or not clave:
            QMessageBox.warning(self, "Login", "Por favor ingresa documento y contraseña.")
            return

        try:
            cursor.execute("SELECT documento, rol FROM Usuarios WHERE documento = ? AND clave = ?", (usuario, clave))
            resultado = cursor.fetchone()
            print("Resultado:", resultado)

            if resultado:
                documento_usuario, rol = resultado
                print("Rol obtenido:", rol)

                QMessageBox.information(self, "Login", f"Inicio de sesión exitoso como {rol}.")
                self.is_logged_in = True
                self.close()

                if rol == "admin":
                    print("Abriendo AdminVuelos")
                    self.ventana_admin = AdminVuelos(conn=conexion)
                    self.ventana_admin.show()
                else:
                    print("Abriendo VistaVuelos")
                    self.ventana_usuario = VistaVuelos(documento_usuario)
                    self.ventana_usuario.show()
            else:
                QMessageBox.warning(self, "Login", "Usuario o contraseña incorrectos.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error en la base de datos: {e}")




    def registrar_usuario(self):
        """
        Abre el formulario de registro de nuevos usuarios.
        """
        self.new_user_form = Registro()
        self.new_user_form.show()

    def cambiar_contrasena(self):
        """
        Abre el diálogo para cambiar la contraseña.
        """
        self.dialog = CambiarContrasena()
        self.dialog.exec()

    def open_main_window(self, usuario_documento):
        
        """
        Método placeholder para abrir la ventana principal del sistema.
        Aquí se puede implementar la lógica para mostrar la ventana de vuelos o cualquier otra funcionalidad.
        """
        
        self.vuelos_window = VistaVuelos(usuario_documento)
        self.vuelos_window.show()


class CambiarContrasena(QDialog):
    """
    Clase que representa el diálogo para cambiar la contraseña.

    Métodos:
    - __init__: Inicializa el diálogo.
    - initUI: Configura la interfaz gráfica del diálogo.
    - actualizar_clave: Actualiza la contraseña en la base de datos.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cambiar Contraseña")
        self.setGeometry(100, 100, 400, 220)
        self.initUI()
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #222;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #f0f0f0;
                border: 1.5px solid #aaa;
                border-radius: 5px;
                padding: 5px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-weight: bold;
                border-radius: 7px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #003f6b;
            }
        """)

    def initUI(self):
        """
        Configura la interfaz gráfica del diálogo para cambiar la contraseña.
        """
        layout = QVBoxLayout(self)

        # Documento (horizontal layout: label + input)
        doc_layout = QHBoxLayout()
        self.doc_label = QLabel("Documento:")
        self.doc_label.setFont(QFont("Arial", 12))
        self.doc_input = QLineEdit()
        self.doc_input.setFixedHeight(28)
        doc_layout.addWidget(self.doc_label)
        doc_layout.addWidget(self.doc_input)

        # Nueva contraseña
        pass_layout = QHBoxLayout()
        self.pass_label = QLabel("Nueva contraseña:")
        self.pass_label.setFont(QFont("Arial", 12))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setFixedHeight(28)
        pass_layout.addWidget(self.pass_label)
        pass_layout.addWidget(self.pass_input)

        # Confirmar contraseña
        pass2_layout = QHBoxLayout()
        self.pass2_label = QLabel("Confirmar:")
        self.pass2_label.setFont(QFont("Arial", 12))
        self.pass2_input = QLineEdit()
        self.pass2_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass2_input.setFixedHeight(28)
        pass2_layout.addWidget(self.pass2_label)
        pass2_layout.addWidget(self.pass2_input)

        # Botón cambiar
        self.cambiar_btn = QPushButton("Cambiar")
        self.cambiar_btn.clicked.connect(self.actualizar_clave)

        # Agregar todos los layouts y botón al layout principal
        layout.addLayout(doc_layout)
        layout.addLayout(pass_layout)
        layout.addLayout(pass2_layout)
        layout.addWidget(self.cambiar_btn)

    def actualizar_clave(self):
        """
        Actualiza la contraseña en la base de datos si los datos son válidos.
        """
        documento = self.doc_input.text().strip()
        nueva = self.pass_input.text()
        confirmar = self.pass2_input.text()

        if not documento or not nueva or not confirmar:
            QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos.")
            return
        if nueva != confirmar:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
            return

        try:
            cursor.execute("SELECT * FROM Usuarios WHERE documento = ?", (documento,))
            if cursor.fetchone():
                cursor.execute("UPDATE Usuarios SET clave = ? WHERE documento = ?", (nueva, documento))
                conexion.commit()
                QMessageBox.information(self, "Éxito", "Contraseña actualizada correctamente.")
                self.close()
            else:
                QMessageBox.warning(self, "No encontrado", "Documento no registrado.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error BD", f"Error al actualizar: {e}")



