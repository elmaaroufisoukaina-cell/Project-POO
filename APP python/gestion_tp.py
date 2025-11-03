import sqlite3
from tkinter import *
import os

# Obtenir le chemin du dossier où se trouve le script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration de la fenêtre principale
main = Tk()
main.title("gestion des TP")
main.geometry("1000x600")
main.configure(bg="#a3b7c2")

# Connexion à la base de données
DB = sqlite3.connect(os.path.join(BASE_DIR, "gestion_des_TP.db"))

# Création des tables
DB.execute("create table if not exists Prof (teacher_id integer, nom text, email text, module text)")
DB.execute("create table if not exists TP (id integer, nom text, teacher_id text, module text, Date_remise text)")
DB.execute("create table if not exists Etudiant (id integer, nom text, teacher_id text, Tp_id integer, Note integer)")

DB.row_factory = sqlite3.Row 
DB.commit()

# Image de fond
try:
    bg_image = PhotoImage(file=os.path.join(BASE_DIR, "PNG_POO", "image.png"))
    bg_label = Label(main, image=bg_image, bg='#a3b7c2')
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

# ==================== CHARGEMENT DES ICÔNES ====================
icons = {}

def load_icons():
    """Charge toutes les icônes nécessaires pour les boutons"""
    icon_names = {
        'ajouter': 'ajouter.png',
        'afficher': 'afficher.png',
        'supprimer': 'supprimer.png',
        'aide': 'aide.png',
        'fermer': 'fermer.png',
        'main': 'gestion_des_tps.png',
        'prof': 'prof.png',
        'tp': 'Tps.png',
        'etudiant': 'etudiant.png'
    }
    
    for name, filename in icon_names.items():
        try:
            icon_path = os.path.join(BASE_DIR, "icons_resized", filename)
            icons[name] = PhotoImage(file=icon_path)
        except:
            icons[name] = None
            print(f"Impossible de charger l'icône: {name}")

# Charger les icônes au démarrage
load_icons()

try: 
    main.iconphoto(False, icons['main'])
except: 
    pass

# ==================== FENÊTRE PROFESSEURS ====================
def Prof_window():
    window1 = Toplevel(main)
    window1.title("Espaces Profs.")
    window1.geometry("1000x600")
    window1.configure(bg="#e3eef4")
    try: window1.iconphoto(False, icons['prof'])
    except: pass

    main_frame = Frame(window1, bg="#e3eef4")
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    top_frame = Frame(main_frame, bg="#e3eef4")
    top_frame.pack(fill=Y, expand=True, pady=(0, 10))

    text_box = Text(top_frame, height=15, width=80)
    text_box.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

    right_buttons_frame = Frame(top_frame, bg="#e3eef4")
    right_buttons_frame.pack(side=RIGHT, anchor=N, pady=10)
    
    def Afficher_Prof():
        text_box.delete("1.0", END)
        cursor = DB.execute("select * from Prof") 
        text_box.insert(END, "teacher_id   | Nom           | Email              | Module\n")
        text_box.insert(END, "-"*60 + "\n") 
        for row in cursor:
            text_box.insert(END, f"{str(row[0]).ljust(12)}|{row[1].ljust(15)}|{row[2].ljust(20)}|{row[3].ljust(15)}\n")

    bottom_frame = Frame(main_frame, bg="#e3eef4")
    bottom_frame.pack(fill=X)

    footer_frame = Frame(main_frame, height=40, bg="#e3eef4")
    footer_frame.pack(side=BOTTOM, fill=X, pady=(10, 0))

    left_frame = Frame(bottom_frame, bg="#e3eef4")
    left_frame.pack(side=LEFT, anchor=W, padx=(300, 0))

    center_frame = Frame(bottom_frame, bg="#e3eef4")
    center_frame.pack(side=RIGHT, anchor=E, padx=(0, 400))

    Button(left_frame, text="Afficher les profs", image=icons['afficher'], compound=LEFT, 
           command=Afficher_Prof, anchor="w").pack(pady=5, fill=X, padx=10)

    Label(center_frame, text="Teacher ID:", bg="#e3eef4").pack(anchor=W, pady=2)
    teacher_id_var = StringVar()
    Entry(center_frame, textvariable=teacher_id_var, width=55).pack(pady=2)

    Label(center_frame, text="Nom:", bg="#e3eef4").pack(anchor=W, pady=2)
    nom_var = StringVar()
    Entry(center_frame, textvariable=nom_var, width=55).pack(pady=2)

    Label(center_frame, text="Email:", bg="#e3eef4").pack(anchor=W, pady=2)
    email_var = StringVar()
    Entry(center_frame, textvariable=email_var, width=55).pack(pady=2)

    Label(center_frame, text="Module:", bg="#e3eef4").pack(anchor=W, pady=2)
    module_var = StringVar()
    Entry(center_frame, textvariable=module_var, width=55).pack(pady=2)

    def Ajouter_prof():
        DB.execute("insert into Prof(teacher_id,nom,email,module) values(?,?,?,?)",
                   (int(teacher_id_var.get()), nom_var.get(), email_var.get(), module_var.get()))
        DB.commit()
        teacher_id_var.set("")
        nom_var.set("")
        email_var.set("")
        module_var.set("")
        Afficher_Prof()
    
    Button(left_frame, text="Ajouter Professeur", image=icons['ajouter'], compound=LEFT, 
           command=Ajouter_prof, anchor="w").pack(pady=5, fill=X, padx=10)

    def remove_prof():
        DB.execute("delete from Prof where teacher_id=?", (int(teacher_id_var.get()),))
        DB.commit()
        teacher_id_var.set("")
        nom_var.set("")
        email_var.set("")
        module_var.set("")
        Afficher_Prof()

    Button(left_frame, text="Supprimer Professeur", image=icons['supprimer'], compound=LEFT, 
           command=remove_prof, anchor="w").pack(pady=5, fill=X, padx=10)

    def instructions():
        aide = Toplevel(window1)
        aide.title("Instructions de manipulation")
        aide.geometry("400x300")
        aide.configure(bg="#a3b7c2")
        Label(aide, text="Instructions:\n\n1. Entrez les informations\n2. Cliquez sur Ajouter\n3. Pour supprimer, entrez l'ID",justify=LEFT).pack(pady=20)
        Button(aide, text="Fermer", command=aide.destroy).pack(pady=10)

    Button(right_buttons_frame, text="Aide", image=icons['aide'], compound=LEFT, 
           command=instructions, anchor="w").pack(pady=5, fill=X, padx=10)
    
    Button(right_buttons_frame, text="Fermer", image=icons['fermer'], compound=LEFT, 
           command=window1.destroy, anchor="w").pack(pady=5, fill=X, padx=10)

