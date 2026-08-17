import argparse
import subprocess
from pathlib import Path
from datetime import datetime

def process_notebooks(source_dir: Path, vault_dir: Path) -> None:
    """
    Convertit les notebooks Jupyter en Markdown et injecte le frontmatter YAML pour Obsidian.
    """
    if not source_dir.exists():
        print(f"Erreur : Le dossier source {source_dir} n'existe pas.")
        return

    vault_dir.mkdir(parents=True, exist_ok=True)

    for ipynb_file in source_dir.glob("*.ipynb"):
        print(f"Traitement de : {ipynb_file.name}")

        try:
            # Exécution de nbconvert
            subprocess.run(
                [
                    "jupyter", "nbconvert",
                    "--to", "markdown",
                    str(ipynb_file),
                    "--output-dir", str(vault_dir)
                ],
                check=True,
                capture_output=True,
                text=True
            )

            # Chemin du fichier Markdown généré
            md_filepath = vault_dir / ipynb_file.with_suffix(".md").name

            if md_filepath.exists():
                content = md_filepath.read_text(encoding="utf-8")
                
                # Injection des métadonnées si absentes
                if not content.startswith("---"):
                    title = ipynb_file.stem.replace("_", " ").capitalize()
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    
                    frontmatter = (
                        "---\n"
                        f"titre: \"{title}\"\n"
                        "type: cours\n"
                        "statut: a_categoriser\n"
                        f"date_ingestion: {date_str}\n"
                        "---\n\n"
                    )
                    md_filepath.write_text(frontmatter + content, encoding="utf-8")
                    print(f"-> YAML injecté avec succès dans {md_filepath.name}")

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la conversion de {ipynb_file.name} : {e.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline RAG : Ingestion de notebooks en Markdown pour Obsidian.")
    parser.add_argument("--source", type=str, default="./data/raw_notebooks", help="Dossier contenant les notebooks.")
    parser.add_argument("--dest", type=str, default="./vault", help="Dossier cible (Obsidian).")

    args = parser.parse_args()
    process_notebooks(Path(args.source), Path(args.dest))
