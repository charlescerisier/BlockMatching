# Compression Vidéo 

## Introduction 

L'objectif de ce TP est de comprendre et de réaliser la partie d'estimation de mouvement d'un encodeur vidéo. En effet, fichier vidéo possède une grande redondance statistique au niveau des données spatiales, mais aussi des données temporelles. Afin de faire une estimation de mouvement, nous avons réalisé, en partie, un algorithme de Block Matching. Ce programme a pour but d'encoder le mouvement dans une vidéo, en recherchant des blocs similaires entre différentes images. Cet algorithme de compensation de mouvement est utilisé dans certaines normes de compression vidéo comme le H.264 et MPEG-2. 

![encodeur](D:\Documents\DSMT S8\Traitement_Video\Python\imagesRapport\encodeur.png)

Les vidéos utilisées lors de ce TP étaient des vidéos YUV non compressées. Le premier objectif était donc de lire les images avec Python 3. 
Sachant que la résolution des images était de $288 \times 352$ et qu'elles étaient échantillonnées en 4:2:0, il était facile de déterminer la taille d'une image. 


$$
Taille_{image} = 352 \times 288 + 2 \times (176*144)  
$$


$$
Taille_{image} =  152064 \mbox{ octets}
$$

Pour obtenir la première image, il est donc nécessaire de récupérer les $152064$ premiers octets du fichier yuv. 

Dans notre algorithme de Block Matching, seule la composante Y de l'image récupérée est intéressante car c'est elle qui possède le plus d'information.

Afin de manipuler plus facilement et d'observer l'image Y  que nous venons de récupérer, on a reconstruit une image en 2 dimensions (2D).

![image1_football](https://github.com/charlescerisier/BlockMatching/tree/master/imagesRapport/image1_football.png)

## Block Matching 

Pour trouver le meilleur bloc correspondant au bloc d'une image courante dans une image de référence, l'algorithme de Block Matching parcourt l'image bloc par bloc dans un certain ordre. Nous avons réalisé 2 types d'algorithme de Block Matching avec le même critère de ressemblance des blocs : la SAD.

### SAD 

La Somme des différences absolues (SAD) est un algorithme simple utilisé afin de trouver une corrélation entre les blocs ou macro-blocs d'une image. Elle est déterminée en calculant la différence absolue entre chaque pixel dans un bloc de l'image référence et le pixel d'un bloc de l'image courante.

$$
SAD = \sum{}{}{\mid block1_{i,j} - block2_{i,j} \mid}
$$

### Full Search Algorithm

Dans un premier temps, la recherche du meilleur bloc était réaliséé dans l'ensemble de l'image de référence. Cependant, cet algorithme était trop gourmand en calcul et nos ordinateurs prenaient en moyenne 25 secondes pour comparer le bloc courant à tous les blocs de l'image de référence. Sachant qu'il y avait 396 blocs  (de $16 \times 16 \mbox{ pixels}$) dans l'image courante, il fallait environ 3 heures de calcul. C'est pourquoi, nous avons réduit notre fenêtre de recherche.

Dans ce second algorithme, nous avons donc utilisé une fenêtre de recherche de $48 \times 48 \mbox{ pixels}$ autour du bloc courant en partant du principe que le mouvement n'a pas été trop important. Le temps de calcul pour tous les blocs est d'ici largement inférieur à l'algorithme précédent, environ 1 minute 30.

![fenetre](https://github.com/charlescerisier/BlockMatching/tree/master/imagesRapport/fenetre.png)

Pour chaque meilleur bloc trouvé, on enregistre un vecteur mouvement qui correspond au déplacement du bloc de l'image de référence à l'image courante : c'est l'estimation de mouvement. 

![champdemouvement](https://github.com/charlescerisier/BlockMatching/tree/master/imagesRapport/champdemouvement.PNG)



### Compensation de mouvement


La compensation du mouvement est un algorithme utilisé dans un décodeur. Le but de la compensation de mouvement est récréer l'image courante à partir de l'image de référence et du champ de vecteurs. 

![image3_comparaison2](https://github.com/charlescerisier/BlockMatching/tree/master/imagesRapport/image3_comparaison2.png)


On observe quelques différences aux endroits où le déplacement a été le plus important. 

### Quart de Pixel 

Le mouvement n'étant pas pixelique, il est intéressant d'essayer d'augmenter la résolution de l'image de façon artificielle. Afin d'obtenir une précision au quart de pixel, il faut dans un premier temps créer une image vide 4 fois plus grande que celle de base. Dans un second temps, on remplace 1 pixel sur 4 de cette nouvelle image par les pixels de l'image de référence. Finalement, on réalise une moyenne pondérée par leur distance entre les 4 pixels existants.


![imagex4_2](https://github.com/charlescerisier/BlockMatching/tree/master/imagesRapport/imagex4_2.png)


Cette nouvelle image, précise au quart de pixel peut être réinjectée dans un algorithme de block matching pour augmenter la précision.

## Conclusion 


Ce TP a été très intéressant car il nous a permis de comprendre en partie un encodeur vidéo et l'algorithme de Block Matching utilisé dans la norme H264. Ce projet a très bien complété notre premier TP de compression d'image où nous nous étions intéressé à la redondance des données spatiales, ici on s'intéresse en plus à la redondance temporelle.

Afin d'améliorer notre programme, nous aurions pu implémenter l'estimation hiérarchique. 
