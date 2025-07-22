from typing import List, Dict, Union, Tuple
import json
import re
import os


class Personnage:
    def __init__(self, force: int, nom: str):
        self.force = force
        self.nom = nom


class Png(Personnage):
    def __init__(self, nom: str, force: int, dialogue: str):
        super().__init__(force, nom)
        self.dialogue = dialogue

    def __str__(self) -> str:
        return f"nom: {self.nom}, force: {self.force}"

    def parler(self) -> None:
        print(self.dialogue)


class Allie(Png):
    def __init__(self, nom: str, force: int, dialogue: str):
        super().__init__(nom, force, dialogue)


class Ennemi(Png):
    def __init__(self, nom: str, force: int, dialogue: str):
        super().__init__(nom, force, dialogue)


class Ressource:
    def __init__(self, nom: str, quantite: int, utilite: str):
        self.nom = nom
        self.quantite = quantite
        self.utilite = utilite

    def __str__(self) -> str:
        return f"{self.nom}, {self.quantite}, {self.utilite}"


class Lieu:
    def __init__(
        self,
        nom: str,
        description: str,
        ressources: List[Ressource],
        ennemis: List[Ennemi],
    ):
        self.nom = nom
        self.description = description
        self.ressources = ressources
        self.ennemis = ennemis

    def representation(self) -> str:
        print(f"nom: {self.nom}, description: {self.description}")
        print("Voici la liste des ressources.")
        for ressource in self.ressources:
            print(ressource)
        print("Voici la liste des ennemis.")
        for ennemi in self.ennemis:
            print(ennemi)


class Joueur(Personnage):
    """Cette classe représente l'avatar du joueur qui à un nom, des points de forces, des points de vie et un inventaire.
    Le joueur peut regarder une carte, peut regarder la liste des alliés dispônible dans la guile des alliés, peut voir sont inventaire,
    peut prendre des objets, peut payer un allié, peut attaquer un ennemi.

    Attributes:
        nom (str): Le nom de l'avatar du joueur que le joeur à choisie au tous début du jeu.
        force (int): Les points de force de l'avatar du joueur.
        vie (int): Les points de vie du joueur. Si il n'y a plus de point de vie, le joueur est mort.
        inventaire (Dict[str, int]): inventaire de l'avatar du joueur.

    Examples:
        >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
        >>> joueur.verification_inventaire()
        {"or": 0}
    """

    def __init__(self, nom: str, force: int, vie: int, inventaire: Dict[str, int]):
        """Initialises un nouveau joueur.

        Args:
            nom (str): Le nom de l'avatar du joueur que le joeur à choisie au tous début du jeu.
            force (int): Les points de force de l'avatar du joueur.
            vie (int): Les points de vie du joueur. Si il n'y a plus de point de vie, le joueur est mort.
            inventaire (Dict[str, int]): inventaire de l'avatar du joueur.
        """
        super().__init__(force, nom)
        self.vie = vie
        self.inventaire = inventaire

    def afficher_lieux(self, lieux: List[Lieu]) -> None:
        """Utlise la carte pour voir tous les lieux disponible et non résolue.

        Args:
            List[Lieu]: Liste d'objet de type lieu qui correspond au lieu disponble sur la carte.

        Exemples:
            >>> lieux = [Lieu(nom="Temple oublié", description="Un temple envahi par la végétation",
            ressources=[Ressource(nom="or", quantite=20, utilite="Acheter de l'aide")],
            ennemis=[Ennemis(nom="Serpent géant", force=8, dialogue="SSSSSh")])]
            >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
            >>> joueur.afficher_lieux(lieux)
            nom: Temple oublié, description: Un temple envahi par la végétation
            Voici la liste des ressources.
            or, 20, Acheter de l'aide
            Voici la liste des ennemis.
            nom: serpent géant, force: 8
        """
        for lieu in lieux:
            lieu.representation()
            print("")

    def afficher_allie(self, allies: List[Allie]) -> None:
        """Utlise le panneaux qui indique la liste des alliés disponible.

        Args:
            List[Allie]: Liste d'objet de type Alliés qui correspond au alliés disponible.

        Exemples:
            >>> Alliés = [Allie(nom="arwen", force = 5, dialogue = "Je peux t'aider à explorer, mais il me faut 10 unités d'or.")]
            >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
            >>> joueur.afficher_allie(Alliés)
            nom: arwen, force: 5
        """
        for allie in allies:
            print(allie)
            print("")

    def verification_inventaire(self) -> None:

        print(self.inventaire)

    def ajout_objet_inventaire(self, ressources: List[Ressource]) -> None:
        for ressource in ressources:
            if ressource.nom in self.inventaire:
                self.inventaire[ressource.nom] += ressource.quantite
            else:
                self.inventaire[ressource.nom] = ressource.quantite
            print(f"Vous avez récupérer {ressource.quantite} de {ressource.nom}")

    def payer_allie(
        self,
        allie: Allie,
    ) -> bool:
        prix = re.search(pattern=r"(\d+) (unités d'or)", string=allie.dialogue)

        if not prix:
            print("Prix non trouver donc c'est gratuit.")
            self.force += allie.force
            return True
        elif int(prix.group(1)) > self.inventaire["or"]:
            print(f"Vous n'avez pas assez d'or pour payer {allie.nom}.")
            return False
        else:
            self.inventaire["or"] -= int(prix.group(1))
            self.force += allie.force
            print("Allié payer avec succés.")
            return True

    def attaquer(self, force_total: int, lieu: Lieu) -> bool:
        if self.force < force_total:
            self.vie -= force_total
            print(
                f"Les ennemis du lieu vous ont fait {force_total} de point de dégats."
            )
            return False
        else:
            print(
                f"Vous avez tuer tous les ennemis du lieu. Vous pouvez donc récupérer toutes les ressources du lieu."
            )
            lieu.ennemis = []
            self.ajout_objet_inventaire(lieu.ressources)
            lieu.ressources = []
            print(f"Vous avez accomplli le lieu {lieu.nom}")
            return True


