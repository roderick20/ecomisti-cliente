from flask import Blueprint, send_file, current_app, request
from datetime import datetime, date, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from collections import defaultdict
from modules.task.models.tarea_model import TareaModel
import os
#task_bp = Blueprint('task', __name__)

from .. import bp 

@bp.route('/task/pdf-diario')
def generar_pdf_diario():
    # === 1. Obtener tareas ===
    tareas = (TareaModel.get_all())['data']

    # === 2. Fecha de hoy ===
    hoy = date.today()

    # === 3. Filtrar tareas del día ===
    tareas_hoy = []
    for tarea in tareas:
        if tarea['fecha_inicio']:
            if isinstance(tarea['fecha_inicio'], str):
                # Si viene como string, parsearlo (ajusta el formato si es necesario)
                fecha_tarea = datetime.fromisoformat(tarea['fecha_inicio'].split('T')[0]).date()
            else:
                fecha_tarea = tarea['fecha_inicio'].date()
            if fecha_tarea == hoy:
                tareas_hoy.append(tarea)

    # === 4. Generar PDF ===
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=50, bottomMargin=30)
    elements = []

    styles = getSampleStyleSheet()

    # === LOGO ===
    logo_path = os.path.join(current_app.root_path, 'static', 'img', 'logo.png')  # Ajusta la ruta
    print(logo_path)
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=(235 / 130) * inch, height=(50 / 130) * inch) # 96
        logo.hAlign = 'LEFT'
        elements.append(logo)
        elements.append(Spacer(1, 12))

    # === Título ===
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=1  # centrado
    )
    elements.append(Paragraph(f"Tareas del Día: {hoy.strftime('%d/%m/%Y')}", title_style))
    elements.append(Spacer(1, 12))

    # === Listado de tareas ===
    if tareas_hoy:
        for tarea in tareas_hoy:
            titulo = tarea.get('titulo', 'Sin título')
            descripcion = tarea.get('descripcion', '') or ''
            # Limitar descripción si es muy larga
            if len(descripcion) > 100:
                descripcion = descripcion[:100] + '…'
            content = f"<b>{titulo}</b><br/>{descripcion}"
            elements.append(Paragraph(content, styles['Normal']))
            elements.append(Spacer(1, 8))
    else:
        elements.append(Paragraph("<i>No hay tareas programadas para hoy.</i>", styles['Normal']))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"<i>Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}</i>", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=False,
        download_name=f"tareas_{hoy.strftime('%Y%m%d')}.pdf",
        mimetype='application/pdf')


def get_week_dates(base_date=None):
    """Devuelve las fechas (date) de la semana (lunes a domingo) que contiene base_date."""
    if base_date is None:
        base_date = date.today()
    elif isinstance(base_date, datetime):
        base_date = base_date.date()
    monday = base_date - timedelta(days=base_date.weekday())
    return [monday + timedelta(days=i) for i in range(7)]

@bp.route('/task/pdf-semanal')
def generar_pdf_semanal():
    # === 1. Obtener las tareas (ajusta esto a tu modelo real) ===
    # Ejemplo: tareas = Tarea.query.all()
    # Asegúrate de que cada tarea tiene .fecha_inicio (datetime) y .titulo, .descripcion
    # from .models import Tarea  # ← Ajusta según tu estructura
    tareas = (TareaModel.get_all())['data']   

    # === 2. Determinar la semana (por defecto: semana actual) ===
    fecha_param = request.args.get('fecha')
    if fecha_param:
        try:
            base_date = datetime.fromisoformat(fecha_param).date()
        except:
            base_date = date.today()
    else:
        base_date = date.today()

    week_dates = get_week_dates(base_date)  # lista de 7 objetos `date`
    week_date_set = set(week_dates)

    # === 3. Agrupar tareas por día (solo si fecha_inicio está en la semana) ===
    tareas_por_dia = defaultdict(list)
    for tarea in tareas:
        print(tarea['fecha_inicio'])
        if tarea['fecha_inicio']:  # asegurarse de que no sea None
            fecha_tarea = tarea['fecha_inicio'].date()  # ✅ extraer solo la fecha
            if fecha_tarea in week_date_set:
                tareas_por_dia[fecha_tarea].append(tarea)

    # === 4. Generar PDF ===
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=30, bottomMargin=30)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=1  # centrado
    )

    semana_str = f"Calendario Semanal: {week_dates[0].strftime('%d/%m/%Y')} – {week_dates[-1].strftime('%d/%m/%Y')}"
    elements.append(Paragraph("Tareas - Vista Semanal", title_style))
    elements.append(Paragraph(semana_str, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Encabezados
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    fechas_cabecera = [d.strftime('%d/%m') for d in week_dates]

    # Contenido por día
    contenido_dias = []
    for d in week_dates:
        tareas_dia = tareas_por_dia.get(d, [])
        if tareas_dia:
            # Limitar descripción a ~70 caracteres para no desbordar
            items = []
            for t in tareas_dia:
                desc = (t['descripcion'] or '')[:70]
                if len(t['descripcion'] or '') > 70:
                    desc += '…'
                items.append(f"<b>{t['titulo']}</b>: {desc}")
            texto = "<br/>".join(items)
        else:
            texto = "<i>Sin tareas</i>"
        contenido_dias.append(Paragraph(texto, styles['Normal']))

    # Crear tabla: 3 filas x 7 columnas
    data = [dias_semana, fechas_cabecera, contenido_dias]
    table = Table(data, colWidths=[1.5 * inch] * 7)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('BACKGROUND', (0, 1), (-1, 1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<i>Documento generado el " + datetime.now().strftime('%d/%m/%Y %H:%M') + "</i>", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=False,
        download_name="calendario_semanal_tareas.pdf",
        mimetype='application/pdf'
    )