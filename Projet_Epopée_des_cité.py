from typing import List, Dict, Union, Tuple
import json
import re
import os


class Joueur:

    def __init__(self, vie: int, force: int, inventaires: Dict[str, int]):
        self.vie = vie
        self.force = force
        self.inventaires = inventaires

    def afficher_lieux(self, lieux: List[Dict[str, Union[str, List[str]]]]) -> None:
        for lieu in lieux:
            print(
                f"numéros:{lieux.index(lieu)}, nom: {lieu["nom"]}, description: {lieu["description"]}, ressources :{lieu["ressources"]}, ennemis: {lieu["ennemis"]}"
            )

    def afficher_allie(
        self,
        environnement: Dict[str, List[Dict[str, Union[str, List[str], int]]]],
    ) -> List[Dict[str, Union[str, int]]]:
        allies = [
            allie for allie in environnement["personnages"] if allie["type"] == "allié"
        ]
        if len(allies) == 0:
            print("Il n'y a plus d'alliés disponible.")
        else:
            print("Voici la liste des alliés disponible:")
            for allie in allies:
                print(
                    f"numéros: {allies.index(allie)} - nom: {allie["nom"]} - force: {allie["force"]} - dialogue: {allie["dialogue"]}"
                )
        return allies

    def afficher_ennemis(
        self,
        environnement: Dict[str, List[Dict[str, Union[str, List[str], int]]]],
        lieu: Dict[str, Union[str, List[str]]],
    ) -> List[Dict[str, Union[str, int]]]:
        ennemis = [
            ennemi
            for ennemi in environnement["personnages"]
            if ennemis["type"] == "ennemi"
        ]
        if len(ennemis) == 0:
            print("Il n'y a plus d'alliés disponible.")
        else:
            print("Voici la liste des alliés disponible:")
            for allie in allies:
                print(
                    f"numéros: {allies.index(allie)} - nom: {allie["nom"]} - force: {allie["force"]} - dialogue: {allie["dialogue"]}"
                )
        return ennemis

    def choisir_allie(
        self,
        choix_allie: int,
        environnement: Dict[str, List[Dict[str, Union[str, List[str], int]]]],
        allies: List[Dict[str, Union[str, int]]],
    ) -> None:
        if choix_allie == -1:
            print("Aucun allie choisie.")
        else:
            try:
                allie_selectionner = allies[choix_allie]
                self.payer_allie(
                    allie_selectionner,
                    environnement["personnages"],
                )
            except IndexError as e:
                print(f"L'index utilisé est en dehors de la plage {e}")

    def verification_inventaire(self) -> None:
        print(self.inventaires)

    def ajout_objet_inventaire(self, ressource: str) -> None:
        self.inventaires[ressource["nom"]] += ressource["quantite"]
        print(f"Vous avez récupérer {ressource["quantite"]} de {ressource["nom"]}")

    def payer_allie(
        self,
        allie: Dict[str, Union[str, int]],
        personnages: List[Dict[str, Union[str, int]]],
    ) -> None:
        prix = re.search(pattern=r"(\d+) unités d'or", string=allie["dialogue"])
        print(prix)
        if not prix:
            print("Prix non trouver donc c'est gratuit.")
            self.force += allie["force"]
            personnages.remove(personnages.index(allie))
        elif int(prix.group()[0]) > self.inventaires["or"]:
            print(f"Vous n'avez pas assez d'or pour payer {allie["nom"]}.")
        else:
            self.inventaires["or"] -= prix
            self.force += allie["force"]
            print("Allié payer avec succés.")
            personnages.remove(personnages.index(allie))

    def attaquer(self, ennemi: Dict[str, Union[str, int]]) -> None:
        if self.force < ennemi["force"]:
            self.vie -= ennemi["force"]
            print(f"L'ennemi vous fait {ennemi["force"]} de point de dégats.")
        else:
            print(f"Vous avez tuer un {ennemi["nom"]}.")


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
    environnement: Dict[str, List[Dict[str, Union[str, List[str], int]]]],
    joueur: Joueur,
) -> None:
    dict_joueur = {
        "vie": joueur.vie,
        "force": joueur.force,
        "inventaire": joueur.inventaires,
    }
    environnement["joueur"] = dict_joueur
    with open(file=filename, mode="w", encoding="utf-8") as fichier:
        json.dump(environnement, fichier, ensure_ascii=False, indent=2)


def creation_environnement(
    filename: str,
) -> Tuple[Union[Dict[str, List[Dict[str, Union[str, List[str], int]]]], Joueur]]:
    if os.path.exists("partie_sauvegarder.json"):
        environnement = load_json("partie_sauvegarder.json")
        joueur = Joueur(
            vie=environnement["joueur"]["vie"],
            force=environnement["joueur"]["force"],
            inventaires=environnement["joueur"]["inventaire"],
        )
    else:
        environnement = load_json(filename)
        joueur = Joueur(vie=100, force=10, inventaires={"or": 0})
    return environnement, joueur


def jouer_une_session(filename: str) -> None:
    environnement, joueur = creation_environnement(filename)
    choix_centre_village = 0
    while choix_centre_village != -1:
        print("Bienvenue au village de Valun.")
        print(
            "Veuillez choisir une action entre: 1: Allée dans la guilde des alliés, 2: Sortir du village et 3: sauvegarder et -1: quitter"
        )
        choix_centre_village = int(input())
        match choix_centre_village:
            case 1:
                choix_menu_allies = 0
                while choix_menu_allies != -1:
                    print(
                        "Veuillez choisir une action entre: 1: voir la liste des allié, 2: sauvegarder et -1: Revenir à la place principale du village"
                    )
                    choix_menu_allies = int(input())
                    match choix_menu_allies:
                        case 1:
                            allies = joueur.afficher_allie(environnement)
                            print(
                                "Sélectionner le numéros correspondant à l'allié que vous voulez sélectionner ou sélectionner -1 pour ne rien choisir."
                            )
                            choix_allie = int(input())
                            joueur.choisir_allie(choix_allie, environnement, allies)
                        case 2:
                            sauvegarder_partie(
                                "partie_sauvegarder.json", environnement, joueur
                            )
                        case _:
                            print("Commande non reconnue.")
            case 2:
                choix_menu_lieu = 0
                while choix_menu_lieu != -1:
                    print(
                        "Veuillez choisir une action entre: 1: voir la liste des lieux, 2: sauvegarder et -1: Revenir à la place principale du village"
                    )
                    choix_menu_lieu = int(input())
                    match choix_menu_lieu:
                        case 1:
                            joueur.afficher_lieux(environnement["lieux"])
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
