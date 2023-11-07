# -*- coding: utf-8 -*-
import tkSimpleDialog
import arcpy
import Tkinter as tk
import tkFileDialog as filedialog
import ttk
import tkMessageBox



def digitaliser_couche_vectorielle(geo_dataset, nom_couche, type_geom):
    arcpy.CreateFeatureclass_management(geo_dataset, nom_couche, type_geom)


def ajouter_colonne_couche(geo_dataset, nom_couche, nom_colonne):
    arcpy.AddField_management(geo_dataset + "/" + nom_couche, nom_colonne)




def afficher_couche(giodataset, couche_selectionnee):
    # Obtenir les noms des attributs de la couche
    attributs = [field.name for field in arcpy.ListFields(couche_selectionnee)]

    # Obtenir les valeurs des attributs pour chaque enregistrement
    valeurs_attributs = []
    with arcpy.da.SearchCursor(couche_selectionnee, '*') as curseur:
        for row in curseur:
            valeurs_attributs.append(row)

    # Créer la fenêtre principale Tkinter
    fenetre=tk.Tk()
    fenetre.title("La Couche " + str(couche_selectionnee).upper())
    fenetre.geometry("800x600")  # Définir la taille de la fenêtre

    # Créer le tableau
    tableau = ttk.Treeview(fenetre, columns=attributs, show="headings")

    # Ajouter les colonnes au tableau
    for attribut in attributs:
        tableau.heading(attribut, text=attribut)
        tableau.column(attribut, width=100)

    # Ajouter les enregistrements au tableau
    for valeur_attribut in valeurs_attributs:
        tableau.insert("", tk.END, values=valeur_attribut)

    # Bouton d'ajout de ligne
    bouton1 = tk.Button(fenetre, text="Ajouter une ligne", command=lambda: ajouter_ligne(couche_selectionnee, fenetre))
    bouton1.grid(row=0, column=0, padx=5, pady=5)

    # Bouton de suppression de colonne
    bouton2 = tk.Button(fenetre, text="Supprimer une Ligne", command=lambda: supprimer_colonne(fenetre, tableau, couche_selectionnee))
    bouton2.grid(row=0, column=1, padx=5, pady=5)

    # Bouton d'ajout de colonne
    bouton3 = tk.Button(fenetre, text="Ajouter une colonne", command=lambda: add_field(couche_selectionnee, fenetre))
    bouton3.grid(row=0, column=2, padx=5, pady=5)

    # Bouton de suppression de colonne
    bouton4 = tk.Button(fenetre, text="Supprimer une colonne", command=lambda: delete_columns(giodataset, couche_selectionnee, fenetre))
    bouton4.grid(row=0, column=3, padx=5, pady=5)

    # Bouton pour supprimer une ligne par son indice
    bouton5 = tk.Button(fenetre, text="Supprimer une ligne par indice", command=lambda: delete_rows_by_indice(giodataset, couche_selectionnee, fenetre))
    bouton5.grid(row=1, column=0, padx=5, pady=5)

    # Bouton pour mettre à jour les valeurs de colonne
    bouton6 = tk.Button(fenetre, text="Mettre à jour les valeurs de colonne", command=lambda: update_column_values(giodataset, couche_selectionnee))
    bouton6.grid(row=1, column=1, padx=5, pady=5)

    bouton7 = tk.Button(fenetre, text="somme_champ", command=lambda: somme_champ(couche_selectionnee, champ_entry, table_frame, text_box))
    bouton7.grid(row=1, column=2, padx=5, pady=5)

    bouton8 = tk.Button(fenetre, text="maximum", command=lambda: maximum(couche_selectionnee, champ_entry, table_frame, text_box))
    bouton8.grid(row=1, column=3, padx=5, pady=5)

    bouton9 = tk.Button(fenetre, text="minimum", command=lambda: minimum(couche_selectionnee, champ_entry, table_frame, text_box))
    bouton9.grid(row=2, column=0, padx=5, pady=5)

    bouton10 = tk.Button(fenetre, text="nombre d'enregistrement", command=lambda: nbre_enreg(couche_selectionnee, champ_entry, table_frame, text_box))
    bouton10.grid(row=2, column=1, padx=5, pady=5)

    bouton11 = tk.Button(fenetre, text="moyenne", command=lambda: moyenne(couche_selectionnee, champ_entry, table_frame, text_box))
    bouton11.grid(row=2, column=2, padx=5, pady=5)

    # Afficher le tableau
    tableau.grid(row=3, column=0, columnspan=4, padx=5, pady=10)

    champ_label = tk.Label(fenetre, text="Nom de champ :")
    champ_label.grid(row=4, column=0, padx=5, pady=5)

    champ_entry = tk.Entry(fenetre)
    champ_entry.grid(row=4, column=1, padx=5, pady=5)

    table_frame = tk.Frame(fenetre)
    table_frame.grid(row=5, column=0, columnspan=4, padx=5, pady=10)

    text_box = tk.Text(fenetre)
    text_box.grid(row=6, column=0, columnspan=4, padx=5, pady=10)

    fenetre.mainloop()
