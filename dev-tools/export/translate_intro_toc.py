#!/usr/bin/env python3
"""Build the translated introductory table of contents from the private source."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "dev-tools/export/_data/source/translations/dnd-phandelver-below.pbso-adventures.json"
TARGET = ROOT / "compendium/dnd-phandelver-below.pbso-adventures.json"

LABELS = {
    "Welcome to Phandalin": "Bienvenido a Phandalin",
    "About This Book": "Sobre este libro",
    "Running the Adventure": "Dirigir la aventura",
    "Character Creation": "Creación de personajes",
    "Adventure Hooks": "Ganchos de aventura",
    "Far Realm Influence": "Influjo del Reino Lejano",
    "Ch 1: A Dangerous Journey": "Cap. 1: Un viaje peligroso",
    "Ch 2: Trouble in Phandalin": "Cap. 2: Problemas en Phandalin",
    "Ch 3: The Spider's Web": "Cap. 3: La Telaraña",
    "Ch 4: Wave Echo Cave": "Cap. 4: La Cueva del Oleaje",
    "Ch 5: Paths of Peril": "Cap. 5: Senderos peligrosos",
    "Ch 6: The Shattered Obelisk": "Cap. 6: El Obelisco Fragmentado",
    "Ch 7: Rifts in Reality": "Cap. 7: Grietas en la realidad",
    "Ch 8: Beyond a Lightless Star": "Cap. 8: Más allá de un sol muerto",
    "Running This Chapter": "Dirigir este capítulo",
    "Running this Chapter": "Dirigir este capítulo",
    "The Road to Phandalin": "El camino a Phandalin",
    "Goblin Ambush": "Emboscada goblin",
    "Goblin Trail": "Sendero de los goblins",
    "Cragmaw Hideout": "Guarida Cragmaw",
    "What's Next?": "¿Y ahora qué?",
    "What’s Next?": "¿Y ahora qué?",
    "What's Next": "¿Y ahora qué?",
    "The Spider's Web": "La Telaraña",
    "Encounters in Phandalin": "Encuentros en Phandalin",
    "Town Description": "Descripción del pueblo",
    "Redbrand Ruffians": "Maleantes Redbrand",
    "Redbrands’ Hideout": "Guarida de los Redbrands",
    "Conyberry and Agatha's Lair": "Conyberry y la guarida de Agatha",
    "Old Owl Well": "Pozo del Viejo Búho",
    "Ruins of Thundertree": "Ruinas de Thundertree",
    "Wyvern Tor": "Túmulo del Wyvern",
    "Cragmaw Castle": "Castillo Cragmaw",
    "Wave Echo Cave": "Cueva del Oleaje",
    "Townmaster's Plight": "Problemas del alcalde",
    "Stolen Shards": "Fragmentos robados",
    "Zorzula's Rest": "Descanso de Zorzula",
    "Indigo Sanctum": "Santuario Índigo",
    "The Sinister Truth": "La siniestra verdad",
    "Return to Phandalin": "Regreso a Phandalin",
    "Talhundereth": "Talhundereth",
    "Crypt of the Talhund": "Cripta de Talhund",
    "Gibbet Crossing": "Cruce del Cadalso",
    "Shadow over Phandalin": "Sombra sobre Phandalin",
    "Journey through the Deep": "Viaje por las profundidades",
    "Illithinoch": "Illithinoch",
    "Far Realm Rifts": "Grietas del Reino Lejano",
    "Doom Comes to Phandalin": "La perdición llega a Phandalin",
    "The Briny Maze": "El Laberinto Salino",
    "The Endless Void": "El Vacío Infinito",
    "Wrapping Up": "Conclusión",
    "Epilogue": "Epílogo",
    "Netherese Obelisks": "Obeliscos netherinos",
}


def adventure(payload: dict) -> dict:
    return next(iter(payload["entries"].values()))


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    target = json.loads(TARGET.read_text(encoding="utf-8"))
    source_page = adventure(source)["journals"]["Welcome to Phandalin"]["pages"]["Table of Contents"]
    target_pages = adventure(target)["journals"]["Welcome to Phandalin"]["pages"]
    source_text = source_page["text"]

    translated_text = re.sub(
        r"\{([^{}]+)\}",
        lambda match: "{" + LABELS.get(match.group(1), match.group(1)) + "}",
        source_text,
    )
    source_refs = re.findall(r"@UUID\[[^\]]+\]", source_text)
    translated_refs = re.findall(r"@UUID\[[^\]]+\]", translated_text)
    if source_refs != translated_refs:
        raise SystemExit("UUID validation failed while translating the table of contents")

    target_pages["Table of Contents"] = {
        "name": "Índice",
        "text": translated_text,
    }
    TARGET.write_text(
        json.dumps(target, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Translated {sum(label in source_text for label in LABELS)} table-of-contents labels")
    print(f"Preserved {len(source_refs)} UUID references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
