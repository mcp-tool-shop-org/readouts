<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.md">English</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/readouts/readme.png" alt="readouts" width="400" />
</p>

<h1 align="center">readouts</h1>

<p align="center">
  Verified, source-backed SQLite knowledge bases that an agent reads one slice at a time.
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/readouts/actions/workflows/verify.yml"><img src="https://github.com/mcp-tool-shop-org/readouts/actions/workflows/verify.yml/badge.svg" alt="verify" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License" /></a>
  <a href="https://mcp-tool-shop-org.github.io/readouts/"><img src="https://img.shields.io/badge/Landing_Page-live-34d399" alt="Landing Page" /></a>
</p>

---

readouts est un ensemble de bases de connaissances sur les outils utilisés par un petit studio de développement de jeux : Rust, Godot, Blender, création de sprites et d’animations, modèles d’IA locaux et les moteurs qui les exécutent et les entraînent, voix chantée, conteneurs GPU et le XRP Ledger.

Chaque base de connaissances (KB) est une base de données SQLite unique avec un index de texte intégral. Chaque entrée indique ses sources, enregistre la phase de recherche qui l’a produite et contient un indicateur `verified`. Seul un verdict provenant d’un vérificateur distinct peut définir cet indicateur ; l’avis personnel de l’auteur sur son travail n’est jamais pris en compte.

