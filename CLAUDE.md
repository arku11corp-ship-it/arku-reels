# ARKU Reels — règles de production des trial reels

Ce dépôt sert à héberger les vidéos (lien public lu par Metricool) et à garder les règles,
le catalogue et l'outil de montage. Les dessins et les sons sont sur le Google Drive
d'Alexis, dossier `ARKU Reels/` (`dessins/<série>/` et `sons/`). Ne jamais écrire d'ID Drive
ni d'ID Metricool dans ce dépôt (il est public).

## Règles fixées par Alexis (à respecter à chaque reel)
- **CTA obligatoire sur chaque reel : « DM to commissions ».** Chaque reel se termine par
  l'écran de fin au format d'Alexis : fond noir, texte blanc centré « DM to commissions »
  / « (limited slots) », environ 4 beats. Le CTA est aussi dans la caption.
- **Safe zone (tous les textes doivent y être) :** zone visible à la fois dans les Reels
  et dans le feed = y de 240 à 1470 px, x de 35 à 1045 px, et pas dans le coin
  x > 945 / y > 1220 (boutons à droite). Le feed coupe l'image en 1080×1440
  (y 240→1680) ; l'interface des Reels couvre le haut (220 px) et le bas (450 px).
  Accroche en haut à y ≈ 330, étiquettes à y ≈ 1330, écran de fin centré à y = 960.
  Vérifier avec `tools/safecheck.py` sur une image de chaque reel.
- **Les étiquettes de cadrage doivent être exactes** (Portrait / Half body / Full body /
  Character sheet). Toujours choisir l'image d'après la colonne `cadrage` du catalogue :
  portrait = tête + épaules/poitrine ; half-body = jusqu'à la taille ;
  three-quarter = jusqu'aux cuisses/genoux (ne pas l'étiqueter « Half body ») ;
  full-body = personnage entier ; sheet = planche avec plusieurs vues.
- **Changements d'image synchronisés sur les beats du son** (détection des beats avec
  librosa dans `tools/reel.py`), en gardant les durées recommandées ci-dessous.

## Style (repris des reels à +300K vues du compte)
- 1080×1920, 30 i/s, dessin 3:4 centré sur fond noir (occupe exactement y 240→1680,
  donc le feed n'affiche que le dessin), noir et blanc.
- Une seule accroche courte en blanc (police Inter Display Medium, ombre portée), la
  commission n'est jamais l'accroche.
- Durée : 3 à 12 s. Son tendance sped up / slowed. Captions en anglais.

## Formats qui ont marché
- Pour les followers : « give him a name » (1 image, 4 s), croquis → final (« sketch vs
  final », paires `pN` du catalogue), fan art de persos connus « in my style », questions.
- Pour les clients : menu des types de commission (Portrait / Half body / Full body /
  Couple / Character sheet), Ref vs Art (dossier `ref-vs-art`, à venir), portraits +
  écran final « DM to commissions ».

## Programmation
- **Jamais plus de 5 trial reels par jour** (règle d'Alexis).
- Metricool gratuit : 20 posts/mois → 5 trial reels par semaine, lundi→vendredi à 10h
  (Europe/Paris), type `TRIAL_REEL`.
- Vidéo publiée dans `videos/` puis référencée via jsDelivr épinglé sur le commit :
  `https://cdn.jsdelivr.net/gh/arku11corp-ship-it/arku-reels@<commit>/videos/<fichier>.mp4`
- Après publication, supprimer la vidéo du dossier `videos/`.
- Mettre à jour la colonne `deja_utilise` de `catalogue.csv` (date) pour ne pas reposter
  le même montage.

## Catalogue
Les OC n'ont pas de nom : les décrire (ex. `fille-bandes`), ne pas inventer de nom.
`catalogue.csv` : un dessin par ligne. Nom de fichier =
`serie_sujet[_pN]_type_cadrage[_variante].png` — `pN` relie un croquis (`sketch`) à son
final (`final`) ; `v2`, `v3` = variantes quasi identiques (n'en utiliser qu'une par reel).
