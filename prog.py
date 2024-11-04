import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def criar_banco():
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT NOT NULL,
        endereco TEXT NOT NULL,
        notas TEXT
    )
    ''')
    conn.commit()
    conn.close()

def cadastrar_aluno():
    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    endereco = entry_endereco.get()

    if not nome or not data_nascimento or not endereco:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alunos (nome, data_nascimento, endereco, notas) VALUES (?, ?, ?, ?)",
                   (nome, data_nascimento, endereco, ""))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_data_nascimento.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    listar_alunos()  # Atualiza a lista de alunos após o cadastro

def cadastrar_nota():
    aluno_id = entry_aluno_id.get()
    disciplina = entry_disciplina.get()
    nota = entry_nota.get()

    if not aluno_id or not disciplina or not nota:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("SELECT notas FROM alunos WHERE id = ?", (aluno_id,))
    result = cursor.fetchone()

    if result:
        notas = result[0]
        notas = notas + f", {disciplina}: {nota}" if notas else f"{disciplina}: {nota}"
        cursor.execute("UPDATE alunos SET notas = ? WHERE id = ?", (notas, aluno_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Nota cadastrada com sucesso!")
    else:
        messagebox.showerror("Erro", "ID do aluno não encontrado.")

    conn.close()
    entry_aluno_id.delete(0, tk.END)
    entry_disciplina.delete(0, tk.END)
    entry_nota.delete(0, tk.END)
    listar_notas()  # Atualiza a lista de notas após o cadastro

def listar_alunos():
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, data_nascimento, endereco FROM alunos")
    alunos = cursor.fetchall()
    conn.close()

    lista_alunos.delete(0, tk.END)
    for aluno in alunos:
        lista_alunos.insert(tk.END, f"ID: {aluno[0]} | Nome: {aluno[1]} | Data: {aluno[2]} | Endereço: {aluno[3]}")

def listar_notas():
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, notas FROM alunos")
    notas = cursor.fetchall()
    conn.close()

    lista_notas.delete(0, tk.END)
    for nota in notas:
        lista_notas.insert(tk.END, f"ID: {nota[0]} | Notas: {nota[1]}")

def remover_aluno():
    aluno_id = entry_remover_id.get()

    if not aluno_id:
        messagebox.showerror("Erro", "Preencha o ID do aluno.")
        return

    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
    entry_remover_id.delete(0, tk.END)
    listar_alunos()

def editar_aluno():
    try:
        aluno_selecionado = lista_alunos.curselection()[0]
        aluno_info = lista_alunos.get(aluno_selecionado).split('|')
        aluno_id = aluno_info[0].split(':')[1].strip()

        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
        aluno = cursor.fetchone()
        conn.close()

        if aluno:
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, aluno[1])
            entry_data_nascimento.delete(0, tk.END)
            entry_data_nascimento.insert(0, aluno[2])
            entry_endereco.delete(0, tk.END)
            entry_endereco.insert(0, aluno[3])
            messagebox.showinfo("Edição", "Preencha os campos e clique em 'Cadastrar Aluno' para atualizar.")
            return aluno_id
    except IndexError:
        messagebox.showerror("Erro", "Selecione um aluno da lista para editar.")

def salvar_edicao(aluno_id):
    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    endereco = entry_endereco.get()

    if not nome or not data_nascimento or not endereco:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE alunos SET nome = ?, data_nascimento = ?, endereco = ? WHERE id = ?",
                   (nome, data_nascimento, endereco, aluno_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_data_nascimento.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    listar_alunos()  # Atualiza a lista de alunos após a edição

def editar_nota():
    try:
        nota_selecionada = lista_notas.curselection()[0]
        nota_info = lista_notas.get(nota_selecionada).split('|')
        aluno_id = nota_info[0].split(':')[1].strip()

        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()
        cursor.execute("SELECT notas FROM alunos WHERE id = ?", (aluno_id,))
        notas = cursor.fetchone()[0]
        conn.close()

        entry_aluno_id.delete(0, tk.END)
        entry_aluno_id.insert(0, aluno_id)
        entry_disciplina.delete(0, tk.END)
        entry_disciplina.insert(0, notas.split(':')[0])  # Assume que a primeira nota é a que será editada
        entry_nota.delete(0, tk.END)
        entry_nota.insert(0, notas.split(':')[1].strip())
        
        messagebox.showinfo("Edição", "Edite a disciplina e a nota e clique em 'Cadastrar Nota' para atualizar.")
    except IndexError:
        messagebox.showerror("Erro", "Selecione uma nota da lista para editar.")

def salvar_edicao_nota(aluno_id):
    disciplina = entry_disciplina.get()
    nota = entry_nota.get()

    if not disciplina or not nota:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("SELECT notas FROM alunos WHERE id = ?", (aluno_id,))
    notas_atual = cursor.fetchone()[0]

    if notas_atual:
        notas = notas_atual.split(',')
        for i, n in enumerate(notas):
            if disciplina in n:
                notas[i] = f"{disciplina}: {nota}"
                break
        notas_atualizado = ', '.join(notas)
        cursor.execute("UPDATE alunos SET notas = ? WHERE id = ?", (notas_atualizado, aluno_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Nota atualizada com sucesso!")
    else:
        messagebox.showerror("Erro", "Nenhuma nota encontrada para atualizar.")

    conn.close()
    entry_aluno_id.delete(0, tk.END)
    entry_disciplina.delete(0, tk.END)
    entry_nota.delete(0, tk.END)
    listar_notas()  # Atualiza a lista de notas após a edição

def buscar_alunos():
    termo = entry_busca_aluno.get().strip().lower()
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, data_nascimento, endereco FROM alunos")
    alunos = cursor.fetchall()
    conn.close()

    lista_alunos.delete(0, tk.END)
    for aluno in alunos:
        if termo in aluno[1].lower():  # Busca pelo nome do aluno
            lista_alunos.insert(tk.END, f"ID: {aluno[0]} | Nome: {aluno[1]} | Data: {aluno[2]} | Endereço: {aluno[3]}")

def buscar_notas():
    termo = entry_busca_nota.get().strip().lower()
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, notas FROM alunos")
    notas = cursor.fetchall()
    conn.close()

    lista_notas.delete(0, tk.END)
    for nota in notas:
        if termo in nota[1].lower():  # Busca nas notas
            lista_notas.insert(tk.END, f"ID: {nota[0]} | Notas: {nota[1]}")

# Configuração da aplicação
app = tk.Tk()
app.title("Sistema de Cadastro de Alunos")
app.geometry("520x600")  # Tamanho fixo da janela
app.resizable(False, False)  # Desativar redimensionamento
app.configure(bg="#eaeaea")

# Frame principal com scroll
main_frame = ttk.Frame(app)
main_frame.pack(fill=tk.BOTH, expand=True)

# Scrollbar
canvas = tk.Canvas(main_frame, bg="#eaeaea")
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Widgets para cadastro de alunos
label_nome = ttk.Label(scrollable_frame, text="Nome:")
label_nome.grid(row=0, column=0, padx=10, pady=5)
entry_nome = ttk.Entry(scrollable_frame)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

label_data_nascimento = ttk.Label(scrollable_frame, text="Data de Nascimento:")
label_data_nascimento.grid(row=1, column=0, padx=10, pady=5)
entry_data_nascimento = ttk.Entry(scrollable_frame)
entry_data_nascimento.grid(row=1, column=1, padx=10, pady=5)

label_endereco = ttk.Label(scrollable_frame, text="Endereço:")
label_endereco.grid(row=2, column=0, padx=10, pady=5)
entry_endereco = ttk.Entry(scrollable_frame)
entry_endereco.grid(row=2, column=1, padx=10, pady=5)

botao_cadastrar_aluno = ttk.Button(scrollable_frame, text="Cadastrar Aluno", command=cadastrar_aluno)
botao_cadastrar_aluno.grid(row=3, columnspan=2, padx=10, pady=10)

# Widgets para busca de alunos
label_busca_aluno = ttk.Label(scrollable_frame, text="Buscar Aluno:")
label_busca_aluno.grid(row=4, column=0, padx=10, pady=5)
entry_busca_aluno = ttk.Entry(scrollable_frame)
entry_busca_aluno.grid(row=4, column=1, padx=10, pady=5)

botao_buscar_aluno = ttk.Button(scrollable_frame, text="Buscar", command=buscar_alunos)
botao_buscar_aluno.grid(row=5, columnspan=2, padx=10, pady=10)

# Lista de alunos
lista_alunos = tk.Listbox(scrollable_frame, width=80)
lista_alunos.grid(row=6, columnspan=2, padx=10, pady=10)
listar_alunos()

# Widgets para cadastro de notas
label_aluno_id = ttk.Label(scrollable_frame, text="ID do Aluno:")
label_aluno_id.grid(row=7, column=0, padx=10, pady=5)
entry_aluno_id = ttk.Entry(scrollable_frame)
entry_aluno_id.grid(row=7, column=1, padx=10, pady=5)

label_disciplina = ttk.Label(scrollable_frame, text="Disciplina:")
label_disciplina.grid(row=8, column=0, padx=10, pady=5)
entry_disciplina = ttk.Entry(scrollable_frame)
entry_disciplina.grid(row=8, column=1, padx=10, pady=5)

label_nota = ttk.Label(scrollable_frame, text="Nota:")
label_nota.grid(row=9, column=0, padx=10, pady=5)
entry_nota = ttk.Entry(scrollable_frame)
entry_nota.grid(row=9, column=1, padx=10, pady=5)

botao_cadastrar_nota = ttk.Button(scrollable_frame, text="Cadastrar Nota", command=cadastrar_nota)
botao_cadastrar_nota.grid(row=10, columnspan=2, padx=10, pady=10)

# Widgets para busca de notas
label_busca_nota = ttk.Label(scrollable_frame, text="Buscar Nota:")
label_busca_nota.grid(row=11, column=0, padx=10, pady=5)
entry_busca_nota = ttk.Entry(scrollable_frame)
entry_busca_nota.grid(row=11, column=1, padx=10, pady=5)

botao_buscar_nota = ttk.Button(scrollable_frame, text="Buscar", command=buscar_notas)
botao_buscar_nota.grid(row=12, columnspan=2, padx=10, pady=10)

# Lista de notas
lista_notas = tk.Listbox(scrollable_frame, width=80)
lista_notas.grid(row=13, columnspan=2, padx=10, pady=10)
listar_notas()

# Remover aluno
label_remover_id = ttk.Label(scrollable_frame, text="ID do Aluno para Remover:")
label_remover_id.grid(row=14, column=0, padx=10, pady=5)
entry_remover_id = ttk.Entry(scrollable_frame)
entry_remover_id.grid(row=14, column=1, padx=10, pady=5)

botao_remover_aluno = ttk.Button(scrollable_frame, text="Remover Aluno", command=remover_aluno)
botao_remover_aluno.grid(row=15, columnspan=2, padx=10, pady=10)

# Botão de edição de aluno
botao_editar_aluno = ttk.Button(scrollable_frame, text="Editar Aluno", command=lambda: salvar_edicao(editar_aluno()))
botao_editar_aluno.grid(row=16, columnspan=2, padx=10, pady=10)

# Botão de edição de nota
botao_editar_nota = ttk.Button(scrollable_frame, text="Editar Nota", command=lambda: salvar_edicao_nota(entry_aluno_id.get()))
botao_editar_nota.grid(row=17, columnspan=2, padx=10, pady=10)

# Criação do banco de dados
criar_banco()
app.mainloop()

