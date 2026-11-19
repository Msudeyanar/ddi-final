"""Verify the fixed IP2 audit. This script never infers correctness from part count."""
from __future__ import annotations
import argparse
import ast
import csv
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "audit" / "sample50_manifest.json"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def saved_sample(notebook):
    cell = next(c for c in notebook["cells"] if c.get("id") == "62e06900")
    text = "".join("".join(o.get("text", [])) for o in cell.get("outputs", []))
    result = []
    for line in text.splitlines():
        m = re.match(r"^\s*(\d+)\.\s+[✓✗]\s+(.*?)\s+\| HAM: (.*?)\s+→ (.*)$", line)
        if m:
            result.append((int(m[1]), m[2], ast.literal_eval(m[4])))
    return result

def self_check(manifest):
    records = manifest["records"]
    require(len(records) == 50, "Manifest must contain the fixed 50 records.")
    require([r["sira"] for r in records] == list(range(1, 51)), "Sample order is incomplete.")
    require(len({r["barkod"] for r in records}) == 50, "Sample barcodes are not unique.")
    table = read_csv(ROOT / "docs" / "ayristirma_kontrol_50.csv")
    require(len(table) == 50, "Review CSV must contain 50 rows.")
    counts = Counter(r["status"] for r in records)
    require(dict(counts) == manifest["counts"], "Manifest label totals disagree.")
    require(Counter(r["karar"] for r in table) == counts, "CSV label totals disagree.")
    notebook = json.loads((ROOT / "reference" / "notebooks" / "02_etken_ayristirma.ipynb").read_text(encoding="utf-8"))
    original = saved_sample(notebook)
    require(len(original) == 50, "Original notebook stdout is incomplete.")
    reproduction = manifest["reproduction"]
    require(len(reproduction["sample_indices"]) == 50, "Reproduction is incomplete.")
    for row, record, (ordinal, prefix, parts), regenerated in zip(
        table, records, original, reproduction["sample_outputs"], strict=True
    ):
        require(int(row["sira"]) == record["sira"] == ordinal, "Ordinal mismatch.")
        require(row["barkod"] == record["barkod"], f"Barcode mismatch at {ordinal}.")
        require(record["urun_adi"].startswith(prefix), f"Notebook name mismatch at {ordinal}.")
        require(record["notebook_bilesenleri"] == parts, f"Notebook output mismatch at {ordinal}.")
        require(record["notebook_bilesenleri"] == [x[2] for x in regenerated], f"Reproduced output mismatch at {ordinal}.")
        require(record["notebook_bilesenleri"] == record["csv_bilesenleri"], f"Uploaded CSV output mismatch at {ordinal}.")
        require(record["note"], f"Missing review reason at {ordinal}.")
        require(record["expected"] is not None or record["expected_note"], f"Unexplained missing expectation at {ordinal}.")
    report = (ROOT / "docs" / "ayristirma_kontrol.md").read_text(encoding="utf-8")
    require(len(re.findall(r"^\| \d+ \| \d{13} —", report, re.MULTILINE)) == 50, "Report table is incomplete.")
    require("[cite:" not in report, "Unresolved pseudo citations remain.")
    return dict(counts)

def verify_inputs(manifest, products, current):
    """Rebuild sample using pinned historical code, then compare the full fixed sample."""
    import numpy as np
    import pandas as pd

    require(len(products) == manifest["inputs"][0]["records"], "Unexpected urun.csv version/row count.")
    require(len(current) == manifest["inputs"][1]["records"], "Unexpected urun_etken.csv version/row count.")
    product_by_barcode = defaultdict(list)
    current_by_barcode = defaultdict(list)
    for p in products:
        product_by_barcode[p["barkod"]].append(p)
    for e in current:
        current_by_barcode[e["barkod"]].append(e)
    for expected in manifest["records"]:
        barcode = expected["barkod"]
        matches = product_by_barcode[barcode]
        require(len(matches) == 1, f"Missing or duplicate product: {barcode}")
        p = matches[0]
        require(p["urun_adi"] == expected["urun_adi"], f"Product name changed: {barcode}")
        require(p["etkin_madde_ham"] == expected["etkin_madde_ham"], f"Raw ingredient text changed: {barcode}")
        parts = [r["bilesen_tr"] for r in sorted(current_by_barcode[barcode], key=lambda r: int(r["sira"]))]
        require(parts == expected["csv_bilesenleri"], f"Ingredient output changed: {barcode}")
    spec = importlib.util.spec_from_file_location(
        "_ip2_pinned_normalize", ROOT / "reference" / "src" / "normalize.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    df = pd.DataFrame(products)
    df.loc[df["barkod"].eq(""), "barkod"] = np.nan
    cooked = []
    combined_per_source_row = 0
    for _, p in df.iterrows():
        parts = module.bilesenlere_ayir(p["etkin_madde_ham"] or None, kaynak=p["kaynak"])
        combined_per_source_row += len(parts) >= 2
        for order, raw, norm in parts:
            cooked.append({"barkod": p["barkod"], "sira": order, "bilesen_ham": raw, "bilesen_tr": norm})
    out = pd.DataFrame(cooked)
    combo_barcodes = out[out["sira"] >= 2]["barkod"].unique()
    eligible = df[df["barkod"].isin(combo_barcodes)].copy()
    sample = eligible.sample(n=50, random_state=42)
    expected_repro = manifest["reproduction"]
    require(len(out) == expected_repro["part_count"], "Historical ingredient row count changed.")
    require(len(eligible) == expected_repro["eligible_count"], "Historical sample population changed.")
    require(sample.index.tolist() == expected_repro["sample_indices"], "Historical sample order changed.")
    require(sample["barkod"].tolist() == [r["barkod"] for r in manifest["records"]], "Historical sample barcodes changed.")
    regenerated_by_barcode = out.groupby("barkod")["bilesen_tr"].apply(list).to_dict()
    for record in manifest["records"]:
        require(regenerated_by_barcode[record["barkod"]] == record["notebook_bilesenleri"],
                f"Historical output mismatch: {record['barkod']}")
    return {
        "product_records": len(products),
        "uploaded_ingredient_records": len(current),
        "historical_ingredient_records": len(out),
        "historical_population": len(eligible),
        "combined_per_source_row": int(combined_per_source_row),
        "blank_product_barcodes": int(df["barkod"].isna().sum()),
        "extra_population_rows_from_barcode_selection": int(len(eligible) - combined_per_source_row),
        "exact_sample_name_and_output_matches": len(manifest["records"]),
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--urun", type=Path)
    parser.add_argument("--urun-etken", type=Path)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    counts = self_check(manifest)
    result = {"status": "ok", "counts": counts}
    if (args.urun is None) != (args.urun_etken is None):
        parser.error("--urun and --urun-etken must be supplied together.")
    if args.urun is not None:
        result["input_verification"] = verify_inputs(manifest, read_csv(args.urun), read_csv(args.urun_etken))
    else:
        result["scope"] = "Package consistency only; pass both CSV paths for full input reproduction."
    total = len(manifest["records"])
    good = counts.get("Doğru", 0)
    pending = counts.get("İnceleme gerekli", 0)
    result["confirmed_correct_percent"] = 100 * good / total
    result["best_possible_correct_percent"] = 100 * (good + pending) / total
    result["final_accuracy_determined"] = pending == 0
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, StopIteration) as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)

