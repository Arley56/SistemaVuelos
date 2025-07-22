from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt


class DialogoCheckIn(QDialog):
    def __init__(self, numero_reserva, conn, parent=None):
        super().__init__(parent)
        self.numero_reserva = numero_reserva
        self.conn = conn
        self.setWindowTitle("Check-in")
        self.setMinimumWidth(400)

        self.obtener_datos_reserva()
        self.setup_ui()

    def obtener_datos_reserva(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT codigo_vuelo, documento_usuario, sillas_preferencial, sillas_economica
            FROM Reservas
            WHERE numero_reserva = ?
        """, (self.numero_reserva,))
        datos = cursor.fetchone()

        if datos:
            self.reserva = {
                "codigo_vuelo": datos[0],
                "documento_usuario": datos[1],
                "sillas_preferencial": datos[2],
                "sillas_economica": datos[3]
            }
        else:
            QMessageBox.critical(self, "Error", "No se encontró la reserva.")
            self.reject()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.label_info = QLabel(
            f"Reserva #{self.numero_reserva} - Vuelo {self.reserva['codigo_vuelo']}\n"
            f"Pasajeros: {self.reserva['sillas_preferencial']} preferencial, "
            f"{self.reserva['sillas_economica']} económica"
        )
        layout.addWidget(self.label_info)

        self.spin_cabina = QSpinBox()
        self.spin_cabina.setRange(0, 10)
        form_layout.addRow("Maletas de cabina (total):", self.spin_cabina)

        self.spin_bodega = QSpinBox()
        self.spin_bodega.setRange(0, 10)
        form_layout.addRow("Maletas de bodega (total):", self.spin_bodega)

        layout.addLayout(form_layout)

        self.btn_confirmar = QPushButton("Confirmar Check-in")
        self.btn_confirmar.clicked.connect(self.confirmar_checkin)
        layout.addWidget(self.btn_confirmar)

        self.setLayout(layout)

    def confirmar_checkin(self):
        cabina = self.spin_cabina.value()
        bodega = self.spin_bodega.value()

        pref = self.reserva['sillas_preferencial']
        econ = self.reserva['sillas_economica']
        total_pasajeros = pref + econ

        # Costos
        costo_adicional = 0

        # Maleta de cabina: gratuita para preferencial, $40.000 por cada una en económica
        cabina_gratis = pref  # 1 por silla preferencial
        cabina_extra = max(0, cabina - cabina_gratis)
        costo_cabina = cabina_extra * 40000
        costo_adicional += costo_cabina

        # Maleta de bodega: 1 incluida por silla preferencial
        bodega_gratis = pref
        bodega_extra = max(0, bodega - bodega_gratis)
        costo_bodega = bodega_extra * 60000
        costo_adicional += costo_bodega

        # Acumular millas
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE Usuarios
            SET millas = millas + 500
            WHERE documento = ?
        """, (self.reserva['documento_usuario'],))

        self.conn.commit()

        resumen = (
            f"✔ Check-in completado para {total_pasajeros} pasajero(s).\n\n"
            f"🧳 Maletas de cabina: {cabina} (Gratis: {cabina_gratis})\n"
            f"📦 Maletas de bodega: {bodega} (Gratis: {bodega_gratis})\n\n"
            f"💰 Costo adicional por cabina: ${costo_cabina:,}\n"
            f"💰 Costo adicional por bodega: ${costo_bodega:,}\n"
            f"🎯 Total adicional: ${costo_adicional:,}\n"
            f"🎁 500 millas acumuladas."
        )

        QMessageBox.information(self, "Resumen Check-in", resumen)
        self.accept()


