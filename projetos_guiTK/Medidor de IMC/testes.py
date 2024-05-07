import customtkinter as ctk

def on_enter(event):
    button.configure(cursor="hand2")

def on_leave(event):
    button.configure(cursor="arrow")

root = ctk.CTk()
button = ctk.CTkButton(root, text="Meu Botão")
button.pack(pady=20)

button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

root.mainloop()
