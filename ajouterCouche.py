# -*- coding: utf-8 -*-
import tkSimpleDialog
import arcpy
from couches import GetCouches
from TP1 import selectionner_carte_geographique
import tkMessageBox

def ajouter_couche_geodataset(dataset):
    chemin_carte=selectionner_carte_geographique()
    nom_couche = tkSimpleDialog.askstring("Ajouter une couche", "Entrez le nom de la couche:")
    Type = tkSimpleDialog.askstring("choisir le type de la couche ", "POINT | MULTIPOINT | POLYGON | POLYLINE.")

    if nom_couche:
        if Type:
            pass
        else:
            return GetCouches(dataset)
        pass
    else:
        return GetCouches(dataset)
    chemin_couche = dataset + "\\" + nom_couche

    # Vérifier si le nom de la couche existe déjà dans le géodataset
    if couche_existe(nom_couche, dataset):
        tkMessageBox.showerror( "Erreur", "La couche spécifiée existe déjà dans le géodataset.")

    # Créer la couche vide avec le nom spécifié
    arcpy.CreateFeatureclass_management(dataset, nom_couche, Type)  # Remplacez "POINT" par le type de géométrie souhaité

    # Ajouter la couche à la carte
    carte = arcpy.mapping.MapDocument(chemin_carte)
    dataframe = arcpy.mapping.ListDataFrames(carte)[0]  # Remplacez [0] par l'index du dataframe souhaité
    couche = arcpy.mapping.Layer(chemin_couche)
    arcpy.mapping.AddLayer(dataframe, couche)

    # Enregistrer la carte
    carte.save()
    "La couche a été ajoutée au géodataset et à la carte avec succès."

    # # Verifier si le nom de couche existe déjà dans le GeoDataset
    # couche_existe(nom_couche,dataset)
    # nom = arcpy.CreateFeatureclass_management(dataset, nom_couche)
    #
    # # Add la couche au GeoDataset
    # if arcpy.ListFeatureClasses():
    #     arcpy.mapping.AddLayer(nom, dataset)
    # else:
    #     arcpy.AddMessage(
    #         "La couche a ete cree, mais elle n'a pas ete ajoutée au GeoDataset car le GeoDataset est vide.")

    return GetCouches(dataset)


def couche_existe(nom_couche, geo_dataset):
    chemin_couche = geo_dataset + "\\" + nom_couche
    return arcpy.Exists(chemin_couche)











