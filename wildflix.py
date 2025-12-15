import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
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


    # Page Dashboard Film
    elif add_menu == "Dashboard Film":
        st.title("Dashboard Film")

        df_film_final = pd.read_csv('df_film_david.csv', sep= ',')

        #Graphique 1 : Top 10 pays producteurs sans les USA avec colonne OMDB
        st.header("Top 10 des pays producteurs de films (hors USA)")
        df_film_final['country'] = df_film_final['country'].str.replace("USA", "United States")
        df_film_final['Pays_Principal'] = df_film_final['country'].astype(str).str.split(',').str[0]
        df_hors_usa = df_film_final[df_film_final['Pays_Principal'] != 'United States']
        top_countries = df_hors_usa[df_hors_usa['Pays_Principal'] != 'Inconnu']['Pays_Principal'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_countries.values, y=top_countries.index,palette="viridis", ax=ax)
        ax.set_title("Top 10 des Pays Producteurs (Hors USA)", fontsize=15)
        ax.set_xlabel("Nombre de films")
        ax.set_ylabel("Pays")
        st.pyplot(fig)

        #Graphique 2 : USA vs reste du monde avec colonne OMDB
        st.header("USA vs Reste du monde")
        nb_usa = df_film_final[df_film_final['Pays_Principal'] == 'United States'].shape[0]
        nb_total = df_film_final.shape[0]
        pourcentage = (nb_usa / nb_total) * 100
        st.metric(
            label="Films Américains",
            value=nb_usa,
            delta=f"{pourcentage:.1f}% du catalogue"
        )
        nb_usa = df_film_final[df_film_final['Pays_Principal'] == 'United States'].shape[0]
        nb_autres =df_film_final[df_film_final['Pays_Principal'] != 'United States'].shape[0]
        labels = ['USA', 'Reste du Monde']
        sizes = [nb_usa, nb_autres]
        colors = ['#3b8ed0', '#e0e0e0']
        fig_vs, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title("Proportion des films USA")
        st.pyplot(fig_vs)

        #Graphique 3 : Distribution des notes
        st.header("Distribution des Notes IMDb")
        sns.set_theme(style="darkgrid")
        fig_distri, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df_film_final['imdbRating'], kde=True, color="skyblue", bins=20, ax=ax)
        moyenne = df_film_final['imdbRating'].mean()
        mediane = df_film_final['imdbRating'].median()
        ax.axvline(moyenne, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {moyenne:.2f}')
        ax.axvline(mediane, color='green', linestyle='-', linewidth=2, label=f'Médiane: {mediane:.2f}')
        ax.set_title("Distribution des Notes IMDb", fontsize=16)
        ax.set_xlabel("Note IMDb (0-10)", fontsize=12)
        ax.set_ylabel("Nombre de films", fontsize=12)
        ax.legend() 
        st.pyplot(fig_distri)

        #Graphique 4 : Top 10 des succès/flops 
        st.header("Top 10 des succès/flops")
        movies_finance = df_film_final.dropna(subset=['budget', 'BoxOffice']).copy()
        movies_finance['Profit_M'] = (movies_finance['BoxOffice'] - movies_finance['budget']) / 1_000_000
        top_10_succes = movies_finance.nlargest(10, 'Profit_M')
        top_10_flops = movies_finance.nsmallest(10, 'Profit_M')
        movies_extremes = pd.concat([top_10_flops, top_10_succes])
        movies_extremes = movies_extremes.sort_values('Profit_M', ascending=True)
        movies_extremes['Type'] = movies_extremes['Profit_M'].apply(lambda x: 'Succès' if x > 0 else 'Flop')
        fig_finance = px.bar(
            movies_extremes,
            x="Profit_M",
            y="Title",
            orientation='h', 
            color="Type",
            color_discrete_map={'Succès': '#00CC96', 'Flop': '#EF553B'},
            hover_data=['budget', 'BoxOffice'],
            text="Profit_M", 
            title="💸 Top 10 Flops vs Succès (Profit Net en Millions $)",
            labels={"Profit_M": "Profit / Perte (M$)", "movie_title_omdb": "Titre"},
            template="plotly_dark"
        )
        fig_finance.update_traces(texttemplate='%{text:.0f} M', textposition='outside')
        fig_finance.show()
        st.plotly_chart(fig_finance)

        #Graphique 5 : Nombre de films par genre
        st.header(" Nombre de films par genre")
        genres_split = df_film_final['Genre'].str.split(', ')
        genres_exploded = genres_split.explode()
        df_genres_counts = genres_exploded.value_counts().reset_index()
        df_genres_counts.columns = ['Genre', 'Nombre_de_Films']
        df_genres_counts = df_genres_counts[df_genres_counts['Genre'] != 'N/A']
        fig_genres = px.bar(
            df_genres_counts,
            x='Nombre_de_Films',
            y='Genre',
            orientation='h',
            title="🎬 Répartition des Films par Genre (Multi-labels)",
            text='Nombre_de_Films',
            color='Nombre_de_Films',
            template="plotly_dark"
        )

        fig_genres.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_genres.show()
        st.plotly_chart(fig_genres)

        #Graphique 6 : Top 10 films les plus primés
        st.header("Top 10 films les plus primés")
        def calcul_wins_simple(texte):
            if pd.isna(texte) or texte == "N/A":
                return 0
            texte_propre = texte.replace('.', ' ').replace(',', ' ').replace('&', ' ')
            mots = texte_propre.split()
            total = 0
            for i in range(len(mots)):
                mot_actuel = mots[i].lower()
                if mot_actuel == 'win' or mot_actuel == 'wins':
                    mot_avant = mots[i-1]
                    if mot_avant.isdigit():
                        total += int(mot_avant)
                elif mot_actuel == 'won':
                    if i < len(mots) - 1:
                        mot_apres = mots[i+1]
                        if mot_apres.isdigit():
                            total += int(mot_apres)

            return total

        df_film_final['Nb_Wins'] = df_film_final['Awards'].apply(calcul_wins_simple)
        print(df_film_final[['Awards', 'Nb_Wins']].head())

        top_films_awards = df_film_final.sort_values('Nb_Wins', ascending=False).head(10)
        fig_top_awards = px.bar(
            top_films_awards,
            x='Nb_Wins',
            y='Title',
            orientation='h',
            title="🏆 Top 10 des Films les plus Récompensés",
            text='Nb_Wins',
            color='Nb_Wins',
            color_continuous_scale='YlOrRd',
            template="plotly_dark"
        )
        fig_top_awards.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_top_awards.show()
        st.plotly_chart(fig_top_awards)

    # Page Dashboard Acteur/Actrice
    elif add_menu == "Dashboard Acteur/Actrice":
        st.title("Dashboard Acteur/Actrice")

        fichier_stats='Emilie_stats_acteurs.csv'
        @st.cache_data
        def load_data(path):
            data = pd.read_csv(path)
            return data

        df_final_actors = load_data(fichier_stats)

        st.header("Acteurs et actrices en base :performing_arts:")
        Count_actors=df_final_actors['Nom_acteur'].nunique()
        st.subheader(f"{Count_actors}")

        col1, col2 = st.columns(2)
        with col1 :
            st.subheader("Genres :mens: :womens:")
            df_final_actors['Genre'] = df_final_actors['Genre'].fillna('NA')
            genre_counts=df_final_actors['Genre'].value_counts()
            fig, ax = plt.subplots()
            ax.pie(
                genre_counts, 
                labels=genre_counts.index, 
                autopct='%1.0f%%', 
                colors=['maroon', 'orange', 'darkseagreen', "mediumpurple"])
            ax.legend(loc="best") 
            ax.axis('equal') 
            st.pyplot(fig)

        with col2 :
            st.subheader("Nationalités (Top 6) :world_map:")
            nationalite_count=df_final_actors['Pays naissance'].value_counts()
            liste_camembert = nationalite_count[0:6]
            fig, ax = plt.subplots()
            ax.pie(liste_camembert, 
            labels=liste_camembert.index, 
            autopct='%1.0f%%',
            colors=['maroon', 'orange', 'darkseagreen', 'mediumpurple', 'cornflowerblue', 'sienna'])
            ax.legend(loc="best") 
            ax.axis('equal') 
            st.pyplot(fig)

        st.header(f"Acteurs et actrices les plus présents :clapper:")
        class_film = df_final_actors.groupby('Nom_acteur')['imdbID'].count()
        top_10_acteurs = class_film.sort_values(ascending=False).head(10)
        df_top_10 = top_10_acteurs.reset_index(name='Nombre de Films')
        st.bar_chart(data=df_top_10, x='Nom_acteur', y='Nombre de Films', color='#800000')

        st.header("Acteurs et actrices les plus rentables :moneybag:")
        class_money = df_final_actors.groupby('Nom_acteur')['BoxOffice'].sum()
        top_10_money = class_money.sort_values(ascending=False).head(10)
        df_top_money = top_10_money.reset_index(name='Revenu total')
        st.bar_chart(data=df_top_money, x='Nom_acteur', y='Revenu total', color="#FFD700")


        st.header("Acteur et actrice en tête d'affiche :sparkles:")
        col1, col2 = st.columns(2)
        with col1:
            top_man = df_final_actors[df_final_actors['Genre'] == 'Homme'].groupby('Nom_acteur')['imdbID'].count()
            one_man = top_man.sort_values(ascending=False).head(1)
            acteur_index = one_man.index
            nom_acteur_ok = acteur_index[0]
            st.subheader("Acteur le plus présent")
            acteur_url = df_final_actors[df_final_actors['Nom_acteur'] == nom_acteur_ok]['Full_Image_URL'].iloc[0]
            st.image(acteur_url, width=300)
            st.text(f"{nom_acteur_ok}")

        with col2:
            top_woman = df_final_actors[df_final_actors['Genre'] == 'Femme'].groupby('Nom_acteur')['imdbID'].count()
            one_woman = top_woman.sort_values(ascending=False).head(1)
            actrice_index = one_woman.index
            nom_actrice_ok = actrice_index[0]
            st.subheader("Actrice la plus présente")
            actrice_url = df_final_actors[df_final_actors['Nom_acteur'] == nom_actrice_ok]['Full_Image_URL'].iloc[0]
            st.image(actrice_url, width=300)
            st.text(f"{nom_actrice_ok}")

        st.header("Acteurs et actrices étrangers qui ont réussi à Hollywood:earth_africa:")
        top_act_etrangers = df_final_actors[(df_final_actors['Pays naissance'] != 'USA') & (df_final_actors['Country'] == 'United States')].groupby(['Nom_acteur', 'Pays naissance'])['imdbID'].count()
        top_etranger = top_act_etrangers.sort_values(ascending=False).head(10)
        df_top_etranger = top_etranger.reset_index(name='Nombre de films')
        fig = px.bar(df_top_etranger, x='Nom_acteur', y='Nombre de films', color="Pays naissance")
        st.plotly_chart(fig, use_container_width=True)




## streamlit run wildflix.py

## source Streamlit_Wildflix/Scripts/activate
## cd Streamlit_Wildflix
