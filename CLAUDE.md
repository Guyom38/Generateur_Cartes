# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Lancement

Ouvrir `index.html` directement dans un navigateur — aucun serveur, aucune dépendance à installer. Toute la logique tient dans ce seul fichier.

## Architecture

Application HTML monofichier (`index.html`) sans build, sans framework JS, sans module ES.

**Dépendances CDN (chargées à l'exécution) :**
- **Tailwind CSS** — utilitaires CSS via CDN
- **html2canvas 1.4.1** — capture de la carte en PNG côté client
- **Balsamiq Sans** (Google Fonts) — police style BD utilisée sur la carte

**Structure interne du fichier :**
1. `<style>` — CSS personnalisé qui complète Tailwind (carte, scrollbar, drag & drop, mode dimensionnement)
2. HTML — deux colonnes : panneau de configuration (gauche, 450 px fixe) + zone d'aperçu live (droite, flex-1)
3. `<script>` — logique vanilla JS en bas de page

**Flux de données :**
- Tous les `<input>` et `<textarea>` du panneau gauche déclenchent `updateCard()` via les événements `input` et `change`
- `updateCard()` lit les valeurs et applique directement les styles inline sur les éléments de la carte (`#the-card` et ses enfants)
- Aucun état partagé : la carte HTML **est** l'état

## Carte (`#the-card`)

Dimensions fixes 1055 × 1491 px (ratio A4 portrait), réduite à 60 % à l'écran via `transform: scale(0.6)`. Lors du téléchargement, le scale est retiré avant la capture `html2canvas` pour obtenir la pleine résolution.

**Zones éditables dans la carte :**
| ID | Rôle |
|----|------|
| `#card-icon` | Cercle icône absolument positionné (haut-gauche) |
| `#card-title` | En-tête / titre |
| `#card-img-wrapper` + `#card-img` | Image centrale |
| `#card-desc` | Texte descriptif |
| `#card-ind` | Pied de carte / indicateur |

**Mode Bonus (inversé) :** fond coloré + textes et bordure blancs au lieu du mode normal (fond crème + éléments colorés).

**Mode Dimensionnement :** ajoute la classe `.sizing-mode` sur `#the-card`, ce qui affiche des bordures pointillées rouges et active `resize: both` sur les zones `.resize-zone`.