class Environnement:
    def __init__(self, joueur: Joueur, allies: List[Allie], lieux: List[Lieu]):
        self.joueur = joueur
        self.allies = allies
        self.lieux = lieux


def load_json(
    filename: str,
) -> Dict[str, List[Dict[str, Union[str, List[str], int]]]]:
    """Fonction qui permet de charger des données à partir d'un fichier json.

    Args:
        filename (str): Le nom du fichier à partir duquel il faut charger les données.

    Returns:
        Dict[str, List[Dict[str, Union[str, List[str], int]]]]: Un dictionnaire qui contient
        trois liste de dictionnaire, le premier pour les lieux, le deuxiéme pour les
        personnages et le troisiéme pour les ressources.

    Raises:
        FileNotFoundError: Quand le fichier n'a pas été trouver.
        JSONDecodeError: Si il y a une erreur dans le json du fichier charger.

    Exemples:
        >>> data = load_json("data.json")
        >>> print(data)
        {
            "lieux": [
                {"nom": "Temple Oublié", "description": "Un temple envahi par la végétation", "ressources": ["or", "pierres"], "ennemis": ["serpent géant"]},
                {"nom": "Forêt Maudite", "description": "Une forêt sombre et mystérieuse", "ressources": ["bois", "herbes"], "ennemis": ["loup spectral"]}
            ],
            "personnages": [
                {"nom": "Arwen", "type": "allié", "force": 5, "dialogue": "Je peux t'aider à explorer, mais il me faut 10 unités d'or."},
                {"nom": "Serpent Géant", "type": "ennemi", "force": 8, "dialogue": "Sssss... Tu ne passeras pas !"}
            ],
            "ressources": [
                {"nom": "or", "quantite": 20, "utilite": "Acheter de l'aide"},
                {"nom": "bois", "quantite": 10, "utilite": "Construire des abris"}
            ]
        }
        >>> data = load_json("d")
        Traceback (most recent call last):
            ...
        FileNotFoundError: f"Le fichier {filename} n'a pas été trouver."
        Si il y a une erreur dans le fichier json.
        >>> data = load_json("data.json")
        Traceback (most recent call last):
            ...
        JSONDecodeError: f"Erreur de décodage : {e}"
    """
    try:
        with open(file=filename, mode="r", encoding="utf-8") as fichier:
            data = json.load(fichier)
    except FileNotFoundError as e:
        print(f"Le fichier {filename} n'a pas été trouver.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage : {e}")
        return {}
    return data


