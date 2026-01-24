# Guide complet de la méthode Truby pour StoryKit

## Table des matières
1. [Fondamentaux](#fondamentaux)
2. [Les 7 étapes](#les-7-étapes)
3. [Les 22 étapes (optionnel)](#les-22-étapes)
4. [Web de personnages](#web-de-personnages)
5. [Argument moral](#argument-moral)
6. [Beats de genre](#beats-de-genre)
7. [Prémisse](#prémisse)
8. [Monde et symboles](#monde-et-symboles)
9. [Workflow complet](#workflow-complet)
10. [Commandes StoryKit](#commandes-storykit)

---

## Fondamentaux

### Qu'est-ce que la méthode Truby ?

John Truby propose une approche **organique** de la dramaturgie qui dépasse le schéma traditionnel des "3 actes".
Au lieu de voir l'histoire comme une mécanique linéaire, Truby la conçoit comme un **système vivant** où :

- **Personnages** : chacun incarne des valeurs en tension
- **Intrigue** : découle du conflit de ces valeurs
- **Thème** : émerge des choix moraux des personnages
- **Monde** : reflète les enjeux intérieurs du héros
- **Symboles** : compriment du sens, guident le récit

### Le principe central

**"L'histoire est l'enregistrement des changements de valeurs chez le protagoniste."**

Chaque scène, chaque décision, chaque révélation doit servir ce changement. C'est l'inverse d'une intrigue venue de l'extérieur où le héros est passif.

### Trois piliers

1. **Prémisse** : la "graine" de l'histoire (une phrase + un principe organisateur)
2. **7 étapes** : le squelette structurel (faiblesse → nouvel équilibre)
3. **Argument moral** : la tension thématique (thèse ↔ antithèse ↔ synthèse)

---

## Les 7 étapes

C'est le **squelette** que partagent toutes les bonnes histoires selon Truby. Chaque étape représente un **pivot moral** — un moment où le protagoniste change de compréhension ou est confronté à une vérité.

### 1. Faiblesse & Besoin (Weakness & Need)

**Définition :** Qui est le protagoniste au départ ? Quel est son **handicap moral ou psychologique** ?

Le handicap n'est pas une faiblesse physique, c'est une **limite morale** ou une **croyance erronée** qui le paralyse ou le pousse vers de mauvaises décisions.

**Exemples :**
- Naïveté morale : croire que la loyauté envers les proches prime sur la vérité
- Orgueil : refuser de demander de l'aide
- Peur : éviter de prendre des risques par peur de l'échec
- Culpabilité : se punir pour une erreur passée

**Le besoin :** c'est ce que le protagoniste **doit apprendre** pour évoluer.
- Si sa faiblesse est la naïveté → il doit apprendre le discernement
- Si c'est l'orgueil → il doit apprendre l'humilité
- Si c'est la peur → il doit apprendre le courage

**Fichier StoryKit :** `story/truby/seven_steps.yaml`
```yaml
weakness_need:
  internal: "Description de la faiblesse morale du héros"
  moral_problem: "Ce que cette faiblesse le pousse à faire (ou à ne pas faire)"
```

---

### 2. Désir (Desire)

**Définition :** Qu'est-ce que le protagoniste **veut** au début de l'histoire ?

C'est souvent quelque chose de **superficiel ou trompeur** — ce n'est **pas** ce dont il a besoin.

**Distinction importante :**
- **Désir** (Want) : ce que le personnage croit vouloir
- **Besoin** (Need) : ce qui le transformera réellement

**Exemples :**
- Le désir : trouver un trésor et devenir riche
- Le besoin : apprendre que la richesse ne résout pas la solitude
- Le désir : se venger d'un ennemi
- Le besoin : apprendre le pardon pour pouvoir avancer

**Fichier StoryKit :**
```yaml
desire: "Objectif concret du protagoniste au démarrage de l'histoire"
```

---

### 3. Opposant (Opponent)

**Définition :** Qui ou qu'est-ce qui **s'oppose au désir du protagoniste** ?

L'opposant n'est **pas nécessairement le méchant**. C'est celui qui a des **intérêts incompatibles** avec le protagoniste.

**Point clé :** L'opposant doit avoir sa propre logique et ses propres raisons. Il croit sincèrement qu'il a raison.

**Exemples :**
- Un parent qui refuse le rêve de l'enfant (pour le "protéger")
- Un rival en amour qui veut le même prix
- Un système bureaucratique qui bloque l'accès à quelque chose
- Un allié qui veut une chose incompatible avec ce que le héros cherche

**Fichier StoryKit :**
```yaml
opponent:
  name: "Nom ou description de l'opposant principal"
  strategy: "Comment l'opposant s'oppose au héros (ses méthodes, ses arguments)"
```

---

### 4. Plan (Plan)

**Définition :** Comment le protagoniste **compte-t-il** résoudre le conflit ?

C'est la **stratégie initiale** du héros. Elle sera souvent brisée ou contredite par les événements.

**Important :**
- Le plan révèle la **personnalité** du héros
- Il montre son niveau de **compréhension** du problème réel
- Il doit être **plausible** — pas juste "prier que tout s'arrange"

**Exemples :**
- Négocier directement avec l'adversaire
- Rassembler des preuves clandestinement
- Monter une contre-équipe
- Prouver que l'opposant a tort en réussissant seul

**Fichier StoryKit :**
```yaml
plan: "La stratégie initiale du protagoniste pour atteindre son désir"
```

---

### 5. Bataille (Battle)

**Définition :** L'**affrontement direct** entre le héros et l'opposant (ou ses conséquences).

Ce n'est pas nécessairement violent. C'est le moment où :
- Les deux forces sont au maximum
- Les enjeux sont les plus élevés
- Un choix **doit** être fait

**Caractéristiques :**
- C'est le **climax** de l'histoire
- Tout ce qui précède converge vers ce moment
- Le héros doit **risquer quelque chose** (sa vie, son amour, sa dignité)

**Exemples :**
- Duel physique ou verbal
- Révélation publique de la vérité
- Ultimatum ou confrontation finale
- Destruction mutuelle ou sacrifice

**Fichier StoryKit :**
```yaml
battle: "L'affrontement majeur du héros avec l'opposant ou les conséquences de son plan"
```

---

### 6. Auto-révélation (Self-revelation)

**Définition :** Qu'est-ce que le protagoniste **apprend sur lui-même** lors de la bataille ?

C'est le moment de **vérité**. Le héros comprend enfin :
- Ce qui le bloquait vraiment
- Ce que sa faiblesse initiale lui a coûté
- Comment il a changé (ou refuse de changer)

**Points clés :**
- C'est une **compréhension interne**, pas une action
- Elle découle **naturellement** de ce qu'il a vécu
- Elle peut être amère ou joyeuse, mais elle est **vraie**

**Exemples :**
- "Ma loyauté aveugle m'a rendu complice du mensonge"
- "J'ai enfin compris que je méritais d'être aimé malgré mes défauts"
- "La vengeance ne résout rien ; seul le pardon peut me libérer"
- "Je n'étais pas assez courageux pour affronter ma peur — j'ai choisi de fuir"

**Fichier StoryKit :**
```yaml
self_revelation: "Ce que le protagoniste apprend sur lui-même suite à la bataille"
```

---

### 7. Nouvel équilibre (New Equilibrium)

**Définition :** Quel est l'**état final** du protagoniste et du monde ?

Ce n'est pas nécessairement un "happy ending". C'est simplement le nouvel équilibre après la transformation.

**Important :**
- Les conséquences du changement sont **réelles et durables**
- Le héros a changé, le monde a changé
- Le coût du changement est **visible**

**Exemples :**
- Le héros a sauvé le jour mais a perdu quelqu'un qu'il aimait
- Il a trouvé son amour mais a dû abandonner sa vie antérieure
- Il a vaincu l'opposant mais a compris qu'il lui ressemblait trop
- Il a accepté son destin et peut enfin avancer

**Fichier StoryKit :**
```yaml
new_equilibrium: "L'état du protagoniste et du monde après la transformation"
```

---

## Les 22 étapes

Les **22 étapes** sont une **extension optionnelle** des 7 étapes. Elles détaillent les **pivots** (révélations, décisions, retournements) qui rendent la progression plus **précise** et **surprenante**.

### Structure des 22 étapes

```
01. Weakness, Need, Desire    → Démarrage (faiblesse exposée)
02-06. Première montée        → Exposition et complications
07. First revelation           → Première révélation majeure
08-14. Développement          → Exploration des possibilités
15. Midpoint reversal         → Retournement du milieu (tout change)
16-20. Montée finale          → Convergence vers la bataille
21. Battle                    → Affrontement majeur
22. New equilibrium           → Nouvel équilibre
```

### Quand les utiliser ?

- **Histoires courtes (< 50 pages)** : les 7 étapes suffisent amplement
- **Romans (100-300 pages)** : les 22 étapes aident à structurer sans laisser de vides narratifs
- **Sagas ou épopées** : les 22 étapes + subdivisions par chapitre ou arc

### Comment les appliquer

1. Commencez par les **7 étapes**
2. Identifiez les **2-3 pivots majeurs** (révélations qui changent la donne)
3. Placez-les stratégiquement (pas trop tôt, pas trop tard)
4. Remplissez les étapes intermédiaires avec des **complications** et des **pistes fausses**

**Fichier StoryKit :** `story/truby/twenty_two_steps.yaml`

---

## Web de personnages

### Concept fondamental

Truby dit : **"Chaque personnage représente une position dans le débat moral de l'histoire."**

**Mauvaise approche :** "Voilà mon personnage, il a un défaut et une force"
**Bonne approche :** "Voilà mon personnage, il incarne cette valeur **contre** celle-ci"

En autres termes, les personnages ne sont **pas des individus isolés**. Ils sont les **incarnations des tensions morales** de votre histoire.

### Structure du web

**Chaque personnage a :**
1. **Fonction dramatique** : quel rôle joue-t-il dans l'arc du héros ?
   - Protagoniste (le héros)
   - Opposant (le bloqueteau)
   - Allié (aide le héros)
   - Mentor (enseigne une leçon)
   - Mentor inverse (incarne ce que le héros ne doit PAS devenir)

2. **Valeurs en tension** : quelles valeurs défend ce personnage ?
   - Le héros croit en : "La loyauté prime sur tout"
   - L'opposant croit en : "Le pouvoir prime sur la morale"

3. **Contraste** : comment ce personnage contraste-t-il avec les autres ?
   - Intellectuel vs impulsif
   - Idéaliste vs pragmatique
   - Collectif vs individuel

### Exemple

```yaml
characters:
  - id: hero
    name: "Nora"
    function: "protagoniste"
    values: ["vérité", "justice", "responsabilité"]
    weakness: "Naïveté morale"
    
  - id: opponent
    name: "Victor"
    function: "opposant"
    values: ["pouvoir", "richesse", "contrôle"]
    strategy: "Acheter les témoins, tuer les preuves"
    
  - id: mentor_false
    name: "Darzac"
    function: "mentor inverse"
    values: ["efficacité", "obéissance", "pragmatisme"]
    lesson: "Montre à Nora ce qu'elle deviendra si elle abandonne son éthique"
    
  - id: mentor_true
    name: "Sofia"
    function: "alliée"
    values: ["vérité", "méthode", "intégrité"]
    lesson: "Confirme à Nora que la vérité est possible sans compromis"
```

### Règle d'or

**Pas de personnage sans fonction dramatique.**
Si un personnage ne sert pas à explorer une **tension de valeurs**, supprimez-le ou donnez-lui un rôle clair.

**Fichier StoryKit :** `story/truby/character_web.yaml`

---

## Argument moral

### Concept

L'**argument moral** est le **débat central** de ton histoire, incarné par les **choix** du héros.

Ce n'est **pas** un message qu'on plaque artificiellement sur l'histoire.
C'est le **cœur** qui fait battre l'intrigue entière.

### Structure

**Thèse** (point de départ du héros)
↔
**Antithèse** (la position opposée, incarnée par l'opposant ou une tentation)
↔
**Synthèse** (ce que le héros apprend à travers ses choix)

### Exemples

#### Exemple 1 : Loyauté vs Vérité
```
Thèse : "La loyauté envers les proches prime sur la vérité"
        → Nora protège ses sources même si c'est un mensonge

Antithèse : "La transparence absolue détruit les liens"
           → Révéler tout expose tout le monde au danger

Synthèse : "Dire la vérité avec méthode et preuves est juste,
           même si le prix personnel est réel"
          → Nora publie et accepte les conséquences
```

#### Exemple 2 : Liberté vs Sécurité
```
Thèse : "La liberté personnelle est le bien suprême"
Antithèse : "La sécurité du groupe prime sur l'individu"
Synthèse : "La vraie liberté exige de la responsabilité envers les autres"
```

#### Exemple 3 : Ambition vs Humilité
```
Thèse : "Je dois réussir à tout prix"
Antithèse : "L'ambition détruit tout ce qui compte"
Synthèse : "La réussite sans sens creux ; le sens sans effort ne vaut rien"
```

### Incorporer dans l'histoire

L'argument moral **n'est jamais énoncé en paroles**. Il est **incarné par les actes** :

- **Scènes** où le héros choisit une valeur contre l'autre
- **Conséquences** réelles, durables de ce choix
- **Révélation** où le héros comprend enfin l'enjeu profond de ses choix

**Fichier StoryKit :** `story/truby/moral_argument.md`

---

## Beats de genre

### Concept

Chaque **genre** (polar, SF, romance, thriller) s'appuie sur des **beats profonds** — des événements 
structurants que le lecteur attend.

Ces beats ne sont **pas facultatifs** ; respecter la promesse de genre c'est **livrer ces beats**.

### Beats courants par genre

#### Polar / Thriller d'enquête
- Crime ou anomalie révélée + Misdirection initiale (fausse piste)
- Matrice d'enquête (suspects, indices, versions)
- Fausse piste significative (red herring)
- Renversement au milieu (midpoint reversal)
- Révélation méthodologique (le **comment** du crime)
- Pression temporelle (horloge qui tourne, deadline)
- Menace physique ou "rencontre avec la mort"
- Piège et confrontation finale
- Preuve et explication rationnelle
- Restauration de l'ordre, à coût moral réel

#### Science-fiction
- Monde établi avec **une règle inviolable**
- Introduction du **problème** (la règle est brisée)
- Exploration des conséquences
- Révélation du **vrai mécanisme** (pas celui qu'on croyait)
- Affrontement avec le système / l'opposant
- Nouvelle compréhension du monde

#### Romance
- Rencontre et attraction initiale
- Complications (obstacles extérieurs et/ou intérieurs)
- Faux équilibre (rapprochement suivi d'une séparation)
- Point bas (tout semble perdu, désespoir)
- Révélation de vérité et confession
- Nouvel équilibre (réunion, transformation mutuelle)

### Comment les définir dans votre histoire

1. Identifiez votre **genre principal** (et sous-genres)
2. Listez les **beats attendus** par le lecteur
3. Adaptez-les à votre **histoire spécifique**
4. Vérifiez qu'ils **convergent vers votre argument moral**

**Fichier StoryKit :** `story/genre/genre_beats.yaml`

---

## Truby en non-fiction

### Adapter la méthode Truby à la non-fiction

La méthode Truby s'applique aussi à la **non-fiction narrative** (biographies, enquêtes, mémoires, essais narratifs).
La différence clé : au lieu d'un **héros fictif qui change**, c'est le **lecteur qui se transforme** à travers la compréhension.

### Les 7 étapes en non-fiction

**1. Faiblesse & Besoin**
- Quelle est la **fausse croyance** que le lecteur partage avant de lire ?
- Qu'est-ce que le lecteur **ne comprend pas** sur le sujet ?

**Exemple :** "On croit que cet événement historique était un accident ; en réalité, c'était systématique."

**2. Désir**
- Que **veut** le lecteur/l'auteur au départ ?
- Quelle est la **quête superficielle** ?

**Exemple :** "Trouver ce qui est arrivé au juge disparu" (le désir apparent)

**3. Opposant**
- Qu'est-ce qui s'oppose à la **découverte de la vérité** ?
- Souvent : le système, le mensonge, les obstacles pratiques, les témoins réticents

**Exemple :** "Les autorités qui cachent les preuves, les témoins terrifiés, les archives détruites"

**4. Plan**
- Comment le narrateur **va-t-il** chercher la vérité ?
- Quelle est sa **méthodologie** ?

**Exemple :** "Interviews, archives, reconstitution chronologique, comparaison des témoignages"

**5. Bataille**
- Le moment où la **vérité se heurte au mensonge établi**
- Confrontation avec la **complexité** ou la **contradiction**

**Exemple :** "Découvrir que l'histoire officielle contredit les faits; affronter les implications"

**6. Auto-révélation**
- Ce que le **narrateur/lecteur apprend** sur lui-même ou le sujet
- Souvent une **compréhension nuancée** plutôt qu'une réponse définitive

**Exemple :** "Ma recherche m'a montré que je n'étais pas objectif; mes préjugés influençaient mes questions"
ou "La vérité est plus complexe et plus morale que je ne l'imaginais"

**7. Nouvel équilibre**
- Quelle est la **nouvelle compréhension** du sujet ?
- Comment cela **change-t-il notre vision** du monde ?

**Exemple :** "L'histoire doit être réécrite avec cette nouvelle perspective"

### Beats spécifiques de la non-fiction narrative

1. **Sujet établi & contexte** : Présenter qui/quoi/pourquoi c'est important
2. **Question ou énigme** : Formuler le mystère ou la question centrale
3. **Recherche & voyage** : Le processus de découverte (entretiens, archives, observations)
4. **Complications** : Les découvertes qui contredisent les idées préconçues
5. **Tournant majeur** : L'insight qui recontextualise tout
6. **Implications** : Explorer comment cela change notre compréhension
7. **Affrontement/Acceptation de la complexité** : Accepter que la vérité est nuancée
8. **Nouvelle compréhension** : La synthèse finale (ce que nous savons maintenant)

### Argument moral en non-fiction

L'argument moral reste clé, mais il s'articule différemment :

**Exemple : Biographie d'une figure politique controversée**
```
Thèse (croyance initiale du lecteur) : 
"C'était un simple tyran, sans redondance morale"

Antithèse (découverte troublante) :
"Il avait aussi une humanité, des doutes, des raisons compréhensibles"

Synthèse (nouvelle compréhension) :
"La compréhension ne justifie pas les crimes, mais elle rend la situation plus morale, 
plus humaine, plus complexe"
```

### Types de non-fiction & leurs structures

#### Enquête investigative (Reportage)
```
Crime/Anomalie révélée 
→ Investigation 
→ Fausses pistes 
→ Tournant (preuve clé)
→ Affrontement avec les faits
→ Révélation complète 
→ Implications systémiques
```

#### Biographie/Mémoires
```
Sujet présenté
→ Contexte de sa vie
→ Crises & transformations clés
→ Découvertes sur sa vraie nature
→ Comment il a changé le monde
→ Héritage & nouvelle évaluation
```

#### Essai thématique/historique
```
Problème ou question posée
→ Idées courantes sur le sujet
→ Contradiction des idées courantes
→ Nouvelle théorie/framework
→ Applications & exemples
→ Implications pour aujourd'hui
```

### Comment structurer en StoryKit (non-fiction)

**Prémisse :**
```
Quand [auteur/journaliste] enquête sur [sujet/énigme] dans [contexte],
il/elle doit [surmonter obstacles] avant [deadline],
ce qui révèle que [nouvelle compréhension/argument moral].
```

**Exemple :**
```
Quand une historienne enquête sur les fonds publics détournés 
après la catastrophe de 2005,
elle doit reconstituer la chaîne de responsabilité avant que les archives ne soient détruites,
ce qui révèle que l'indifférence institutionnelle était aussi grave que la malveillance.
```

**Argument moral :**
```
Thèse : "Les autorités ont géré la crise au mieux de leurs capacités"
Antithèse : "C'était une incompétence/corruption délibérée"
Synthèse : "C'était systémique — la structure elle-même était défaillante, 
           pas seulement les individus"
```

**Beats de genre :**
```yaml
required_beats:
  - id: nf01
    name: "Sujet établi & contexte"
    description: "Qui, quoi, où, quand, pourquoi ça importe"
    status: locked
  - id: nf02
    name: "Énigme ou question centrale"
    description: "Qu'est-ce qu'on ne sait pas? Qu'est-ce qui est caché?"
    status: locked
  - id: nf03
    name: "Recherche & obstacles"
    description: "Processus de découverte, défis pratiques, résistances"
    status: locked
  - id: nf04
    name: "Révélations mineures & complications"
    description: "Chaque découverte complique la compréhension"
    status: locked
  - id: nf05
    name: "Tournant majeur (Insight)"
    description: "Le moment où la compréhension bascule"
    status: locked
  - id: nf06
    name: "Implications explorées"
    description: "Comment cela change notre vision du sujet/du monde?"
    status: locked
  - id: nf07
    name: "Affrontement/Acceptation de la complexité"
    description: "Accepter que la vérité est nuancée, pas simple"
    status: locked
  - id: nf08
    name: "Synthèse & nouvelle compréhension"
    description: "Ce que nous savons maintenant; leçons extraites"
    status: locked
```

### Conseils pour écrire une non-fiction structurée par Truby

- **Chronologie claire** : le processus de découverte se déploie dans le temps
- **Montrez les fausses pistes** : le lecteur vit votre confusion avant votre clarté
- **Créez de la tension** : "Vais-je trouver la réponse avant que..."
- **Soyez honnête sur vos limitations** : "Voici ce que je ne peux pas savoir"
- **Humanisez les sujets** : même les antagonistes ont des motivations compréhensibles
- **Terminez avec une synthèse morale** : pas juste "voilà les faits", mais "voilà ce que cela signifie pour notre compréhension"

---

## Prémisse

### Définition

Une **prémisse** est une phrase qui contient :
- **Qui** (le protagoniste)
- **La situation** (où, quoi, contexte)
- **L'enjeu majeur** (qu'est-ce qui est en jeu)
- **La révélation thématique** (ce que cette histoire enseigne)

### Formule

```
Quand [situation], [protagoniste] doit [action/choix] avant [deadline/conséquence],
ce qui révèle que [enjeu thématique].
```

### Exemple

```
Quand une journaliste enquête sur la disparition d'un juge anticorruption
dans une ville minée par les intérêts privés,
elle doit démêler un réseau de mensonges avant qu'un faux coupable ne soit sacrifié,
ce qui révèle que la vérité exige un prix personnel.
```

### Principe organisateur

Le **principe organisateur** est la **logique centrale** qui relie tous les éléments.

```
Exemple : "Chaque indice est une histoire concurrente"
        → L'enquête confronte des versions différentes jusqu'à la plus cohérente
        
Exemple : "La transformation morale est plus importante que la solution technique"
        → Même si on résout le crime, le héros change intérieurement

Exemple : "Les cycles se répètent jusqu'à ce que quelqu'un les brise"
        → Les personnages reproduisent des schémas jusqu'à une prise de conscience
```

**Fichier StoryKit :** `story/premise/premise.md`

---

## Monde et symboles

### Monde (Story World)

Le **monde** n'est **pas** juste le cadre. C'est un **personnage** qui **reflète** le conflit interne du héros.

**Exemples :**
- Une ville en ruines où tout est à reconstruire (héros doit se reconstruire)
- Un royaume oppressif où la parole est interdite (héros doit apprendre à parler)
- Un laboratoire stérile où l'humanité est éradiquée (héros lutte pour l'humanité)

### Symboles

Les **symboles** compriment du **sens** ; un objet, un lieu, une action qu'on retrouve tout au long de l'histoire.

**Comment créer des symboles :**

1. Identifiez l'**enjeu central** (loyauté, liberté, vérité)
2. Trouvez un **objet, un lieu ou une action** qui l'incarne
3. Répétez-le, transformez-le au fil de l'histoire

**Exemples :**
- **Objet :** une clé (accès, déverrouillage, secret)
- **Lieu :** un pont (passage, transition, risque)
- **Action :** écrire (vérité, mémoire, contrôle)
- **Palettes :** couleurs qui associent des significations (le rouge = danger/passion, le bleu = froid/sérénité)

**Fichier StoryKit :** `story/truby/symbol_web.yaml` et `story/truby/story_world.md`

---

## Workflow complet

### Étape 1 : Intention (Phase 1)

**Fichiers à remplir :**
- `story/premise/premise.md` : 1 phrase + principe organisateur
- `story/genre/genre_choice.yaml` : genre + beats attendus

**Questions à se poser :**
- Qui est mon héros et qu'est-ce qui le bloque ?
- Qu'est-ce que cette histoire enseigne ?
- Quel genre promets-je au lecteur ?

**Commande StoryKit :**

**Windows (PowerShell) :**
```powershell
../storykit-run.ps1 assemble --target premise
```

**macOS / Linux (Bash) :**
```bash
../storykit-run.sh assemble --target premise
```

---

### Étape 2 : Structure (Phase 2)

**Fichiers à remplir :**
- `story/truby/seven_steps.yaml` : les 7 piliers
- `story/truby/character_web.yaml` : les personnages et leurs rôles
- `story/truby/moral_argument.md` : thèse → antithèse → synthèse
- `story/truby/story_world.md` : le monde + symboles

**Questions à se poser :**
- Quel est le **handicap moral** de mon héros au départ ?
- Qui s'oppose à lui et **pourquoi** (du point de vue de l'opposant) ?
- Qu'est-ce que mon héros doit **apprendre** pour changer ?
- Comment le **monde** reflète ce conflit interne ?

**Commandes StoryKit :**

**Windows (PowerShell) :**
```powershell
../storykit-run.ps1 assemble --target truby7
../storykit-run.ps1 assemble --target truby22  # optionnel
```

**macOS / Linux (Bash) :**
```bash
../storykit-run.sh assemble --target truby7
../storykit-run.sh assemble --target truby22  # optionnel
```

---

### Étape 3 : Scènes (Phase 3)

**Fichiers à remplir :**
- `story/outline/scene_weave.md` : liste des scènes avec leurs enjeux

**Dans chaque scène, demandez-vous :**
- Quelle **valeur** (ou tension de valeurs) est testée dans cette scène ?
- Le héros **change-t-il** de position sur cette valeur ?
- Comment cette scène prépare-t-elle la **révélation finale** ?
- Quel **beat de genre** cette scène remplit-elle ?

**Commande StoryKit :**

**Windows (PowerShell) :**
```powershell
../storykit-run.ps1 assemble --target weave
```

**macOS / Linux (Bash) :**
```bash
../storykit-run.sh assemble --target weave
```

---

### Étape 4 : Rédaction (Phase 4)

**Pour chaque chapitre/scène :**
- Relisez le **scene-weave** et les **7 étapes**
- Vérifiez que la scène **incarne une tension de valeurs** du débat moral
- Assurez-vous que le **dialogue et l'action** révèlent la **personnalité** authentique des personnages
- Vérifiez que vous **respectez le style et la voix** (ton, rythme, focalisation, perspective)

**Commande StoryKit :**

**Windows (PowerShell) :**
```powershell
../storykit-run.ps1 assemble --target draft --chapter 1
```

**macOS / Linux (Bash) :**
```bash
../storykit-run.sh assemble --target draft --chapter 1
```

---

## Bonnes pratiques — Au-delà de la structure

### Conseil 1 : La cohérence des enjeux

Chaque **beat**, chaque **scène** doit illuminer votre **argument moral**. Si une scène ne teste pas une valeur du débat central, c'est qu'elle dilate l'histoire inutilement.

### Conseil 2 : L'authenticité du coût

Le **nouvel équilibre** doit montrer un **prix réel**. Même les "happy endings" coûtent quelque chose — l'innocence perdue, le temps sacrifié, la relation modifiée. C'est ce coût qui rend la transformation **crédible**.

## Commandes StoryKit

### Valider le projet complet

**Windows (PowerShell) :**
```powershell
../storykit-run.ps1 validate
```

**macOS / Linux (Bash) :**
```bash
../storykit-run.sh validate
```

Vérifie que tous les fichiers YAML/Markdown sont cohérents et complets.

### Assembler un prompt pour la prémisse
```powershell
../storykit-run.ps1 assemble --target premise
```
Génère un prompt structuré pour affiner votre prémisse avec une IA.

### Assembler un prompt pour les 7 étapes
```powershell
../storykit-run.ps1 assemble --target truby7
```
Génère un prompt structuré pour développer vos 7 étapes.

### Assembler un prompt pour les 22 étapes
```powershell
../storykit-run.ps1 assemble --target truby22
```
Génère un prompt structuré pour détailler les pivots (étapes 2-20).

### Assembler un prompt pour le scene-weave
```powershell
../storykit-run.ps1 assemble --target weave
```
Génère un prompt structuré pour planifier et séquencer vos scènes.

### Assembler un prompt pour un brouillon de chapitre
```powershell
../storykit-run.ps1 assemble --target draft --chapter 1
```
Génère un prompt structuré pour rédiger un chapitre spécifique.

---

## Checklist finale

Avant de publier ou de présenter, vérifiez que votre histoire :

- [ ] **Prémisse** : 1 phrase claire + principe organisateur explicite
- [ ] **7 étapes** : progression de faiblesse → nouvel équilibre, avec transformation morale réelle
- [ ] **Argument moral** : thèse visible dans les choix du héros, antithèse incarnée, synthèse révélée
- [ ] **Personnages** : chacun incarne une position du débat moral, contrastes clairs
- [ ] **Beats de genre** : tous les beats attendus sont présents et paraissent naturels
- [ ] **Monde & symboles** : le monde reflète l'arc interne du héros, symboles répétés et transformés
- [ ] **Style & Voix** : cohérents et distinctifs du début à la fin
- [ ] **Scènes** : chacune teste une valeur ou tension de l'argument moral
- [ ] **Coût réel** : le nouvel équilibre inclut une **perte** ou **transformation** tangible, pas un happy ending gratuit

---

## Ressources et références

- **Livre fondateur** : *The Anatomy of Story* par John Truby (disponible en anglais, traduction française *La Mécanique de l'Histoire*)
- **Intégration StoryKit** : voir [README.md](README.md), section "Workflow recommandé"
- **Prompts générés** : tous les prompts IA sont générés dynamiquement par la commande `assemble` à partir de vos fichiers YAML/Markdown

---

**Bonne création !**
