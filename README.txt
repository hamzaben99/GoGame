Travail réalisé par Hamza Benmendil et Marin Pau

------------------------
Bibliothèque d'ouverture
------------------------

Pour les premiers mouvements nous allons analyser le fichier game_pro.json fourni avec le sujet pour trouver les premiers coups les plus fréquemment joués.
Ainsi pour le coup numéro 'k' nous jouerons le coup numéro 'k' qui a été le plus joué par les professionnels.


myPlayer.py
-----------

Fichier que vous devrez modifier pour y mettre votre IA pour le tournoi. En l'état actuel, il contient la copie du
joueur randomPlayer.py
Apres modification:
    Le but de ce joueuer est de entourer les stones de l'adversaire afin de les prendre. il essaye aussi d'avoir le plus grand nombre de stone sur le plateau,
    et de capturer le plus possible. pour faire cela nous avons implementé un algorithme alpha-beta qui renvoie les meilleurs move en prenant en compte les
    fonction d'evaluation. Il choisit aussi les premiers moves en utilisant un fichier contenant les meilleurs moves.
    


namedGame.py
------------

Permet de lancer deux joueurs différents l'un contre l'autre.
Il attent en argument les deux modules des deux joueurs à importer.


EXEMPLES DE LIGNES DE COMMANDES:
================================

python3 localGame.py
--> Va lancer un match myPlayer.py contre myPlayer.py

python3 namedGame.py myPlayer randomPlayer
--> Va lancer un match entre votre joueur (NOIRS) et le randomPlayer
 (BLANC)

 python3 namedGame gnugoPlayer myPlayer
 --> gnugo (level 0) contre votre joueur (très dur à battre)