def supprimer_colonne(fenetre,tableau,couche_selectionnee):
    # Créer une nouvelle fenêtre pop-up pour la suppression de colonne
    fenetre_suppression = tk.Toplevel(fenetre)
    fenetre_suppression.title("Supprimer une colonne")

    def supprimer_colonne_selectionnee(tableau,couche_selectionnee):
        colonne_selectionnee = tableau.selection()[0]  # Sélectionner la colonne dans le tableau
        nom_colonne = tableau.item(colonne_selectionnee)['values'][0]  # Obtenir le nom de la colonne sélectionnée

        # Supprimer la colonne de la classe d'entités
        arcpy.DeleteField_management(couche_selectionnee, nom_colonne)

        # Rafraîchir le tableau
        tableau.delete(colonne_selectionnee)

        # Fermer la fenêtre de suppression
        fenetre_suppression.destroy()

    # Bouton de suppression de colonne
    bouton_supprimer = tk.Button(fenetre_suppression, text="Supprimer", command=lambda:supprimer_colonne_selectionnee(tableau, couche_selectionnee))
    bouton_supprimer.pack()


def ajouter_ligne(fc_name,fenetre):
    if fc_name:
        fields = arcpy.ListFields(fc_name)
        field_names = [field.name for field in fields]
        row_values = []
        # Demande les valeurs des champs pour la nouvelle ligne à ajouter
        for field in fields:
            value = tkSimpleDialog.askstring("Ajouter des lignes", "Valeur pour le champ {}:".format(field.name))
            if field.type == "Integer":
                row_values.append(int(value))
            elif field.type == "Double":
                row_values.append(float(value))
            else:
                row_values.append(value)
        with arcpy.da.InsertCursor(fc_name, field_names) as cursor:
            cursor.insertRow(row_values)
        tkMessageBox.showinfo("Ajouter des lignes", "La ligne a été ajoutée avec succès.")
    else:
        tkMessageBox.showwarning("Ajouter des lignes", "Le nom de la classe d'entités est manquant.")
    fenetre.update()

    # Mettre à jour les tâches en attente de l'interface
    fenetre.update_idletasks()

def add_field(fc,fenetre):
    if fc:
        field_name = tkSimpleDialog.askstring("Ajouter un champ", "Nom du nouveau champ :")
        if field_name:
            field_type = tkSimpleDialog.askstring("Ajouter un champ", "Type de donnée (TEXT, INTEGER, FLOAT, etc.) :")
            if field_type:
                try:
                    arcpy.AddField_management(fc, field_name, field_type)
                    tkMessageBox.showinfo("Ajouter un champ", "Le champ a été ajouté avec succès.")
                except Exception as e:
                    tkMessageBox.showerror("Erreur", "Erreur lors de l'ajout du champ : {}".format(str(e)))

    fenetre.update()

    # Mettre à jour les tâches en attente de l'interface
    fenetre.update_idletasks()

def delete_columns(dataset,fc_name,fenetre):
    # Si l'utilisateur a saisi une dataset et une feature class
    if dataset and fc_name:
        # Chemin complet de la feature class
        fc = dataset + "\\" + fc_name

        # Liste des champs de la feature class
        fields = arcpy.ListFields(fc)

        # Liste des noms de champs
        field_names = [field.name for field in fields]

        # Demande à l'utilisateur de saisir les noms des colonnes à supprimer, séparés par des virgules
        fields_to_delete_str = tkSimpleDialog.askstring("Supprimer des colonnes", "Noms des colonnes à supprimer, séparés par des virgules :")

        # Si l'utilisateur a saisi des noms de colonnes
        if fields_to_delete_str:
            # Sépare les noms de colonnes en une liste
            fields_to_delete = fields_to_delete_str.split(",")

            # Vérifie que toutes les colonnes existent dans la feature class
            for field in fields_to_delete:
                if field.strip() not in field_names:
                    tkMessageBox.showerror("Supprimer des colonnes", "La colonne {} n'existe pas dans la feature class.".format(field.strip()))
                    return

            # Supprime les colonnes
            arcpy.DeleteField_management(fc, fields_to_delete)
            tkMessageBox.showinfo("Supprimer des colonnes", "Les colonnes ont été supprimées avec succès.")
        else:
            tkMessageBox.showerror("Supprimer des colonnes", "Aucun nom de colonne n'a été saisi.")
    fenetre.update()

    # Mettre à jour les tâches en attente de l'interface
    fenetre.update_idletasks()

