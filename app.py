from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
import os

import config
from auth_utils import delete_upload, login_required, save_upload
from database import (
    create_document,
    create_service,
    delete_document,
    delete_service,
    get_all_documents,
    get_all_services,
    get_document,
    get_documents_for_service,
    get_service,
    get_service_document_ids,
    get_site_settings,
    init_db,
    update_site_settings,
    update_document,
    update_service,
)
from excel_store import (
    append_record,
    delete_record,
    ensure_workbook_ready,
    get_all_records,
    get_monthly_report,
    update_record,
    validate_submission,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

init_db()


@app.context_processor
def inject_company():
    settings = get_site_settings()
    return settings


@app.route("/uploads/certificates/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(config.UPLOAD_DIR, filename)


@app.route("/")
def index():
    services = get_all_services()
    return render_template("index.html", services=services)


@app.route("/documents")
def documents_page():
    documents = get_all_documents()
    return render_template("documents.html", documents=documents)


@app.route("/service/<int:service_id>", methods=["GET", "POST"])
def service_detail(service_id):
    service = get_service(service_id)
    if not service:
        flash("Service not found.", "error")
        return redirect(url_for("index"))

    errors = []
    if request.method == "POST":
        errors, name, mobile, aadhaar = validate_submission(
            request.form.get("customer_name"),
            request.form.get("mobile"),
            request.form.get("aadhaar"),
        )
        if not errors:
            append_record(
                service["name"],
                service["amount"],
                name,
                mobile,
                aadhaar,
                service.get("government_amount", 0),
            )
            flash("Customer details saved successfully to Excel.", "success")
            return redirect(url_for("service_detail", service_id=service_id))

    return render_template(
        "service_detail.html",
        service=service,
        required_documents=get_documents_for_service(service_id),
        errors=errors,
        form_data=request.form if request.method == "POST" else {},
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        valid_logins = {
            config.ADMIN_USERNAME: config.ADMIN_PASSWORD,
            config.ADMIN_USERNAME_2: config.ADMIN_PASSWORD_2,
        }
        if username in valid_logins and password == valid_logins[username]:
            session["admin_logged_in"] = True
            flash("Welcome to the admin panel.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid username or password.", "error")

    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    services = get_all_services()
    documents = get_all_documents()
    records = get_all_records()
    return render_template(
        "admin/dashboard.html",
        services_count=len(services),
        documents_count=len(documents),
        records_count=len(records),
    )


@app.route("/admin/settings", methods=["GET", "POST"])
@login_required
def admin_settings():
    settings = get_site_settings()
    if request.method == "POST":
        update_site_settings(request.form)
        flash("Website text updated successfully.", "success")
        return redirect(url_for("admin_settings"))

    return render_template("admin/settings.html", settings=settings)


@app.route("/admin/services", methods=["GET", "POST"])
@login_required
def admin_services():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            name = request.form.get("name", "").strip()
            amount_raw = request.form.get("amount", "").strip()
            government_amount_raw = request.form.get("government_amount", "").strip()
            image = request.files.get("image")

            if not name:
                flash("Service name is required.", "error")
            else:
                try:
                    amount = float(amount_raw)
                    if amount <= 0:
                        raise ValueError
                except ValueError:
                    flash("Amount must be a positive number.", "error")
                    return redirect(url_for("admin_services"))

                try:
                    government_amount = (
                        float(government_amount_raw) if government_amount_raw else 0
                    )
                    if government_amount < 0:
                        raise ValueError
                except ValueError:
                    flash("Government amount must be zero or a positive number.", "error")
                    return redirect(url_for("admin_services"))

                if government_amount > amount:
                    flash("Government amount cannot be more than the customer amount.", "error")
                    return redirect(url_for("admin_services"))

                filename, error = save_upload(image)
                if error:
                    flash(error, "error")
                else:
                    document_ids = request.form.getlist("document_ids")
                    create_service(
                        name, amount, filename, document_ids, government_amount
                    )
                    flash("Service added successfully.", "success")

        elif action == "edit":
            service_id = request.form.get("service_id")
            name = request.form.get("name", "").strip()
            amount_raw = request.form.get("amount", "").strip()
            government_amount_raw = request.form.get("government_amount", "").strip()
            image = request.files.get("image")

            service = get_service(service_id)
            if not service:
                flash("Service not found.", "error")
            elif not name:
                flash("Service name is required.", "error")
            else:
                try:
                    amount = float(amount_raw)
                    if amount <= 0:
                        raise ValueError
                except ValueError:
                    flash("Amount must be a positive number.", "error")
                    return redirect(url_for("admin_services"))

                try:
                    government_amount = (
                        float(government_amount_raw) if government_amount_raw else 0
                    )
                    if government_amount < 0:
                        raise ValueError
                except ValueError:
                    flash("Government amount must be zero or a positive number.", "error")
                    return redirect(url_for("admin_services"))

                if government_amount > amount:
                    flash("Government amount cannot be more than the customer amount.", "error")
                    return redirect(url_for("admin_services"))

                new_filename = None
                if image and image.filename:
                    new_filename, error = save_upload(image)
                    if error:
                        flash(error, "error")
                        return redirect(url_for("admin_services"))
                    delete_upload(service.get("image_filename"))

                update_service(
                    service_id,
                    name,
                    amount,
                    new_filename,
                    request.form.getlist("document_ids"),
                    government_amount,
                )
                flash("Service updated successfully.", "success")

        elif action == "delete":
            service_id = request.form.get("service_id")
            service = get_service(service_id)
            if service:
                delete_upload(service.get("image_filename"))
                delete_service(service_id)
                flash("Service deleted successfully.", "success")
            else:
                flash("Service not found.", "error")

        return redirect(url_for("admin_services"))

    services = get_all_services()
    for service in services:
        service["government_amount"] = service.get("government_amount") or 0
        service["profit"] = service["amount"] - service["government_amount"]
    all_documents = get_all_documents()
    service_documents = {
        service["id"]: get_service_document_ids(service["id"]) for service in services
    }
    return render_template(
        "admin/services.html",
        services=services,
        all_documents=all_documents,
        service_documents=service_documents,
    )


@app.route("/admin/records")
@login_required
def admin_records():
    records = get_all_records()
    return render_template("admin/records.html", records=records)


@app.route("/admin/records/edit", methods=["POST"])
@login_required
def admin_records_edit():
    row_number = request.form.get("row_number", type=int)
    if not row_number:
        flash("Record not found.", "error")
        return redirect(url_for("admin_records"))

    errors, name, mobile, aadhaar = validate_submission(
        request.form.get("customer_name"),
        request.form.get("mobile"),
        request.form.get("aadhaar"),
    )
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("admin_records"))

    service_name = request.form.get("service_name", "").strip()
    if not service_name:
        flash("Service name is required.", "error")
        return redirect(url_for("admin_records"))

    try:
        amount = float(request.form.get("amount", "0") or 0)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be a positive number.", "error")
        return redirect(url_for("admin_records"))

    try:
        government_amount = float(request.form.get("government_amount", "0") or 0)
        if government_amount < 0:
            raise ValueError
    except ValueError:
        flash("Government amount must be zero or a positive number.", "error")
        return redirect(url_for("admin_records"))

    if government_amount > amount:
        flash("Government amount cannot be more than the customer amount.", "error")
        return redirect(url_for("admin_records"))

    updated = update_record(
        row_number,
        service_name,
        amount,
        name,
        mobile,
        aadhaar,
        request.form.get("status", "").strip(),
        request.form.get("reference_number", "").strip(),
        government_amount,
    )
    if updated:
        flash("Record updated successfully.", "success")
    else:
        flash("Record not found. It may have already been deleted.", "error")
    return redirect(url_for("admin_records"))


@app.route("/admin/records/delete", methods=["POST"])
@login_required
def admin_records_delete():
    row_number = request.form.get("row_number", type=int)
    if row_number and delete_record(row_number):
        flash("Record deleted successfully.", "success")
    else:
        flash("Record not found. It may have already been deleted.", "error")
    return redirect(url_for("admin_records"))


@app.route("/admin/reports")
@login_required
def admin_reports():
    report = get_monthly_report()
    return render_template(
        "admin/reports.html",
        overall=report["overall"],
        months=report["months"],
    )


@app.route("/admin/records/download")
@login_required
def admin_records_download():
    ensure_workbook_ready()
    if not config.EXCEL_PATH.exists():
        flash("No records file found yet.", "error")
        return redirect(url_for("admin_records"))
    return send_from_directory(
        config.EXCEL_PATH.parent,
        config.EXCEL_PATH.name,
        as_attachment=True,
    )


@app.route("/admin/documents", methods=["GET", "POST"])
@login_required
def admin_documents():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            name = request.form.get("name", "").strip()
            description = request.form.get("description", "").strip()
            is_mandatory = request.form.get("is_mandatory") == "1"

            if not name:
                flash("Document name is required.", "error")
            else:
                create_document(name, description, is_mandatory)
                flash("Document added successfully.", "success")

        elif action == "edit":
            document_id = request.form.get("document_id")
            name = request.form.get("name", "").strip()
            description = request.form.get("description", "").strip()
            is_mandatory = request.form.get("is_mandatory") == "1"

            document = get_document(document_id)
            if not document:
                flash("Document not found.", "error")
            elif not name:
                flash("Document name is required.", "error")
            else:
                update_document(document_id, name, description, is_mandatory)
                flash("Document updated successfully.", "success")

        elif action == "delete":
            document_id = request.form.get("document_id")
            document = get_document(document_id)
            if document:
                delete_document(document_id)
                flash("Document deleted successfully.", "success")
            else:
                flash("Document not found.", "error")

        return redirect(url_for("admin_documents"))

    documents = get_all_documents()
    return render_template("admin/documents.html", documents=documents)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    print(f"RI ENTERPRISES website running at http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop.")
    app.run(debug=True, host="0.0.0.0", port=port)
