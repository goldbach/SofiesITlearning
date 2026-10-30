claude's svar på 3:
Til at filtrere på forfatter og tidsrum bruger du de her flag:

Forfatter

- --author=<mønster> viser commits, hvor forfatterens navn eller e-mail matcher mønsteret. Mønsteret er et regulært udtryk, så et delvist navn er nok.
git log --author="Sofie"
  Du kan angive --author flere gange. Så vises commits, der matcher mindst ét af dem.
- --committer=<mønster> gør det samme, men for committeren. Det er den, der faktisk lavede committet, og det er ikke altid forfatteren, fx efter et rebase eller cherry-pick.

Tidsrum

- --since=<dato> eller --after=<dato> viser commits efter datoen.
- --until=<dato> eller --before=<dato> viser commits før datoen.

Git forstår både faste datoer og relative udtryk:
git log --since="2026-10-01" --until="2026-10-29"
git log --since="2 weeks ago"
git log --since="yesterday"

Kombineret

git log --author="Sofie" --since="2026-10-01" --until="2026-10-31"

Nyttige tilføjelser

- --oneline viser én linje pr. commit.
- --date=short viser datoer som ÅÅÅÅ-MM-DD.
- -i (--regexp-ignore-case) ignorerer store og små bogstaver i mønsteret.
- --format="%h %an %ad %s" lader dig selv vælge, hvad der vises: hash, forfatter, dato og besked.

Eksempel:
git log --author="sofie" -i --since="1 month ago" --date=short --format="%h %ad %an  %s"

Bemærk, at --since og --until som standard ser på committer-datoen og ikke forfatter-datoen. De to datoer er næsten altid ens, men de kan være forskellige efter et rebase.






OBS!! jeg kunne ikke selv finde disse flag og jeg ved ikke hvordan jeg går ud af log help når jeg er der miv :(((( 






En ting jeg ikke ville lægge ind i AI:
alt det min arbejdsgiver/kunde ikke har givet adgang til - eller rettere alt det jeg ikke specifikt har fået godkendt. Hvis jeg spørger ai om hjælp ville jeg ikke engang bruge rigtige navne eller for konkrete scenarier, mere generelle problemer og løsnigner. 

