# coding=utf-8
import tkSimpleDialog
import tkMessageBox

import arcpy
from couches import GetCouches
from TP1 import selectionner_carte_geographique
def supprimer_couche_geodataset(dataset):
    """
    Supprime une couche de la Géodatabase.

    Args:
        dataset (str): Le chemin complet vers la Géodatabase contenant la couche.
        nom_couche (str): Le nom de la couche à supprimer.

    Returns:
        str: Un message de confirmation si la couche a été supprimée avec succès.

    Raises:
        ValueError: Si le nom de la couche n'est pas valide.
        arcpy.ExecuteError: Si une erreur se produit lors de la suppression de la couche.
    """
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

