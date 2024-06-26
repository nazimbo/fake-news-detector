import nltk
import ssl

#Contourner la vérification SSL pour les téléchargements NLTK
ssl._create_default_https_context = ssl._create_unverified_context

nltk.download("stopwords")
nltk.download("wordnet")

#Restaurer le paramètre de vérification SSL par défaut
ssl._create_default_https_context = ssl._create_default_https_context