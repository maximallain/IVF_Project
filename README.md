<h1 align='center'> Projet Introduction à la Vérification Formelle </h1>
<p align='center'>
<i>Option ISIA - Centrale Paris <br>
Février 2018 <hr></i></p>

__Auteur__ : Maxime Allain, Eymard Houdeville<br>

## Index
0. [Requirements](#req)
1. [Présentation du problème](#prob)
2. [Structures de données et approche](#crit)
3. [Critères de tests](#crit)
4. [Jeux de tests](#init)
5. [Puissance des critères](#pui)

## <a name="prob"></a>0. Requirements
Les librairies utilisées sont:
- networkx: une librairie qui permet d'implémenter facilement des graphs
- sympy : une librairie qui permet d'effectuer des calculs sous la forme symbolique et qui va nous être utile pour la partie "génération de tests"

Elles peuvent être installées via une commande pip de la forme:

`sudo pip3 install networkx`

`sudo pip3 install sympy`

## <a name="prob"></a>1. Présentation du problème

Le problème proposé est une exploration des concepts d'analyse de couverture et de génération de tests sur un langage particulier: le langage "while" donné en partie 3 du sujet.

L'analyse de couverture correspond au fait de vérifier qu'un jeu de tests couvre bien un critère de tests.

La génération de tests correspond à la construction d'un jeu de tests à partir d'un code source et d'un critère.

En vérification formelle, notre projet se situe en aval du parsing du code et de sa transformation en control flow graph.

Définition d'un control flow graph:
`En informatique, un graphe de flot de contrôle (abrégé en GFC, control flow graph ou CFG en anglais) est une représentation sous forme de graphe de tous les chemins qui peuvent être suivis par un programme durant son exécution.` (Source: Wikipedia)

## <a name="crit"></a>2. Structures de données et approche

Il est important de présenter en quelques mots notre structure de données.

Nous avons pris le problème à l'étape du control flow graph (cfg par la suite). Ces cfg sont stockés dans le dossier cfg de notre projet.
L'idée très simple du cfg correspond à labbeliser chacun des noeuds (if, assign, while etc) et à donner à chaque arrête du graph une fonction:

*Exemple d'arrête dans un CFG*:

`G.add_edge(2, 4, bool=True, cmd='assign', func=lambda var: assign_1(var), var=('x'), symb=-x)`

Cette arrête relie le noeud 2 au noeud 4. On lui associe la commande du noeud père (assign) et une lambda fonction liée à la commande (ici une fonction d'assignation). On garde également dans notre edge une mémoire sous la forme symbolique (x est une variable sympy) de la fonction d'assignation.

Dans le cas où la commande est if, ou while, c'est dans le "bool" que l'on pourra stocker une fonction d'évaluation. Sa forme symbolique sera toujours stockée dans "symb"

Nous disposons donc en input d'un graph avec des transformations (assign) et des tests (if, while) sur lequel nous allons pouvoir travailler.

## <a name="crit"></a>3. Critères de tests

Explications et remarques sur notre code.

Nous avons mis chacun des critères dans un dossier à part pour simplifier leur lecture et leur dévelopement.
Chacun des critères va avec son jeu de tests.

Pour executer un critère:
`python3 1_ta.py`

Tous nos tests de couverture reposent sur une même façon de procéder: on commence par extraire les chemins ou noeuds où il faut passer pour vérifier le critère. On génère ensuite tous les chemins instanciés par nos tests et on vérifie qu'ils couvrent bien ce cahier des charges.

Concrètement nous avons un tableau avec chacun des noeuds à visiter (ou un dictionnaire lorsqu'il faut visiter plusieurs fois un noeud dans des situations différentes). Lorsqu'un noeud est visité dans la configuration voulue (par exemple évalué à TRUE) on supprime le booléen correspondant de notre structure de données. Les éléments restant sont ceux que l'on a pas visité et qui marquent les défaillance du jeu de test.

## TA
Pour ce critère, toutes les affectations doivent être executées au moins une fois.

On fait une liste des noeuds avec la commande "assign" au moyen de la fonction extract_label. On parcourt le cfg avec nos jeux de tests et on vérifie que cet ensemble recouvre bien l'ensemble des noeuds à couvrir.

## TD
Avec la fonction extract_labels on fait une liste des labels if et while. Lors du parcours de notre graph avec les jeux de tests on vérifiera ensuite que ces noeuds sont bien évalués alternativement à True et False.

## kTC
On génère tous les k-chemins (k=3 dans notre exemple) et on vérifie qu'ils sont bien couverts par les jeux de test.

## iTB
L'idée est de générer tous les chemins possibles dans le graph (en se limitant à i boucles) et de vérifier que ces chemins sont bien couverts par le jeu de tests.

Notre stratégie est toujours de remplir un tableau avec tous ces chemins (ou des élements permettant de les représenter de façon unique tel que le passage en un noeud particulier) et d'enlever ces derniers au fur et à mesure.

## TDEF
Pour chaque variable, nous vérifions que l'ensemble des noeuds de définition (assign) sont parcourus au moins une fois.

Pour chaque variable, nous parcourons l'ensemble des noeds du graphe. Nous créons ensuite un dictionnaire dont la clé est une variable et sa valeur une liste de noeuds. Nous créons un dictionnaire de la même forme en parcourant le graphe avec chaque valeur de test. Nous comparons les deux et s'ils sont égaux, alors, le critère est vérifié.

## TU
Pour chaque affectation de la variable x (assign), on vérifie que tous les tests if et while en aval et avant une autre affectation sont bien évalués à True et False alternativement.
Concrètement on commence par remplir un dictionnaire dont les clefs sont chacun des noeuds assign: les valeurs sont elles mêmes des dictionnaires avec les différents noeuds if et while dont on doit vérifier qu'ils vont être évalués à True et False.

On réalise ensuite un parcours du cfg avec notre jeu de données en prenant soin d'enlever de notre dictionnaire les chemins couverts. Les chemins restants sont les chemins orphelins de tests.

## TDU
Pour chaque couple définition-utilisation d’une variable, tous les chemins simples sans redéfinition intermédiaire de cette variable sont exécutés une fois.

L'idée de l'algorithme est de parcourir l'ensemble du graphe pour chaque variable, et de stocker les chemins dont le début est une affectation assign jusqu'à une commande 'if' ou 'while', sans qu'une autre affectation soit parcouru. Puis on parcours le graphe pour chaque valeur de test.

## TC
Idem: on génère toutes les conditions c dans un tableau et on les élimine au fur et à mesure que l'on vérifie qu'elles sont bien couvertes par un jeu de tests. Les conditions non couvertes sont celles qui restent.

## <a name="crit"></a>4. Jeux de tests

# Etape 1

Pour commencer il nous faut générer tous les chemins possibles dans le graph.

Ce problème est NP et nous avons d'abord pensé un algorithme DFS adapté qui générererait tous les chemins.

Cette étape peut être correctement effectuée via la fonction all_simple_paths de Networkx, la librairie de graph que nous utilisons et qui génère tous les chemins simples du graph.
Cette stratégie nous permet déjà de générer des jeux de tests pour un certain nombre de critères.

# Etape 2

Il faut ensuite associer à chacun des chemins la suite de contraintes qui définit ce dernier (les prédicats de chemin). Par exemple tel chemin ne sera emprunté que si x>0 dans la première étape puis dans la seconde x+1<10 (avec une transformation x -> x+1 entre les deux étapes)

Nous manipulons pour cela les expressions symboliques (fonctions) avec la librairie sympy.

Lorsque nous traversons le graph avec un chemin, nous sommmes amenés à rencontrer deux types de situation:

- On doit faire une transformation sur les variables : il s'agit d'une composition de fonctions sous leur forme symbolique
- On doit appliquer l'ensemble des fonctions rencontrées jusqu'à maintenant dans un chemin à un test et générer la contrainte associée à ce test

# Etape 3

Dans cette étape on associe chaque chemin à un critère.
Il suffira alors d'associer les jeux de tests associés aux chemins à l'étape précédente aux critères.

En fait, l'équation est la suivante:
1 critère = 1 ensemble de chemin = des tests associés à chaque chemin

Cette étape nous permet également de répondre à une question posée dans l'ennoncé: certains critères s'avèrent en effet plus forts que d'autres dans le sens où l'ensemble des chemins auxquels ils sont associés recouvre les chemins d'autres critères (est plus large).

L'association se fait sur le mode suivant:

## TA
Tous les chemins qui passent par un noeud "assign" au moins une fois.

## TD
On garde au moins (et au plus si l'on veut l'ensemble de chemins le plus restreint possible) un chemin par alternative (TRUE or FALSE) pour chaque noeud if/while.

## kTC
On garde tous les chemins dont la longueur est inférieure ou égale à k.

## iTB
On garde tous les chemins pour tous les labels à l'exception de while.
Pour les chemins passant par un noeud while on ne garde que les chemins qui re-passent au maximum i-1 fois par ce même noeud.

## TDEF
Pour chaque variable, nous obtenons une liste de noeuds où l'on assigne une variable.

## TU
On fait une liste des noeuds où l'on assigne une variable. On garde un chemin par élement de cette liste qui évalue à True ou False une condition avant l'assignation suivante (i.e. l'élement suivant dans la liste)

## TDU
Pour chaque variable, on garde les chemins composés d'une définition (assign) et d'une utilisation (if, while), sans redéfinition.

## TC
On "casse" les expressions booléennes dans les conditions des noeuds if et while en les exprimant sous la forme normale conjonctive et on en fait une liste . On garde au moins un chemin par évaluation de chacun des éléments de cette liste (ou bien True ou bien False).

## <a name="pui"></a>4. Puissance des critères

On évalue chacun des critères en fonction de la cardinalité des ensembles de chemins qu'ils amènent à générer.

- Le critère kTC avec de grandes valeurs pour k est évidemment le plus puissant puisqu'il couvre tous les chemins.
- Le critère iTB est également puissant dès lors que i augmente.

- Le critère TC est plus général que le critère TD puisqu'il couvre TA et nous amène à dissocier les conjonctions de conditions que l'on regarde comme un tout dans TA ce qui augmente mécaniquement le nombre potentiel de chemins associés.

- TU est pour sa part plus fort que TA: TA ne couvre que les assignations dans notre code alors que TU couvre toutes les assignations et les chemins intermédiaires IF ou WHILE (TRUE ou FALSE)
