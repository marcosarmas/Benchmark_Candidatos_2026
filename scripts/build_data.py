#!/usr/bin/env python3
"""Genera data/<ciudad>.js a partir de data/<ciudad>/candidatos.json e intereses.json.

Uso:
  python3 scripts/build_data.py                    # regenera todas las ciudades
  python3 scripts/build_data.py quito              # solo una ciudad
  python3 scripts/build_data.py merge latacunga a.json b.json ...   # reemplaza los candidatos de esa ciudad
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

EJES = [
    {"key": "movilidad", "nombre": "Movilidad y transporte", "desc": "Transporte público, tráfico, vías."},
    {"key": "seguridad", "nombre": "Seguridad ciudadana", "desc": "Prevención, vigilancia, coordinación con la Policía, gestión de riesgos."},
    {"key": "servicios", "nombre": "Agua, basura y servicios", "desc": "Agua potable, alcantarillado, recolección de residuos."},
    {"key": "ambiente", "nombre": "Ambiente y espacio público", "desc": "Áreas verdes, ríos, quebradas, calidad del aire, parques."},
    {"key": "economia", "nombre": "Empleo y economía", "desc": "Emprendimiento, comercio, empleo, informalidad."},
    {"key": "barrios", "nombre": "Barrios, parroquias y obras", "desc": "Obra pública barrial, parroquias rurales, vivienda."},
    {"key": "finanzas", "nombre": "Finanzas y transparencia", "desc": "Presupuesto, deuda, impuestos, anticorrupción, gestión."},
    {"key": "cultura", "nombre": "Cultura, deporte y turismo", "desc": "Patrimonio, fiestas, deporte barrial, turismo."},
]
KEYS = [e["key"] for e in EJES]


def normalize(c, keys=KEYS):
    c.setdefault("propuestas", {})
    for k in keys:
        c["propuestas"].setdefault(k, [])
        for p in c["propuestas"][k]:
            p["concreta"] = bool(p.get("concreta"))
            p["plazo"] = p.get("plazo") or None
            p["costo"] = p.get("costo") or None
            if p.get("competencia") not in ("si", "parcial", "no"):
                p["competencia"] = None
            p.setdefault("intereses", [])
    return c


def build(city):
    d = DATA / city
    src = d / "candidatos.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    # Un conjunto de datos puede definir sus propios ejes (p. ej. el CPCCS) en "ejes_custom"
    data["ejes"] = data.get("ejes_custom") or EJES
    keys = [e["key"] for e in data["ejes"]]
    data["candidatos"] = [normalize(c, keys) for c in data["candidatos"]]
    src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    cat_file = d / "intereses.json"
    cat = json.loads(cat_file.read_text(encoding="utf-8"))["intereses"] if cat_file.exists() else []
    ids = {i["id"] for i in cat}
    for c in data["candidatos"]:
        for ps in c["propuestas"].values():
            for p in ps:
                bad = [t for t in p["intereses"] if t not in ids]
                if bad:
                    sys.exit(f"[{city}] Interés desconocido {bad} en {c['id']}")
    data["intereses"] = cat
    out = DATA / f"{city}.js"
    out.write_text(f"// Generado por scripts/build_data.py — editar data/{city}/*.json\nwindow.BENCHMARK = "
                   + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    n = sum(len(v) for c in data["candidatos"] for v in c["propuestas"].values())
    print(f"{city}: {len(data['candidatos'])} candidatos, {n} propuestas, {len(cat)} intereses -> data/{out.name}")


def main():
    args = sys.argv[1:]
    if args and args[0] == "merge":
        city, files = args[1], args[2:]
        cands = []
        for f in files:
            cands += json.loads(pathlib.Path(f).read_text(encoding="utf-8"))
        src = DATA / city / "candidatos.json"
        base = json.loads(src.read_text(encoding="utf-8")) if src.exists() else {}
        base["candidatos"] = cands
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
        args = [city]
    cities = args or sorted(p.name for p in DATA.iterdir() if p.is_dir() and (p / "candidatos.json").exists())
    for c in cities:
        build(c)


if __name__ == "__main__":
    main()
