from pathlib import Path

SAMPLE = {
    "title": "Hybrid bio-polymer coating for recyclable food packaging",
    "domain": "materials",
    "problem_statement": "Reduce oxygen permeability while maintaining compostability.",
}

def main() -> None:
    out = Path("/tmp/innovation_sample_data.json")
    out.write_text(str(SAMPLE), encoding="utf-8")
    print(f"Sample data written to {out}")

if __name__ == "__main__":
    main()
