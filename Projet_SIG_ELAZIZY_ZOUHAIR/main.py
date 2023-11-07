# coding=utf-8
import Tkinter as tk
from couches import *
from ajouterCouche import ajouter_couche_geodataset
from SupprimerCouche import supprimer_couche_geodataset
from ModifierCouche import renommer_couche
from TP1 import *

# Creation de la fenetre principale
root = tk.Tk()
root.title("Zouhair el-azizy")
Dataset = r"D:\Master BDSaS\S2\SIG systeme informatique geographique\Carte\Carte\New Folder\Geodatabase.gdb"
# Creation de la zone d'affichage des résultats
result_frame = tk.Frame(root, width=700, height=500)
result_frame.grid(row=1, column=0, padx=10, pady=20)

# Création d'une listebox pour afficher les résultats
result_list = tk.Listbox(result_frame, width=70, height=20)
result_list.pack(side=tk.LEFT)

# Création d'une scrollbar pour la liste
scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configuration de la scrollbar pour la liste
result_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=result_list.yview)


# Fonction pour afficher les resultats dans la listebox
def afficher_resultats(resultats):
    result_list.delete(0, tk.END)  # Effacer le contenu précédent de la liste

    if type(resultats) == str:
        result_list.insert(tk.END, resultats)
    elif hasattr(resultats, '__iter__'):
        for item in resultats:
            result_list.insert(tk.END, item)
    else:
        result_list.insert(tk.END, str(resultats))
def on_listbox_select(event):
    selected_item = result_list.get(result_list.curselection())
    afficher_couche(Dataset,selected_item)



afficher_resultats(GetCouches(Dataset))



# Associer la fonction de rappel à l'événement de sélection de la listebox
result_list.bind('<<ListboxSelect>>', on_listbox_select)


# Creation des boutons
button1 = tk.Button(root, text="les couches", command=lambda: afficher_resultats(GetCouches(Dataset)))
button2 = tk.Button(root, text="Ajouter", command=lambda: afficher_resultats(ajouter_couche_geodataset(Dataset)))
button3 = tk.Button(root, text="modifier", command=lambda: afficher_resultats(renommer_couche(Dataset)))
button4 = tk.Button(root, text="supprime", command=lambda: afficher_resultats(supprimer_couche_geodataset(Dataset)))
button5 = tk.Button(root, text="Quitter", command=root.destroy)

# Placement des boutons
button1.grid(row=0, column=0, padx=5, pady=5)
button2.grid(row=0, column=1, padx=5, pady=5)
button3.grid(row=0, column=2, padx=5, pady=5)
button4.grid(row=0, column=3, padx=5, pady=5)
button5.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

# Advancement de la boucle mainloop
root.mainloop()

def GetCouches(Dataset):
    if not arcpy.Exists(Dataset):
        tkMessageBox.showerror( "Erreur", "La géodatabase spécifiée n'existe pas.")

    arcpy.env.workspace = Dataset
    layer_list = []

    # Parcourir les couches à la racine de la géodatabase
    for layer in arcpy.ListFeatureClasses():
        layer_list.append(layer)

    # Parcourir les datasets dans la géodatabase
    for data in arcpy.ListDatasets():
        # Parcourir les couches dans le dataset
        for layer in arcpy.ListFeatureClasses("", "", data):
            layer_list.append(layer)

    if not layer_list:
        tkMessageBox.showerror( "Erreur", "Aucune couche n'a été trouvée dans le dataset.")
    else:
        return layer_list

def supprimer_couche_geodataset(dataset):
    chemin_carte=selectionner_carte_geographique()
    nom_couche = tkSimpleDialog.askstring("Supprimer une couche", "Entrez le nom de la couche:")
    chemin_couche = dataset + "\\" + nom_couche
    # Verifier si la couches exist dans la Database
    if not couche_existe(nom_couche, dataset):
        tkMessageBox.showerror( "Erreur", "La couche spécifiée n'existe pas dans le géodataset.")
    try:
        # Delete the couches
        arcpy.Delete_management(dataset + "\\" + nom_couche)

        # Ouvrir la carte géographique
        mxd = arcpy.mapping.MapDocument(chemin_carte)

        # Obtenir le data frame actif
        df = arcpy.mapping.ListDataFrames(mxd)[0]

        # Trouver la couche à supprimer
        layers = arcpy.mapping.ListLayers(mxd, nom_couche, df)
        for layer in layers:
            arcpy.mapping.RemoveLayer(df, layer)

        # Enregistrer les modifications de la carte géographique
        mxd.save()
        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()
        return GetCouches(Dataset=dataset)
    except arcpy.ExecuteError:
         tkMessageBox.showerror("Erreur", str(arcpy.GetMessages(2)))



def couche_existe(nom_couche, geo_dataset):
    chemin_couche = geo_dataset + "\\" + nom_couche
    return arcpy.Exists(chemin_couche)