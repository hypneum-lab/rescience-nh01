#!/usr/bin/env bash
# Regenerate content.tex from article.md (run from article/).
#  - drops the "# References" section (bibliography.bib + \printbibliography)
#  - pandoc markdown citations [@key] -> \autocite -> \supercite (ReScience style)
#  - pandoc's \def\LTcaptype{none} breaks the caption package of rescience.cls
#    ("No counter 'none' defined"); the group is kept, the \def removed.
set -euo pipefail
cd "$(dirname "$0")"
awk '/^# References/{exit} {print}' article.md \
  | pandoc -f markdown+yaml_metadata_block -t latex --biblatex \
  | sed -e 's/\\autocite{/\\supercite{/g' \
        -e 's/^{\\def\\LTcaptype{none} % do not increment counter$/{/' \
  > content.tex
echo "content.tex: $(wc -l < content.tex) lines"
