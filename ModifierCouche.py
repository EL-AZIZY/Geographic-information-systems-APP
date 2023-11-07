# -*- coding: utf-8 -*-
import tkSimpleDialog
from couches import GetCouches
import tkMessageBox

import arcpy


def renommer_couche(dataset):
    nom_actuel = tkSimpleDialog.askstring("nom actuel", "Entrez le nom actuel de la couche:")
    layer_list = []
    for layer in arcpy.ListFeatureClasses():
        layer_list.append(layer)
    if layer_list is not None:
        if nom_actuel not in layer_list or nom_actuel is None:
            tkMessageBox.showerror( "Erreur","La couche spécifiée n'existe pas dans la Géodatabase.\n" + "les couches actuel:\n" + GetCouches(dataset))
    nouveau_nom = tkSimpleDialog.askstring("nouveau nom", "Entrez le nouveau nom de la couche:")
    try:
        arcpy.Rename_management(dataset + "\\" + nom_actuel, dataset + "\\" + nouveau_nom)
        return GetCouches(dataset)
    except Exception as e:
        tkMessageBox.showerror("Erreur","Une erreur s'est produite lors du renommage de la couche : {}".format(str(e)))

