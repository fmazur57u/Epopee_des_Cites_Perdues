from typing import List, Dict, Union, Tuple
import json
import re
import os


class Personnage:
    """Classe qui représente un personnage avec un nom et des points de force. Cette classe est la classe mére de Joueur
    et de Png.

    Attributes:
        nom (str): le nom du personnage.
        force (int): les points de force du personnage.

    Exemple:
        >>> personnage = Personnage(nom="Talion", force=5)
        >>> personnage.nom
        "Talion"
        >>> personnage.force
        5
    """

    def __init__(self, nom: str, force: int):
        """Initialise un nouveau personnage.

        Args:
            nom (str): le nom du personnage.
            force (int): les points de force du personnage.
        """
        self.nom = nom
        self.force = force


class Png(Personnage):
    """Classe fille de Personnage et mére des classe Allie et Ennemi qui représente un personnage non jouable avec un nom, des points de force, et un dialogue.
    Le png peut parler.

    Attributes:
        nom (str): le nom du png.
        force (int): les points de force du png.
        dialogue (str): Ce que dit le png.

    Exemples:
        >>> png = Png(nom = Talion, force = 5, dialogue = "Si tu veut que je t'aide, il faut me payer 10 unités d'or.")
        >>> png.parler()
        "Si tu veut que je t'aide, il faut me payer 10 unités d'or."
    """

    def __init__(self, nom: str, force: int, dialogue: str):
        """ "Initialise un nouveau png.

        Args:
            nom (str): le nom du png.
            force (int): les points de force du png.
            dialogue (str): Ce que dit le png.
        """
        super().__init__(nom, force)
        self.dialogue = dialogue

    def __str__(self) -> str:
        """Permet de donner une représentation lisible des caractéristiques d'un png (nom et force).

        returns:
            str: Une représentation lisible de l'objet

        Exemples:
            >>> png = Png("Talion", 5, "Si tu veut que je t'aide, il faut me payer 10 unités d'or.")
            >>> print(png)
            nom: Talion, force: 5

        """
        return f"nom: {self.nom}, force: {self.force}"

    def parler(self) -> None:
        """Permet au png instancier de dire sont dialogue.

        Exemples:
            >>> png = Png(nom = Talion, force = 5, dialogue = "Si tu veut que je t'aide, il faut me payer 10 unités d'or.")
            >>> png.parler()
            "Si tu veut que je t'aide, il faut me payer 10 unités d'or."
        """
        print(self.dialogue)


class Allie(Png):
    """Classe fille de Png qui représente un allié.

    Attributes:
        nom (str): Le nom de l'allié
        force (int): Les points de force de l'allié
        dialogue (str): Ce que dit l'allié

    Exemples:
        >>> allie = Allie("Talion", 5, "Si tu veut que je t'aide, il faut me payer 10 unités d'or.")
        >>> allie.parler()
        "Si tu veut que je t'aide, il faut me payer 10 unités d'or."
    """

    def __init__(self, nom: str, force: int, dialogue: str):
        """Initialise un nouveau allié

        Args:
            nom (str): Le nom de l'allié
            force (int): Les points de force de l'allié
            dialogue (str): Ce que dit l'allié
        """
        super().__init__(nom, force, dialogue)


class Ennemi(Png):
    """Classe fille de Png qui représente un ennemi.

    Attributes:
        nom (str): Le nom de l'ennemi
        force (int): Les points de force de l'ennemi
        dialogue (str): Ce que dit l'ennemi

    Exemples:
        >>> ennemi = Ennemi("Serpent géant", 5, "SSSH")
        >>> ennemi.parler()
        "SSSH"
    """

    def __init__(self, nom: str, force: int, dialogue: str):
        """Initialise un nouveau ennemi

        Args:
            nom (str): Le nom de l'ennemi
            force (int): Les points de force de l'ennemi
            dialogue (str): Ce que dit l'ennemi
        """
        super().__init__(nom, force, dialogue)


