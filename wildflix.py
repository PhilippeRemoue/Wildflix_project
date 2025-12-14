import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import re
from datetime import date, time
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate
from pathlib import Path

# ajouter un Fond d'écran
def set_bg(image_file):
    """
    Définit une image de fond pour l'application Streamlit.
    """
    # Lire l'image et l'encoder en base64
    img_bytes = Path(image_file).read_bytes()
    b64 = base64.b64encode(img_bytes).decode()
    
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Charger le fichier CSV
df = pd.read_csv("users.csv",sep=",")

# Initialiser la session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""

# CSS pour la sidebar
st.markdown(
    """
    <style>
    /* Fond noir Netflix + texte blanc */
    [data-testid="stSidebar"] {
        background-color: #141414 !important;
        color: white !important;
    }

    /* Titres en rouge Netflix */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #E50914 !important;
        font-weight: bold !important;
    }

    /* Texte normal en blanc */
    [data-testid="stSidebar"] p {
        color: white !important;
    }

    /* Boutons style Netflix */
    [data-testid="stSidebar"] button {
        background-color: #E50914 !important; /* rouge Netflix */
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        padding: 8px 20px !important;
        transition: 0.3s;
        border: none !important;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #B20710 !important; /* rouge plus sombre */
        transform: scale(1.05);
    }

    /* Menu option (option_menu) style Netflix */
    .nav-link {
        color: white !important;
        font-weight: bold !important;
        background-color: transparent !important;
    }
    .nav-link:hover {
        color: #E50914 !important;
        background-color: #333333 !important;
    }
    .nav-link.active {
        color: white !important;
        background-color: #E50914 !important;
        border-radius: 6px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Page de connexion
if not st.session_state.authenticated:
    set_bg("Image_salle_cine_copilot.png")

    # Titre rouge fixe au centre
    st.markdown(
        """
        <div style='
            position: fixed;
            top: 32%;
            left: 45%;
            transform: translate(-50%, -50%);
            text-align: center;
            z-index: 999;
        '>
            <h1 style='color: #E50914; font-size: 60px; line-height: 1.2; margin: 0;'>
                &nbsp;&nbsp;&nbsp;Bienvenue<br>sur<br>&nbsp;&nbsp;&nbsp;&nbsp;WILDFLIX
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Styles des champs et du bouton (Netflix)
    st.markdown(
        """
        <style>
        /* Labels en blanc */
        label { color: white !important; font-weight: bold; }

        /* Champs translucides */
        .stTextInput > div > div > input {
            background-color: rgba(0,0,0,0.6) !important;
            color: white !important;
            border-radius: 6px !important;
        }

        /* Bouton Connexion rouge Netflix */
        div.stButton > button:first-child {
            background-color: #E50914 !important;
            color: white !important;
            font-size: 20px !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            transition: 0.3s;
        }
        div.stButton > button:first-child:hover {
            background-color: #B20710 !important;
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Styles du message d'erreur de connexion
    st.markdown(
        """
        <style>
        /* Forcer les messages d'erreur en blanc */
        .stAlert p {
            color: white !important;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # Espacement sous le titre fixe pour laisser voir le fond
    st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

    # Formulaire "normal" (défile, mais stylé correctement)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Connexion"):
        user = df[(df["name"] == username) & (df["password"] == password)]
        if not username or not password:
            st.error("Les champs username et mot de passe doivent être remplis")
        elif not user.empty:
            st.session_state.authenticated = True
            st.session_state.username = user.iloc[0]["name"]
            st.session_state.role = user.iloc[0]["role"]

            df.loc[df["name"] == username, "logged_in"] = True
            df.to_csv("users.csv", index=False)

            st.success(f"Bienvenue {username} !")
            st.rerun()
        else:
            if username in df["name"].values:
                df.loc[df["name"] == username, "failed_login_attempts"] += 1
                df.to_csv("users.csv", index=False)
            st.error("Login ou mot de passe incorrect")

else:
    ##Bouton de déconnexion en haut de la sidebar
    if st.sidebar.button("Déconnexion"):
        df.loc[df["name"] == st.session_state.username, "logged_in"] = False
        df.to_csv("users.csv", index=False)

        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    # Message de bienvenue (juste après le bouton)
    st.sidebar.markdown(f"### Bienvenue {st.session_state.username}")

    # On affiche un menu (option_menu) dans la barre latérale (sidebar)
    # L'utilisateur peut choisir la page qu'il souhaite entre deux options
    with st.sidebar:
        add_menu = option_menu(
                menu_title=None,
                options = ["Accueil", "Dashboard Réalisateur", "Dashboard Film", "Dashboard Acteur/Actrice", "Dashboard Genre"]

            )
    # Charger le fichier df_film.csv
    df_film = pd.read_csv("df_film.csv", sep=";")


    # Page Accueil
    if add_menu == "Accueil":
        st.title("Accueil")

        # Liste déroulante basée sur la colonne Title
        choix_titre = st.selectbox(
            "Choisissez un film :",
            options=df_film["Title"].dropna().unique()
        )

        # Récupération des infos du film choisi
        film = df_film[df_film["Title"] == choix_titre].iloc[0]

        # Bloc poster + infos
        col1, col2 = st.columns([1.2, 2.4])  # col1 plus étroite, col2 plus large

        with col1:
            st.image(film["Poster"], width=250)  # affiche le poster via l'URL

        with col2:
            st.markdown(f"""
            ### {film['Title']}
            **Genre :** {film['Genre']}  
            **Réalisateur :** {film['Director']}  
            **Année :** {film['Year']}  
            **Durée :** {film['Runtime']}  
            **Acteurs :** {film['Actors']}  
            **Synopsis :** {film['Plot']}
            """)

        st.markdown("---")

        # Bloc recommandations (5 colonnes)
        st.subheader("Recommandations")

        rec_cols = st.columns(5)
        # Exemple : recommandations basées sur le même genre que le film choisi
        recommandations = df_film[
            (df_film["Title"] != choix_titre) & 
            (df_film["Genre"] == film["Genre"])
        ].head(5)

        # Boucle sécurisée
        for i, rec in enumerate(recommandations.itertuples(index=False)):
            with rec_cols[i]:
                # Vérifie que l'URL du poster est valide
                if pd.notna(rec.Poster) and str(rec.Poster).startswith("http"):
                    st.image(rec.Poster, width=150)
                else:
                    st.write("📌 Poster indisponible")
                st.caption(rec.Title)

    # Page Dashboard Réalisateur
    elif add_menu == "Dashboard Réalisateur":
        st.title("Dashboard Réalisateur")
        
        # --- 1. Sélection du Réalisateur ---
        
        # Liste unique des réalisateurs, triée et sans valeurs manquantes
        realisateurs = df_film["Director"].dropna().unique()
        
        # Liste déroulante pour choisir le réalisateur
        realisateur_choisi = st.selectbox(
            "Sélectionnez un réalisateur :",
            options=realisateurs
        )
        
        # Filtrer le DataFrame pour le réalisateur sélectionné
        df_realisateur = df_film[df_film["Director"] == realisateur_choisi]
        
        # Fonction pour extraire et sommer les valeurs numériques pour les prix/nominations
        def extract_and_sum_awards(df, keyword):
            # Regex pour trouver le nombre associé au mot-clé (ex: '20 wins' -> 20)
            # On cherche soit 'X keyword', soit 'X total' (pour les nominations)
            pattern = rf"(\d+)\s+{keyword}"
            
            # Extraction de toutes les valeurs et conversion en int
            all_values = df["Awards"].dropna().str.extractall(pattern)[0].astype(int)
            
            return all_values.sum() if not all_values.empty else 0

        # --- Nouveaux Calculs (Genre, Prix) ---

        # Calcul du Genre Favori
        genres = df_realisateur["Genre"].dropna().str.split(", ").explode()
        if not genres.empty:
            genre_favori = genres.mode().iloc[0]
        else:
            genre_favori = "Non disponible"
        
        # Calcul des Prix
        total_oscars = extract_and_sum_awards(df_realisateur, "Oscar")
        total_wins = extract_and_sum_awards(df_realisateur, "win")
        total_nominations = extract_and_sum_awards(df_realisateur, "nomination")


        # --- 2. Indicateurs Clés (KPIs) ---
        
        st.subheader(f"Statistiques pour {realisateur_choisi} 📊")
        
        # Affichage du Genre Favori en info box
        st.info(f"✨ **Genre Favori :** **{genre_favori}**")
        
        # Calcul des métriques déjà existantes
        nombre_films = df_realisateur.shape[0]
        
        # CORRECTION : Utilisation de "imdbRating"
        note_moyenne = df_realisateur["imdbRating"].mean()
        
        try:
            metascore_moyen = df_realisateur["Metascore"].astype(float).mean()
        except KeyError:
            metascore_moyen = "N/A"
        except:
            metascore_moyen = "Données invalides"

        # Ligne 1 d'indicateurs (Films, Note, Metascore)
        col_films, col_note, col_meta = st.columns(3)

        with col_films:
            st.metric(label="Nombre de films réalisés", value=nombre_films)

        with col_note:
            st.metric(label="Note IMDb Moyenne", value=f"{note_moyenne:.2f}")
            
        with col_meta:
            st.metric(label="Metascore Moyen", value=f"{metascore_moyen:.2f}" if isinstance(metascore_moyen, float) else metascore_moyen)

        st.markdown("---")

        # Ligne 2 d'indicateurs (Prix et Nominations)
        col_oscars, col_wins, col_nominations = st.columns(3)

        with col_oscars:
            st.metric(label="Oscars Gagnés 🏆", value=total_oscars)

        with col_wins:
            st.metric(label="Total Prix Gagnés (y compris Oscars)", value=total_wins)
            
        with col_nominations:
            st.metric(label="Total Nominations", value=total_nominations)
            
        st.markdown("---")
        
        # --- 3. Acteurs Fétiches (Top 3) ---
        
        st.subheader("Les 3 Acteurs Fétiches 🎭")
        
        # Joindre toutes les chaînes d'acteurs en une seule
        tous_acteurs = " | ".join(df_realisateur["Actors"].dropna().tolist())
        
        # Séparer chaque acteur individuel
        liste_acteurs = [acteur.strip() for film_acteurs in tous_acteurs.split(" | ") for acteur in film_acteurs.split(",")]
        
        # Compter les occurrences et obtenir le Top 3
        df_acteurs = pd.Series(liste_acteurs)
        top_acteurs = df_acteurs.value_counts().head(3)
        
        # Affichage sous forme de tableau ou de liste
        if not top_acteurs.empty:
            
            # Création d'un petit DataFrame pour l'affichage
            df_top_acteurs = top_acteurs.rename_axis('Acteur').reset_index(name='Nombre de films')
            st.dataframe(df_top_acteurs, hide_index=True)
            
            # Génération d'un graphique à barres pour le Top 3 (visualisation)
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x='Acteur', y='Nombre de films', data=df_top_acteurs, ax=ax, palette="flare")
            ax.set_title(f"Top 3 des acteurs pour {realisateur_choisi}")
            ax.set_xlabel("")
            ax.set_ylabel("Nombre de films tournés")
            plt.xticks(rotation=0)
            st.pyplot(fig)
            
        else:
            st.info("Aucune donnée d'acteur disponible pour ce réalisateur.")
            
        st.markdown("---")
        
        # --- 4. Top 5 des Meilleurs Films ---
        
        st.subheader("Top 5 des Films par Note IMDb 🌟")
        
        # Trier les films par 'imdbRating' décroissant et prendre les 5 premiers
        top_films = df_realisateur.sort_values(by="imdbRating", ascending=False).head(5)
        
        if not top_films.empty:
            # Afficher les informations clés dans un tableau
            st.dataframe(
                top_films[["Title", "Year", "imdbRating", "imdbVotes", "Runtime"]].rename(
                    columns={
                        "Title": "Titre", 
                        "Year": "Année", 
                        "imdbRating": "Note IMDb", 
                        "imdbVotes": "Votes", 
                        "Runtime": "Durée"
                    }
                ),
                hide_index=True
            )
            
            # --- 5. Visualisation (Graphique) du Top 5 ---
            
            # Créer un graphique à barres horizontal pour les notes
            fig_top, ax_top = plt.subplots(figsize=(10, 5))
            sns.barplot(x="imdbRating", y="Title", data=top_films, ax=ax_top, palette="viridis")
            ax_top.set_title(f"Notes IMDb des 5 meilleurs films de {realisateur_choisi}")
            ax_top.set_xlabel("Note IMDb")
            ax_top.set_ylabel("")
            st.pyplot(fig_top)
            

        else:
            st.info("Aucun film trouvé pour afficher le Top 5.")



## streamlit run wildflix.py

## source Streamlit_Wildflix/Scripts/activate
## cd Streamlit_Wildflix
