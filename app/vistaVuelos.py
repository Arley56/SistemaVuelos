from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QDialog, QFormLayout,QInputDialog,
    QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QBrush, QPixmap
import sqlite3
import os
import random
from app.gestionReservas import GestionReservas


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QPainter, QColor, QLinearGradient
from PyQt6.QtCore import Qt
import os

class VistaVuelos(QWidget):
    def __init__(self, documento_usuario):
        super().__init__()
        self.documento_usuario = documento_usuario
        self.setWindowTitle("Vuelos Disponibles")
        self.resize(1000, 600)

        # Layout principal horizontal: Izquierda (form+tabla) - Derecha (imagen)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(40)

        # --- IZQUIERDA: form + tabla ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Título
        titulo = QLabel("Buscar y Reservar Vuelos")
        titulo.setObjectName("titulo")
        left_layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Formulario búsqueda
        busqueda_layout = QHBoxLayout()

        origen_layout = QVBoxLayout()
        origen_label = QLabel("Ciudad de origen")
        self.origen_input = QLineEdit()
        self.origen_input.setPlaceholderText("Ej. Bogotá")
        origen_layout.addWidget(origen_label)
        origen_layout.addWidget(self.origen_input)

        destino_layout = QVBoxLayout()
        destino_label = QLabel("Ciudad de destino")
        self.destino_input = QLineEdit()
        self.destino_input.setPlaceholderText("Ej. Medellín")
        destino_layout.addWidget(destino_label)
        destino_layout.addWidget(self.destino_input)

        self.btn_buscar = QPushButton("🔍 Buscar")
        self.btn_buscar.setFixedHeight(45)
        self.btn_buscar.setFixedWidth(120)
        self.btn_buscar.clicked.connect(self.buscar_vuelos)

        busqueda_layout.addLayout(origen_layout)
        busqueda_layout.addSpacing(15)
        busqueda_layout.addLayout(destino_layout)
        busqueda_layout.addSpacing(20)
        busqueda_layout.addWidget(self.btn_buscar)

        left_layout.addLayout(busqueda_layout)

        # Tabla de vuelos
        self.tabla = QTableWidget()
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSortingEnabled(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla.setMinimumHeight(300)
        left_layout.addWidget(self.tabla, stretch=1)

        # Botones inferiores
        botones_layout = QHBoxLayout()
        self.btn_reservar = QPushButton("✈️ Reservar vuelo seleccionado")
        self.btn_reservar.clicked.connect(self.reservar_vuelo_seleccionado)
        self.btn_gestion_reservas = QPushButton("📋 Gestionar mis reservas")
        self.btn_gestion_reservas.clicked.connect(self.abrir_gestion_reservas)
        botones_layout.addWidget(self.btn_reservar)
        botones_layout.addWidget(self.btn_gestion_reservas)
        left_layout.addLayout(botones_layout)

 # --- DERECHA (IMAGEN) ---
        right_widget = QLabel()
        right_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Sube un nivel
        imagen_path = os.path.join(BASE_DIR, "assets", "imagen_vista.jpg")
        print("Ruta imagen:", imagen_path)
        print("Existe archivo?", os.path.exists(imagen_path))

        if os.path.exists(imagen_path):
            pixmap = QPixmap(imagen_path)
            if not pixmap.isNull():
                # Escalar proporcionalmente al alto de la ventana
                pixmap = pixmap.scaledToHeight(500, Qt.TransformationMode.SmoothTransformation)
                right_widget.setPixmap(pixmap)
            else:
                right_widget.setText("❌ Imagen inválida")
        else:
            right_widget.setText("❌ Imagen no encontrada")

        # Agregar widgets con proporción 1:1
        main_layout.addWidget(left_widget, stretch=1)
        main_layout.addWidget(right_widget, stretch=1)


        # Estilos
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #ffffff;
                color: #0a3d62;
            }

            QLabel#titulo {
                font-size: 28px;
                font-weight: 700;
                color: #2980b9;
                margin-bottom: 20px;
            }

            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #34495e;
                margin-bottom: 6px;
            }

            QLineEdit {
                padding: 8px 10px;
                font-size: 14px;
                border: 2px solid #aed6f1;
                border-radius: 6px;
                background-color: #ffffff;
            }

            QLineEdit:focus {
                border-color: #2980b9;
                background-color: #f0f8ff;
            }

            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 700;
                border: none;
                min-width: 140px;
            }

            QPushButton:hover {
                background-color: #1c5980;
            }

            QPushButton:pressed {
                background-color: #134563;
            }

            QTableWidget {
                border: 1px solid #aed6f1;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
                color: #2c3e50;
                gridline-color: #d6eaf8;
            }

            QHeaderView::section {
                background-color: #2980b9;
                color: white;
                font-weight: 700;
                padding: 8px;
                border: none;
            }

            QTableWidget::item:selected {
                background-color: #d6eaf8;
                color: #154360;
            }

            QTableWidget::item:hover {
                background-color: #ebf5fb;
            }
        """)

        self.cargar_vuelos()



    
    def abrir_gestion_reservas(self):
         self.gestion_reservas_window = GestionReservas(self.documento_usuario)
         self.gestion_reservas_window.show()


    def cargar_vuelos(self, origen=None, destino=None):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "db", "data_base.db")

        try:
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()

            consulta = "SELECT * FROM Vuelos"
            parametros = []

            if origen and destino:
                consulta += " WHERE ciudad_origen LIKE ? AND ciudad_destino LIKE ?"
                parametros = [f"%{origen}%", f"%{destino}%"]
            elif origen:
                consulta += " WHERE ciudad_origen LIKE ?"
                parametros = [f"%{origen}%"]
            elif destino:
                consulta += " WHERE ciudad_destino LIKE ?"
                parametros = [f"%{destino}%"]

            cursor.execute(consulta, parametros)
            vuelos = cursor.fetchall()
            conexion.close()

            self.tabla.setColumnCount(6)
            self.tabla.setHorizontalHeaderLabels([
                "Código", "Origen", "Destino", "Horario", "sillas_preferencial", "sillas_economica"
            ])
            self.tabla.setRowCount(len(vuelos))

            for row_idx, vuelo in enumerate(vuelos):
                for col_idx, valor in enumerate(vuelo):
                    self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))

            self.tabla.resizeColumnsToContents()
            self.tabla.resizeRowsToContents()
            
    

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error en la base de datos: {e}")
            
            
    def abrir_reserva(self, row, column):
        # Obtener datos del vuelo seleccionado
        vuelo = []
        for col in range(self.tabla.columnCount()):
            item = self.tabla.item(row, col)
            vuelo.append(item.text() if item else "")

        # Convertir sillas a int
        vuelo[4] = int(vuelo[4])
        vuelo[5] = int(vuelo[5])

        # Abrir diálogo reserva
        dialogo = DialogoReserva(vuelo, self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            # Recarga la tabla para mostrar los nuevos asientos disponibles
            self.buscar_vuelos()
            

    def buscar_vuelos(self):
        origen = self.origen_input.text().strip()
        destino = self.destino_input.text().strip()
        self.cargar_vuelos(origen, destino)
        
    def reservar_vuelo_seleccionado(self):
        # Este método debe estar definido para manejar la acción del botón
        # Ejemplo básico:
        seleccion = self.tabla.currentRow()
        if seleccion == -1:
            QMessageBox.warning(self, "Atención", "Por favor selecciona un vuelo primero.")
            return
        
        vuelo = []
        for col in range(self.tabla.columnCount()):
            item = self.tabla.item(seleccion, col)
            vuelo.append(item.text() if item else "")

        # Convierte asientos a int
        vuelo[4] = int(vuelo[4])
        vuelo[5] = int(vuelo[5])

        # Abre el diálogo de reserva con el vuelo seleccionado
        dialogo = DialogoReserva(vuelo, self.documento_usuario, self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.buscar_vuelos()
class DialogoReserva(QDialog):
    def __init__(self, vuelo, documento_usuario,parent=None):
        super().__init__(parent)
        self.vuelo = vuelo  # tupla con datos vuelo
        self.documento_usuario = documento_usuario
        self.setWindowTitle(f"Reservar vuelo {vuelo[0]}")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(self)

        info = QLabel(
            f"Vuelo: {vuelo[0]}\n"
            f"Origen: {vuelo[1]}\n"
            f"Destino: {vuelo[2]}\n"
            f"Horario: {vuelo[3]}\n"
            f"Sillas Preferencial disponibles: {vuelo[4]}\n"
            f"Sillas Económica disponibles: {vuelo[5]}"
        )
        layout.addWidget(info)

        form_layout = QFormLayout()

        self.pref_spin = QSpinBox()
        self.pref_spin.setRange(0, min(3, vuelo[4]))  # máximo 3 pasajeros y sillas disponibles
        form_layout.addRow("Sillas Preferencial a reservar:", self.pref_spin)

        self.econ_spin = QSpinBox()
        self.econ_spin.setRange(0, min(3, vuelo[5]))
        form_layout.addRow("Sillas Económica a reservar:", self.econ_spin)

        layout.addLayout(form_layout)

        self.total_label = QLabel("Total a pagar: $0")
        layout.addWidget(self.total_label)

        self.pref_spin.valueChanged.connect(self.actualizar_total)
        self.econ_spin.valueChanged.connect(self.actualizar_total)

        btn_layout = QHBoxLayout()
        confirmar_btn = QPushButton("Confirmar Reserva")
        cancelar_btn = QPushButton("Cancelar")

        confirmar_btn.clicked.connect(self.confirmar_reserva)
        cancelar_btn.clicked.connect(self.reject)

        btn_layout.addWidget(confirmar_btn)
        btn_layout.addWidget(cancelar_btn)
        layout.addLayout(btn_layout)

        self.actualizar_total()

    def actualizar_total(self):
        total = self.pref_spin.value() * 850000 + self.econ_spin.value() * 235000
        self.total_label.setText(f"Total a pagar: ${total:,}")
        
    def confirmar_reserva(self):
        pref = self.pref_spin.value()
        econ = self.econ_spin.value()
        total_sillas = pref + econ

        # Validar máximo 3 sillas
        if total_sillas == 0:
            QMessageBox.warning(self, "Error", "Debe reservar al menos una silla.")
            return
        if total_sillas > 3:
            QMessageBox.warning(self, "Error", "No puede reservar más de 3 sillas.")
            return

        total = pref * 850000 + econ * 235000

        resumen = (
            f"Resumen de la reserva:\n"
            f"Vuelo: {self.vuelo[0]}\n"
            f"Sillas Preferencial: {pref}\n"
            f"Sillas Económica: {econ}\n"
            f"Total a pagar: ${total:,}\n\n"
            "¿Desea confirmar la reserva?"
        )

        respuesta = QMessageBox.question(
            self,
            "Confirmar Reserva",
            resumen,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.No:
            return

        # Pedir datos de pasajeros
        pasajeros = []
        for i in range(total_sillas):
            nombre, ok1 = QInputDialog.getText(self, f"Pasajero {i+1}", "Nombre completo:")
            if not ok1 or not nombre.strip():
                QMessageBox.warning(self, "Error", "Debe ingresar un nombre válido para todos los pasajeros.")
                return
            documento, ok2 = QInputDialog.getText(self, f"Pasajero {i+1}", "Documento:")
            if not ok2 or not documento.strip():
                QMessageBox.warning(self, "Error", "Debe ingresar un documento válido para todos los pasajeros.")
                return
            pasajeros.append((nombre.strip(), documento.strip()))

        reserva_num = random.randint(100000, 999999)

        try:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(BASE_DIR, "db", "data_base.db")

            with sqlite3.connect(db_path, timeout=10) as conexion:
                cursor = conexion.cursor()

                nuevas_pref = self.vuelo[4] - pref
                nuevas_econ = self.vuelo[5] - econ

                cursor.execute("""
                    UPDATE Vuelos SET sillas_preferencial = ?, sillas_economica = ?
                    WHERE codigo_vuelo = ?
                """, (nuevas_pref, nuevas_econ, self.vuelo[0]))

                cursor.execute("""
                    INSERT INTO Reservas (
                        codigo_vuelo, documento_usuario, numero_reserva,
                        total, sillas_preferencial, sillas_economica
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.vuelo[0], self.documento_usuario, reserva_num, total, pref, econ))

                # Insertar pasajeros asociados
                for nombre, documento in pasajeros:
                    cursor.execute("""
                        INSERT INTO Pasajeros (numero_reserva, nombre, documento)
                        VALUES (?, ?, ?)
                    """, (reserva_num, nombre, documento))

            QMessageBox.information(
                self,
                "Reserva Confirmada",
                f"Reserva #{reserva_num} confirmada.\nTotal a pagar: ${total:,}"
            )
            self.accept()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo completar la reserva:\n{e}")

    





