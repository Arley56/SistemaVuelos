from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHBoxLayout, QDialog, QInputDialog
)
import sqlite3
import os

from app.dialogoCheckIn import DialogoCheckIn

class GestionReservas(QWidget):
    def __init__(self, documento_usuario):
        super().__init__()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "db", "data_base.db")
        self.conn = sqlite3.connect(db_path)
        
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

        try:
            cursor = self.conn.cursor()


            cursor.execute("""
                SELECT numero_reserva, codigo_vuelo, fecha, sillas_preferencial, sillas_economica, total
                FROM Reservas WHERE documento_usuario = ?
                ORDER BY fecha DESC
            """, (self.documento_usuario,))
            reservas = cursor.fetchall()

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

        confirm = QMessageBox.question(
        self,
        "Modificar reserva",
        f"¿Deseas modificar la reserva #{numero_reserva}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
)

        if confirm != QMessageBox.StandardButton.Yes:

            return

        cursor = self.conn.cursor()

        # Obtener datos actuales de la reserva
        cursor.execute("SELECT codigo_vuelo, sillas_preferencial, sillas_economica FROM Reservas WHERE numero_reserva = ?", (numero_reserva,))
        reserva = cursor.fetchone()

        if not reserva:
            QMessageBox.warning(self, "Error", "Reserva no encontrada.")
            return

        codigo_vuelo, prev_pref, prev_econ = reserva

        # Obtener disponibilidad actual del vuelo
        cursor.execute("SELECT sillas_preferencial, sillas_economica FROM Vuelos WHERE codigo_vuelo = ?", (codigo_vuelo,))
        vuelo = cursor.fetchone()
        if not vuelo:
            QMessageBox.warning(self, "Error", "Vuelo no encontrado.")
            return

        sillas_disp_pref, sillas_disp_econ = vuelo

        # InputDialog para nuevas cantidades
        pref, ok1 = QInputDialog.getInt(self, "Modificar Preferencial", "¿Cuántas sillas preferenciales?", min=0, max=sillas_disp_pref + prev_pref)
        if not ok1:
            return
        econ, ok2 = QInputDialog.getInt(self, "Modificar Económica", "¿Cuántas sillas económicas?", min=0, max=sillas_disp_econ + prev_econ)
        if not ok2:
            return

        if pref + econ > 3:
            QMessageBox.warning(self, "Límite excedido", "Máximo puedes reservar 3 sillas.")
            return

        # Calcular diferencia y actualizar disponibilidad del vuelo
        nuevas_disp_pref = sillas_disp_pref + prev_pref - pref
        nuevas_disp_econ = sillas_disp_econ + prev_econ - econ
        cursor.execute("UPDATE Vuelos SET sillas_preferencial = ?, sillas_economica = ? WHERE codigo_vuelo = ?",
                    (nuevas_disp_pref, nuevas_disp_econ, codigo_vuelo))

        # Calcular nuevo total
        total = pref * 850000 + econ * 235000

        # Actualizar reserva
        cursor.execute("""UPDATE Reservas 
                        SET sillas_preferencial = ?, sillas_economica = ?, total = ?
                        WHERE numero_reserva = ?""", (pref, econ, total, numero_reserva))

        # Eliminar antiguos pasajeros
        cursor.execute("DELETE FROM Pasajeros WHERE numero_reserva = ?", (numero_reserva,))

        # Insertar nuevos pasajeros
        for i in range(pref + econ):
            nombre, ok1 = QInputDialog.getText(self, f"Pasajero {i+1}", "Nombre completo:")
            if not ok1 or not nombre.strip():
                QMessageBox.warning(self, "Cancelado", "Nombre no válido. Modificación cancelada.")
                self.conn.rollback()
                return
            documento, ok2 = QInputDialog.getText(self, f"Pasajero {i+1}", "Número de documento:")
            if not ok2 or not documento.strip():
                QMessageBox.warning(self, "Cancelado", "Documento no válido. Modificación cancelada.")
                self.conn.rollback()
                return

            cursor.execute("INSERT INTO Pasajeros (numero_reserva, nombre, documento) VALUES (?, ?, ?)",
                        (numero_reserva, nombre.strip(), documento.strip()))

        self.conn.commit()
        QMessageBox.information(self, "Éxito", f"Reserva #{numero_reserva} actualizada correctamente.")
        self.cargar_reservas()


    def realizar_checkin(self):
        numero_reserva = self.obtener_reserva_seleccionada()
        if not numero_reserva:
            return

        dialogo = DialogoCheckIn(numero_reserva, self.conn, parent=self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Check-in", f"Check-in completado para reserva #{numero_reserva}")
            # Puedes refrescar datos si es necesario

