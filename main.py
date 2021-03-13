import sys
import argparse
import configparser
import logging
import os.path
from azure.storage.blob import BlobServiceClient


def listb(args, containerclient):
    """
    Liste le contenu du blob
    cmd : python main.py list
    """
    logging.debug(f"Compte {config['storage']['account']}")
    logging.debug(f"Conteneur {config['storage']['container']}")
    logging.info("Connexion réussie")
    logging.info(
        f"Affichage de la liste du conteneur {config['storage']['container']}"
        )
    blob_list = containerclient.list_blobs()
    for blob in blob_list:
        logging.info(
            f"Contenu de {config['storage']['container']}: {blob.name}"
            )
        print(blob.name)


def upload(cible, blobclient):
    """
    Permet d'envoyer un ou plusieurs fichiers vers le blob en spécifiant
    le chemin d'accès du ou des fichiers
    Ecrasement du fichier s'il existe dans le conteneur
    cmd : python main.py upload 'chemin d'accès avec nom du/des fichier'
    """
    logging.debug(f"Compte {config['storage']['account']}")
    logging.debug(f"Conteneur {config['storage']['container']}")
    logging.info("Connexion réussie")
    with open(cible, "rb") as f:
        logging.info(f"Upload du fichier {cible} vers le conteneur")
        logging.warning(
            f"Ecrasement du fichier {cible} s'il existe dans le conteneur")
        blobclient.upload_blob(f, overwrite=True)


def download(filename, dl_folder, blobclient):
    """
    Permet de télécharger le contenu du container vers le dossier de restore
    Il faut préciser le ou les fichiers à télécharger
    cmd : python main.py download 'nom du/des fichiers'
    """
    logging.debug(f"Compte {config['storage']['account']}")
    logging.debug(f"Conteneur {config['storage']['container']}")
    logging.info("Connexion réussie")
    with open(os.path.join(dl_folder, filename), "wb") as my_blob:
        logging.info(f"Téléchargement de {filename} vers \
{config['general']['restoredir']}")
        logging.warning(
            f"Ecrasement du fichier {filename} s'il existe dans \
{config['general']['restoredir']}")
        blob_data = blobclient.download_blob()
        blob_data.readinto(my_blob)


def main(args, config):
    """
    Cette fonction est lancé au démarrage du script
    Fais le liens avec le fichier config.ini
    En fonction de l'argument, appel la fonction associée
    """
    blobclient = BlobServiceClient(
        f"https://{config['storage']['account']}.blob.core.windows.net",
        config["storage"]["key"],
        logging_enable=False)
    containerclient = blobclient.get_container_client(
        config["storage"]["container"])
    logging.info(f"Argument appelé {args}")
    if args.action == "list":
        return listb(args, containerclient)
    else:
        if args.action == "upload":
            blobclient = containerclient.get_blob_client(
                os.path.basename(args.cible))
            return upload(args.cible, blobclient)
        elif args.action == "download":
            blobclient = containerclient.get_blob_client(
                os.path.basename(args.remote))
            return download(
                args.remote, config["general"]["restoredir"], blobclient)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Logiciel d'archivage de documents")
    parser.add_argument(
        "-cfg",
        default="config.ini",
        help="chemin du fichier de configuration")
    parser.add_argument(
        "-lvl", default="info", help="niveau de log")
    subparsers = parser.add_subparsers(dest="action", help="type d'operation")
    subparsers.required = True

    parser_s = subparsers.add_parser("upload")
    parser_s.add_argument("cible", help="fichier à envoyer")

    parser_r = subparsers.add_parser("download")
    parser_r.add_argument("remote", help="nom du fichier à télécharger")
    parser_r = subparsers.add_parser("list")

    args = parser.parse_args()

    loglevels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
        }
    print(loglevels[args.lvl.lower()])
    logging.basicConfig(level=loglevels[args.lvl.lower()])

    config = configparser.ConfigParser()
    config.read(args.cfg)

    sys.exit(main(args, config))
