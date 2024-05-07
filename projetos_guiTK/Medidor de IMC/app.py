import customtkinter as ctk
from configs import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=VERDE)

        # Configurações da janela
        self.title('Calculadora | IMC')
        self.geometry('400x400')
        self.resizable(False, False)
        self.mudar_barra()

        # Grid layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')

        # Dados
        self.altura_int = ctk.IntVar(value=170)
        self.peso_float = ctk.DoubleVar(value=70)
        self.imc_string = ctk.StringVar()
        self.update_imc()

        # Tracing
        self.altura_int.trace_add('write', self.update_imc)
        self.peso_float.trace_add('write', self.update_imc)

        # Widgets
        Resultado(self, self.imc_string)
        Peso(self, self.peso_float)
        Altura(self, self.altura_int)

        # Rodando o aplicativo
        self.mainloop()

        # Funções
    def update_imc(self, *args):
        altura_metro = self.altura_int.get() / 100
        peso_kilograma = self.peso_float.get()
        imc = round(peso_kilograma / altura_metro ** 2, 2)
        self.imc_string.set(value=imc)

    def mudar_barra(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            cor_barra = COR_BARRA
            windll.dwmapi.DwmSetWindowAttribute(
                HWND,
                35,
                byref(c_int(cor_barra)),
                sizeof(c_int)
            )
        except:
            pass


class Resultado(ctk.CTkLabel):
    def __init__(self, parent, imc_string):
        fonte = ctk.CTkFont(FONTE, TEXTO_PRINCIPAL, weight='bold')
        super().__init__(master=parent, text='22.5',
                         font=fonte, text_color=BRANCO, textvariable=imc_string)

        self.grid(column=0, row=0, rowspan=2, sticky='nsew')


class Peso(ctk.CTkFrame):
    def __init__(self, parent, peso_float):
        super().__init__(master=parent, fg_color=BRANCO, corner_radius=10)

        self.peso_float = peso_float

        # Grid layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')
        self.columnconfigure(3, weight=1, uniform='b')
        self.columnconfigure(4, weight=2, uniform='b')

        # Widgets
        botao_mais_grande = ctk.CTkButton(master=self, text='+', fg_color=CINZA_CLARO,
                                          corner_radius=10, hover_color=VERDE, text_color='black', command=lambda: self.update_peso(('mais', 'grande')))
        botao_mais_grande.grid(row=0, column=4, padx=8, pady=15, sticky='ns')

        botao_menos_grande = ctk.CTkButton(master=self, text='-', fg_color=CINZA_CLARO,
                                           corner_radius=10, hover_color=VERDE, text_color='black', command=lambda: self.update_peso(('menos', 'grande')))
        botao_menos_grande.grid(row=0, column=0, padx=8, pady=15, sticky='ns')

        botao_mais_nanico = ctk.CTkButton(
            master=self, text='+', fg_color=CINZA_CLARO, corner_radius=10, hover_color=VERDE, text_color='black', command=lambda: self.update_peso(('mais', 'nanico')))
        botao_mais_nanico.grid(row=0, column=3, padx=2, pady=8)

        botao_menos_nanico = ctk.CTkButton(
            master=self, text='-', fg_color=CINZA_CLARO, corner_radius=10, hover_color=VERDE, text_color='black', command=lambda: self.update_peso(('menos', 'nanico')))
        botao_menos_nanico.grid(row=0, column=1, padx=2, pady=8)

        fonte = ctk.CTkFont(FONTE, TEXTO_INPUT)

        self.peso_var = ctk.StringVar(value='70kg')

        label_peso = ctk.CTkLabel(
            master=self, text='85 kg', text_color='black', font=fonte, textvariable=self.peso_var)
        label_peso.grid(row=0, column=2)

        self.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)

    def update_peso(self, info=None):
        quantidade = 1 if info[1] == 'grande' else 0.1
        if info[0] == 'mais':
            self.peso_float.set(self.peso_float.get() + quantidade)
        else:
            self.peso_float.set(self.peso_float.get() - quantidade)

        self.peso_var.set(f'{round(self.peso_float.get(), 1)}kg')


class Altura(ctk.CTkFrame):
    def __init__(self, parent, altura_int):
        super().__init__(master=parent, fg_color=BRANCO)

        # Widgets
        slider = ctk.CTkSlider(master=self,
                               command=self.update_text,
                               progress_color=VERDE,
                               fg_color=CINZA_CLARO,
                               button_color=CINZA,
                               button_hover_color=CINZA,
                               variable=altura_int,
                               from_=100,
                               to=250)
        slider.pack(expand=True, fill='x', side='left', padx=10, pady=10)

        fonte = ctk.CTkFont(FONTE, TEXTO_INPUT)

        self.label_string = ctk.StringVar(value='1.60m')

        label_altura = ctk.CTkLabel(
            master=self, text='1.80 m', font=fonte, text_color='black', textvariable=self.label_string)
        label_altura.pack(side='left', expand=True, fill='both')

        self.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

    def update_text(self, quantidade):
        quantidade_string = str(int(quantidade))
        metro = quantidade_string[0]
        cm = quantidade_string[1:]
        self.label_string.set(value=f'{metro}.{cm}m')


if __name__ == '__main__':
    App()
