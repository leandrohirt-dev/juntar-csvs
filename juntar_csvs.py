#!/usr/bin/env python3
"""Junta vários arquivos CSV de uma pasta em um único arquivo."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def juntar_csvs(
    pasta_entrada: Path,
    arquivo_saida: Path,
    *,
    delimitador: str = ",",
    encoding: str = "utf-8",
) -> int:
    arquivos = sorted(pasta_entrada.glob("*.csv"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum .csv em {pasta_entrada}")

    linhas: list[list[str]] = []
    primeira_vez = True

    for arquivo in arquivos:
        with arquivo.open(encoding=encoding, newline="") as f:
            leitor = csv.reader(f, delimiter=delimitador)
            for i, linha in enumerate(leitor):
                if not primeira_vez and i == 0:
                    continue  # pula cabeçalho duplicado
                linhas.append(linha)
        primeira_vez = False

    arquivo_saida.parent.mkdir(parents=True, exist_ok=True)
    with arquivo_saida.open("w", encoding="utf-8-sig", newline="") as f:
        escritor = csv.writer(f, delimiter=delimitador)
        escritor.writerows(linhas)

    return len(linhas) - 1  # desconta cabeçalho


def main() -> int:
    parser = argparse.ArgumentParser(description="Junta CSVs de uma pasta.")
    parser.add_argument(
        "-i", "--entrada", type=Path, default=Path("dados"), help="Pasta com .csv"
    )
    parser.add_argument(
        "-o",
        "--saida",
        type=Path,
        default=Path("saida/consolidado.csv"),
        help="Arquivo de saída",
    )
    args = parser.parse_args()

    total = juntar_csvs(args.entrada, args.saida)
    print(f"Salvo: {args.saida} ({total} linhas de dados)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
