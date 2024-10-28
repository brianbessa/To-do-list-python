import tkinter as tk
from tkinter import simpledialog, messagebox

tarefas = []

def carregar_tarefas():
    try:
        with open("tarefas.txt", "r") as file:
            return [linha.strip() for linha in file.readlines()]
    except FileNotFoundError:
        return []

def salvar_tarefas():
    with open("tarefas.txt", "w") as file:
        for tarefa in tarefas:
            file.write(f"{tarefa}\n")

tarefas = carregar_tarefas()

def adicionar_tarefas():
    dialogo = tk.Toplevel()
    dialogo.title("Adicionar Tarefa")
    dialogo.geometry("200x180")
    dialogo.resizable(False, False)

    label_tarefa = tk.Label(dialogo, text="Digite a tarefa: ")
    label_tarefa.pack(pady=(10, 5), padx=10, anchor='w')

    frame_entrada = tk.Frame(dialogo)
    frame_entrada.pack(pady=5)

    entrada_tarefa = tk.Entry(frame_entrada, width=27) 
    entrada_tarefa.pack()

    var_horario = tk.BooleanVar()

    def toggle_horario():
        if var_horario.get():
            spinbox_horas.config(state="normal")
            spinbox_minutos.config(state="normal")
        else:
            spinbox_horas.config(state="disabled")
            spinbox_minutos.config(state="disabled")
            spinbox_minutos.delete(0, 'end')
            spinbox_minutos.insert(0, 0)
            spinbox_horas.delete(0, 'end')
            spinbox_horas.insert(0, 0)

    check_horario = tk.Checkbutton(dialogo, text="Adicionar Horário", variable=var_horario, command=toggle_horario)
    check_horario.pack(pady=5)

    frame_horario = tk.Frame(dialogo)
    frame_horario.pack(pady=5)

    spinbox_horas = tk.Spinbox(frame_horario, from_=0, to=23, width=5, format="%02.0f", state='disabled')
    spinbox_horas.pack(side=tk.LEFT, padx=(0, 5))

    spinbox_minutos = tk.Spinbox(frame_horario, from_=0, to=59, width=5, format="%02.0f", state='disabled')
    spinbox_minutos.pack(side=tk.LEFT, padx=(5, 0))

    def validar_minutos():
        minutos = int(spinbox_minutos.get())
        horas = int(spinbox_horas.get())
        if minutos == 0:  
            spinbox_minutos.delete(0, 'end')
            spinbox_minutos.insert(0, 59)
            if horas > 0:
                spinbox_horas.delete(0, 'end')
                spinbox_horas.insert(0, horas - 1)
        elif minutos == 59:  
            spinbox_minutos.delete(0, 'end')
            spinbox_minutos.insert(0, 0)
            if horas < 23:
                spinbox_horas.delete(0, 'end')
                spinbox_horas.insert(0, horas + 1)

    def validar_horas():
        horas = int(spinbox_horas.get())
        if horas == 0:  
            spinbox_horas.delete(0, 'end')
            spinbox_horas.insert(0, 23)
        elif horas == 23:  
            spinbox_horas.delete(0, 'end')
            spinbox_horas.insert(0, 0)

    spinbox_minutos.bind("<Button-1>", lambda event: validar_minutos())
    spinbox_horas.bind("<Button-1>", lambda event: validar_horas())

    def confirmar():
        tarefa = entrada_tarefa.get()
        if tarefa:
            if var_horario.get():
                horas = spinbox_horas.get()
                minutos = spinbox_minutos.get()
                horario = f"{horas}:{minutos}"
                tarefas.append(f"{tarefa} ({horario})")
            else:
                tarefas.append(tarefa)
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            salvar_tarefas()
            dialogo.destroy()

    botao_confirmar = tk.Button(dialogo, text="Confirmar", command=confirmar)
    botao_confirmar.pack(pady=5)

def mostrar_tarefa():
    if tarefas:
        tarefas_str = "\n".join(tarefas)
        messagebox.showinfo("Lista de tarefas", tarefas_str)
    else:
        messagebox.showinfo("Lista de tarefas", "Nenhuma tarefa encontrada.")

def remover_tarefa():
    dialogo = tk.Toplevel()
    dialogo.title("Remover Tarefa")

    # Frame principal e canvas para a rolagem
    frame_principal = tk.Frame(dialogo)
    frame_principal.pack()

    canvas = tk.Canvas(frame_principal)
    scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas)

    # Configurar o canvas e scrollbar
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    var_checks = []

    for tarefa in tarefas:
        var = tk.BooleanVar()
        var_checks.append(var)
        checkbutton = tk.Checkbutton(frame, text=tarefa, variable=var)
        checkbutton.pack(anchor='w')

    def confirmar_remocao():    
        for i in reversed(range(len(var_checks))):
            if var_checks[i].get():
                tarefas.pop(i)
        messagebox.showinfo("Sucesso", "Tarefa(s) removida com sucesso!")
        salvar_tarefas()
        dialogo.destroy()

    botao_confirmar = tk.Button(dialogo, text="Confirmar", command=confirmar_remocao)
    botao_confirmar.pack(pady=5)

janela = tk.Tk()
janela.title("Todo List")
janela.geometry("200x280")

# Impede o redimensionamento da janela
janela.resizable(False, False)

botao_adicionar = tk.Button(
    janela, 
    text="Adicionar Tarefa", 
    command=adicionar_tarefas, 
    width=(25), 
    height=(5)
)

botao_adicionar.pack(pady=5)

botao_exibir = tk.Button(
    janela,
    text="Exibir Lista",
    command=mostrar_tarefa,
    width=(25),
    height=(5)
)

botao_exibir.pack(pady=5)

botao_remover = tk.Button(
    janela,
    text="Remover Tarefa",
    command=remover_tarefa,
    width=(25),
    height=(5)
)

botao_remover.pack(pady=5)

janela.mainloop()
