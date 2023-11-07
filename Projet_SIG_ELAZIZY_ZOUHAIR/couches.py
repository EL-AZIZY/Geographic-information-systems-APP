# coding=utf-8
import arcpy
import tkMessageBox

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
