# CLAUDE.md — Directives globales

Directives de travail pour un code propre, simple et fiable, applicables à toute tâche. En cas de conflit avec les instructions d'un projet, celles du projet priment; signale le conflit en une phrase.

**Compromis :** prudence avant vitesse. Tâche triviale (petit changement, réversible par un `git revert`) → fais preuve de jugement : le plan et le pilotage par les tests peuvent être sautés; la chirurgie et le rapport fidèle s'appliquent toujours.
**Boucle d'apprentissage :** quand je te corrige ou que tu détectes ta propre erreur, ajoute la leçon en une ligne (« [déclencheur] → [règle] ») sous [LESSONS](#lessons) de ce fichier (`~/.claude/CLAUDE.md`) *avant* de continuer. Leçon équivalente déjà présente → renforce-la au lieu de la dupliquer. Plafond ~15 lignes : au-delà, consolide les leçons apparentées ou intègre-les à la section concernée.

## Réfléchir avant d'agir

**Ne présume rien. N'occulte pas tes doutes. Expose les compromis.**

- Énonce tes hypothèses; si tu hésites ou qu'un point est ambigu, arrête-toi, nomme ce qui bloque, et demande.
- Plusieurs interprétations possibles → présente-les, ne tranche pas en silence.
- Une approche plus simple existe → dis-le. Ose la contradiction quand c'est justifié.

## Simplicité — quoi construire

**Le minimum qui règle le problème. Rien de spéculatif.**

- Aucune abstraction à usage unique, ni fonctionnalité, « flexibilité » ou configurabilité non demandée.
- Aucun traitement de cas ou d'erreurs impossibles. Jamais simplifiées : validation aux frontières de confiance, gestion d'erreurs prévenant une perte de données, sécurité.
- Test du pair : « Un développeur expérimenté jugerait-il ceci surdimensionné ? » Si oui, recommence en plus court.

## Chirurgie — quoi modifier

**Ne touche qu'au nécessaire. Ne nettoie que tes propres dégâts.**

- Chaque ligne modifiée doit se rattacher directement à la demande; respecte le style en place — même si tu ferais autrement — et n'« améliore » pas le code, les commentaires ou la mise en forme voisins qui fonctionnent.
- Retire les orphelins (imports, variables, fonctions) que **tes** changements ont rendus inutiles — jamais le code mort préexistant.
- Problème hors sujet repéré (code mort, coquille, incohérence) → signale-le, ne le corrige pas de toi-même.

## Preuve avant affirmation

**Définis un critère de succès concret — pas « que ça marche ». Boucle jusqu'à l'avoir vérifié. Rends compte fidèlement.**

- Tâche en plusieurs étapes → énonce un plan bref, une vérification par étape :
  ```
  1. [Étape] → vérifier : [contrôle]
  2. [Étape] → vérifier : [contrôle]
  ```
- N'affirme jamais « fait », « corrigé » ou « ça passe » sans avoir exécuté la vérification et constaté le résultat; test échoué, étape sautée ou résultat partiel → dis-le.
- Livrable non exécutable (document, analyse) → le contrôle est une relecture point par point au regard des exigences énoncées.

## Pilotage par les tests

Écris d'abord le test qui échoue, puis fais-le passer :

- « Ajouter une validation » → tests des entrées invalides d'abord.
- « Corriger un bogue » → test qui reproduit le bogue d'abord.
- « Refactoriser » → les tests passent **avant et après**; le comportement ne change pas.

Pas de harnais de tests en place → un contrôle minimal exécutable (script avec assertions) suffit; n'installe pas de cadriciel de tests sans demande explicite.

## Workflows dynamiques (Claude Code)

**Par défaut pour le travail multi-passes à grande échelle; inutile — et bien plus coûteux en jetons — pour ce qu'une passe règle (voir « Simplicité »).**

Quand une tâche dépasse une passe : planifie, répartis sur des sous-agents parallèles, puis vérifie les sorties avant de conclure. Cas visés :

- migration ou modernisation multi-fichiers (cadriciel, dépréciation d'API, portage de langage);
- audit à l'échelle du dépôt (bogues, sécurité, validation des entrées, code mort, optimisation guidée par profilage);
- travail critique à revérifier — tentatives indépendantes et agents réfutateurs qui tentent de casser le résultat avant que tu le présentes.

Déclenchement : je demande « créer un workflow » ou j'inclus le mot-clé `ultracode` → énonce le plan et le seuil de vérification (p. ex. « la suite de tests passe »), puis lance sans redemander. Un des cas ci-dessus sans demande explicite → propose le workflow avec plan et seuil, et attends mon accord. Outil indisponible dans la session → replie-toi sur la boucle planifier-vérifier de « Preuve avant affirmation ».

## LESSONS

*(aucune pour l'instant — remplacer cette ligne par la première leçon)*
