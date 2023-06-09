from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from conectar import conexao, cursor
from read import listar_marcas, listar_produtos, search_products
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from web import Web
import pandas as pd
import openpyxl

janela = Tk()


class Aplicacao():
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frames()
        self.botoes()
        self.labels()
        self.inserts()
        self.lista()
        self.grafico()
        janela.mainloop()

    def tela(self):
        self.janela.title("MAGAZU")
        self.janela.configure(background="cyan")
        self.janela.geometry("700x800")
        self.janela.resizable(True, True)
        self.janela.minsize(width=700, height=700)

    def frames(self):
        self.frame0 = Frame(self.janela, bg="blue")
        self.frame0.place(relheight=0.07, relwidth=0.94, relx=0.03, rely=0.03)
        self.frame1 = Frame(self.janela, bg="blue")
        self.frame1.place(relheight=0.07, relwidth=0.94, relx=0.03, rely=0.115)
        self.frame2 = Frame(self.janela, bg="blue")
        self.frame2.place(relheight=0.25, relwidth=0.94, relx=0.03, rely=0.21)
        self.frame3 = Frame(self.janela, bg="blue")
        self.frame3.place(relheight=0.45, relwidth=0.94, relx=0.03, rely=0.475)

    def botoes(self):
        self.btBuscarAll = Button(self.frame0, text='Ler', bg="cyan", command=self.ler_produtos)
        self.btBuscarAll.place(relx=0.48, rely=0.15, relwidth=0.15, relheight=0.70)

        self.btBuscar = Button(self.frame0, text='Buscar', bg="cyan", command=self.procurar_produtos)
        self.btBuscar.place(relx=0.64, rely=0.15, relwidth=0.15, relheight=0.70)

        self.btClear = Button(self.frame0, text='Limpar', bg="cyan", command=self.limpar)
        self.btClear.place(relx=0.80, rely=0.15, relwidth=0.15, relheight=0.70)

        self.btExportar = Button(self.frame1, text='Exportar', bg="cyan", command=self.exportar)
        self.btExportar.place(relx=0.48, rely=0.15, relwidth=0.15, relheight=0.70)

        self.btExportarMarca = Button(self.frame1, text='Exportar Marca', bg="cyan", command=self.exportar_marca)
        self.btExportarMarca.place(relx=0.64, rely=0.15, relwidth=0.15, relheight=0.70)

        self.btWeb = Button(self.frame1, text='Web Scraping', bg="cyan", command=self.web)
        self.btWeb.place(relx=0.80, rely=0.15, relwidth=0.15, relheight=0.70)


    def labels(self):
        self.lbMarca = Label(self.frame0, text="Marcas:", background="cyan")
        self.lbMarca.place(relx=0.05, rely=0.03, relwidth=0.4, relheight=0.20)

        self.lbFormato = Label(self.frame1, text="Formato de Arquivo:", bg="cyan")
        self.lbFormato.place(relx=0.05, rely=0.03, relwidth=0.4, relheight=0.20)

    def inserts(self):
        self.marcas = ["Macbooks", "Notebook Acer", "Notebook Dell", "Notebook Lenovo", "Notebook Samsung"]

        self.clicked = StringVar()

        self.clicked.set("")

        self.drop_marcas = OptionMenu(self.frame0, self.clicked, *self.marcas)
        self.drop_marcas.pack()
        self.drop_marcas.place(relx=0.05, rely=0.30, relwidth=0.4, relheight=0.60)

        self.formatos = [".xlsx", ".csv"]

        self.clicked2 = StringVar()

        self.clicked2.set("")

        self.drop_formatos = OptionMenu(self.frame1, self.clicked2, *self.formatos)
        self.drop_formatos.pack()
        self.drop_formatos.place(relx=0.05, rely=0.30, relwidth=0.4, relheight=0.60)




    def lista(self):
        self.listaProdutos = ttk.Treeview(self.frame2, height=3, columns=("col1", "col2", "col3", "col4"))

        self.listaProdutos.heading('#0', text='ID')
        self.listaProdutos.heading('#1', text='Modelo')
        self.listaProdutos.heading('#2', text='Preço')
        self.listaProdutos.heading('#3', text='Marca')

        self.listaProdutos.column('#0', width=50)
        self.listaProdutos.column('#1', width=360)
        self.listaProdutos.column('#2', width=80)
        self.listaProdutos.column('#3', width=120)

        self.listaProdutos.place(relx=0.025, rely=0.075, relwidth=0.925, relheight=0.85)

        self.scrollLista = Scrollbar(self.frame2, orient='vertical')
        self.listaProdutos.configure(yscrollcommand=self.scrollLista.set)
        self.scrollLista.place(relx=0.949, rely=0.079, relwidth=0.02, relheight=0.84)
        self.scrollLista.config(command=self.listaProdutos.yview)



    def delete_lista(self):
        self.listaProdutos.delete(*self.listaProdutos.get_children())

    def procurar_produtos(self):
        self.delete_lista()
        linhas = search_products(self.clicked.get())
        for i in range(len(linhas)):
            self.listaProdutos.insert(index=i, values=[linhas[i][1], linhas[i][2], linhas[i][3]], parent="", text=linhas[i][0])

    def ler_produtos(self):
        self.delete_lista()
        linhas = listar_produtos()
        for i in range(len(linhas)):
            self.listaProdutos.insert(index=i, values=[linhas[i][1], linhas[i][2], linhas[i][3]], parent="", text=linhas[i][0])

    def limpar(self):
        self.delete_lista()

    def web(self):
        W1 = Web()
        W1.webscraping()

    def grafico(self):
        fig = plt.Figure(figsize=(12, 6), dpi=50)
        ax = fig.add_subplot(111)

        marcas = ["Macbooks", "Notebook Acer", "Notebook Dell", "Notebook Lenovo", "Notebook Samsung"]

        valores = []
        for marca in marcas:
            sql = f'select * from produtos where marca = "{marca}"'
            cursor.execute(sql)
            linhas = cursor.fetchall()
            soma_valor = 0
            for linha in linhas:
                preco = linha[2]
                preco_num = preco.replace("R$", "").replace(".", "").replace(",", ".")
                valor = float(preco_num)
                soma_valor = soma_valor + valor
            media_valores = soma_valor/len(linhas)
            valores.append(media_valores)

        ax.bar(marcas, valores)

        ax.set_ylabel('Média de preços')
        ax.set_title('Média de preço por marca')

        canva = FigureCanvasTkAgg(fig, self.janela)
        canva.get_tk_widget().place(relx=0.05, rely=0.50)

    def del_xlsx(self):
        dados = pd.read_excel("Produtos.xlsx")
        df = pd.DataFrame(dados)
        df.drop()

    def create_xlsx(self):
        d = {"Produto": [''], "Preço": [''], "Marca": ['']}
        dados = pd.DataFrame(data=d)
        dados.to_excel("Produtos.xlsx", index=False)

    def del_csv(self):
        dados = pd.read_csv("Produtos.csv")
        df = pd.DataFrame(dados)
        df.drop()

    def create_csv(self):
        d = {"Produto": [''], "Preço": [''], "Marca": ['']}
        dados = pd.DataFrame(data=d)
        dados.to_csv("Produtos.csv", index=False)

    def exportar_marca(self):
        linhas = search_products(self.clicked.get())
        if self.clicked2.get() == ".xlsx":
            try:
                self.del_xlsx()
            except:
                pass

            self.create_xlsx()
            df = pd.read_excel("Produtos.xlsx")
            for linha in linhas:
                df.loc[len(df)] = [linha[1], linha[2], linha[3]]
            df.to_excel("Produtos.xlsx", index=False)

        elif self.clicked2.get() == ".csv":
            try:
                self.del_csv()
            except:
                pass

            self.create_csv()
            df = pd.read_csv("Produtos.csv")
            for linha in linhas:
                df.loc[len(df)] = [linha[1], linha[2], linha[3]]
            df.to_csv("Produtos.csv", index=False)

        showinfo("Atenção", "Arquivo Criado")

    def exportar(self):
        linhas = listar_produtos()
        if self.clicked2.get() == ".xlsx":
            try:
                self.del_xlsx()
            except:
                pass

            self.create_xlsx()
            df = pd.read_excel("Produtos.xlsx")
            for linha in linhas:
                df.loc[len(df)] = [linha[1], linha[2], linha[3]]
            df.to_excel("Produtos.xlsx", index=False)

        elif self.clicked2.get() == ".csv":
            try:
                self.del_csv()
            except:
                pass

            self.create_csv()
            df = pd.read_csv("Produtos.csv")
            for linha in linhas:
                df.loc[len(df)] = [linha[1], linha[2], linha[3]]
            df.to_csv("Produtos.csv", index=False)

        showinfo("Atenção", "Arquivo Criado")