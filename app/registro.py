from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QMessageBox
import sqlite3
import os
from PyQt6.QtGui import QFont

# Ruta base y conexión
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "db", "data_base.db")
conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

class Registro(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setGeometry(100, 100, 450, 400)  # Ampliar un poco ventana
        self.setWindowTitle("Registro de Usuario")
        
        # Nombre completo
        nombre_label = QLabel("Nombre Completo:", self)
        nombre_label.setFont(QFont("Arial", 12))
        nombre_label.move(20, 30)
        
        self.nombre_input = QLineEdit(self)
        self.nombre_input.resize(280, 24)
        self.nombre_input.move(160, 30)
        
        # Correo electrónico
        correo_label = QLabel("Correo Electrónico:", self)
        correo_label.setFont(QFont("Arial", 12))
        correo_label.move(20, 70)
        
        self.correo_input = QLineEdit(self)
        self.correo_input.resize(280, 24)
        self.correo_input.move(160, 70)
        
        # Número de documento
        documento_label = QLabel("Número de Documento:", self)
        documento_label.setFont(QFont("Arial", 12))
        documento_label.move(20, 110)
        
        self.documento_input = QLineEdit(self)
        self.documento_input.resize(280, 24)
        self.documento_input.move(160, 110)
        
        # Contraseña
        password1_label = QLabel("Contraseña:", self)
        password1_label.setFont(QFont("Arial", 12))
        password1_label.move(20, 150)
        
        self.password1_input = QLineEdit(self)
        self.password1_input.resize(280, 24)
        self.password1_input.move(160, 150)
        self.password1_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Confirmar contraseña
        password2_label = QLabel("Confirmar Contraseña:", self)
        password2_label.setFont(QFont("Arial", 12))
        password2_label.move(20, 190)
        
        self.password2_input = QLineEdit(self)
        self.password2_input.resize(280, 24)
        self.password2_input.move(160, 190)
        self.password2_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Botones
        create_button = QPushButton("Crear Usuario", self)
        create_button.resize(120, 30)
        create_button.move(160, 240)
        create_button.clicked.connect(self.crear_usuario)
        
        cancel_button = QPushButton("Cancelar", self)
        cancel_button.resize(120, 30)
        cancel_button.move(300, 240)
        cancel_button.clicked.connect(self.cancelar_creacion)
        
    def crear_usuario(self):
        # Recoger valores
        nombre = self.nombre_input.text().strip()
        correo = self.correo_input.text().strip()
        documento = self.documento_input.text().strip()
        password1 = self.password1_input.text()
        password2 = self.password2_input.text()

        # Validaciones básicas
        if not nombre or not correo or not documento or not password1 or not password2:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        if password1 != password2:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
            return
        
        # Puedes agregar validaciones extras para correo, documento, etc.

        try:
            # Insertar en la base de datos
            cursor.execute("""
                INSERT INTO Usuarios (nombre, correo, documento, clave) 
                VALUES (?, ?, ?, ?)
            """, (nombre, correo, documento, password1))
            conexion.commit()

            QMessageBox.information(self, "Éxito", "Usuario creado exitosamente.")
            
            # Limpiar campos
            self.nombre_input.clear()
            self.correo_input.clear()
            self.documento_input.clear()
            self.password1_input.clear()
            self.password2_input.clear()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error en la base de datos: {e}")

    def cancelar_creacion(self):
        self.close()
