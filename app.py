app.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Digite o nome do funcionário:")
    context.user_data["etapa"] = "nome"

async def coletar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    etapa = context.user_data.get("etapa")

    if etapa == "nome":
        context.user_data["nome"] = texto
        await update.message.reply_text("Cargo:")
        context.user_data["etapa"] = "cargo"

    elif etapa == "cargo":
        context.user_data["cargo"] = texto
        await update.message.reply_text("Empresa:")
        context.user_data["etapa"] = "empresa"

    elif etapa == "empresa":
        context.user_data["empresa"] = texto

        file_name = f"Carta_{context.user_data['nome']}.pdf"
        doc = SimpleDocTemplate(file_name, pagesize=A4)
        styles = getSampleStyleSheet()

        texto_pdf = f"""
        À quem possa interessar,

        Apresentamos {context.user_data['nome']}, que atuará como {context.user_data['cargo']} na empresa {context.user_data['empresa']}.

        Atenciosamente,
        {context.user_data['empresa']}
        """

        elements = [Paragraph(texto_pdf, styles["Normal"])]
        doc.build(elements)

        await update.message.reply_document(document=open(file_name, "rb"))
        context.user_data.clear()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, coletar))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url="https://telegramgeracartas.onrender.com"

    )
Commit changes
