from telegram import Update
from telegram.ext import ContextTypes
from utils.Validators import is_valid_ip, is_valid_domain, sanitize_entity
from utils.Ocr import extract_ip_or_domain_from_image
from utils.Qr_Decoder import extract_from_qr
from utils.Intelligence import analyze_entity
from utils.report import generate_html_report
import os
from uuid import uuid4
from pathlib import Path
import socket

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an IP/domain as text or image (OCR/QR).")
#help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me an IP or domain in text or image (OCR/QR).\n"
        "Supported input:\n"
        "• Text: IP or domain\n"
        "• Image: QR code or image with IP/domain\n\n"
        "Unsupported inputs will be ignored."
    )    
# Handle unsupported files that not picture or text.
async def handle_unsupported(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" Unsupported format. Please send text with an IP/domain or a valid image only.")

# Handle text input
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original = sanitize_entity(update.message.text.strip())
    resolved_ip = original

    if is_valid_domain(original):
         try:
            resolved_ip = socket.gethostbyname(original)
            await update.message.reply_text(f"The domain {original} resolves to IP: {resolved_ip}")
         except socket.gaierror:
            resolved_ip = None
            await update.message.reply_text(f"Could not resolve domain: {original}. It may not exist.")

    elif not is_valid_ip(original):
        await update.message.reply_text("Unsupported format. Please send text with an IP/domain or a valid image only.")
        return

    await update.message.reply_text(f"Analyzing ...")

    try:
        results = analyze_entity(original, resolved_ip)
        report_path = generate_html_report(original, results)
        with open(report_path, "rb") as report_file:
            await update.message.reply_document(document=report_file)
        try:
            os.remove(report_path)
        except OSError:
            pass
    except Exception as e:
        await update.message.reply_text(f"Error during analysis: {e}")

# Handle image messages (OCR or QR)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = f"/tmp/{uuid4().hex}.jpg"
    await file.download_to_drive(file_path)

    extracted = extract_from_qr(file_path) or extract_ip_or_domain_from_image(file_path) or []
    if isinstance(extracted, str):
        extracted = [extracted]

    if extracted:
        for original in extracted:
            original = sanitize_entity(original)
            resolved_ip = original

            if is_valid_domain(original):
                try:
                    resolved_ip = socket.gethostbyname(original)
                    await update.message.reply_text(f"The domain {original} resolves to IP: {resolved_ip}")
                except socket.gaierror:
                    resolved_ip = None
                    await update.message.reply_text(f"Could not resolve domain: {original}. It may not exist.")

            elif not is_valid_ip(original):
                await update.message.reply_text(f"Ignored unsupported input: {original}")
                continue

            await update.message.reply_text(f"Analyzing ...")

            try:
                results = analyze_entity(original, resolved_ip)
                report_path = generate_html_report(original, results)
                with open(report_path, "rb") as report_file:
                    await update.message.reply_document(document=report_file)
                try:
                    os.remove(report_path)
                except OSError:
                    pass
            except Exception as e:
                await update.message.reply_text(f"Error during analysis: {e}")
    else:
        await update.message.reply_text("Could not extract valid IP/domain from image.")

    try:
        os.remove(file_path)
    except OSError:
        pass