from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QDialog, QFormLayout,QInputDialog,
    QSpinBox
)
from PyQt6.QtCore import Qt
import sqlite3
import os
import random
from app.gestionReservas import GestionReservas
class VistaVuelos(QWidget):
    def __init__(self, documento_usuario):
        super().__init__()
        self.documento_usuario = documento_usuario  # Guardar documento del usuario
        self.setWindowTitle("Vuelos disponibles")
        self.resize(800, 500)
        

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 4px;
                font-size: 14px;
            }
            QPushButton {
                padding: 5px;
                font-size: 14px;
                background-color: #004080;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0066cc;
            }
            QTableWidget {
                font-size: 13px;
                border: 1px solid #ccc;
                gridline-color: #bbb;
                selection-background-color: #a4c9ff;
            }
            QHeaderView::section {
                background-color: #004080;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
        """)

        layout.addWidget(QLabel("Buscar vuelos por origen o destino:"))

        # Barra de búsqueda
        search_layout = QHBoxLayout()
        self.origen_input = QLineEdit()
        self.origen_input.setPlaceholderText("Ciudad de origen")
        self.destino_input = QLineEdit()
        self.destino_input.setPlaceholderText("Ciudad de destino")
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.buscar_vuelos)

        search_layout.addWidget(self.origen_input)
        search_layout.addWidget(self.destino_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        # Tabla de resultados
        self.tabla = QTableWidget()
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSortingEnabled(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.tabla)
        
        # Botón reservar
        self.btn_reservar = QPushButton("Reservar vuelo seleccionado")
        self.btn_reservar.clicked.connect(self.reservar_vuelo_seleccionado)
        layout.addWidget(self.btn_reservar)
        
        self.btn_gestion_reservas = QPushButton("Gestionar Mis Reservas")
        self.btn_gestion_reservas.clicked.connect(self.abrir_gestion_reservas)
        layout.addWidget(self.btn_gestion_reservas)

        self.cargar_vuelos()  # mostrar todos al principio
        
    
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

    





