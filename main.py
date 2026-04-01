from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import shutil
import tempfile
import os
import uuid
import boto3
from botocore.client import Config

app = FastAPI()

R2_ACCESS_KEY = "862f75946a5dfb47607dd8a027490d2a"
R2_SECRET_KEY = "f7ca3cad76f6659b0ee4c3c3f0ed392c2306f8ec8db7d47604408d9d292ba90e"



R2_ENDPOINT = "https://1fd52e7b154a3635b4c72513c9c0b901.r2.cloudflarestorage.com"
R2_PUBLIC_BASE_URL = "https://mwabaprod.consulttechies.com"


class HtmlToR2Payload(BaseModel):
    html: str
    path: str
    bucket: str


def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )


@app.post("/html-to-pdf-r2")
def html_to_pdf_r2(payload: HtmlToR2Payload):
    html_fd, html_path = tempfile.mkstemp(suffix=".html")
    last_segment = payload.path.rstrip('/').split('/')[-1]
    pdf_filename = last_segment if last_segment.endswith('.pdf') else f"{last_segment}.pdf"
    pdf_path = os.path.join(tempfile.gettempdir(), pdf_filename)

    try:
        with os.fdopen(html_fd, "w", encoding="utf-8") as f:
            f.write(payload.html)

        wkhtmltopdf_bin = shutil.which("wkhtmltopdf")
        if not wkhtmltopdf_bin:
            return {"success": False, "error": "wkhtmltopdf is not installed or not in PATH"}
        result = subprocess.run(
            [wkhtmltopdf_bin, "--quiet", html_path, pdf_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode != 0:
            return {
                "error": "PDF generation failed",
                "details": result.stderr.decode("utf-8", errors="ignore"),
            }

        r2 = get_r2_client()
        path_parts = payload.path.rstrip("/").split("/")
        path_dir = "/".join(path_parts[:-1])   # "Media/3/7/Receipt"
        object_key = f"{path_dir}/{pdf_filename}"  # "Media/3/7/Receipt/receipt_KayzLN.pdf"

        with open(pdf_path, "rb") as f:
            r2.upload_fileobj(
                f,
                payload.bucket,
                object_key,
                ExtraArgs={"ContentType": "application/pdf"},
            )

        file_url = f"{R2_PUBLIC_BASE_URL}/{object_key}"

        return {
            "status": "success",
            "fileName": pdf_filename,
            "url": file_url,
            "mimeType": "application/pdf",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

    finally:
        if os.path.exists(html_path):
            os.remove(html_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