def sauvegarder_partie(
    filename: str,
    environnement: Environnement,
) -> None:
    dict_allies = [allie.__dict__ for allie in environnement.allies]
    dict_lieux = []
    for lieu in environnement.lieux:
        ressources = lieu.ressources
        ennemis = lieu.ennemis
        dict_ressources = [ressource.__dict__ for ressource in ressources]
        dict_ennemis = [ennemi.__dict__ for ennemi in ennemis]
        dict_lieux.append(
            {
                "nom": lieu.nom,
                "description": lieu.description,
                "ressources": dict_ressources,
                "ennemis": dict_ennemis,
            }
        )
    dict_environnement = {
        "joueur": environnement.joueur.__dict__,
        "allies": dict_allies,
        "lieux": dict_lieux,
    }
    with open(file=filename, mode="w", encoding="utf-8") as fichier:
        json.dump(dict_environnement, fichier, ensure_ascii=False, indent=2)


def creation_environnement(
    filename: str,
) -> Environnement:
    if os.path.exists("partie_sauvegarder.json"):
        environnement_dict = load_json("partie_sauvegarder.json")
        dict_joueur = environnement_dict["joueur"]
        joueur = Joueur(
            nom=dict_joueur["nom"],
            vie=dict_joueur["vie"],
            force=dict_joueur["force"],
            inventaire=dict_joueur["inventaire"],
        )
        dict_allies = environnement_dict["allies"]
        allies = [
            Allie(
                nom=allie["nom"],
                force=allie["force"],
                dialogue=allie["dialogue"],
            )
            for allie in dict_allies
        ]
        dict_lieux = environnement_dict["lieux"]
        ressources = []
        ennemis = []
        lieux = []
        for lieu in dict_lieux:
            ressources = [
                Ressource(
                    nom=ressource["nom"],
                    quantite=ressource["quantite"],
                    utilite=ressource["utilite"],
                )
                for ressource in lieu["ressources"]
            ]
            ennemis = [
                Ennemi(
                    nom=ennemi["nom"],
                    force=ennemi["force"],
                    dialogue=ennemi["dialogue"],
                )
                for ennemi in lieu["ennemis"]
            ]
            lieux.append(
                Lieu(
                    nom=lieu["nom"],
                    description=lieu["description"],
                    ressources=ressources,
                    ennemis=ennemis,
                )
            )

        environnement = Environnement(joueur=joueur, allies=allies, lieux=lieux)
    else:
        print("Veuillez choisir un nom. Attention vous ne pourrez pas le changer.")
        environnement_dict = load_json(filename)
        nom = input()
        joueur = Joueur(nom=nom, vie=100, force=10, inventaire={"or": 0})
        personnages = environnement_dict["personnages"]
        allies = [
            Allie(
                nom=personnage["nom"].lower(),
                force=personnage["force"],
                dialogue=personnage["dialogue"],
            )
            for personnage in personnages
            if personnage["type"] == "allié"
        ]
        lieux = [
            Lieu(
                nom=lieu["nom"].lower(),
                description=lieu["description"],
                ressources=[
                    Ressource(
                        nom=ressource["nom"],
                        quantite=ressource["quantite"],
                        utilite=ressource["utilite"],
                    )
                    for ressource in environnement_dict["ressources"]
                    if ressource["nom"] in lieu["ressources"]
                ],
                ennemis=[
                    Ennemi(
                        nom=personnage["nom"].lower(),
                        force=personnage["force"],
                        dialogue=personnage["dialogue"],
                    )
                    for personnage in personnages
                    if personnage["type"] == "ennemi"
                    and personnage["nom"].lower() in lieu["ennemis"]
                ],
            )
            for lieu in environnement_dict["lieux"]
        ]
        environnement = Environnement(joueur=joueur, allies=allies, lieux=lieux)
    return environnement


