# app/adminVuelos.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QFormLayout, QLineEdit, QMessageBox, QTextEdit
import sqlite3

class AdminVuelos(QWidget):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.setWindowTitle("Panel de Administrador")
        self.resize(500, 400)

        layout = QVBoxLayout(self)

        btn_agregar = QPushButton("Agregar nuevo vuelo")
        btn_agregar.clicked.connect(self.agregar_vuelo)
        layout.addWidget(btn_agregar)

        btn_consultar = QPushButton("Consultar vuelos con sillas vendidas")
        btn_consultar.clicked.connect(self.consultar_vendidos)
        layout.addWidget(btn_consultar)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

    def agregar_vuelo(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Agregar vuelo")
        form = QFormLayout(dialogo)

        campos = {}
        for label in ["Código", "Origen", "Destino", "Horario", "Sillas Preferencial", "Sillas Económica"]:
            campos[label] = QLineEdit()
            form.addRow(label, campos[label])

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(lambda: self.insertar_vuelo(campos, dialogo))
        form.addRow(btn_guardar)

        dialogo.exec()

    def insertar_vuelo(self, campos, dialogo):
        try:
            codigo = campos["Código"].text()
            origen = campos["Origen"].text()
            destino = campos["Destino"].text()
            horario = campos["Horario"].text()
            pref = int(campos["Sillas Preferencial"].text())
            econ = int(campos["Sillas Económica"].text())

            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Vuelos (
                    codigo_vuelo,
                    ciudad_origen,
                    ciudad_destino,
                    horario,
                    sillas_preferencial,
                    sillas_economica
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (codigo, origen, destino, horario, pref, econ))

            self.conn.commit()

            QMessageBox.information(self, "Éxito", "Vuelo agregado correctamente.")
            dialogo.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")

    def consultar_vendidos(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT V.codigo_vuelo, V.ciudad_destino, V.horario, 
                    SUM(R.sillas_preferencial + R.sillas_economica) AS total_vendidas
                FROM Vuelos V
                JOIN Reservas R ON V.codigo_vuelo = R.codigo_vuelo
                GROUP BY V.codigo_vuelo
                HAVING total_vendidas > 0
            """)
            vuelos = cursor.fetchall()

            resultado = ""
            for vuelo in vuelos:
                codigo = vuelo[0]
                resultado += f"\n✈ Vuelo {codigo} ({vuelo[1]} → {vuelo[2]}) - Sillas vendidas: {vuelo[3]}\n"
                cursor.execute("""
                    SELECT P.nombre, P.documento
                    FROM Pasajeros P
                    JOIN Reservas R ON P.numero_reserva = R.numero_reserva
                    WHERE R.codigo_vuelo = ?
                """, (codigo,))
                pasajeros = cursor.fetchall()
                for p in pasajeros:
                    resultado += f"    - {p[0]} ({p[1]})\n"

            if not resultado:
                resultado = "No hay vuelos con sillas vendidas aún."

            self.resultado.setPlainText(resultado)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo consultar: {e}")
