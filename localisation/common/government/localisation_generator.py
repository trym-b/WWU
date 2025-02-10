import os
import codecs

def clone_and_translate_files(target_languages=("french", "spanish", "german")):
    # Obtenir la liste des fichiers YAML dans le dossier courant
    current_dir = os.getcwd()
    files_to_clone = [f for f in os.listdir(current_dir) if f.endswith("_l_english.yml")]

    if not files_to_clone:
        print("Aucun fichier '_l_english.yml' trouvé dans le répertoire.")
        return

    for file_name in files_to_clone:
        source_path = os.path.join(current_dir, file_name)

        try:
            # Lire le contenu avec UTF-8 BOM
            with codecs.open(source_path, 'r', encoding='utf-8-sig') as file:
                lines = file.readlines()

            # Cloner le fichier pour chaque langue cible
            for language in target_languages:
                target_name = file_name.replace("_l_english", f"_l_{language}")
                target_path = os.path.join(current_dir, target_name)

                # Modifier la première ligne avec la langue correcte
                if lines:
                    lines[0] = f"l_{language}:\n"

                # Écrire dans le fichier cible en UTF-8 BOM
                with codecs.open(target_path, 'w', encoding='utf-8-sig') as file:
                    file.writelines(lines)

                print(f"Fichier cloné : '{source_path}' → '{target_path}'")

        except Exception as e:
            print(f"Erreur lors du traitement de '{file_name}': {e}")


# Exécuter la fonction
clone_and_translate_files(["french", "spanish", "german"])
