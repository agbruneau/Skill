# CLAUDE.md — Skill

Collection de directives comportementales et de prompts systèmes pour différents modèles d'IA (LLM). Sert de base de connaissances en ingénierie de prompts pour standardiser et optimiser les réponses de chaque système.

## Projet

- **Auteur** : André-Guy Bruneau
- **Type** : Prompt engineering knowledge base
- **Langues** : Français (principal), Anglais (Claude.md)

## Contenu

| Fichier | Cible | Domaine |
|---------|-------|---------|
| `Claude.md` | Claude (Anthropic) | Directives de développement logiciel |
| `Gemini.md` | Gemini (Google) | Architecture d'entreprise, rigueur absolue, citations traçables |
| `OIA.md` | Méthode O.I.A. | Analyse théologique/biblique (Observation, Interprétation, Application) |
| `Perplexcity.md` | Perplexity | Recherche technique, format pyramidal, concision |
| `Theo.md` | Framework théologique | Théologie réformée (VERSION 3.0), herméneutique littérale-grammaticale-historique |

## Conventions

- Chaque fichier est autonome et auto-contenu.
- Les fichiers AI (`Claude.md`, `Gemini.md`, `Perplexcity.md`) définissent persona, style de réponse et protocoles de citation.
- Les fichiers théologiques (`OIA.md`, `Theo.md`) définissent des cadres méthodologiques rigoureux.
- Branche principale : `main`

## Directives pour Claude

1. **Ce fichier est auto-référentiel** : Claude.md dans ce dépôt définit les directives *pour* Claude. Les modifications ici affectent le comportement de Claude dans ce contexte.
2. **Cohérence inter-fichiers** : Les principes de rigueur, citation et clarté sont communs à tous les fichiers — ne pas introduire de contradictions.
3. **Pas de fusion** : Chaque fichier cible un système distinct. Ne pas mélanger les conventions de Gemini dans Perplexcity, etc.
4. **Respect du cadre théologique** : `Theo.md` et `OIA.md` suivent une tradition réformée précise. Ne pas modifier les présupposés doctrinaux sans instruction explicite.
5. **Versioning** : `Theo.md` est versionné (VERSION 3.0). Incrémenter le numéro de version lors de modifications substantielles.
6. **Format** : Markdown pur, pas de dépendances, pas de build system.
