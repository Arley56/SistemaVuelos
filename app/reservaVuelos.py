from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton,
    QMessageBox, QHBoxLayout, QFormLayout, QWidget
)
import sqlite3
import os
import random
import string





class ReservaVuelo(QDialog):
    def __init__(self, usuario_documento, codigo_vuelo):
        super().__init__()
        self.usuario_documento = usuario_documento
        self.codigo_vuelo = codigo_vuelo

        self.setWindowTitle("Reserva de Vuelo")
        self.resize(500, 600)

        layout = QVBoxLayout(self)

        # Mostrar info vuelo (podrías cargar más info desde BD si quieres)
        self.info_label = QLabel(f"Reserva para vuelo: {codigo_vuelo}")
        layout.addWidget(self.info_label)

        self.pasajeros_widgets = []

        # Form para datos de hasta 3 pasajeros
        self.form_layout = QVBoxLayout()
        layout.addLayout(self.form_layout)

        for i in range(3):
            grupo = self.crear_form_pasajero(i + 1)
            self.form_layout.addWidget(grupo)
            self.pasajeros_widgets.append(grupo)

        # Botón para calcular y mostrar resumen
        self.calcular_button = QPushButton("Calcular Total y Resumen")
        self.calcular_button.clicked.connect(self.calcular_resumen)
        layout.addWidget(self.calcular_button)

        # Label resumen
        self.resumen_label = QLabel("")
        layout.addWidget(self.resumen_label)

        # Confirmar reserva
        self.confirmar_button = QPushButton("Confirmar Reserva")
        self.confirmar_button.setEnabled(False)
        self.confirmar_button.clicked.connect(self.confirmar_reserva)
        layout.addWidget(self.confirmar_button)

        # Ruta base BD
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.BASE_DIR, "db", "data_base.db")

        # Precios
        self.precio_preferencial = 850000
        self.precio_economica = 235000

        # Variables para guardar resumen
        self.total = 0
        self.pasajeros = []

    def crear_form_pasajero(self, nro):
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.addRow(QLabel(f"Pasajero {nro}"))

        nombre_input = QLineEdit()
        documento_input = QLineEdit()
        tipo_silla = QComboBox()
        tipo_silla.addItems(["preferencial", "economica"])

        layout.addRow("Nombre:", nombre_input)
        layout.addRow("Documento:", documento_input)
        layout.addRow("Tipo de silla:", tipo_silla)

        # Guardar widgets para acceder luego
        widget.nombre_input = nombre_input
        widget.documento_input = documento_input
        widget.tipo_silla = tipo_silla

        return widget

    def calcular_resumen(self):
        self.pasajeros.clear()
        self.total = 0
        detalles = []

        # Validar y obtener datos
        for widget in self.pasajeros_widgets:
            nombre = widget.nombre_input.text().strip()
            doc = widget.documento_input.text().strip()
            silla = widget.tipo_silla.currentText()

            if nombre == "" and doc == "":
                # Pasajero no llenado, ignorar
                continue

            if not nombre or not doc:
                QMessageBox.warning(self, "Datos incompletos", "Completa nombre y documento para todos los pasajeros indicados.")
                return

            self.pasajeros.append({
                "nombre": nombre,
                "documento": doc,
                "tipo_silla": silla
            })

            if silla == "preferencial":
                self.total += self.precio_preferencial
            else:
                self.total += self.precio_economica

            detalles.append(f"{nombre} ({doc}) - {silla} - ${self.total:,}")

        if len(self.pasajeros) == 0:
            QMessageBox.warning(self, "Sin pasajeros", "Debes ingresar al menos un pasajero.")
            return

        # Mostrar resumen
        resumen_text = f"Total a pagar: ${self.total:,.0f}\n\nDetalles:\n"
        for p in self.pasajeros:
            precio_p = self.precio_preferencial if p["tipo_silla"] == "preferencial" else self.precio_economica
            resumen_text += f"- {p['nombre']} ({p['documento']}): {p['tipo_silla']} - ${precio_p:,}\n"

        self.resumen_label.setText(resumen_text)
        self.confirmar_button.setEnabled(True)
    



