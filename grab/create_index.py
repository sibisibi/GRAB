import argparse
import csv
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grab-path", type=str, default=str(Path(__file__).parent))
    parser.add_argument("--index-file", type=str, required=True)
    args = parser.parse_args()

    grab_path = Path(args.grab_path)
    index_file = Path(args.index_file)
    index_file.parent.mkdir(parents=True, exist_ok=True)

    subjects = sorted(
        [d.name for d in grab_path.iterdir() if d.is_dir() and d.name.startswith("s")],
        key=lambda x: int(x[1:])
    )

    rows = []
    for subject in subjects:
        subject_dir = grab_path / subject
        motions = sorted([f.stem for f in subject_dir.glob("*.npz")])
        status = "test" if subject == "s10" else "train"
        for motion in motions:
            rows.append({"subject": subject, "motion": motion, "status": status})

    with open(index_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["subject", "motion", "status"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
