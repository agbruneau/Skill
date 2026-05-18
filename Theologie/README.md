# TheoSkills

Skills d'IA pour la préparation de prédications **dans la tradition Baptiste Réformée**, principalement orientés sur l'enseignement expositif de **John MacArthur**. Conçus pour [Claude Code](https://claude.ai/code) et compatibles avec les Projects de Claude.ai.

Ce dépôt est un fork allégé de [pastor-ai-skills](https://github.com/tkcostello/pastor-ai-skills) de Thomas Costello, recentré sur la préparation de prédications (sermon prep) et **repositionné sur une posture confessionnelle explicite** (1689 LBCF, soteriologie calviniste, cessationnisme, Lordship salvation, complémentarisme, prémillénialisme dispensationaliste à la MacArthur). Les autres familles de skills (communication écrite, repurposing, médias sociaux, rythme pastoral) du dépôt original ne sont pas incluses ici.

> **Posture théologique assumée.** Ce n'est pas un toolkit neutre. Si vous cherchez une boîte à outils évangélique généraliste, c'est le dépôt original de Thomas Costello qu'il vous faut. Si vous êtes Baptiste Réformé et que vous prêchez dans la lignée de MacArthur (ou de Spurgeon, ou de la 1689), vous êtes au bon endroit.

---

## Les skills disponibles

Deux familles de skills cohabitent dans ce dépôt : la **préparation de prédication** (sermon-prep) pour le travail pastoral hebdomadaire, et l'**analyse théologique académique** (analyse-theologique) pour l'exégèse rigoureuse et la dogmatique systématique.

| Skill | Famille | Rôle | Dépendances |
|---|---|---|---|
| `pastor-foundation` | foundation | Couche de contexte partagée : posture confessionnelle Baptiste Réformée + MacArthur, voix pastorale, variables d'église, garde-fous, standards de sortie. Requis par tous les autres skills. | — |
| `/sermon-research` | sermon-prep | Recherche approfondie sur un passage à travers une lentille Baptiste Réformée : commentaires hiérarchisés (MacArthur, Calvin, Spurgeon, Owen, Schreiner...), contexte historique, études de mots, doctrines réformées en jeu, pistes de réflexion. **Sortie en français** (PDF formaté Quiet Doctrine **+ Markdown jumelé**). | `reportlab` + polices fournies |
| `/sermon-brainstorm` | sermon-prep | Session interactive qui produit un brief de prédication expositif, ancré dans l'intention auctoriale, la doctrine réformée et la grâce souveraine. | `reportlab` |
| `/sermon-series` | sermon-prep | Plan de série, par défaut **exposition consécutive d'un livre** (modèle Grace Community Church). Séries doctrinales topiques en option. **Sortie PDF + Markdown jumelé.** | `reportlab` |
| `/oia-reformee` | analyse-theologique | Analyse théologique O.I.A. (Observation, Interprétation, Application) en français académique dense, sous cadre Baptiste Réformé MacArthurien (1689-MA, WCF ou 3FU). Mode péricopal (passage biblique) ou non-péricopal (*locus* doctrinal, apologétique). Sortie texte/markdown structuré, NEG 1979 + LSB, NA28/BHS. | — |

> **Note sur la langue.** `/sermon-research` est entièrement francophone (en-têtes, étiquettes, tableau, footer). `/oia-reformee` est nativement francophone (français académique strict). `/sermon-brainstorm` et `/sermon-series` produisent encore en anglais par défaut ; configurez `LANGUAGE: Français` et `BIBLE_TRANSLATION: S21` (ou Darby, NEG 1979, LSG) dans `pastor-foundation` pour orienter leurs sorties textuelles vers le français — la mise en page graphique de leurs PDFs reste pour l'instant en anglais (à migrer sur le même modèle que sermon-research si besoin).

---

## Mode de fonctionnement et orchestration

Voici un résumé pratique des trois skills et de la façon dont ils s'enchaînent.

### Vue d'ensemble

| Skill | Rôle | Entrée | Sortie |
|---|---|---|---|
| **`/sermon-series`** | Planifier une série multi-semaines | Thème, livre biblique, nombre de semaines | PDF + Markdown jumelé : 3 titres, table hebdomadaire (passage + big idea + fil conducteur), arc, notes pratiques |
| **`/sermon-brainstorm`** | Partenaire de réflexion interactive | Un passage ou un sujet flou | PDF : *Sermon Brief* (big idea, tension, audience, réponse désirée, le « turn », illustration) |
| **`/sermon-research`** | Recherche exégétique en profondeur | Un passage précis | PDF + Markdown jumelé en français : contexte, arrière-plan, étude de mots, commentateurs (MacArthur, Calvin, Spurgeon, Schreiner…), références croisées, thèmes, *thinking prompts* |

Tous trois opèrent sous le cadre **Baptiste réformé / MacArthur** posé par `pastor-foundation` (TULIP, cessationnisme, Lordship, dispensationnalisme prémillénariste avec mention honnête du 1689 LBCF amillénariste).

### Distinction clé

- **`/sermon-brainstorm` ne fait PAS de recherche** — c'est un dialogue maïeutique pour faire émerger *ce que toi tu veux dire*.
- **`/sermon-research` ne fait PAS de structure ni de brainstorm** — c'est de la matière première exégétique.
- **`/sermon-series` ne fait PAS de sermon individuel** — c'est l'architecture macro.

Aucun des trois n'écrit le sermon. C'est volontaire.

### Workflow recommandé

**Phase 1 — Macro (1× par trimestre/semestre)**

1. `/sermon-series` → choisir le livre/thème, obtenir la table hebdomadaire avec passage + big idea provisoire pour chaque semaine.

**Phase 2 — Micro (chaque semaine, lundi-mardi)**

2. `/sermon-research` sur le passage de la semaine → PDF de recherche en français. *Fais ça en premier* : tu veux que le texte parle avant de projeter ce que tu veux dire.
3. `/sermon-brainstorm` avec la recherche en main → conversation guidée qui produit le *Sermon Brief* (big idea affinée, tension, le « turn », l'illustration). La recherche nourrit tes réponses au lieu de les fabriquer.

**Phase 3 — Rédaction (mercredi-samedi)**

4. À toi : structure, manuscrit, prière. Les skills s'arrêtent au brief.

### Pourquoi cet ordre (research → brainstorm)

La séquence inverse (brainstorm avant recherche) est tentante mais piège : tu verrouilles ton angle avant que le texte ait pesé sur toi. Faire la recherche d'abord laisse l'autorité au passage ; le brainstorm devient alors un outil pour *clarifier ce que le texte t'a déjà dit*, pas pour *décider ce que tu vas lui faire dire*.

L'exception : si tu es complètement bloqué (« je prêche dimanche et je n'ai rien »), `/sermon-brainstorm` peut venir en premier juste pour débloquer le passage à choisir, puis tu reviens à la recherche.

### Et `/oia-reformee` dans tout ça ?

`/oia-reformee` n'appartient pas au workflow hebdomadaire de prédication — c'est un **skill d'analyse théologique académique**, à mobiliser quand on veut une exégèse rigoureuse, dense, citable, sous gabarit strict (voir la section dédiée plus bas). Différence pratique :

- `/sermon-research` te livre un PDF de **matière première pastorale** (commentateurs, contexte, mots, thèmes, pistes de réflexion) que tu peux annoter en marge dimanche matin.
- `/oia-reformee` te livre un **dossier exégétique académique** (critique textuelle, analyse grammaticale détaillée, sources hiérarchisées avec citations reconductibles, calibrage épistémique, mention nominative des positions réfutées) en français académique dense.

Les deux sont complémentaires : `/oia-reformee` peut nourrir la rigueur doctrinale d'une recherche faite par `/sermon-research`, ou répondre à une question apologétique posée par un membre de l'assemblée, ou préparer un cours d'école du dimanche sur un *locus* (justification, Israël/Église, cessationnisme…), sans être dans une logique de prédication dominicale.

---

## Le skill `/oia-reformee` — analyse théologique approfondie

Ce skill produit une analyse théologique selon la méthode classique **O.I.A.** (Observation → Interprétation → Application), en français académique dense, sous un gabarit strict. Il est conçu pour le travail doctrinal sérieux : exégèse fine, défense apologétique, comparaison translationnelle, étude lexicale.

### Quand l'invoquer

Mobiliser `/oia-reformee` chaque fois que la requête porte sur :

- **Exégèse d'une péricope biblique** avec le besoin d'une sortie analytique structurée (critique textuelle, structure littéraire, syntaxe et morphologie verbale, lexique grec/hébreu translittéré + glose, occurrences canoniques).
- **Analyse d'un *locus* doctrinal** (justification, élection, pneumatologie, eschatologie, *imago Dei*, alliance, ordo salutis, etc.) sous cadre confessionnel réformé.
- **Réfutation ou défense apologétique** d'une position doctrinale : pélagianisme, arminianisme, charismatisme, *Free Grace*, *Federal Vision*, *New Perspective on Paul*, *replacement theology*, sotériologie sacramentaire romaine, *open theism*, etc.
- **Comparaison translationnelle** entre NEG 1979, LSB, ESV, CSB, NIV, ou décision textuelle NA28/BHS.
- **Synthèse confessionnelle** sous 1689 LBCF, WCF (Westminster), ou 3FU (Belgique–Heidelberg–Dort).

Le skill se déclenche aussi automatiquement sur des mentions comme **MacArthur**, **Sproul**, **Master's Seminary**, **1689 LBCF**, **dispensationalisme**, **cessationnisme**, **Lordship Salvation**, **sotériologie monergique**, **eschatologie prémillénariste**, **herméneutique grammatico-historique**.

### Quand NE PAS l'invoquer

- **Préparation de prédication hebdomadaire** → utiliser `/sermon-research`, plus orienté usage pastoral, sortie PDF formatée pour annotation.
- **Brainstorm exploratoire ou question floue** → utiliser `/sermon-brainstorm`, dialogue maïeutique.
- **Plan de série de prédication** → utiliser `/sermon-series`.
- **Prose dévotionnelle, prière, communication pastorale, compte rendu lyrique** → ce skill refuse explicitement le registre dévotionnel ; il sort en français académique sans préambule, sans conclusion lyrique.

### Comment l'invoquer

Trois modes d'usage typiques :

**Mode péricopal** (analyse d'un passage)
```
/oia-reformee Romains 9.10-24
```
Le skill produit observation (genre, structure, syntaxe, lexique grec), interprétation (sens auctorial, hiérarchie de sources commençant par MacArthur, *analogia fidei*), application (didactique, élenctique, normative).

**Mode non-péricopal — *locus* doctrinal**
```
/oia-reformee Analyse-moi la doctrine de l'expiation particulière sous cadre 1689-MA, avec réfutation de la position amyraldienne.
```

**Mode non-péricopal — apologétique**
```
/oia-reformee Réfutation de la position continuationniste sur 1 Corinthiens 12-14, avec hiérarchie des arguments cessationnistes.
```

Le cadre confessionnel par défaut est **1689-MA** (1689 London Baptist Confession lue selon Master's Seminary). Pour spécifier un autre cadre, le mentionner explicitement : `…sous cadre WCF` ou `…sous cadre 3FU`.

### Cadres confessionnels disponibles

| Cadre | Confessions | Distinctifs |
|---|---|---|
| **1689-MA** *(défaut)* | *Second London Baptist Confession* (1677/1689) tenue dans la lecture du Master's Seminary | Credo · cessationnisme strict · congrégationalisme à pluralité d'aînés · RPW modérée · **dispensationalisme prémillénariste pré-tribulationaliste** · *Lordship Salvation* · sabbat dominical modéré |
| **WCF** | Westminster (1647) + Catéchismes | Paedo · sabbat strict · presbytérianisme · RPW stricte · amillénarisme historique · théologie de l'alliance covenantale |
| **3FU** | Belgique (1561) · Heidelberg (1563) · Dort (1619) | Paedo · sabbat continental · presbytérianisme · principe normatif souple · amillénarisme historique |

Le cadre nommé est l'**arbitre confessionnel de session** ; les autres confessions sont des témoins externes qui ne renversent pas le cadre.

### Hiérarchie des sources

L'autorité matérielle suivie par le skill, dans l'ordre :

1. **Écriture** (NEG 1979 ; LSB en référence anglaise ; substrats NA28 et BHS) — seule autorité infaillible.
2. **Cadre §0** (1689-MA par défaut) — arbitre confessionnel subordonné.
3. **MacArthur** — autorité exégétique principale (*MacArthur NT Commentary* 33 vol., *MacArthur Study Bible*, *Biblical Doctrine* avec Mayhue, *The Gospel According to Jesus*, *Strange Fire*, *Slave*).
4. **Corpus du Master's Seminary** — Mayhue, Vlach, Snoeberger, Naselli, Chou.
5. **R.C. Sproul** — témoin systématique calviniste classique (avec note de divergence ecclésiologique paedobaptiste).
6. **Bibles d'étude évangéliques** complémentaires (ESV, CSB, NIV).
7. **Corpus réformé classique et puritain** — Calvin, Owen, Spurgeon, Bavinck, Berkhof, Turretin, Hodge, Murray, Beeke / Jones (filtré sur ecclésiologie/eschatologie).
8. **Corpus dispensationaliste de référence** — Ryrie, Pentecost, Saucy, Vlach, Feinberg, Walvoord (avec discernement).

### Ce que la sortie contient

Chaque analyse suit exactement ce gabarit, sans préambule ni conclusion :

- **🏛️ Thèse doctrinale centrale** — cadre confessionnel + synthèse en une phrase.
- **🔍 I. Observation** — péricope/locus, contexte, critique textuelle (NA28/BHS), structure littéraire, analyse grammaticale (syntaxe, morphologie, termes originaux translittérés).
- **📖 II. Interprétation** — sens auctorial, apport exégétique hiérarchisé (MacArthur d'abord, puis TMS, Sproul, corpus réformé classique, comparaisons translationnelles), divergence MacArthur ↔ tradition réformée covenantale si applicable, *analogia fidei*.
- **🛡️ III. Application** — didactique (orthodoxie + réfutation nominative), élenctique (deux questions sondant la conscience), normative (impératif concret *Coram Deo*).
- **🧭 Calibrage épistémique** — texte (certitude), exégèse (forte/contestée + motif), application (prudentielle + réserves).

### Ce que la sortie ne contient JAMAIS

- Aucune salutation, préambule, méta-commentaire, conclusion lyrique, prière ou prose dévotionnelle.
- Aucune psychologisation, allégorisme, lecture subjectivante.
- Aucune citation inventée, référence non-vérifiable, lexique grec/hébreu fabriqué.
- Aucune lecture spiritualisante de la prophétie qui collapse Israël dans l'Église.
- Aucun glissement vers le langage charismatique (« Dieu m'a dit », « j'ai été conduit ») ou vers l'*easy-believism* (« demande Jésus dans ton cœur »).

### Exemples d'invocation

```
/oia-reformee Éphésiens 1.3-14
```
> Analyse péricopale du *prologue eulogique* trinitaire ; doctrine de l'élection inconditionnelle, ordo salutis, sotériologie monergique.

```
/oia-reformee Cessationnisme strict — défense scripturaire et réfutation de la position continuationniste de Wayne Grudem
```
> Mode apologétique non-péricopal ; mobilise *Strange Fire* (MacArthur), *To Be Continued?* (Waldron), 1 Co 13.8-13, Hé 2.3-4, Mc 16.9-20 (note textuelle).

```
/oia-reformee Distinction Israël / Église dans la promesse abrahamique ; sous cadre 1689-MA
```
> Mode non-péricopal eschatologique ; mobilise Vlach (*Has the Church Replaced Israel?*), MacArthur, contre la *replacement theology* covenantale.

```
/oia-reformee Comparaison translationnelle de Romains 3.25 (hilastērion) entre NEG 1979, LSB, ESV, CSB ; implications doctrinales
```
> Mode lexical/translationnel ; tranche entre « propitiation » (LSB) et « expiation » / « sacrifice de réconciliation » (autres) ; implications sur la sotériologie pénale-substitutive.

### Pourquoi cette rigueur

Le skill assume que le travail théologique sérieux est un **acte de fidélité** : la doctrine se manie avec la même précision qu'un texte de droit constitutionnel. Citations reconductibles, sources hiérarchisées, divergences nommées, calibrage épistémique séparant ce qui est certain (le texte) de ce qui est forte exégèse, de ce qui reste prudentiel (l'application). Pas de remplissage rhétorique. Pas d'humilité performative qui dilue la conviction. Pas de polysémie cachée derrière du vocabulaire flou.

C'est l'outil pour le **temps long** de la formation doctrinale — pas pour la pression du dimanche matin (`/sermon-research` est là pour ça).

---

## Structure du dépôt

```
TheoSkills/
├── foundation/
│   └── pastor-foundation/             # SKILL.md + références (traductions bibliques)
├── sermon-prep/
│   ├── sermon-brainstorm/             # SKILL.md + generate-pdf.py
│   ├── sermon-research/               # SKILL.md + generate-pdf.py + sources de commentaires
│   └── sermon-series/                 # SKILL.md + generate-pdf.py
├── analyse-theologique/
│   └── oia-reformee/                  # SKILL.md (gabarit O.I.A. baptiste réformé MacArthurien)
├── shared/
│   ├── pdf_utils.py                   # Helpers communs : palette, styles, layout, footer
│   └── fonts/                         # CrimsonPro (serif éditorial) + ArsenalSC (petites capitales)
└── docs/
    ├── design-philosophy-quiet-doctrine.md   # Manifeste de la mise en page Quiet Doctrine
    └── superpowers/                   # Plans et specs de design interne
```

---

## Mise en page — Quiet Doctrine

Les PDFs générés suivent une philosophie typographique nommée **« Quiet Doctrine »** (voir [`docs/design-philosophy-quiet-doctrine.md`](docs/design-philosophy-quiet-doctrine.md)). En résumé :

- **Polices** : *Crimson Pro* pour le corps de texte (vraie old-style transitional, héritière des coupes du XVIᵉ s.) et *Arsenal SC* pour les en-têtes et étiquettes (vraies petites capitales). Les fichiers TTF sont dans [`shared/fonts/`](shared/fonts/) ; le générateur se rabat automatiquement sur les Type 1 standards (Times/Helvetica) si les polices ne sont pas trouvées.
- **Palette restreinte** : encre profonde bleu-noir (`#1A2438`), bronze patiné (`#8C6B3A`) employé uniquement aux moments-clés, parchemin tiède pour les encadrés. Pas d'or vif, pas de coloration décorative.
- **Marges étroites** (0.75″ tout autour) pour la densité éditoriale, avec interlignage généreux pour la lecture soutenue.
- **Hiérarchie inversée du bandeau de titre** : étiquette en petites capitales (« RECHERCHE EXÉGÉTIQUE ») au-dessus de la référence en grand serif gras (« Luc 17.1-10 »).
- **En-têtes de section** en petites capitales 16pt — repérage visuel net sans rompre la lecture.
- **Tableau d'étude des mots** en composition ouverte : pas de bandeau coloré, filet bold au-dessus + filet fin en dessous des en-têtes, hairlines entre les rangées.
- **Renvois** en liste de définition (référence en gras serif + type en petites capitales mutées, connection en retrait).
- **Pistes de réflexion** dans une boîte ombrée à bordure bronze qui se segmente proprement entre les pages si nécessaire.
- **Aucun bandeau publicitaire** — la marque REACHRIGHT a été retirée du sermon-research (les fonctions restent dans `pdf_utils.py` pour les autres skills si besoin).
- **Sortie Markdown jumelée** — `/sermon-research` et `/sermon-series` produisent un fichier `.md` portant le même nom de base que le PDF, dans le même répertoire, pour réutilisation dans des notes, un blog ou un suivi versionné.

Référence implicite : la Bible de Genève (1560) et l'édition princeps des Institutions de Calvin (Estienne, 1559).

---

## Installation

### Option 1 : Claude Code (recommandé)

Ouvrir Claude Code et coller :

> Installe les skills depuis https://github.com/agbruneau/TheoSkills. Je veux les trois skills de sermon-prep, le skill d'analyse théologique oia-reformee, et la foundation.

Claude clone le repo et copie les skills dans `~/.claude/skills/`, ainsi que le dossier `shared/` (incluant les polices) à `~/.claude/shared/`.

### Option 2 : Installation manuelle

```bash
git clone https://github.com/agbruneau/TheoSkills.git

# Foundation requise pour tous les skills
cp -r TheoSkills/foundation/pastor-foundation ~/.claude/skills/

# Skills de sermon-prep (choisir ceux qu'on veut)
cp -r TheoSkills/sermon-prep/sermon-research ~/.claude/skills/
cp -r TheoSkills/sermon-prep/sermon-brainstorm ~/.claude/skills/
cp -r TheoSkills/sermon-prep/sermon-series ~/.claude/skills/

# Skill d'analyse théologique académique
cp -r TheoSkills/analyse-theologique/oia-reformee ~/.claude/skills/

# Helpers PDF partagés (incluant les polices Quiet Doctrine)
mkdir -p ~/.claude/shared
cp TheoSkills/shared/pdf_utils.py ~/.claude/shared/
cp -r TheoSkills/shared/fonts ~/.claude/shared/
```

### Option 3 : Claude.ai Projects

1. Créer un nouveau Project dans Claude.ai.
2. Coller le contenu de `foundation/pastor-foundation/SKILL.md` dans les instructions personnalisées.
3. Ajouter ensuite le `SKILL.md` du skill voulu.
4. Note : la génération PDF n'est pas disponible dans les Projects ; le contenu est rendu en texte/markdown.

---

## Configuration initiale

Au premier usage, `pastor-foundation` demande quelques détails sur l'église. À renseigner une seule fois :

- `CHURCH_NAME` (requis)
- `PASTOR_NAME` (requis)
- `DENOMINATION` (défaut : Reformed Baptist — 1689 LBCF, tradition expositive MacArthur)
- `ATTENDANCE` (requis)
- `LOCATION` (requis)
- `BIBLE_TRANSLATION` (défaut : **LSB** en anglais ; **S21** en français)
- `LANGUAGE` (défaut : English ; mettre `Français` pour cibler la francophonie)

Ces variables sont reprises automatiquement par chaque skill pour personnaliser ses sorties. Le détail des traductions recommandées (LSB, NASB 1995, ESV, KJV, NKJV en anglais ; S21, NEG 1979, Darby, LSG, KJF en français) figure dans [`foundation/pastor-foundation/references/bible-translations.md`](foundation/pastor-foundation/references/bible-translations.md).

---

## Dépendances

Les trois skills de `sermon-prep` génèrent un PDF via `reportlab` :

```bash
pip install reportlab
```

Claude Code l'installe automatiquement au premier usage si nécessaire. Les polices Crimson Pro et Arsenal SC sont fournies dans [`shared/fonts/`](shared/fonts/) sous licence SIL Open Font License — aucune installation système requise.

---

## Philosophie

- **Les skills de prédication aident à chercher et à réfléchir. Ils n'écrivent jamais la prédication.** La recherche fouille les commentaires et le contexte. Le brainstorm pose des questions. Aucun ne livre un manuscrit.
- **L'analyse théologique académique est un registre distinct.** `/oia-reformee` n'est pas un skill pastoral mais doctrinal : sortie dense, citations reconductibles, calibrage épistémique, gabarit strict. C'est l'outil pour le temps long de la formation, pas pour la pression du dimanche.
- **La foundation impose la cohérence confessionnelle.** Posture théologique, ton, et détails de l'église se propagent automatiquement à chaque skill.
- **Posture explicite, pas neutre.** Quand un texte enseigne l'élection, la propitiation particulière, la dépravation totale ou la persévérance des saints, ces doctrines sont nommées comme vérité biblique, pas comme une école parmi d'autres. Quand MacArthur (dispensationaliste) diverge de la 1689 (largement amillénariste), les deux positions sont nommées honnêtement.
- **Exposition consécutive par défaut.** Pour les séries, le modèle de référence est l'exposition verset par verset d'un livre biblique (modèle Grace Community Church, sur 43 ans). Les séries topiques sont possibles mais ancrées dans la doctrine, jamais dans le « felt-need ».
- **Sortie prête à l'usage.** Pas une ébauche à réécrire. Si plus de 20 % du contenu doit être réécrit, le skill a manqué sa cible.
- **Mise en page comme acte théologique.** La composition de la page n'est pas un emballage : la sobriété typographique reflète la doctrine de la grâce souveraine. Quiet Doctrine est l'esthétique de la conviction qui n'a pas besoin de hausser la voix.

---

## Crédit

Skills originaux par [Thomas Costello](https://github.com/tkcostello) ([REACHRIGHT](https://reachrightstudios.com)). Ce fork garde la même licence MIT.

Modifications de ce fork :

- Périmètre réduit aux trois skills de `sermon-prep` + `pastor-foundation`.
- Nettoyage des familles de skills non utilisées (written-communication, sermon-repurposing, social-media, pastoral-rhythm).
- Repositionnement confessionnel : abandon de la neutralité évangélique généraliste pour une posture **Baptiste Réformée + MacArthur** explicite (1689 LBCF, TULIP, cessationnisme, Lordship salvation, complémentarisme, prémillénialisme dispensationaliste).
- Refonte de `commentary-sources.md` en trois tiers, avec MacArthur, Calvin, Spurgeon, Owen, Schreiner et les standards confessionnels (1689 LBCF, Westminster, Dort) en lentille primaire.
- Refonte de `bible-translations.md` : priorité **LSB > NASB 1995 > ESV > KJV > NKJV** en anglais, ajout des traductions françaises de tradition réformée (S21, NEG 1979, Darby, LSG, KJF). NIV (post-2011), NLT, MSG, TPT et AMP signalés comme inadaptés à la prédication expositive.
- Élargissement de la liste de phrases bannies pour inclure le vocabulaire décisionnel, prosperity-adjacent, expressivism, et soft-continuationism.
- **Localisation française complète de `/sermon-research`** : tous les en-têtes, étiquettes de tableau, libellés de thèmes et footer rendus en français canadien.
- **Retrait des références REACHRIGHT** du PDF de `/sermon-research` (bandeau de fin et mention « Propulsé par » du footer).
- **Refonte typographique « Quiet Doctrine »** : polices Crimson Pro + Arsenal SC bundle, palette mutée (encre profonde + bronze patiné), marges étroites (0.75″), hiérarchie éditoriale, en-têtes de section agrandis (16pt en petites capitales), tableau ouvert sans fond coloré, renvois en liste de définition, encadrés ombrés splittables entre pages.
- **Sortie Markdown jumelée** pour `/sermon-research` et `/sermon-series` : à chaque génération de PDF, un fichier `.md` du même nom de base est produit dans le même répertoire (titres, tables, listes, prompts), pour réutilisation hors PDF (notes, blog, contrôle de version).
- Manifeste de design dans [`docs/design-philosophy-quiet-doctrine.md`](docs/design-philosophy-quiet-doctrine.md).
- **Ajout d'une nouvelle famille `analyse-theologique/`** avec le skill `/oia-reformee` : analyse O.I.A. (Observation, Interprétation, Application) en français académique dense sous gabarit strict, cadre Baptiste Réformé MacArthurien (1689-MA par défaut, WCF / 3FU optionnels). Modes péricopal, *locus* doctrinal, apologétique, comparaison translationnelle. Hiérarchie de sources explicite (MacArthur · TMS · Sproul · corpus réformé classique · corpus dispensationaliste).

## License

MIT.
