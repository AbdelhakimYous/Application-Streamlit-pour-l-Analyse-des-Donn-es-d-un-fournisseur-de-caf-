from datetime import date
import streamlit as st
from PIL import Image
from pandas import read_csv
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from pandas.plotting import scatter_matrix

try:
    fichier = 'BeansDataSet.csv'
    col = ['Channel', 'Region', 'Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    col2 = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    data = read_csv(fichier, names=col)
    data2 = read_csv(fichier, names=col2)
    
except:
    st.error("Erreur de lecture du fichier. Assurez-vous que 'BeansDataSet.csv' est présent.")

st.sidebar.title('Navigation')
menu = st.sidebar.selectbox('Choisir un volet', ['Accueil', 'Aperçu des données', 'Analyse de corrélation', 'Visualisation', 'Rapport'])

if menu == 'Accueil':
    st.markdown(
        """
        <div style='text-align:center;'>
        <h1> Analyse des données Beans & Pods </h1>
        </div>
        """, unsafe_allow_html=True
    )
    st.subheader("Aperçu des données")
    st.dataframe(data)


elif menu == 'Aperçu des données':
    st.header("Aperçu des données")
    st.subheader("15 premières transactions")
    st.dataframe(data.head(15))
    
    st.subheader("15 dernières transactions")
    st.dataframe(data.tail(15))

    st.subheader("Statistiques descriptives")
    st.write(data.describe())

    st.write('On voit ici plusieurs statistiques interessantes. Deja, on remarque que plusieurs de nos produits ont un minimum qui est similaire. Le latte a la moyenne la plus faible, donc il serait bien davoir plus de data sur la satisafaction des clients sur le late. Alors que le Robusta est de loin le produit phare, cest celui avec la plu sgrandes moyenne, le plus grand max,etc.')

    st.subheader("le nombre total vendu par categorie selon la region et channel")
    class_count=data.groupby(['Channel', 'Region']).sum()
    st.write(class_count)
    st.write('On remarque que le robusta est notre produit phare au niveau du sud en magasin alors qu<au nord, cest un des produits les moins populaire. Donc il serait bien de faire un sondage pour recuperer des donnees au niveau de la satisfaction des clients concerant le robusta au nord afin dameliorer nos chiffres daffaires.')

    st.subheader("le nombre total vendu par categorie selon le channel")
    class_count=data.groupby(['Channel']).sum()
    st.write(class_count)
    st.write('Ici, par exemple, le robusta est notre deuxieme produit qui se vend le plus en magasin, mais en ligne, il fait parti des chiffres les plus faible. Donc il serait interessent davoir des donnees au pres des clients pour savoir sil y a une difference de qualite au niveau du robusta selon sil est pris en ligne ou non. ')

    st.subheader("Répartition des ventes online et en magasin")
    class_count=data.groupby('Channel').size()
    st.write(class_count)
    st.write('On constate quun plus grand nombre de vente local compare aux vente en-ligne. Ce qui est bien, mais si on souhaite am/liorer notre presence sur le marche en-ligne, il serait bien de trouver des idees pour accroitre les ventes en ligne. , ')
    
    figure, ax_class = plt.subplots()
    data['Channel'].value_counts().plot(kind='bar', color=['green', 'red'], ax=ax_class)
    ax_class.set_xlabel('Store / Online')
    ax_class.set_ylabel('Nombre de ventes')
    st.pyplot(figure)


elif menu == 'Analyse de corrélation':
    st.header("Analyse de corrélation")
    st.subheader("Corrélation de Pearson")
    st.write(data2.corr())

    st.subheader("Matrice de corrélation")
    fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
    sns.heatmap(data2.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax_corr)
    st.pyplot(fig_corr)
    st.write('Pour simplifier ces chiffres, plus un chiffre se rapproche de 1 plus la correlation est possitive. Alors que plus un chiffre se rapproche de -1 plus la correlation est negative. Donc a partir de la, on comprend bien que par exemple, nous voyons que les gens qui achetent un latte prennent aussi bien souvent un expresson. Bien que la correlation ne soit pas aussi forte pour ce prochain duo, mais il y a bien une correlation entre arabica et expresso. Ce quon pourrait faire pour potentiellement ameliorer les chiffres daffaires, ca serait de faire en sorte que expresso et arabica soient assez proche au niveau du menu pour insiter plus de gens a prendre les deux.')

elif menu == 'Visualisation':
    st.header("Visualisation des données")

    st.subheader("Histogrammes des ventes")
    data.hist(figsize=(12, 8), bins=20, grid=False)
    st.pyplot(plt.gcf())
    from scipy.stats import shapiro
    stat, p_value  = shapiro(data2)
    if p_value>0.05:
        st.write("Les données semblent suivre une distribution normale (échec de rejet de H0)")
    else:
        st.write("Les données ne semblent pas suivre une distribution normale (rejet de H0)")
        st.write('Ici, nous avons une distribution asymetrique. Car les observation ne se situent pas vers la moyenne et na pas une une courbe en forme de cloche. Aussi, par rapport aux histogrammes, on remarque quil y a une forte concentration au niveau des valeurs faibles au niveau des x. Donc cela pourrait sous-entendre que les clients achetent souvent en petit quantite')
        

    st.subheader("Densité des ventes")
    data.plot(kind='density', subplots=True, layout=(4, 2), figsize=(12, 12), sharex=False)
    st.pyplot(plt.gcf())

    st.subheader("Boîtes à moustaches")
    data.plot(kind='box', subplots=True, layout=(4, 2), figsize=(12, 12), sharex=False)
    st.pyplot(plt.gcf())
    Q1 = np.percentile(data2, 25)
    median = np.percentile(data2, 50)
    Q3 = np.percentile(data2, 75)
    st.write(f"Q1: {Q1}, Median: {median}, Q3: {Q3}")
    aberant=6772.5 + (1.5*5938.5)
    st.write(f"aberant: {aberant}")
    st.write('Ici, nous avons beaucoup de valeurs qui sont aberants cest a dire des donnees qui sont largements superieurs ou inferieur que les autres donnees')
    st.subheader("Scatter Matrix")
    scatter_matrix(data, figsize=(12, 12), diagonal='kde', color='b')
    st.write('Ici, pour simplifier ce qui se passe. Plus les éléments sont alignés vers une ligne bien droite diagonale. Plus il y aune corréaltion négatif ou postif. Déterminer un postif, il faut que la ligne semble se former du bas de laxe des y monte graduellement vers la droite. Nous avons un deux parfaits exemples de corrélations positives fortes entre expresso et latte. Sinon le reste a des correlation qui sont faibles voir même négatif comme latte et robusta qui ets une correlation negative faiblement négative.')
    st.pyplot(plt.gcf())

else:
    st.title(" Analyse des données Beans & Pods")

    st.write('Les gens qui se proccurent un epresso prennent aussi souvent un latte')
    st.write('Les ventes en magasin domine, mais il faudrait penser a des moyens de populariser notre entreprise sur lechelle globale et davoir des avis des clients qui passent des commandes en ligne sur la qualite des produits pour avoir des datas pour nous aider dans cette quete')
    st.write('Le robusta ets notre produit phare')
    st.write('Les gens achteent souvent a petite quantite plutot quen grande qunatite')
    st.write('Notre produit phare qui est le robusta nest pas populaire au nord donc il faudrait recuperer des donnes sur la satisfaction des clients la-bas pour savoir ce quil faudraiyt pour ameliorer le produit')
