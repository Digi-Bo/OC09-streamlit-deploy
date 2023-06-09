import streamlit as st
import pandas as pd
import numpy as np
import glob
from datetime import datetime, time
import requests  
import json 


# Titre de l'application
st.title("Système de recommandation hybride")

# Sélection de l'utilisateur
user_id = st.number_input("Entrez l'ID de l'utilisateur :", min_value=1, max_value=1000, value=1)

# Dates pour les périodes de référence et de prédiction
ref_start_date = st.date_input("Date de début de la période de référence :", value=pd.to_datetime('2017-10-01'))
ref_end_date = st.date_input("Date de fin de la période de référence :", value=pd.to_datetime('2017-10-08'))

pred_start_date = st.date_input("Date de début de la période de prédiction :", value=pd.to_datetime('2017-10-09'))
pred_end_date = st.date_input("Date de fin de la période de prédiction :", value=pd.to_datetime('2017-10-16'))

# Convertir les objets date en objets datetime avec une heure de 0
ref_start_date = datetime.combine(ref_start_date, time(0, 0))
ref_end_date = datetime.combine(ref_end_date, time(0, 0))
pred_start_date = datetime.combine(pred_start_date, time(0, 0))
pred_end_date = datetime.combine(pred_end_date, time(0, 0))

# Bouton pour lancer la recommandation
if st.button("Recommander des articles"):
    if ref_end_date < ref_start_date or pred_end_date < pred_start_date:
        st.error("Les dates de fin doivent être ultérieures aux dates de début.")
    else:
        # Remplacez cette URL fonction Azure Functions
        azure_function_url = "https://hybridrecommender.azurewebsites.net/api/httpHybridTrigger?code=dfT6H1Fmgn29O23f12Q5zbhjmAfBkaAqMoXTmOOxTOHeAzFu8jLJvw=="
                                
        try:
            # Envoyer une requête GET à la fonction Azure
            response = requests.get(
                azure_function_url,
                params={
                    "userid": user_id,
                    "ref_start_date": ref_start_date.strftime('%Y-%m-%d'),
                    "ref_end_date": ref_end_date.strftime('%Y-%m-%d'),
                    "pred_start_date": pred_start_date.strftime('%Y-%m-%d'),
                    "pred_end_date": pred_end_date.strftime('%Y-%m-%d'),
                },
            )

            # Vérifier le statut de la réponse
            response.raise_for_status()

            # Tenter de lire la réponse comme JSON
            top_articles = response.json()

            # Afficher les résultats
            st.header("Top 5 articles recommandés :")
            for article in top_articles:
                st.write(f"ID de l'article : {article}")

        except requests.exceptions.HTTPError as http_err:
            st.error(f"Erreur HTTP s'est produite: {http_err}")
        except Exception as err:
            st.error(f"Une erreur s'est produite: {err}")
