from pathlib import Path
import sys
from pypdf import PdfWriter

base = Path(__file__).resolve().parent
output = Path(sys.argv[1]).resolve()
inputs = [
    base / "main.pdf",
    base / "../../trabalhos/trabalho_metodos_diretos/relatorio_calculo_numerico.pdf",
    base / "../../trabalhos/trabalho_metodos_interativos/relatorio_calculo_numerico_2.pdf",
    base / "../../trabalhos/trabalho_interpolacao_ajuste_curvas/relatorio_calculo_numerico_3.pdf",
    base / "../../trabalhos/trabalho_derivacao_integracao_numerica/relatorio_cnum_4.pdf",
]
writer = PdfWriter()
for path in inputs:
    writer.append(str(path))
writer.add_metadata({
    "/Title": "Cálculo Numérico: Fundamentos, Métodos e Investigações em Python",
    "/Author": "Jeann Victor (organização); coautorias preservadas nos relatórios anexos",
    "/Subject": "Notas de aula e investigações computacionais de Cálculo Numérico",
})
with output.open("wb") as stream:
    writer.write(stream)
