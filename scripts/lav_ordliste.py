"""Samler ordlisterne fra alle moduler i ORDLISTE.md, sorteret alfabetisk.

Kør fra roden af repoet:  python3 scripts/lav_ordliste.py

Ret ord i de enkelte tutorials, ikke i ORDLISTE.md. Den bliver overskrevet.
"""

import re
from pathlib import Path

ROD = Path(__file__).resolve().parent.parent

# Dansk alfabet: æ, ø, å kommer efter z
DANSK = str.maketrans({"æ": "z{", "ø": "z|", "å": "z}"})


def modul_titel(readme: Path) -> str:
    # "# Dag 2: Hvordan et system hænger sammen" -> "Hvordan et system hænger sammen"
    forste_linje = readme.read_text(encoding="utf-8").splitlines()[0]
    return forste_linje.split(":", 1)[-1].strip()


def ord_i(readme: Path):
    tekst = readme.read_text(encoding="utf-8")
    afsnit = tekst.split("## Ordliste", 1)
    if len(afsnit) < 2:
        return
    for linje in afsnit[1].splitlines():
        celler = [c.strip() for c in re.split(r"(?<!\\)\|", linje.strip())[1:-1]]
        if len(celler) != 2 or celler[0] in ("Ord", "") or set(celler[0]) <= {"-"}:
            continue
        yield celler[0].replace("**", ""), celler[1]


def sorteringsnoegle(ord: str) -> str:
    return ord.replace("`", "").lstrip(".").lower().translate(DANSK)


def main():
    rækker = []
    for mappe in sorted(p for p in ROD.iterdir() if p.is_dir() and re.match(r"\d\d", p.name)):
        readme = mappe / "README.md"
        if not readme.exists():
            continue
        modul = mappe.name.split("-", 1)[0]
        link = f"[{modul}]({mappe.name}/README.md#ordliste)"
        for ord, betydning in ord_i(readme):
            rækker.append((sorteringsnoegle(ord), ord, betydning, link, modul_titel(readme)))

    rækker.sort()
    linjer = [
        "# Samlet ordliste",
        "",
        "Alle ord fra forløbets moduler, sorteret alfabetisk. Kolonnen *Modul* linker til det modul, ordet kommer fra.",
        "",
        "*Filen er genereret af `scripts/lav_ordliste.py`. Ret i de enkelte tutorials, ikke her.*",
        "",
    ]
    bogstav = None
    for noegle, ord, betydning, link, _ in rækker:
        forste = noegle[0].upper() if noegle[0].isalpha() else "#"
        forste = {"Z{": "Æ", "Z|": "Ø", "Z}": "Å"}.get(noegle[:2].upper(), forste)
        if forste != bogstav:
            bogstav = forste
            linjer += ["", f"## {bogstav}", "", "| Ord | Betydning | Modul |", "|-----|-----------|-------|"]
        linjer.append(f"| **{ord}** | {betydning} | {link} |")

    (ROD / "ORDLISTE.md").write_text("\n".join(linjer) + "\n", encoding="utf-8")
    print(f"{len(rækker)} ord skrevet til ORDLISTE.md")


if __name__ == "__main__":
    main()
