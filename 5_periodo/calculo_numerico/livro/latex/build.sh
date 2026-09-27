#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
python3 merge_pdf.py ../livro_calculo_numerico.pdf
latexmk -C