def choix_allies(environnement: Environnement):
    if len(environnement.allies) == 0:
        print("Il n'y a plus d'allies disponible.")
    else:
        environnement.joueur.afficher_allie(environnement.allies)
        print(
            "Sélectionner le nom de l'allié que vous voulez sélectionner ou sélectionner -1 pour ne rien choisir."
        )
        choix_allie = input().lower()
        if choix_allie == "-1":
            print("Aucun allie choisie.")
        elif choix_allie not in [allie.nom for allie in environnement.allies]:
            print("L'allie sélectionner n'est pas disponible.")
        else:
            for allie in environnement.allies:
                if allie.nom == choix_allie:
                    if environnement.joueur.payer_allie(allie):
                        environnement.allies.remove(allie)


def choix_lieux(environnement: Environnement):
    environnement.joueur.afficher_lieux(environnement.lieux)
    print(
        "Sélectionner le nom correspondant au lieu que vous voulez sélectionner ou sélectionner -1 pour ne rien choisir."
    )
    choix_lieu = input().lower()
    if choix_lieu == "-1":
        print("Aucun lieu choisie.")
    elif choix_lieu not in [lieu.nom for lieu in environnement.lieux]:
        print("Le lieu sélectionner n'éxiste pas.")
    else:
        for lieu in environnement.lieux:
            if lieu.nom == choix_lieu:
                force_total = 0
                for ennemi in lieu.ennemis:
                    ennemi.parler()
                    force_total += ennemi.force
                print(
                    "Voici la force total de tous les ennemis du lieu.",
                    force_total,
                )
                if environnement.joueur.attaquer(force_total, lieu):
                    environnement.lieux.remove(lieu)


def menu_allies(environnement: Environnement) -> None:
    choix_menu_allies = 0
    while choix_menu_allies != -1:
        print(
            "Veuillez choisir une action entre: 1: voir la liste des allié, 2: sauvegarder, 3: voir inventaire-1: Revenir à la place principale du village"
        )
        choix_menu_allies = int(input())
        match choix_menu_allies:
            case 1:
                choix_allies(environnement=environnement)
            case 2:
                sauvegarder_partie("partie_sauvegarder.json", environnement)
            case 3:
                environnement.joueur.verification_inventaire()
            case -1:
                print("Retour à la place principale du village.")
            case _:
                print("Commande non reconnue.")


def menu_lieux(environnement: Environnement):
    choix_menu_lieu = 0
    while choix_menu_lieu != -1:
        if len(environnement.lieux) == 0 or environnement.joueur.vie <= 0:
            choix_menu_lieu = -1
        else:
            print(
                "Veuillez choisir une action entre: 1: voir la liste des lieux, 2: sauvegarder, 3: voir inventaire et -1: Revenir à la place principale du village"
            )
            choix_menu_lieu = int(input())
            match choix_menu_lieu:
                case 1:
                    choix_lieux(environnement)
                case 2:
                    sauvegarder_partie("partie_sauvegarder.json", environnement)
                case 3:
                    environnement.joueur.verification_inventaire()
                case -1:
                    print("Retour à la place principale du village.")
                case _:
                    print("Commande non reconnue.")


def jouer_une_session(filename: str) -> None:
    environnement = creation_environnement(filename)
    choix_centre_village = 0
    while choix_centre_village != -1:
        if len(environnement.lieux) == 0:
            print("Vous avez gagnez")
            choix_centre_village = -1
        elif environnement.joueur.vie <= 0:
            print("Vous êtes mort. Game over.")
            choix_centre_village = -1
        else:
            print("Bienvenue au village de Valun.")
            print(
                "Veuillez choisir une action entre: 1: Allée dans la guilde des alliés, 2: Sortir du village, 3: sauvegarder, 4: Voir inventaire et -1: quitter"
            )
            choix_centre_village = int(input())
            match choix_centre_village:
                case 1:
                    menu_allies(environnement)
                case 2:
                    menu_lieux(environnement)
                case 3:
                    sauvegarder_partie("partie_sauvegarder.json", environnement)
                case 4:
                    environnement.joueur.verification_inventaire()
                case -1:
                    print("Vous avez quitter la partie. Sauvegarde en cours")
                    sauvegarder_partie("partie_sauvegarder.json", environnement)
                case _:
                    print("Commande non reconnue.")


jouer_une_session("data.json")