Le nom provient de [loadout-os](https://github.com/mcp-tool-shop-org/loadout-os), qui *charge* les connaissances appropriées pour une tâche. readouts est ce qu’il lit.

## Les bases de connaissances

| KB | Quoi | Statut |
|----|------|--------|
| [blender-knowledge](blender-knowledge/) | Pratique actuelle, basée sur le web, de Blender 4.x pour le pipeline de rendu de sprites sans interface graphique du studio (importation d’un GLB généré par TRELLIS → rendu de sprites dans 8 directions via blender --background --python → composition en un jeu 2,5D) ainsi que préparation générale des éléments du jeu. | **219 recettes · 10 domaines · 8 phases · 83/219 vérifiées** |
| [docker-knowledge](docker-knowledge/) | La base de connaissances qui prend en charge le produit gpu-container : comment empaqueter, mesurer et placer les modèles de manière transparente sur une seule GPU. | **160 résultats · 6 domaines · 9 phases · 73/160 vérifiés** |
| [godot-knowledge](godot-knowledge/) | Connaissances actuelles et vérifiées de manière contradictoire pour Godot 4, afin de créer un RPG tactique au tour par tour en 2,5D. | **177 recettes · 6 domaines · 7 phases · 50/177 vérifiées** |
| [model-knowledge](model-knowledge/) | Base de connaissances vérifiée des meilleurs MODÈLES d’IA générative locaux par objectif (image / édition / contrôle / vidéo / 3D / audio / LLM / légende) pour la configuration RTX 5090, avec une priorité accordée aux licences commerciales. | **129 modèles · 9 domaines · 19 phases · 126/129 vérifiés** |
| [rust-knowledge](rust-knowledge/) | Rust vérifié pour la création de si-rpg-engine (essentiel, avancé et comment le moteur l’utilise : ABI WASM brut, déterminisme des nombres à virgule flottante, état et restauration de Rapier 0.35, octets reproductibles) et une première étape pour la législation musicale de si-jam-sessions, chaque vérification de code étant effectuée par le compilateur rustc 1.98.1. | **267 recettes · 27 domaines · 4 phases · 266/267 vérifiées** |
| [sprite-motion-knowledge](sprite-motion-knowledge/) | La technique portable d’animation de sprites pour cette configuration | **246 recettes · 19 domaines · 8 phases · 170/246 vérifiées** |
| [sprites-knowledge](sprites-knowledge/) | La technique portable de création d’illustrations conceptuelles → sprites 2,5D prêts pour le jeu pour cette configuration | **215 recettes · 8 domaines · 6 phases · 92/215 vérifiées** |
| [tensor-engine-knowledge](tensor-engine-knowledge/) | Base de connaissances vérifiée des MOTEURS qui exécutent et entraînent les modèles d’IA localement sur la configuration RTX 5090 (Blackwell / sm_120 / Windows). | **193 moteurs · 10 domaines · 17 phases · 134/193 vérifiés** |
| [training-knowledge](training-knowledge/) | Base de connaissances vérifiée des TECHNIQUES d’ENTRAÎNEMENT portables : méthodes, recettes, valeurs d’hyperparamètres, connaissances sur les ensembles de données et l’évaluation : pour l’entraînement de LoRA / affinage sur la configuration RTX 5090 unique (Blackwell / Windows / WSL2). La couche de savoir-faire pour l’entraînement entre les poids (connaissances du modèle) et le logiciel (connaissances du moteur de tenseur). | **204 techniques · 13 domaines · 16 phases · 101/204 vérifiées** |
| [vocology-knowledge](vocology-knowledge/) | Technique de voix chantée : vocologie (source-filtre, registres, formant de chanteur), prosodie musicale par rapport à la prosodie de la parole, alignement des paroles sur les notes, SVS contrôlable par partition par rapport aux générateurs de chansons à partir de paroles, évaluation de l’admission/de l’enseignement | **317 résultats · 19 domaines · 13 phases · 214/317 vérifiés** |
| [xrpl-knowledge](xrpl-knowledge/) | Base de connaissances vérifiée de l’ÉCOSYSTÈME XRP Ledger pour un développeur : fonctionnalités du protocole, types de transactions, normes XLS, bibliothèques et outils clients : chacun étant étiqueté avec son statut actuel sur le réseau principal / en cours d’amendement. Écosystème complet : XRPL mainnet + Xahau/Hooks + la chaîne latérale XRPL EVM + la couche institutionnelle (RLUSD, conformité). | **457 capacités · 12 domaines · 10 phases · 362/457 vérifiées** |

Le tableau est généré à partir de [`index.json`](index.json) par `shared/sync_readme_table.py`, et `python verify.py` échoue s’il dérive. [`index.md`](index.md) est la même carte écrite pour les agents, et [`index.html`](index.html) l’affiche.

Chaque dossier KB contient sa base de données, un `catalog/` de pages Markdown générées par domaine, un `waves/` dossier contenant les enregistrements de recherche et de vérification de chaque phase, et sa propre `README.md`.

## Démarrage rapide

```bash
git clone https://github.com/mcp-tool-shop-org/readouts
cd readouts
python verify.py
```

`verify.py` nécessite Python 3.10 ou une version ultérieure et rien d’autre que la bibliothèque standard. Les bases de données sont des fichiers SQLite ordinaires, de sorte que tout client SQLite peut les ouvrir.

Recherchez dans une KB via son index de texte intégral, puis rejoignez-la à l’entrée :

```sql
-- sqlite3 rust-knowledge/rust.db
SELECT r.name, r.verified
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'rapier'
LIMIT 5;
```

Ajoutez `AND r.verified = 1` pour ne conserver que ce que le vérificateur a confirmé. Le même modèle fonctionne dans chaque KB. Le nom de la table d’entités est indiqué dans [`index.md`](index.md) : `recipes`, `findings`, `models`, `engines`, `techniques` ou `capabilities`, chacun ayant un index `<table>_fts` correspondant. La plupart des KB ont également une vue `v_recommended` (docker-knowledge et vocology-knowledge ont `v_load_bearing`). Ces vues sélectionnent en fonction du champ de recommandation de chaque KB, et non en fonction de `verified`.

## Comment une entrée obtient-elle `verified`

1. **Une phase de recherche.** Un fil de recherche par domaine rédige des entrées, et chaque entrée cite ses sources sous forme de paires `{url, claim}`.
2. **Un vérificateur distinct.** Un deuxième agent, qui n’a jamais accès au raisonnement du chercheur, vérifie chaque entrée par rapport aux pages qu’elle cite et renvoie un verdict. Dans la plupart des phases, ce vérificateur provient de la même famille de modèles que le chercheur ; certaines phases ajoutent un membre d’une famille différente. L’enregistrement de chaque phase indique lequel.
3. **Une définition de `verified`.** `verified = 1` uniquement lorsque ce verdict externe l’indique ([`shared/verdicts.py`](shared/verdicts.py)). Une entrée sans verdict reste non vérifiée. Considérez-la comme une piste, et non comme un fait.
4. **Un compilateur, lorsqu’il y a du code.** Chaque vérification de code dans rust-knowledge est compilée, et, le cas échéant, exécutée par `rustc 1.98.1`. Une recette dont l’exemple échoue à la compilation n’est jamais vérifiée.

Chaque itération conserve son historique dans le dossier `waves/` du KB : `dispatch.md` (ce qui a été demandé et ce qui a été renvoyé), `research-raw.json` (ce qui a été chargé) et, lorsque l’itération en a une, `verification.md` (ce que le vérificateur et le compilateur ont trouvé). Les KB qui conservent un registre de verdicts durable le conservent dans `verification/verdicts.json`.

## Attribuer un agent à une tranche

Deux index de configuration empêchent un agent de lire l’ensemble du corpus :

1. Le fichier racine [`.claude/loadout/index.json`](.claude/loadout/index.json) attribue une tâche au KB approprié.
2. Le fichier `.claude/loadout/index.json` de chaque KB l’attribue au domaine approprié à l’intérieur de ce KB.

```bash
npx @mcptoolshop/loadout-os validate .claude/loadout/index.json
npx @mcptoolshop/loadout-os resolve --project .
```

`resolve` fusionne également votre propre couche de configuration globale si vous en avez une.

## Vérifiez vous-même le corpus

`python verify.py` est la base du référentiel. Il vérifie que les fichiers générés sont exacts par rapport aux bases de données : que chaque rowid de texte intégral est associé à son entrée correspondante, qu’aucune entrée vérifiée ne manque de source, que `verified` renvoie à un verdict externe, que la page d’accueil et le tableau de ce fichier README correspondent aux bases de données, et qu’aucun lien relatif n’est rompu.

- `FAIL` viole un contrat ou fournit des données incorrectes. Il bloque la publication.
- `WARN` est un défaut réel, connu, limité et enregistré.

Chaque résultat FAIL et WARN contient un code stable et une indication pour l’étape suivante. `python verify.py --json` affiche un objet JSON par vérification. Le code de sortie est 0 en cas de succès, 1 en cas de FAIL et 2 si la vérification elle-même a échoué. CI l’exécute à chaque envoi qui modifie le corpus.

## Sécurité et modèle de menace

- **Ce qu’est ce référentiel :** des données. Il contient des bases de données SQLite, du markdown, du JSON et les scripts Python qui les ont créés. Rien ne s’exécute lors de l’installation, et il n’y a rien à installer.
- **Le chemin de lecture est local.** Interroger une base de données, `verify.py`, et les générateurs (`regen.py`, `shared/gen_*.py`, le fichier `load_db.py` de chaque KB, `gen_catalog.py` et `gen_loadout.py`) lisent les fichiers de ce répertoire et n’écrivent que les fichiers dérivés à l’intérieur. Ils n’établissent aucune connexion réseau, ne lisent aucun identifiant et n’envoient aucune télémétrie. `verify.py` n’écrit rien du tout.
- **Les outils de recherche ne le sont pas.** Les scripts conservés comme enregistrement de la façon dont les itérations ont été créées (par exemple, chaque `verify_cloud.py`, le fichier `openrouter_lane.py` de rust-knowledge et le fichier `verifier/` de tensor-engine-knowledge) appellent un modèle : un démon Ollama local ou OpenRouter avec un `OPENROUTER_API_KEY` que vous définissez dans l’environnement. Certains récupèrent également les pages qu’ils citent. Aucune clé n’est stockée dans le référentiel. `compile_oracle.py setup` télécharge les crates Rust épinglés via cargo, une seule fois. Aucun de ces éléments ne s’exécute à moins que vous ne l’exécutiez.
- **Autorisations :** accès en lecture au répertoire ; accès en écriture uniquement si vous régénérez.
- **Aucune télémétrie**, nulle part dans le référentiel.
- **Le contenu :** notes de recherche avec citations. Une entrée non vérifiée est une piste, pas un fait. Les notes de licence concernant les modèles, les ensembles de données et les crates ne constituent pas un avis juridique ; lisez la licence elle-même avant de distribuer quoi que ce soit.

Pour signaler un problème, consultez le fichier [SECURITY.md](SECURITY.md).

## Maintenance

[MAINTENANCE.md](MAINTENANCE.md) est le manuel d’utilisation : ajout d’une itération ou d’un KB, exécution d’une analyse de vérification et les pièges qui ont déjà coûté une après-midi à quelqu’un. [CONVENTIONS.md](CONVENTIONS.md) décrit la structure que chaque KB partage. Le [manuel](https://mcp-tool-shop-org.github.io/readouts/handbook/) explique en détail l’interrogation, la vérification et le routage. Les modifications sont répertoriées dans [CHANGELOG.md](CHANGELOG.md).

## Licence

[MIT](LICENSE)

---

Créé par <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
