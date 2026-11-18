#!/usr/bin/env python3
"""Genera data.js a partir de data/candidatos.json.

Uso:
  python3 scripts/build_data.py                 # regenera data.js
  python3 scripts/build_data.py merge a.json b.json ...   # reemplaza los candidatos con los de esos archivos
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "candidatos.json"
OUT = ROOT / "data.js"

EJES = [
    {"key": "movilidad", "nombre": "Movilidad y transporte", "desc": "Metro, buses, trolebús, tráfico, vías."},
    {"key": "seguridad", "nombre": "Seguridad ciudadana", "desc": "Prevención, vigilancia, coordinación con la Policía."},
    {"key": "servicios", "nombre": "Agua, basura y servicios", "desc": "Agua potable, alcantarillado, recolección de residuos."},
    {"key": "ambiente", "nombre": "Ambiente y espacio público", "desc": "Áreas verdes, quebradas, calidad del aire, parques."},
    {"key": "economia", "nombre": "Empleo y economía", "desc": "Emprendimiento, comercio, empleo, informalidad."},
    {"key": "barrios", "nombre": "Barrios, parroquias y obras", "desc": "Obra pública barrial, parroquias rurales, vivienda."},
    {"key": "finanzas", "nombre": "Finanzas y transparencia", "desc": "Presupuesto, deuda, impuestos, anticorrupción, gestión."},
    {"key": "cultura", "nombre": "Cultura, deporte y turismo", "desc": "Centro Histórico, eventos, deporte barrial, turismo."},
]
KEYS = [e["key"] for e in EJES]


def normalize(c):
    c.setdefault("propuestas", {})
    for k in KEYS:
        c["propuestas"].setdefault(k, [])
        for p in c["propuestas"][k]:
            p["concreta"] = bool(p.get("concreta"))
            p["plazo"] = p.get("plazo") or None
            p["costo"] = p.get("costo") or None
            if p.get("competencia") not in ("si", "parcial", "no"):
                p["competencia"] = None
    return c


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "merge":
        cands = []
        for f in sys.argv[2:]:
            cands += json.loads(pathlib.Path(f).read_text(encoding="utf-8"))
        base = json.loads(SRC.read_text(encoding="utf-8")) if SRC.exists() else {}
        base["candidatos"] = cands
        SRC.parent.mkdir(exist_ok=True)
        SRC.write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
    data = json.loads(SRC.read_text(encoding="utf-8"))
    data["ejes"] = EJES
    data["candidatos"] = [normalize(c) for c in data["candidatos"]]
    SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT.write_text("// Generado por scripts/build_data.py — editar data/candidatos.json\nwindow.BENCHMARK = "
                   + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    n = sum(len(v) for c in data["candidatos"] for v in c["propuestas"].values())
    print(f"{len(data['candidatos'])} candidatos, {n} propuestas -> {OUT.name}")


if __name__ == "__main__":
    main()
