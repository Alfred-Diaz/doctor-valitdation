from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, send_file, redirect, url_for, flash

from src.processor import consolidate_pdfs_to_template

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

for folder in [UPLOAD_DIR, OUTPUT_DIR, LOG_DIR]:
    folder.mkdir(exist_ok=True)

app = Flask(__name__)
app.secret_key = "change-this-local-secret"

ALLOWED_PDF = {".pdf"}
ALLOWED_EXCEL = {".xlsx"}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    pdf_files = request.files.getlist("pdf_files")
    template = request.files.get("template_file")

    if not pdf_files or all(not f.filename for f in pdf_files):
        flash("Please upload at least one PDF file.", "error")
        return redirect(url_for("index"))

    if not template or not template.filename:
        flash("Please upload the PPS FINAL TEMPLATE.xlsx file.", "error")
        return redirect(url_for("index"))

    if Path(template.filename).suffix.lower() not in ALLOWED_EXCEL:
        flash("Template must be an .xlsx file.", "error")
        return redirect(url_for("index"))

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_upload_dir = UPLOAD_DIR / run_id
    run_upload_dir.mkdir(parents=True, exist_ok=True)

    saved_pdfs = []
    for uploaded in pdf_files:
        if not uploaded.filename:
            continue
        if Path(uploaded.filename).suffix.lower() not in ALLOWED_PDF:
            continue
        save_path = run_upload_dir / Path(uploaded.filename).name
        uploaded.save(save_path)
        saved_pdfs.append(save_path)

    if not saved_pdfs:
        flash("No valid PDF files were uploaded.", "error")
        return redirect(url_for("index"))

    template_path = run_upload_dir / "PPS FINAL TEMPLATE.xlsx"
    template.save(template_path)

    output_path = OUTPUT_DIR / f"pps_final_consolidated_{run_id}.xlsx"
    report = consolidate_pdfs_to_template(saved_pdfs, template_path, output_path)

    return render_template(
        "result.html",
        output_file=output_path.name,
        total_records=report.get("total_records", 0),
        warnings=report.get("warnings", []),
    )


@app.route("/download/<filename>")
def download(filename):
    path = OUTPUT_DIR / filename
    if not path.exists():
        flash("Output file no longer exists.", "error")
        return redirect(url_for("index"))
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