# ==================== FENÊTRE TP ====================
def TP_window():
    window2 = Toplevel(main)
    window2.title("Espaces TPs.")
    window2.geometry("1000x600")
    window2.configure(bg="#e3eef4")
    try: window2.iconphoto(False, icons['tp'])
    except: pass

    main_frame = Frame(window2, bg="#e3eef4")
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    top_frame = Frame(main_frame, bg="#e3eef4")
    top_frame.pack(fill=Y, expand=True, pady=(0, 10))

    text_box = Text(top_frame, height=15, width=80)
    text_box.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

    right_buttons_frame = Frame(top_frame, bg="#e3eef4")
    right_buttons_frame.pack(side=RIGHT, anchor=N, pady=10)
    
    def Afficher_Tp():
        text_box.delete("1.0", END)
        cursor = DB.execute("select * from Tp") 
        text_box.insert(END, "id          | Nom           | teacher_id    | Module           | Date_remise\n")
        text_box.insert(END, "-"*80 + "\n")
        for row in cursor:
            text_box.insert(END, f"{str(row[0]).ljust(12)}|{row[1].ljust(15)}|{str(row[2]).ljust(15)}|{row[3].ljust(18)}|{row[4].ljust(15)}\n")

    bottom_frame = Frame(main_frame, bg="#e3eef4")
    bottom_frame.pack(fill=X)

    footer_frame = Frame(main_frame, height=40, bg="#e3eef4")
    footer_frame.pack(side=BOTTOM, fill=X, pady=(10, 0))

    left_frame = Frame(bottom_frame, bg="#e3eef4")
    left_frame.pack(side=LEFT, anchor=W, padx=(300, 0))

    center_frame = Frame(bottom_frame, bg="#e3eef4")
    center_frame.pack(side=RIGHT, anchor=E, padx=(0, 400))

    Button(left_frame, text="Afficher les TP", image=icons['afficher'], compound=LEFT, 
           command=Afficher_Tp, anchor="w").pack(pady=5, fill=X, padx=10)
    
    Label(center_frame, text="ID:", bg="#e3eef4").pack(anchor=W, pady=2)
    id_var = StringVar()
    Entry(center_frame, textvariable=id_var, width=55).pack(pady=2)

    Label(center_frame, text="Nom:", bg="#e3eef4").pack(anchor=W, pady=2)
    nom_var = StringVar()
    Entry(center_frame, textvariable=nom_var, width=55).pack(pady=2)

    Label(center_frame, text="Teacher ID:", bg="#e3eef4").pack(anchor=W, pady=2)
    teacher_id_var = StringVar()
    Entry(center_frame, textvariable=teacher_id_var, width=55).pack(pady=2)

    Label(center_frame, text="Module:", bg="#e3eef4").pack(anchor=W, pady=2)
    module_var = StringVar()
    Entry(center_frame, textvariable=module_var, width=55).pack(pady=2)

    Label(center_frame, text="Date de remise:", bg="#e3eef4").pack(anchor=W, pady=2)
    Date_remise_var = StringVar()
    Entry(center_frame, textvariable=Date_remise_var, width=55).pack(pady=2)

    def Ajouter_Tp():
        DB.execute("insert into Tp(id,nom,teacher_id,module,Date_remise) values(?,?,?,?,?)",
                   (int(id_var.get()), nom_var.get(), int(teacher_id_var.get()), module_var.get(), Date_remise_var.get()))
        DB.commit()
        id_var.set("")
        nom_var.set("")
        teacher_id_var.set("")
        module_var.set("")
        Date_remise_var.set("")
        Afficher_Tp()

    Button(left_frame, text="Ajouter un TP", image=icons['ajouter'], compound=LEFT, 
           command=Ajouter_Tp, anchor="w").pack(pady=5, fill=X, padx=10)

    def remove_Tp():
        DB.execute("delete from Tp where id=?", (int(id_var.get()),))
        DB.commit()
        id_var.set("")
        nom_var.set("")
        teacher_id_var.set("")
        module_var.set("")
        Date_remise_var.set("")
        Afficher_Tp()

    Button(left_frame, text="Supprimer un TP", image=icons['supprimer'], compound=LEFT, 
           command=remove_Tp, anchor="w").pack(pady=5, fill=X, padx=10)
    
    def instructions():
        aide = Toplevel(window2)
        aide.title("Instructions")
        aide.geometry("400x300")
        aide.configure(bg="#a3b7c2")
        Label(aide, text="Instructions:\n\n1. Remplissez les champs\n2. Cliquez sur Ajouter ou Supprimer",justify=LEFT).pack(pady=20)
        Button(aide, text="Fermer", command=aide.destroy).pack(pady=10)

    Button(right_buttons_frame, text="Aide", image=icons['aide'], compound=LEFT, 
           command=instructions, anchor="w").pack(pady=5, fill=X, padx=10)
    
    Button(right_buttons_frame, text="Fermer", image=icons['fermer'], compound=LEFT, 
           command=window2.destroy, anchor="w").pack(pady=5, fill=X, padx=10)