def delete_rows_by_indice(dataset,fc_name,fenetre):

    # Si l'utilisateur a saisi une dataset et une feature class
    if dataset and fc_name:
        # Chemin complet de la feature class
        fc = dataset + "\\" + fc_name

        # Liste des champs de la feature class
        fields = arcpy.ListFields(fc)

        # Liste des noms de champs
        field_names = [field.name for field in fields]

        # Demande à l'utilisateur de saisir le nom de la colonne contenant les ID des lignes à supprimer
        id_column = tkSimpleDialog.askstring("Supprimer des lignes", "Nom de la colonne contenant les ID des lignes à supprimer :", initialvalue="")

        # Si l'utilisateur a saisi un nom de colonne
        if id_column:
            # Vérifie que la colonne existe dans la feature class
            if id_column in field_names:
                # Demande à l'utilisateur de saisir les ID des lignes à supprimer
                ids = tkSimpleDialog.askstring("Supprimer des lignes", "ID des lignes à supprimer (séparés par des virgules) :", initialvalue="")

                # Si l'utilisateur a saisi des ID
                if ids:
                    # Convertit les ID en une liste
                    id_list = ids.split(",")

                    # Crée une requête pour sélectionner les lignes à supprimer
                    query = "{} IN ({})".format(arcpy.AddFieldDelimiters(fc, id_column), ",".join(id_list))

                    # Utilise un UpdateCursor pour supprimer les lignes sélectionnées
                    with arcpy.da.UpdateCursor(fc, ["*"], query) as cursor:
                        for row in cursor:
                            cursor.deleteRow()

                    tkMessageBox.showinfo("Supprimer des lignes", "{} lignes ont été supprimées avec succès.".format(len(id_list)))
                else:
                    tkMessageBox.showerror("Supprimer des lignes", "Aucun ID n'a été saisi.")
            else:
                tkMessageBox.showerror("Supprimer des lignes", "La colonne n'existe pas dans la feature class.")
        else:
            tkMessageBox.showerror("Supprimer des lignes", "Aucun nom de colonne n'a été saisi.")

    fenetre.update()

    # Mettre à jour les tâches en attente de l'interface
    fenetre.update_idletasks()

def update_column_values(dataset,fc_name):
    # Si l'utilisateur a saisi une dataset et une feature class
    if dataset and fc_name:
        # Chemin complet de la feature class
        fc = dataset + "\\" + fc_name

        # Liste des champs de la feature class
        fields = arcpy.ListFields(fc)

        # Liste des noms de champs
        field_names = [field.name for field in fields]

        # Demande à l'utilisateur de saisir le nom de la colonne à mettre à jour
        column_name = tkSimpleDialog.askstring("Mettre à jour une valeur", "Nom de la colonne désirée :", initialvalue="")

        # Si l'utilisateur a saisi un nom de colonne
        if column_name:
            # Vérifie que la colonne existe dans la feature class
            if column_name in field_names:
                # Demande à l'utilisateur de saisir l'identifiant de la ligne à mettre à jour
                row_id = tkSimpleDialog.askinteger("Mettre à jour une valeur", "Numéro de la ligne :")

                # Si l'utilisateur a saisi un identifiant de ligne
                if row_id:
                    # Utilise un SearchCursor pour récupérer les valeurs des champs pour la ligne spécifiée
                    with arcpy.da.SearchCursor(fc, ["OID@", column_name], "{} = {}".format(arcpy.AddFieldDelimiters(fc, "OBJECTID"), row_id)) as cursor:
                        row = next(cursor, None)
                        # Si la ligne existe, demande à l'utilisateur de saisir la nouvelle valeur pour la colonne
                        if row:
                            new_value = tkSimpleDialog.askstring("Mettre à jour une valeur", "La valeur de la colonne {} pour la ligne {} devient :".format(column_name, row_id), initialvalue=row[1])
                            # Si l'utilisateur a saisi une nouvelle valeur
                            if new_value:
                                # Utilise un UpdateCursor pour mettre à jour la valeur de la colonne pour la ligne spécifiée
                                with arcpy.da.UpdateCursor(fc, [column_name], "{} = {}".format(arcpy.AddFieldDelimiters(fc, "OBJECTID"), row_id)) as cursor:
                                    for row in cursor:
                                        row[0] = new_value
                                        cursor.updateRow(row)

                                tkMessageBox.showinfo("Mettre à jour une valeur", "La valeur de la colonne {} pour la ligne {} a été modifiée.".format(column_name, row_id))
                            else:
                                tkMessageBox.showerror("Mettre à jour une valeur", "Aucune nouvelle valeur n'a été saisie.")
                        else:
                            tkMessageBox.showerror("Mettre à jour une valeur", "La ligne spécifiée n'existe pas dans la feature class.")
                else:
                    tkMessageBox.showerror("Mettre à jour une valeur", "Aucun identifiant de ligne n'a été saisi.")
            else:
                tkMessageBox.showerror("Mettre à jour une valeur", "La colonne n'existe pas dans la feature class.")


