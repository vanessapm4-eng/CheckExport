from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from datetime import date
from apps.predios.models import Predio
from apps.checklist.models import FaseChecklist

@login_required
def reporte_pdf(request, predio_pk):
    predio = get_object_or_404(Predio, pk=predio_pk, usuarios=request.user)
    response = HttpResponse(content_type='application/pdf')
    nombre_archivo = f"reporte_fitosanitario_{predio.registro_ica}_{date.today()}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'

    doc = SimpleDocTemplate(
        response, pagesize=letter,
        topMargin=2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm
    )

    # ── Paleta rosa ──────────────────────────────────────────────────
    rosa       = colors.HexColor('#c14b85')
    rosa_dark  = colors.HexColor('#8f2f61')
    rosa_light = colors.HexColor('#f6dce9')
    rosa_borde = colors.HexColor('#e8b8d0')
    rojo       = colors.HexColor('#c0392b')
    rojo_light = colors.HexColor('#fdecea')
    amber      = colors.HexColor('#e8a020')
    amber_light= colors.HexColor('#fef3dc')
    gris       = colors.HexColor('#f5eef2')
    gris_texto = colors.HexColor('#5a4050')
    # ─────────────────────────────────────────────────────────────────

    styles = getSampleStyleSheet()
    estilo_normal = ParagraphStyle('normal', fontName='Helvetica',         fontSize=8, leading=11, textColor=colors.HexColor('#2c1f27'))
    estilo_item   = ParagraphStyle('item',   fontName='Helvetica',         fontSize=8, leading=12, textColor=colors.HexColor('#2c1f27'))
    estilo_norma  = ParagraphStyle('norma',  fontName='Helvetica-Oblique', fontSize=7, leading=10, textColor=gris_texto)

    elements = []

    # ── Encabezado ───────────────────────────────────────────────────
    header_data = [[
        Paragraph(
            f'<font size="18"><b>CheckExport</b></font><br/>'
            f'<font size="9" color="#5a4050">Sistema de Verificación Fitosanitaria</font>',
            styles['Normal']
        ),
        Paragraph(
            f'<font size="8" color="#5a4050">Resolución ICA 2191/2024<br/>'
            f'Flores ornamentales frescas<br/>'
            f'Generado: {date.today().strftime("%d/%m/%Y")}</font>',
            ParagraphStyle('right', alignment=2, fontSize=8, leading=12)
        )
    ]]
    header_table = Table(header_data, colWidths=[10*cm, 7*cm])
    header_table.setStyle(TableStyle([
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=2, color=rosa))
    elements.append(Spacer(1, 0.4*cm))

    # ── Info del predio ───────────────────────────────────────────────
    porcentaje = predio.porcentaje_cumplimiento()
    if porcentaje >= 80:
        color_pct    = rosa
        estado_texto = 'CUMPLIMIENTO ALTO'
    elif porcentaje >= 50:
        color_pct    = amber
        estado_texto = 'CUMPLIMIENTO MEDIO'
    else:
        color_pct    = rojo
        estado_texto = 'CUMPLIMIENTO BAJO'

    predio_data = [[
        Paragraph(f'<b>Predio:</b> {predio.nombre}',                                 estilo_normal),
        Paragraph(f'<b>Registro ICA:</b> {predio.registro_ica}',                     estilo_normal),
        Paragraph(f'<b>Municipio:</b> {predio.municipio}, {predio.departamento}',    estilo_normal),
        Paragraph(f'<font color="{color_pct.hexval()}"><b>{porcentaje}% — {estado_texto}</b></font>', estilo_normal),
    ]]
    predio_table = Table(predio_data, colWidths=[4.5*cm, 4*cm, 5*cm, 3.5*cm])
    predio_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), gris),
        ('PADDING',    (0,0), (-1,-1), 8),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(predio_table)
    elements.append(Spacer(1, 0.5*cm))

    # ── Resumen de cumplimiento ───────────────────────────────────────
    registros_all = predio.registros_checklist.all()
    total      = registros_all.exclude(estado='na').count()
    cumplen    = registros_all.filter(estado='cumple').count()
    no_cumplen = registros_all.filter(estado='no_cumple').count()
    pendientes = registros_all.filter(estado='pendiente').count()

    resumen_data = [
        ['', 'Cantidad'],
        ['✓  Cumplen',     str(cumplen)],
        ['✗  No cumplen',  str(no_cumplen)],
        ['⏳  Pendientes', str(pendientes)],
        ['Total evaluados',str(total)],
    ]
    resumen_table = Table(resumen_data, colWidths=[5*cm, 3*cm])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), rosa_dark),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,1), (-1,1), rosa_light),
        ('BACKGROUND', (0,2), (-1,2), rojo_light),
        ('BACKGROUND', (0,3), (-1,3), amber_light),
        ('GRID',       (0,0), (-1,-1), 0.3, rosa_borde),
        ('PADDING',    (0,0), (-1,-1), 6),
        ('FONTNAME',   (0,1), (0,-1), 'Helvetica-Bold'),
    ]))
    elements.append(Paragraph(
        '<b>Resumen de cumplimiento</b>',
        ParagraphStyle('titulo', fontName='Helvetica-Bold', fontSize=10,
                       spaceBefore=4, spaceAfter=6, textColor=rosa_dark)
    ))
    elements.append(resumen_table)
    elements.append(Spacer(1, 0.5*cm))

    # ── Detalle por fases ─────────────────────────────────────────────
    elements.append(Paragraph(
        '<b>Detalle por fases — Anexo 2</b>',
        ParagraphStyle('titulo', fontName='Helvetica-Bold', fontSize=10,
                       spaceBefore=4, spaceAfter=6, textColor=rosa_dark)
    ))

    for fase in FaseChecklist.objects.prefetch_related('items').all():
        elements.append(Paragraph(
            fase.nombre,
            ParagraphStyle('fase', fontName='Helvetica-Bold', fontSize=9,
                           textColor=rosa_dark, spaceBefore=8, spaceAfter=4,
                           backColor=rosa_light, borderPadding=4)
        ))

        # 4 columnas: #, Requisito, Norma, Estado  (sin Observación)
        tabla_data = [['#', 'Requisito fitosanitario', 'Norma', 'Estado']]
        items_list = list(fase.items.all())

        for i, item in enumerate(items_list, 1):
            try:
                reg    = predio.registros_checklist.get(item=item)
                estado = reg.get_estado_display()
                if reg.estado == 'cumple':
                    color_fila  = rosa_light
                    color_estado = rosa
                elif reg.estado == 'no_cumple':
                    color_fila  = rojo_light
                    color_estado = rojo
                elif reg.estado == 'na':
                    color_fila  = gris
                    color_estado = gris_texto
                else:
                    color_fila  = colors.white
                    color_estado = amber
            except Exception:
                estado       = 'Pendiente'
                color_fila   = colors.white
                color_estado = amber

            tabla_data.append([
                str(i),
                Paragraph(item.descripcion[:100], estilo_item),
                Paragraph(item.norma_referencia[:25] if item.norma_referencia else '', estilo_norma),
                Paragraph(
                    f'<b>{estado}</b>',
                    ParagraphStyle('est', fontName='Helvetica-Bold', fontSize=8, textColor=color_estado)
                ),
            ])

        # Anchos: #(0.6) + Requisito(9.5) + Norma(3) + Estado(2.9) = 16 cm ≈ página útil
        tabla = Table(tabla_data, colWidths=[0.6*cm, 9.5*cm, 3*cm, 2.9*cm])
        tabla_style = [
            ('BACKGROUND', (0,0), (-1,0), rosa_dark),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,-1), 8),
            ('GRID',       (0,0), (-1,-1), 0.3, rosa_borde),
            ('VALIGN',     (0,0), (-1,-1), 'TOP'),
            ('PADDING',    (0,0), (-1,-1), 5),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, gris]),
        ]
        for idx, item in enumerate(items_list, 1):
            try:
                reg = predio.registros_checklist.get(item=item)
                if reg.estado == 'cumple':
                    tabla_style.append(('BACKGROUND', (0,idx), (-1,idx), rosa_light))
                elif reg.estado == 'no_cumple':
                    tabla_style.append(('BACKGROUND', (0,idx), (-1,idx), rojo_light))
            except Exception:
                pass

        tabla.setStyle(TableStyle(tabla_style))
        elements.append(tabla)
        elements.append(Spacer(1, 0.3*cm))

    # ── Pie de página ─────────────────────────────────────────────────
    elements.append(Spacer(1, 0.5*cm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=rosa_borde))
    elements.append(Paragraph(
        f'Documento generado por CheckExport · '
        f'{date.today().strftime("%d de %B de %Y")} · Resolución ICA 2191/2024',
        ParagraphStyle('pie', fontName='Helvetica-Oblique', fontSize=7,
                       textColor=gris_texto, alignment=1, spaceBefore=6)
    ))

    doc.build(elements)
    return response