# ==================== FENÊTRE ÉTUDIANTS ====================
def Etudiant_window():
    window3 = Toplevel(main)
    window3.title("Espaces Etudiants.")
    window3.geometry("1000x600")
    window3.configure(bg="#e3eef4")
    try: window3.iconphoto(False, icons['etudiant'])
    except: pass

    main_frame = Frame(window3, bg="#e3eef4")
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    top_frame = Frame(main_frame, bg="#e3eef4")
    top_frame.pack(fill=Y, expand=True, pady=(0, 10))

    text_box = Text(top_frame, height=15, width=80)
    text_box.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

    right_buttons_frame = Frame(top_frame, bg="#e3eef4")
    right_buttons_frame.pack(side=RIGHT, anchor=N, pady=10)
    
    def Afficher_Etudiant():
        text_box.delete("1.0", END)
        cursor = DB.execute("select * from Etudiant") 
        text_box.insert(END, "id          | Nom           | teacher_id    | Tp_id        | Note\n")
        text_box.insert(END, "-"*70 + "\n")
        for row in cursor:
            text_box.insert(END, f"{str(row[0]).ljust(12)}|{row[1].ljust(15)}|{str(row[2]).ljust(15)}|{str(row[3]).ljust(12)}|{str(row[4]).ljust(5)}\n")

    bottom_frame = Frame(main_frame, bg="#e3eef4")
    bottom_frame.pack(fill=X)

    footer_frame = Frame(main_frame, height=40, bg="#e3eef4")
    footer_frame.pack(side=BOTTOM, fill=X, pady=(10, 0))

    left_frame = Frame(bottom_frame, bg="#e3eef4")
    left_frame.pack(side=LEFT, anchor=W, padx=(300, 0))

    center_frame = Frame(bottom_frame, bg="#e3eef4")
    center_frame.pack(side=RIGHT, anchor=E, padx=(0, 400))

    Button(left_frame, text="Afficher les Etudiants", image=icons['afficher'], compound=LEFT, 
           command=Afficher_Etudiant, anchor="w").pack(pady=5, fill=X, padx=10)
    
    Label(center_frame, text="ID:", bg="#e3eef4").pack(anchor=W, pady=2)
    id_var = StringVar()
    Entry(center_frame, textvariable=id_var, width=55).pack(pady=2)

    Label(center_frame, text="Nom:", bg="#e3eef4").pack(anchor=W, pady=2)
    nom_var = StringVar()
    Entry(center_frame, textvariable=nom_var, width=55).pack(pady=2)

    Label(center_frame, text="Teacher ID:", bg="#e3eef4").pack(anchor=W, pady=2)
    teacher_id_var = StringVar()
    Entry(center_frame, textvariable=teacher_id_var, width=55).pack(pady=2)

    Label(center_frame, text="TP ID:", bg="#e3eef4").pack(anchor=W, pady=2)
    Tp_id_var = StringVar()
    Entry(center_frame, textvariable=Tp_id_var, width=55).pack(pady=2)

    Label(center_frame, text="Note:", bg="#e3eef4").pack(anchor=W, pady=2)
    Note_var = StringVar()
    Entry(center_frame, textvariable=Note_var, width=55).pack(pady=2)

    def Ajouter_Etudiant():
        DB.execute("insert into Etudiant(id,nom,teacher_id,Tp_id,Note) values(?,?,?,?,?)",
                   (int(id_var.get()), nom_var.get(), int(teacher_id_var.get()), Tp_id_var.get(), int(Note_var.get())))
        DB.commit()
        id_var.set("")
        nom_var.set("")
        teacher_id_var.set("")
        Tp_id_var.set("")
        Note_var.set("")
        Afficher_Etudiant()

    Button(left_frame, text="Ajouter un Etudiant", image=icons['ajouter'], compound=LEFT, 
           command=Ajouter_Etudiant, anchor="w").pack(pady=5, fill=X, padx=10)

    def remove_Etudiant():
        DB.execute("DELETE FROM Etudiant WHERE Tp_id=?", (int(Tp_id_var.get()),))
        DB.commit()
        id_var.set("")
        nom_var.set("")
        teacher_id_var.set("")
        Tp_id_var.set("")
        Note_var.set("")
        Afficher_Etudiant()

    Button(left_frame, text="Supprimer un Etudiant", image=icons['supprimer'], compound=LEFT, 
           command=remove_Etudiant, anchor="w").pack(pady=5, fill=X, padx=10)

    def instructions():
        aide = Toplevel(window3)
        aide.title("Instructions")
        aide.geometry("400x300")
        aide.configure(bg="#a3b7c2")
        Label(aide, text="Instructions:\n\n1. Remplissez les champs\n2. Cliquez sur Ajouter ou Supprimer",justify=LEFT).pack(pady=20)
        Button(aide, text="Fermer", command=aide.destroy).pack(pady=10)

    Button(right_buttons_frame, text="Aide", image=icons['aide'], compound=LEFT, 
           command=instructions, anchor="w").pack(pady=5, fill=X, padx=10)
    
    Button(right_buttons_frame, text="Fermer", image=icons['fermer'], compound=LEFT, 
           command=window3.destroy, anchor="w").pack(pady=5, fill=X, padx=10)

# ==================== BOUTONS PRINCIPAUX ====================
btn_prof = Button(main, text="Professeurs", width=20, command=Prof_window)
btn_TP = Button(main, text="TP", width=20, command=TP_window)
btn_Etudiant = Button(main, text="Etudiants", width=20, command=Etudiant_window)

btn_prof.place(relx=0.7, rely=0.72, anchor=CENTER)
btn_TP.place(relx=0.5, rely=0.72, anchor=CENTER)
btn_Etudiant.place(relx=0.3, rely=0.72, anchor=CENTER)

main.mainloop()
DB.close()