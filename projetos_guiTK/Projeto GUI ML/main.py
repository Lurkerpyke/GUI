from typing import Tuple
import customtkinter as ctk
import webbrowser
from PIL import Image, ImageTk
import pandas as pd


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color='#141326')

        # Configurações da janela
        self.title('Formulário | Titanic modelo ML')
        self.geometry('900x600+100+100')
        self.resizable(False, False)

        # Grid layout
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='teste')

        # Frames
        self.direita = Frame_direita(self)
        self.centro = Frame_centro(self)
        self.esquerda = Frame_esquerda(self)

        # Run
        self.mainloop()

    def get_response(self):
        dict_to_save = self.centro.get_dicionario_ofc()
        self.direita.get_response(dict_to_save)


class Frame_direita(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # Grid layout
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='b')
        self.rowconfigure(5, weight=5, uniform='b')
        self.columnconfigure((0, 1), weight=1, uniform='c')

        # Variáveis

        def update_idade(valor):
            idade_var.set(value=valor)

        def update_convidados(valor):
            convidados_var.set(f"${valor}")

        slider_idade = ctk.IntVar(value=20)
        slider_convidados = ctk.IntVar(value=0)

        idade_var = ctk.StringVar()
        convidados_var = ctk.StringVar()

        idade_var.set(slider_idade)
        convidados_var.set(slider_convidados)

        # Widgets

        def create_window(parent):
            if not hasattr(parent, "extra_window"):
                parent.extra_window = ctk.CTkToplevel(master=parent)
                parent.extra_window.title('Informações')
                parent.extra_window.geometry('400x400+1300+100')
                parent.extra_window.resizable(False, False)

                parent.extra_window.protocol(
                    "WM_DELETE_WINDOW", lambda: close_window(parent))

        def close_window(parent):
            if hasattr(parent, "extra_window"):
                parent.extra_window.destroy()
                del parent.extra_window

        fonte = ctk.CTkFont('Roboto', 12, 'bold')
        button1 = ctk.CTkButton(
            master=self, text='Informações', corner_radius=10, command=lambda: create_window(parent))
        button2 = ctk.CTkButton(
            master=self, text='Entre em contato', corner_radius=10)
        button3 = ctk.CTkButton(
            master=self, text='Prever', corner_radius=10, command=lambda: self.master.get_response())

        slider1 = ctk.CTkSlider(master=self, from_=1,
                                to=90, orientation='vertical', variable=slider_idade, command=update_idade)
        slider2 = ctk.CTkSlider(master=self, from_=1,
                                to=600, orientation='vertical', variable=slider_convidados, command=update_convidados)

        label1 = ctk.CTkLabel(master=self, text='idade', font=fonte, padx=5)
        label2 = ctk.CTkLabel(
            master=self, text='Tarifa\n$', font=fonte, padx=5)
        label3 = ctk.CTkLabel(master=self, textvariable=idade_var.get(
        ), font=fonte, padx=2, fg_color='#202021', corner_radius=20)
        label4 = ctk.CTkLabel(master=self, textvariable=convidados_var.get(
        ), font=fonte, padx=2, fg_color='#202021', corner_radius=20)

        # Pack
        button1.grid(row=0, column=0, columnspan=2, padx=5)
        button2.grid(row=1, column=0, columnspan=2, padx=5)
        button3.grid(row=2, column=0, columnspan=2, padx=5)
        label1.grid(row=3, column=0)
        label2.grid(row=3, column=1)
        label3.grid(row=4, column=0, padx=5)
        label4.grid(row=4, column=1, padx=5)
        slider1.grid(row=5, column=0, sticky='ns', pady=20)
        slider2.grid(row=5, column=1, sticky='ns', pady=20)

        self.grid(row=0, column=4, sticky='nsew', padx=5, pady=10)

    def get_response(self, dict):
        # Save the dictionary to an Excel file
        df = pd.DataFrame.from_dict(dict)
        df.to_excel('output.xlsx', index=False)


