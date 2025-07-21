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

    def __str__(self) -> str:
        return f"nom: {self.nom}, description: {self.description}, ressources: {self.ressources}, ennemis: {self.ennemis}"


class Joueur(Personnage):

    def __init__(self, nom: str, force: int, vie: int, inventaire: Dict[str, int]):
        super().__init__(force, nom)
        self.vie = vie
        self.inventaires = inventaire

    def afficher_lieux(self, lieux: List[Lieu]) -> None:
        for lieu in lieux:
            print(lieu)

    def afficher_allie(self, allies: List[Allie]) -> None:
        for allie in allies:
            print(allie)

    def verification_inventaire(self) -> None:
        print(self.inventaires)

    def ajout_objet_inventaire(self, ressource: str) -> None:
        self.inventaires[ressource["nom"]] += ressource["quantite"]
        print(f"Vous avez récupérer {ressource["quantite"]} de {ressource["nom"]}")

    def payer_allie(
        self,
        allie: Allie,
    ) -> bool:
        prix = re.search(pattern=r"(\d+) unités d'or", string=allie.dialogue)
        print(prix)
        if not prix:
            print("Prix non trouver donc c'est gratuit.")
            self.force += allie.force
            return True
        elif int(prix.group()[0]) > self.inventaires["or"]:
            print(f"Vous n'avez pas assez d'or pour payer {allie.nom}.")
            return False
        else:
            self.inventaires["or"] -= prix
            self.force += allie.force
            print("Allié payer avec succés.")
            return True

    def attaquer(self, ennemi: Dict[str, Union[str, int]]) -> None:
        if self.force < ennemi["force"]:
            self.vie -= ennemi["force"]
            print(f"L'ennemi vous fait {ennemi["force"]} de point de dégats.")
        else:
            print(f"Vous avez tuer un {ennemi["nom"]}.")


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
    dict_lieux = [lieu.__dict__ for lieu in environnement.lieux]
    dict_ressources = []
    dict_ennemis = []
    for lieu in dict_lieux:
        ressources = lieu["ressources"]
        ennemis = lieu["ennemis"]
        dict_ressources = [ressource.__dict__ for ressource in ressources]
        dict_ennemis = [ennemi.__dict__ for ennemi in ennemis]
        lieu["ressources"] = dict_ressources
        lieu["ennemis"] = dict_ennemis
    dict_environnement = {
        "joueur": environnement.joueur.__dict__,
        "allies": dict_allies,
        "lieux": dict_lieux,
    }
    print(dict_environnement)
    with open(file=filename, mode="w", encoding="utf-8") as fichier:
        json.dump(dict_environnement, fichier, ensure_ascii=False, indent=2)


def creation_environnement(
    filename: str,
) -> Environnement:
    if os.path.exists("partie_sauvegarder.json"):
        environnement_dict = load_json("partie_sauvegarder.json")
        environnement = Environnement(
            joueur=environnement_dict["joueur"],
            allies=environnement_dict["allies"],
            lieux=environnement_dict["lieux"],
        )
    else:
        print("Veuillez choisir un nom. Attention vous ne pourrez pas le changer.")
        environnement_dict = load_json(filename)
        nom = input()
        joueur = Joueur(nom=nom, vie=100, force=10, inventaire={"or": 0})
        personnages = environnement_dict["personnages"]
        allies = [
            Allie(
                nom=personnage["nom"],
                force=personnage["force"],
                dialogue=personnage["dialogue"],
            )
            for personnage in personnages
            if personnage["type"] == "allié"
        ]
        ennemis = [
            Ennemi(
                nom=personnage["nom"],
                force=personnage["force"],
                dialogue=personnage["dialogue"],
            )
            for personnage in personnages
            if personnage["type"] == "ennemi"
        ]
        ressources = [
            Ressource(
                nom=ressource["nom"],
                quantite=ressource["quantite"],
                utilite=ressource["utilite"],
            )
            for ressource in environnement_dict["ressources"]
        ]
        lieux = [
            Lieu(
                nom=lieu["nom"],
                description=lieu["description"],
                ressources=ressources,
                ennemis=ennemis,
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
        choix_allie = input()
        if choix_allie == -1:
            print("Aucun allie choisie.")
        else:
            for allie in environnement.allies:
                if allie.nom == choix_allie:
                    if environnement.joueur.payer_allie(allie):
                        environnement.allies.remove(allie)


def menu_allies(environnement: Environnement) -> None:
    choix_menu_allies = 0
    while choix_menu_allies != -1:
        print(
            "Veuillez choisir une action entre: 1: voir la liste des allié, 2: sauvegarder et -1: Revenir à la place principale du village"
        )
        choix_menu_allies = int(input())
        match choix_menu_allies:
            case 1:
                choix_allies(environnement=environnement)
            case 2:
                sauvegarder_partie("partie_sauvegarder.json", environnement)
            case _:
                print("Commande non reconnue.")


def jouer_une_session(filename: str) -> None:
    environnement = creation_environnement(filename)
    choix_centre_village = 0
    while choix_centre_village != -1:
        print("Bienvenue au village de Valun.")
        print(
            "Veuillez choisir une action entre: 1: Allée dans la guilde des alliés, 2: Sortir du village et 3: sauvegarder et -1: quitter"
        )
        choix_centre_village = int(input())
        match choix_centre_village:
            case 1:
                menu_allies(environnement)
            case 2:
                choix_menu_lieu = 0
                while choix_menu_lieu != -1:
                    print(
                        "Veuillez choisir une action entre: 1: voir la liste des lieux, 2: sauvegarder et -1: Revenir à la place principale du village"
                    )
                    choix_menu_lieu = int(input())
                    match choix_menu_lieu:
                        case 1:
                            environnement.joueur.afficher_lieux(environnement.lieux)
                            print(
                                "Sélectionner le numéros correspondant au lieu que vous voulez sélectionner ou sélectionner -1 pour ne rien choisir."
                            )
                            choix_lieu = int(input())
                            if choix_lieu == -1:
                                print("Aucun lieu choisie.")
                            else:
                                try:
                                    lieu_selectionner = environnement["lieux"][
                                        choix_lieu
                                    ]
                                    print(f"Vous entrez dans {lieu_selectionner}")
                                    choix_action = 0
                                    while choix_action != -1:
                                        print(
                                            "Veuillez sélectionner l'action que vous souhaitez faire: 1-Voir les ennemis de la zone, 2-Voir les ressource de la zone, 3-Sauvegarder, -1:Revenir au menu des lieux"
                                        )
                                        choix_action = int(input())
                                except IndexError as e:
                                    print(
                                        f"L'index utilisé est en dehors de la plage {e}"
                                    )


jouer_une_session("data.json")
