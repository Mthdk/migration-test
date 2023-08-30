import os
import pandas as pd
from openpyxl import load_workbook
from sqlalchemy import create_engine
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tqdm import tqdm

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação de Gerenciamento de Arquivos e Banco de Dados")

        self.db_engine = create_engine(DB_URL)
        self.file_path_column = 'path'  # Coluna que contém os caminhos no arquivo

        self.file_label = Label(root, text="Selecione o arquivo:")
        self.file_label.pack()

        self.file_path_entry = Entry(root)
        self.file_path_entry.pack()

        self.browse_button = Button(root, text="Procurar", command=self.browse_file)
        self.browse_button.pack()

        self.process_button = Button(root, text="Processar", command=self.process_files)
        self.process_button.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV e XLSX files", "*.csv *.xlsx")])
        self.file_path_entry.delete(0, END)
        self.file_path_entry.insert(0, file_path)

    def insert_data_to_db(self, file_path):
        df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
        df.to_sql('data', self.db_engine, if_exists='append', index=False)

    def move_files(self, files, destination_folder):
        os.makedirs(destination_folder, exist_ok=True)
        for file in tqdm(files, desc='Moving files', unit='file'):
            new_path = os.path.join(destination_folder, os.path.basename(file))
            os.rename(file, new_path)

    def process_files(self):
        file_path = self.file_path_entry.get()
        if not file_path:
            messagebox.showerror("Erro", "Selecione um arquivo.")
            return

        with self.db_engine.connect() as connection:
            result = connection.execute(f'SELECT DISTINCT {self.file_path_column} FROM data')
            files_to_move = [row[0] for row in result]

        self.insert_data_to_db(file_path)
        self.move_files(files_to_move, DESTINATION_FOLDER)
        messagebox.showinfo("Concluído", "Processamento concluído com sucesso.")

if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()