class Ressource:
    """Classe qui représente une ressource définit par un nom, une quantité et une utilité.

    Attributes:
        nom (str): le nom de la ressource
        quantite (int): La quantité de la ressource
        utilite (str): L'utilité de la ressource

    Exemples:
        >>> ressource = Ressource("or", 20, "Permet de payer un allié.")
        >>> print ressource
        or, 20, Permet de payer un allié.
    """

    def __init__(self, nom: str, quantite: int, utilite: str):
        """Initialise une nouvelle ressource.

        Args:
            nom (str): le nom de la ressource
            quantite (int): La quantité de la ressource
            utilite (str): L'utilité de la ressource
        """
        self.nom = nom
        self.quantite = quantite
        self.utilite = utilite

    def __str__(self) -> str:
        """Permet de donner une représentation lisible d'une ressource.

        Returns:
            str: représentation lisible d'une ressource

        Exemples:
            >>> ressource = Ressource("or", 20, "Permet de payer un allié.")
            >>> print ressource
            or, 20, Permet de payer un allié.
        """
        return f"{self.nom}, {self.quantite}, {self.utilite}"


class Lieu:
    """Classe qui représente un lieu à visiter sui à un nom, une description, des ressources disponible et des ennemis à combattre.

    Attributes:
        nom (str): Le nom du lieu
        description (str): La description du lieu
        ressources (List[Ressources]): Une liste d'objet de type ressource qui représente toutes les ressources disponible.
        ennemis (List[Ennemi]): Une liste d'objet de type ennemi qui représente les ennemis à combattre.

    Exemples:
        >>> ressources = [Ressource("or", 20, "Acheter de l'aide")]
        >>> ennemis = [Ennemi("serpent géant", 8, "SSSH")]
        >>> lieu = Lieu("Temple oublié", "Un temple envahi par la végétation", ressources, ennemis)
        >>> lieu.representation()
        nom: Temple oublié, description: Un temple envahi par la végétation
        Voici la liste des ressources.
        or, 20, Acheter de l'aide
        Voici la liste des ennemis.
        nom: serpent géant, force: 8
    """

    def __init__(
        self,
        nom: str,
        description: str,
        ressources: List[Ressource],
        ennemis: List[Ennemi],
    ):
        """Initialise un nouveau lieu.

        Args:
            nom (str): Le nom du lieu
            description (str): La description du lieu
            ressources (List[Ressources]): Une liste d'objet de type ressource qui représente toutes les ressources disponible.
            ennemis (List[Ennemi]): Une liste d'objet de type ennemi qui représente les ennemis à combattre.
        """
        self.nom = nom
        self.description = description
        self.ressources = ressources
        self.ennemis = ennemis

    def representation(self) -> str:
        """Donne une représenttion complete et précise d'un lieu.

        Returns:
            str: La représentation complete et précise d'un lieu.

        Exemples:
            >>> ressources = [Ressource("or", 20, "Acheter de l'aide")]
            >>> ennemis = [Ennemi("serpent géant", 8, "SSSH")]
            >>> lieu = Lieu("Temple oublié", "Un temple envahi par la végétation", ressources, ennemis)
            >>> lieu.representation()
            nom: Temple oublié, description: Un temple envahi par la végétation
            Voici la liste des ressources.
            or, 20, Acheter de l'aide
            Voici la liste des ennemis.
            nom: serpent géant, force: 8
        """
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
            >>> alliés = [Allie(nom="arwen", force = 5, dialogue = "Je peux t'aider à explorer, mais il me faut 10 unités d'or.")]
            >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
            >>> joueur.afficher_allie(alliés)
            nom: arwen, force: 5
        """
        for allie in allies:
            print(allie)
            print("")

    def verification_inventaire(self) -> None:
        """Permet de voir l'inventaire.

        Exemples:
            >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
            >>> joueur.verification_inventaire()
            {"or": 0}
        """
        print(self.inventaire)

    def ajout_objet_inventaire(self, ressources: List[Ressource]) -> None:
        """Permet de récupérer une ressource.

        Args:
            ressources (List[Ressource]): La liste des ressources du lieu sélectionner.

        Exemples:
            >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
            >>> ressources = [Ressource(or, 20, "Permet d'acheter de l'aide"), Ressource(pierres, 20, "Permet de construire de mur de pierre")]
            >>> joueur.ressource(ressources)
            Vous avez récupérer 20 de or.
            >>> joueur.verification_inventaire()
            {"or": 20, "pierres": 20}

        """
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
        """Permet de payer un allié.

        Args:
            allie (Allie): Un objet de type allie qui correponds à un allié qui à été sélectionner par le joueur.

        Returns:
            bool: Valeur qui montre si le payement à été un succés ou pas.

        Exemples:
            >>> allie = Allie(nom="arwen", force = 5, dialogue = "Je peux t'aider à explorer.")
            >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
            >>> joueur.payer_allie(allie)
            "Prix non trouver donc c'est gratuit."
            >>> print(joueur.payer_allie(allie)
            True
            >>> joueur.verification_inventaire()
            {or: 0}
            >>> joueur.force()
            15

            >>> allie = Allie(nom="arwen", force = 5, dialogue = "Je peux t'aider à explorer, mais il me faut 10 unités d'or.")
            >>> joueur.payer_allie(allie)
            "Vous n'avez pas assez d'or pour payer arwen"
            >>> print(joueur.payer_allie(allie)
            False
            >>> joueur.force()
            10

            >>> allie = Allie(nom="arwen", force = 5, dialogue = "Je peux t'aider à explorer, mais il me faut 10 unités d'or.")
            >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 11})
            >>> joueur.payer_allie(allie)
            "Allié payer avec succés."
            >>> print(joueur.payer_allie(allie))
            True
            >>> joueur.verification_inventaire()
            {or: 1}
            >>> joueur.force()
            15
        """
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
        """Permet d'attaquer tous les ennemis d'un lieu en même temps ainsi que de récupérer toutes les ressources du lieu.

        Args:
            force_total (int): Le total des points de force des ennemis d'un lieu.
            lieu (Lieu): Le lieu visiter.

        Returns:
            bool: Issue du combat. Si c'est true, tous les ennemis du lieu ont été
            tuer. Si c'est False, le joueur perds autant de points de vie que de point de force de l'ennemi

        Exemples:
            >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
            >>> lieu = Lieu(nom="Temple oublié", description="Un temple envahi par la végétation",
            ressources=[Ressource(nom="or", quantite=20, utilite="Acheter de l'aide")],
            ennemis=[Ennemis(nom="Serpent géant", force=8, dialogue="SSSSSh")])
            >>> force_total = 8
            >>> joueur.attaquer(force_total, lieu)
            Vous avez tuer tous les ennemis du lieu. Vous pouvez donc récupérer toutes les ressources du lieu.
            Vous avez accomplli le lieu Temple oublié
            Vous avez récupérer 20 de or
            >>> print(joueur.attaquer(force_total, lieu))
            True
            >>> lieu.ennemis
            []
            >>> lieu.ressources
            []
            >>> joueur.verification_inventaire()
            {or: 20}
            >>> joueur.vie
            100

            >>> lieu = Lieu(nom="Temple oublié", description="Un temple envahi par la végétation",
            ressources=[Ressource(nom="or", quantite=20, utilite="Acheter de l'aide")],
            ennemis=[Ennemis(nom="Serpent géant", force=15, dialogue="SSSSSh")])
            >>> force_total = 15
            >>> joueur.attaquer(force_total, lieu)
            Les ennemis du lieu vous ont fait 15 de point de dégats.
            >>> print(joueur.attaquer(force_total, lieu))
            False
            >>> lieu.ennemis
            [Ennemis(nom="Serpent géant", force=15, dialogue="SSSSSh")]
            >>> lieu.ressources
            [Ressource(nom="or", quantite=20, utilite="Acheter de l'aide")]
            >>> joueur.verification_inventaire()
            {or: 0}
            >>> joueur.vie
            85

        """
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
    """Cette classes représente l'environnement de jeu qui contient les informations du joueur, des alliés et des lieux.

    Attributes:
        joueur (Joueur): Un objet de type joueur qui correspond à l'avatar du joueur.
        allies (List[Allies]): Liste d'objet de type allies qui correspond à tous les alliés disponible dans la guilde des alliés.
        lieux (List[Lieu]): Liste d'objets de type lieu qui correspond à tous les lieux disponible sur la carte.

    Exemples:
        >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
        >>> allies = [Allie(nom="arwen", force = 5, dialogue = "Je peux t'aider à explorer.")]
        >>> lieux = [Lieu(nom="Temple oublié", description="Un temple envahi par la végétation",
        ressources=[Ressource(nom="or", quantite=20, utilite="Acheter de l'aide")],
        ennemis=[Ennemis(nom="Serpent géant", force=8, dialogue="SSSSSh")])]
        >>> environnement = Environnement(joueur, allies, lieux)
        >>> print(environnement.joueur.vie)
        100
    """

    def __init__(self, joueur: Joueur, allies: List[Allie], lieux: List[Lieu]):
        """Initialise un nouveau environnement.

        Args:
            joueur (Joueur): Un objet de type joueur qui correspond à l'avatar du joueur.
            allies (List[Allies]): Liste d'objet de type allies qui correspond à tous les alliés disponible dans la guilde des alliés.
            lieux (List[Lieu]): Liste d'objets de type lieu qui correspond à tous les lieux disponible sur la carte.
        """
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
    """Fonction qui permet de sauvegarder la partie dans un fichier.

    Args:
        filename (str): nom du fichier de sauvegarde.
        environnement (Environnement): L'environnement qui contient tous les informations sur le joeur, les alliés et les lieux.

    Exemples:
        >>> filename = "fichier_sauvegarde"
        >>> joueur = Joueur("Talion", 10, 100, inventaire = {"or": 0})
        >>> allies = [Allie(nom="arwen", force = 5, dialogue = "Je peux t'aider à explorer.")]
        >>> lieux = [Lieu(nom="Temple oublié", description="Un temple envahi par la végétation",
        ressources=[Ressource(nom="or", quantite=20, utilite="Acheter de l'aide")],
        ennemis=[Ennemis(nom="Serpent géant", force=8, dialogue="SSSSSh")])]
        >>> environnement = Environnement(joueur, allies, lieux)
        >>> sauvegarder_partie(filename, environnement)
        Le résultats dans le fichier est le suivant:
        {
            "joueur": {
                "nom": 10,
                "force": "Talion",
                "vie": 100,
                "inventaire": {
                "or": 0
                }
            },
            "allies": [
                {
                "nom": "arwen",
                "force": 5,
                "dialogue": "Je peux t'aider à explorer."
                }
            ],
            "lieux": [
                {
                "nom": "Temple oublié",
                "description": "Un temple envahi par la végétation",
                "ressources": [
                    {
                    "nom": "or",
                    "quantite": 20,
                    "utilite": "Acheter de l'aide"
                    }
                ],
                "ennemis": [
                    {
                    "nom": "serpent géant",
                    "force": 8,
                    "dialogue": "SSSSSh"
                    }
                ]
                }
            ]
        }
    """
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
    """Fonction qui permet de créer l'objet environnement correspondant à l'avancer du jeu.

    Args:
        filename (str): Le fichier qui contient les informations du jeu.

    Returns:
        Environnement: Objet qui contient toutes les informations de joueur, d'alliés et de lieux.

    Exemples:
        >>> filename = data.json
        >>> creation_environnement(filename)
        Veuillez choisir un nom. Attention vous ne pourrez pas le changer.
        Talion
        >>> environnement = creation_environnement(filename)
        >>> print(environnement.joueur.nom)
        Talion
    """
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


def choix_allies(environnement: Environnement) -> None:
    """Fonction qui permet de choisir un alliés."""
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


def choix_lieux(environnement: Environnement) -> None:
    """Fonction qui premet de choisir un lieu."""
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
    """Fonction du menu de la guilde des alliés."""
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


def menu_lieux(environnement: Environnement) -> None:
    """Fonction du menu de la guilde des lieux."""
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
    """Fonction qui permet de joueur au jeu."""
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
