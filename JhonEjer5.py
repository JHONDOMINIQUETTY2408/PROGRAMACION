#Nombre: JHON JAIRO PENARANDA DOMINIQUETTY
#Fecha: 27/09/2026
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
# Class Usuario
class Usuario:
    def __init__(self, usuario, password):
        self._usuario = usuario
        self._password = password
    def validar(self, usuario_ingresado, password_ingresada):
        return (usuario_ingresado == self._usuario and
                password_ingresada == self._password)
# Class ReservaSala
class ReservaSala:
    def __init__(self, usuario, tarifa_hora):
        self._usuario= usuario
        self._hora_inicio= None
        self._tarifa_hora= tarifa_hora
    def registrar_inicio(self, hora):
        self._hora_inicio=datetime.strptime(hora, "%H:%M")
        return True
    def registrar_fin(self,hora):
        hora_fin = datetime.strptime(hora, "%H:%M")
        if hora_fin<=self._hora_inicio:
            return False
        self._hora_fin= hora_fin
        return True
    def calcular_costo(self, hora_fin):
        fin =datetime.strptime(hora_fin, "%H:%M")
        if fin<=self._hora_inicio:
            return 0
        tiempo = fin -self._hora_inicio
        horas = tiempo.total_seconds() / 3600
        return horas *self._tarifa_hora
    def obtener_usuario(self):
        return self._usuario
class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Study Room Reservation System")
        self.ventana.geometry("500x450")
        self.reservas = []
        self.usuario = Usuario("programación", "programación")
        self.mostrar_login()
    def mostrar_login(self):
        self.limpiar_ventana()
        tk.Label(
            self.ventana,
            text="LOGIN",
            font=("Arial", 20, "bold")
        ).pack(pady=20)
        tk.Label(
            self.ventana,
            text="Username:"
        ).pack()
        self.entrada_usuario = tk.Entry(self.ventana)
        self.entrada_usuario.pack(pady=5)
        tk.Label(
            self.ventana,
            text="Password:"
        ).pack()
        self.entrada_password = tk.Entry(
            self.ventana,
            show="*"
        )
        self.entrada_password.pack(pady=5)
        tk.Button(
            self.ventana,
            text="Login",
            command=self.validar_login
        ).pack(pady=20)
    def validar_login(self):
        usuario =self.entrada_usuario.get()
        password= self.entrada_password.get()
        if self.usuario.validar(usuario, password):
            self.mostrar_sistema()
        else:
            messagebox.showerror(
                "Login Error",
                "Incorrect username or password."
            )
    def mostrar_sistema(self):
        self.limpiar_ventana()
        tk.Label(
            self.ventana,
            text="STUDY ROOM RESERVATION SYSTEM",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        tk.Label(
            self.ventana,
            text="Responsible User:"
        ).pack()
        self.entrada_usuario_reserva = tk.Entry(self.ventana)
        self.entrada_usuario_reserva.pack(pady=5)
        tk.Label(
            self.ventana,
            text="Start Time (HH:MM):"
        ).pack()
        self.entrada_hora = tk.Entry(self.ventana)
        self.entrada_hora.pack(pady=5)
        tk.Label(
            self.ventana,
            text="Cost per Hour:"
        ).pack()
        self.entrada_tarifa = tk.Entry(self.ventana)
        self.entrada_tarifa.pack(pady=5)
        tk.Button(
            self.ventana,
            text="Register Reservation",
            command=self.registrar_reserva
        ).pack(pady=10)
        tk.Label(
            self.ventana,
            text="Select Reservation:"
        ).pack(pady=5)
        self.lista_reservas = ttk.Combobox(
            self.ventana,
            state="readonly"
        )
        self.lista_reservas.pack(pady=5)
        tk.Label(
            self.ventana,
            text="End Time (HH:MM):"
        ).pack()
        self.entrada_fin = tk.Entry(self.ventana)
        self.entrada_fin.pack(pady=5)
        tk.Button(
            self.ventana,
            text="Register End",
            command=self.registrar_fin
        ).pack(pady=10)
        tk.Button(
            self.ventana,
            text="Logout",
            command=self.mostrar_login
        ).pack(pady=5)
    def registrar_reserva(self):
        usuario = self.entrada_usuario_reserva.get()
        hora = self.entrada_hora.get()
        tarifa = self.entrada_tarifa.get()
        if usuario == "" or hora == "" or tarifa == "":
            messagebox.showwarning(
                "Warning",
                "Please complete all fields."
            )
            return
        try:
            tarifa = float(tarifa)
            reserva = ReservaSala(
                usuario,
                tarifa
            )
            reserva.registrar_inicio(hora)
            self.reservas.append(reserva)
            self.lista_reservas["values"] = [
                reserva.obtener_usuario()
                for reserva in self.reservas
            ]
            messagebox.showinfo(
                "Success",
                "Reservation registered successfully."
            )
            self.entrada_usuario_reserva.delete(0, tk.END)
            self.entrada_hora.delete(0, tk.END)
            self.entrada_tarifa.delete(0, tk.END)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Use HH:MM for the time and a valid number for the cost."
            )
    def registrar_fin(self):
        seleccion = self.lista_reservas.get()
        hora_fin = self.entrada_fin.get()
        if seleccion == "" or hora_fin == "":
            messagebox.showwarning(
                "Warning",
                "Select a reservation and enter the end time."
            )
            return
        for reserva in self.reservas:
            if reserva.obtener_usuario() == seleccion:
                try:
                    if reserva.registrar_fin(hora_fin):
                        total = reserva.calcular_costo(hora_fin)
                        messagebox.showinfo(
                            "Reservation Completed",
                            f"User: {seleccion}\n"
                            f"Total Cost: ${total:.2f}"
                        )
                        self.entrada_fin.delete(0, tk.END)
                    else:
                        messagebox.showerror(
                            "Invalid Time",
                            "End time must be greater than start time."
                        )
                except ValueError:
                    messagebox.showerror(
                        "Error",
                        "Use HH:MM for the end time."
                    )
                return
    def limpiar_ventana(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()
ventana = tk.Tk()
app = Aplicacion(ventana)
ventana.mainloop()