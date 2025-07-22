from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHBoxLayout, QDialog
)
import sqlite3
import os

class GestionReservas(QWidget):
    def __init__(self, documento_usuario):
        super().__init__()
        self.documento_usuario = documento_usuario
        self.setWindowTitle("Gestión de Reservas")
        self.resize(700, 400)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Tabla reservas del usuario
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Reserva #", "Código Vuelo", "Fecha", "Sillas Preferencial",
            "Sillas Económica", "Total"
        ])
        layout.addWidget(self.tabla)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_cancelar = QPushButton("Cancelar Reserva")
        self.btn_modificar = QPushButton("Modificar Reserva")
        self.btn_checkin = QPushButton("Realizar Check-in")

        self.btn_cancelar.clicked.connect(self.cancelar_reserva)
        self.btn_modificar.clicked.connect(self.modificar_reserva)
        self.btn_checkin.clicked.connect(self.realizar_checkin)

        btn_layout.addWidget(self.btn_cancelar)
        btn_layout.addWidget(self.btn_modificar)
        btn_layout.addWidget(self.btn_checkin)

        layout.addLayout(btn_layout)

        self.cargar_reservas()

    def cargar_reservas(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "db", "data_base.db")

        try:
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT numero_reserva, codigo_vuelo, fecha, sillas_preferencial, sillas_economica, total
                FROM Reservas WHERE documento_usuario = ?
                ORDER BY fecha DESC
            """, (self.documento_usuario,))
            reservas = cursor.fetchall()
            conexion.close()

            self.tabla.setRowCount(len(reservas))
            for row_idx, reserva in enumerate(reservas):
                for col_idx, valor in enumerate(reserva):
                    self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))

            self.tabla.resizeColumnsToContents()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo cargar las reservas:\n{e}")

    def obtener_reserva_seleccionada(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Atención", "Por favor selecciona una reserva.")
            return None
        numero_reserva = self.tabla.item(fila, 0).text()
        return numero_reserva

    def cancelar_reserva(self):
        numero_reserva = self.obtener_reserva_seleccionada()
        if not numero_reserva:
            return

        confirm = QMessageBox.question(
            self, "Confirmar Cancelación",
            f"¿Está seguro que desea cancelar la reserva #{numero_reserva}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                db_path = os.path.join(BASE_DIR, "db", "data_base.db")
                conexion = sqlite3.connect(db_path)
                cursor = conexion.cursor()

                # Eliminar reserva
                cursor.execute("DELETE FROM Reservas WHERE numero_reserva = ?", (numero_reserva,))

                conexion.commit()
                conexion.close()

                QMessageBox.information(self, "Cancelada", "Reserva cancelada exitosamente.")
                self.cargar_reservas()

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error BD", f"No se pudo cancelar la reserva:\n{e}")

    def modificar_reserva(self):
        numero_reserva = self.obtener_reserva_seleccionada()
        if not numero_reserva:
            return
        # Aquí abrirías un diálogo para modificar la reserva (cantidad sillas, pasajeros, etc.)
        # Puedes reutilizar o adaptar tu DialogoReserva para edición
        QMessageBox.information(self, "Modificar", f"Funcionalidad modificar reserva #{numero_reserva} pendiente por implementar.")

    def realizar_checkin(self):
        numero_reserva = self.obtener_reserva_seleccionada()
        if not numero_reserva:
            return
        # Aquí abrirías un diálogo para realizar check-in (mostrar info, acumular millas, elegir equipaje)
        QMessageBox.information(self, "Check-in", f"Funcionalidad check-in para reserva #{numero_reserva} pendiente por implementar.")