def somme_champ(couche_selectionnee,champ_entry,table_frame,text_box):
    table = couche_selectionnee
    champ = champ_entry.get()
    tableauliste = []
    message = ""

    try:
        cursor = arcpy.da.SearchCursor(table, champ)
        # Suppression du contenu précédent
        vider_contenu(table_frame)
        for row in cursor:
            tableauliste.append(int(row[0]))
        contenu = sum(tableauliste)
        contenu_label = tk.Label(table_frame, text=contenu)
        message = "La somme du champ '{}' dans la table '{}' est : {}".format(champ, table, contenu)
        print("\n")
    except Exception as e:
        message = "Erreur lors du calcul de la somme : {}".format(str(e))

    text_box.delete('1.0', tk.END)
    text_box.insert(tk.END, message)

def maximum(couche_selectionnee,champ_entry,table_frame,text_box):
    table = couche_selectionnee
    champ = champ_entry.get()
    tableauliste = []

    try:
        cursor = arcpy.da.SearchCursor(table, champ)
        # Suppression du contenu précédent
        vider_contenu(table_frame)
        for row in cursor:
            tableauliste.append(int(row[0]))
        contenu = max(tableauliste)
        contenu_label = tk.Label(table_frame, text=contenu)
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "Le maximum du champ '{}' dans la table '{}' est : {}\n".format(champ, table, contenu))
    except Exception as e:
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "Erreur lors du calcul du maximum : {}\n".format(str(e)))


def minimum(couche_selectionnee,champ_entry,table_frame,text_box):
    table = couche_selectionnee
    champ = champ_entry.get()
    tableauliste = []

    try:
        cursor = arcpy.da.SearchCursor(table, champ)
        # Suppression du contenu précédent
        vider_contenu(table_frame)
        for row in cursor:
            tableauliste.append(int(row[0]))
        contenu = min(tableauliste)
        contenu_label = tk.Label(table_frame, text=contenu)
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "Le minimum du champ '{}' dans la table '{}' est : {}\n".format(champ, table, contenu))
    except Exception as e:
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "Erreur lors du calcul du minimum : {}\n".format(str(e)))

def nbre_enreg(couche_selectionnee,champ_entry,table_frame,text_box):
    table = couche_selectionnee
    champ = champ_entry.get()
    tableauliste = []

    try:
        cursor = arcpy.da.SearchCursor(table, champ)
        # Suppression du contenu précédent
        vider_contenu(table_frame)
        for row in cursor:
            tableauliste.append(int(row[0]))
        contenu = len(tableauliste)
        contenu_label = tk.Label(table_frame, text=contenu)
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "Le nombre d'enregistrements du champ '{}' dans la table '{}' est : {}\n".format(champ, table, contenu))
    except Exception as e:
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "Erreur lors du calcul du nombre d'enregistrements : {}\n".format(str(e)))

def moyenne(couche_selectionnee,champ_entry,table_frame,text_box):
    table =couche_selectionnee
    champ = champ_entry.get()
    tableauliste = []

    try:
        cursor = arcpy.da.SearchCursor(table, champ)
        # Suppression du contenu précédent
        vider_contenu(table_frame)
        for row in cursor:
            tableauliste.append(int(row[0]))
        contenu = float(sum(tableauliste)) / len(tableauliste)
        contenu_label = tk.Label(table_frame, text=contenu)
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "La moyenne du champ '{}' dans la table '{}' est : {}\n".format(champ, table, contenu))
    except Exception as e:
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, "Erreur lors du calcul de la moyenne : {}\n".format(str(e)))



def vider_contenu(table_frame):
    # Suppression du contenu précédent
    for widget in table_frame.winfo_children():
        widget.destroy()
def selectionner_carte_geographique():
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale

    # Ouvrir la boîte de dialogue de sélection de fichier
    fichier_carte = filedialog.askopenfilename(
        filetypes=(("Fichiers de carte géographique", "*.mxd"), ("Tous les fichiers", "*.*")),
        title="Sélectionner une carte géographique"
    )

    return fichier_carte