class Frame_centro(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.dicionario_ofc = {'classe': [],
                               'sexo': [],
                               'Irmãs_Cônjugue': [],
                               'Pais_crianças': [],
                               'Embarque': [],
                               'homen?': [],
                               'Deck': []
                               }

        # Grid layout
        for i in range(12):
            self.rowconfigure(i, weight=1, uniform='g')
        self.columnconfigure(0, weight=2, uniform='o')
        self.columnconfigure(1, weight=2, uniform='o')
        self.columnconfigure(2, weight=1, uniform='o')

        # Widgets
        self.create_label('Dados Titanic', 20).grid(
            row=0, column=0, columnspan=3, pady=5, rowspan=2)

        # Classe do passageiro
        self.create_label('Classe', 12).grid(
            row=3, column=0, pady=10, padx=10)
        self.create_dropdown(['classe 1', 'classe 2', 'classe 3']).grid(
            row=3, column=1, padx=10, pady=2, sticky='ew')

        # Sexo do passageiro
        self.create_label('Sexo', 12).grid(
            row=4, column=0, pady=10, padx=10)
        self.create_dropdown(['Masculino', 'Feminino', 'Criança']).grid(
            row=4, column=1, padx=10, pady=2, sticky='ew')

        # Quantidade de Irmãs e/ou Esposas
        self.create_label('Irmãs e/ou Cônjugue', 12).grid(
            row=5, column=0, pady=10, padx=10)
        self.create_dropdown(['0.0', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0']).grid(
            row=5, column=1, padx=10, pady=2, sticky='ew')

        # Quantidade de pais e/ou crianças
        self.create_label('Pais e/ou crianças', 12).grid(
            row=6, column=0, pady=10, padx=10)
        self.create_dropdown(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']).grid(
            row=6, column=1, padx=10, pady=2, sticky='ew')

        # Porto de embarque
        self.create_label('Embarque', 12).grid(
            row=7, column=0, pady=10, padx=10)
        self.create_dropdown(['Southampton', 'Cherbourg', 'Queenstown']).grid(
            row=7, column=1, padx=10, pady=2, sticky='ew')

        # Homen presente na cabine?
        self.create_label('Tinha homen?', 12).grid(
            row=8, column=0, pady=10, padx=10)
        self.create_dropdown(['Sim', 'Não']).grid(
            row=8, column=1, padx=10, pady=2, sticky='ew')

        # Deck
        self.create_label('Deck', 12).grid(
            row=9, column=0, pady=10, padx=10)
        self.create_dropdown(['A', 'B', 'C', 'D', 'E', 'F', 'G']).grid(
            row=9, column=1, padx=10, pady=2, sticky='ew')

        self.grid(column=1, row=0, columnspan=3,
                  sticky='nsew', padx=5, pady=10)

    # Funções

    def get_dicionario_ofc(self):
        if all(value is not None for value in self.dicionario_ofc.values()):
            return self.dicionario_ofc
        else:
            print('Preencha todos os valores')

    def create_label(self, texto, tamanho):
        fonte = ctk.CTkFont('Roboto', tamanho, 'bold')
        label = ctk.CTkLabel(master=self, text=texto, font=fonte)
        return label

    def create_dropdown(self, opcoes):
        if not isinstance(opcoes, list):
            raise TypeError("O parâmetro 'options' deve ser uma lista.")
        dicionario = {'classe': ['classe 1', 'classe 2', 'classe 3'],
                      'sexo': ['Masculino', 'Feminino', 'Criança'],
                      'Irmãs_Cônjugue': ['0.0', '1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0'],
                      'Pais_crianças': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                      'Embarque': ['Southampton', 'Cherbourg', 'Queenstown'],
                      'homen?': ['Sim', 'Não'],
                      'Deck': ['A', 'B', 'C', 'D', 'E', 'F', 'G']
                      }

        def combobox_callback(choice, dicionario=dicionario):
            print("combobox dropdown clicked:", choice)
            for key, value in dicionario.items():
                if choice in value:
                    if key in self.dicionario_ofc and not self.dicionario_ofc[key]:
                        self.dicionario_ofc[key].append(choice)
                    else:
                        self.dicionario_ofc[key] = []
                        self.dicionario_ofc[key].append(choice)
                    break

            print(self.dicionario_ofc)

        combobox = ctk.CTkComboBox(
            master=self, values=opcoes, command=combobox_callback, state='readonly')

        return combobox


class Frame_esquerda(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # Grid layout
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='b')
        self.columnconfigure((0, 1), weight=1, uniform='c')

        # Widgets
        fonte_titulo = ctk.CTkFont('Calibri', 20, 'bold')
        fonte_apresentação = ctk.CTkFont('Calibri', 12, 'normal')

        label_titulo = ctk.CTkLabel(
            master=self, text='Sobre mim', font=fonte_titulo)
        label_titulo.grid(row=0, column=0, columnspan=2,
                          padx=10, pady=10, sticky='n')

        label_apresentação = ctk.CTkLabel(
            master=self, text='Olá user!\nme chamo\nLeandro Soares.\nSou desenvolvedor\natualmente focado\nem aprendizado\nde máquina em\npython, Interfaces\ngráficas e com\nconhecimento em HTML\ne CSS.\nDê uma olhada nos\nmeus projetos e\nredes sociais\nabaixo, até!')
        label_apresentação.grid(row=1, column=0, padx=10,
                                pady=0, sticky='n', rowspan=4, columnspan=2)

        # Facebook Logo
        facebook_logo = Image.open('imagens/facebook_logo.png')
        facebook_logo = facebook_logo.resize((60, 60))
        facebook_logo = ImageTk.PhotoImage(facebook_logo)
        Logo(parent=self, texto='Facebook\n',
             imagem=facebook_logo, coluna=0, linha=5, link='https://www.facebook.com/profile.php?id=100007163133910')

        # Github Logo
        github_logo = Image.open('imagens/github_logo.png')
        github_logo = github_logo.resize((60, 60))
        github_logo = ImageTk.PhotoImage(github_logo)
        Logo(parent=self, texto='GitHub\n',
             imagem=github_logo, coluna=1, linha=5, link='https://github.com/Lurkerpyke')

        # Linkedin Logo
        linkedin_logo = Image.open('imagens/linkedin_logo.png')
        linkedin_logo = linkedin_logo.resize((160, 60))
        linkedin_logo = ImageTk.PhotoImage(linkedin_logo)
        Logo(parent=self, texto='LinkedIn\n',
             imagem=linkedin_logo, coluna=0, linha=6, spancolumn=2, link='https://www.linkedin.com/authwall?trk=bf&trkInfo=AQFQgauEzmHVcgAAAY5jvE5IIe6Avb6QFs8seXgPV_6ocBnNYoOT0iugtjjyjPgMgCYJ22fT50ssNGrPPJrVPfIeEWm4GxVkZeK3P2YGHQj-FetutubU6rqf3rQBbz2ihx9sU6Y=&original_referer=&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fleandro-soares-71525a243%3Futm_source%3Dshare%26utm_campaign%3Dshare_via%26utm_content%3Dprofile%26utm_medium%3Dandroid_app')

        # LINKS

        # Grid
        self.grid(row=0, column=0, sticky='nsew', padx=5, pady=10)


class Logo(ctk.CTkLabel):
    def __init__(self, parent, texto, imagem, linha, coluna, link, spancolumn=1):
        fonte = ctk.CTkFont('Calibre', 12, 'bold')
        super().__init__(master=parent, text=texto,
                         image=imagem, font=fonte, compound='bottom')

        def open_url(url):
            webbrowser.open_new_tab(url)

        self.bind("<Button-1>", lambda e: open_url(link))

        self.grid(row=linha, column=coluna, columnspan=spancolumn, pady=5)


App()
