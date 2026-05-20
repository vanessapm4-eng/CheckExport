# apps/checklist/management/commands/cargar_checklist_exportador.py
from django.core.management.base import BaseCommand
from apps.checklist.models import FaseChecklist, ItemChecklist

FASES = [
    {
        "nombre": "1. Registro del exportador ante el ICA",
        "orden": 1,
        "items": [
            {"desc": "Inscripción realizada en el sistema SimplifICA como exportador (Art. 4)", "norma": "Res. ICA 2191/2024, Art. 4"},
            {"desc": "Asistente técnico (Ing. Agrónomo) inscrito en SimplifICA con registro de sanidad vegetal vigente (Art. 12.1.4)", "norma": "Art. 12.1.4"},
            {"desc": "Número y fecha de vencimiento del registro SV del asistente técnico registrado (Art. 12.1.4)", "norma": "Art. 12.1.4"},
            {"desc": "Pago de tarifa ICA vigente para generación del registro de exportador (Art. 12.4)", "norma": "Art. 12.4"},
            {"desc": "Tipo de propiedad, posesión o tenencia del área de poscosecha declarado (Art. 12.1.5)", "norma": "Art. 12.1.5"},
            {"desc": "Coordenadas geográficas en grados decimales del área de poscosecha registradas (Art. 12.1.2)", "norma": "Art. 12.1.2"},
            {"desc": "Especies a exportar (nombre común y científico) con proveedores y números de registro declarados (Art. 12.1.3)", "norma": "Art. 12.1.3"},
        ]
    },
    {
        "nombre": "2. Requisitos documentales (Art. 12.2)",
        "orden": 2,
        "items": [
            {"desc": "Documento con distribución interna y flujo secuencial de procesos en poscosecha elaborado y adjunto (Art. 12.2.1)", "norma": "Art. 12.2.1"},
            {"desc": "Plan de Manejo Integrado de Plagas para exportadores (Anexo 2) elaborado, firmado por asistente técnico y adjunto (Art. 12.2.2)", "norma": "Art. 12.2.2 / Anexo 2"},
            {"desc": "Sistema documentado de control de procesos (facturas, constancias) que respaldan procedencia y sanidad implementado (Art. 12.2.3)", "norma": "Art. 12.2.3"},
            {"desc": "Informe fitosanitario suscrito por el asistente técnico adjunto (Art. 12.2.4)", "norma": "Art. 12.2.4"},
            {"desc": "Croquis con ruta detallada al lugar de poscosecha adjunto (Art. 12.2.5)", "norma": "Art. 12.2.5"},
            {"desc": "Copia del registro de sanidad vegetal vigente del asistente técnico adjunta (Art. 12.2.6)", "norma": "Art. 12.2.6"},
        ]
    },
    {
        "nombre": "3. Infraestructura del área de poscosecha (Art. 12.3)",
        "orden": 3,
        "items": [
            {"desc": "Área de manejo de residuos vegetales aislada, señalizada y con separación física que mitigue riesgo fitosanitario (Art. 12.3.1)", "norma": "Art. 12.3.1"},
            {"desc": "Área de almacenamiento de materiales e insumos con estructura sólida, techo, ventilación e iluminación adecuada (Art. 12.3.2)", "norma": "Art. 12.3.2"},
            {"desc": "Área de almacenamiento separada físicamente del flujo secuencial del material vegetal (Art. 12.3.2)", "norma": "Art. 12.3.2"},
            {"desc": "Área de poscosecha con capacidad instalada suficiente para el volumen de exportación y de uso exclusivo (Art. 12.3.3.1)", "norma": "Art. 12.3.3.1"},
            {"desc": "Flujo secuencial del material vegetal desde ingreso hasta despacho, sin contraflujo ni contaminación cruzada (Art. 12.3.3.2)", "norma": "Art. 12.3.3.2"},
            {"desc": "Cerramiento perimetral externo con material rígido que impide ingreso de artrópodos u otras plagas (Art. 12.3.3.3)", "norma": "Art. 12.3.3.3"},
            {"desc": "Piso rígido, impermeable, liso, lavable, no poroso, sin grietas ni fisuras, apto para alto tráfico (Art. 12.3.3.4)", "norma": "Art. 12.3.3.4"},
            {"desc": "Área de monitoreo debidamente aislada físicamente del resto del proceso de poscosecha (Art. 12.3.3.5)", "norma": "Art. 12.3.3.5"},
            {"desc": "Puertas de ingreso y salida con cierre automático o permanentemente cerradas (Art. 12.3.3.6)", "norma": "Art. 12.3.3.6"},
            {"desc": "Área administrativa y de almacenamiento de insumos separadas y señalizadas del flujo de poscosecha (Art. 12.3.3.7)", "norma": "Art. 12.3.3.7"},
            {"desc": "Cubierta (techo) íntegra de material impermeable, resistente a granizadas y que impide ingreso de plagas (Art. 12.3.3.8)", "norma": "Art. 12.3.3.8"},
        ]
    },
    {
        "nombre": "4. Plan MIP - Identificación de plagas (Anexo 2, cap. 1)",
        "orden": 4,
        "items": [
            {"desc": "Plagas clave identificadas taxonómicamente a nivel de especie por profesional especializado o entidad certificada", "norma": "Anexo 2, cap. 1.1"},
            {"desc": "Certificación de identidad taxonómica incluye método de identificación empleado", "norma": "Anexo 2, cap. 1.1"},
            {"desc": "Información biológica de las plagas presentes documentada (ciclo de vida, hábitos, daños)", "norma": "Anexo 2, cap. 1.2"},
            {"desc": "Plagas de control oficial identificadas: Puccinia horiana (Roya Blanca) y Thrips palmi (Art. 17.1.3)", "norma": "Art. 17.1.3 / Anexo 2"},
        ]
    },
    {
        "nombre": "5. Plan MIP - Prevención de plagas (Anexo 2, cap. 2)",
        "orden": 5,
        "items": [
            {"desc": "Prácticas profilácticas del proceso de poscosecha documentadas e implementadas", "norma": "Anexo 2, cap. 2"},
            {"desc": "Programa de limpieza y desinfección de instalaciones, empaques y equipos de poscosecha con seguimiento (Art. 17.1.17.5)", "norma": "Art. 17.1.17.5 / Anexo 2"},
            {"desc": "Medidas de bioseguridad para evitar ingreso y diseminación de plagas en poscosecha implementadas", "norma": "Anexo 2, cap. 2"},
            {"desc": "Plan Nacional de Prevención Roya Blanca del Crisantemo (Puccinia horiana) implementado (Art. 17.1.3)", "norma": "Art. 17.1.3"},
            {"desc": "Plan de Detección, Prevención y Contingencia de Thrips palmi implementado (Art. 17.1.3)", "norma": "Art. 17.1.3"},
        ]
    },
    {
        "nombre": "6. Plan MIP - Monitoreo de plagas (Anexo 2, cap. 3)",
        "orden": 6,
        "items": [
            {"desc": "Sistema de monitoreo periódico de plagas en poscosecha implementado y con registros actualizados", "norma": "Anexo 2, cap. 3"},
            {"desc": "Sitio de monitoreo habilitado: mesa lisa de color adecuado, buena iluminación, lupa, pinzas, pinceles (Art. 3.35)", "norma": "Art. 3.35 / Anexo 2"},
            {"desc": "Registros de monitoreo de trips (Thysanoptera) disponibles y actualizados", "norma": "Anexo 2, cap. 3"},
            {"desc": "Registros de monitoreo de ácaros disponibles y actualizados", "norma": "Anexo 2, cap. 3"},
            {"desc": "Registros de monitoreo de mosca blanca disponibles y actualizados", "norma": "Anexo 2, cap. 3"},
            {"desc": "Umbral de acción definido para cada plaga clave del proceso de poscosecha", "norma": "Anexo 2, cap. 3"},
            {"desc": "Programa de monitoreo reportado trimestralmente al ICA (Art. 17.1.12)", "norma": "Art. 17.1.12"},
        ]
    },
    {
        "nombre": "7. Plan MIP - Control de plagas (Anexo 2, cap. 4)",
        "orden": 7,
        "items": [
            {"desc": "Medidas de control físico, biológico y químico documentadas para cada plaga clave", "norma": "Anexo 2, cap. 4"},
            {"desc": "Productos fitosanitarios aplicados autorizados por el ICA con registro vigente", "norma": "Anexo 2, cap. 4"},
            {"desc": "Registros de aplicaciones fitosanitarias incluyen: producto, dosis, fecha, lote y responsable", "norma": "Anexo 2, cap. 4"},
            {"desc": "Períodos de carencia de productos fitosanitarios cumplidos antes del despacho", "norma": "Anexo 2, cap. 4"},
            {"desc": "Acciones ejecutadas ante interceptaciones en país de destino reportadas al ICA (Art. 17.1.7)", "norma": "Art. 17.1.7"},
        ]
    },
    {
        "nombre": "8. Trazabilidad y documentación (Art. 17.1)",
        "orden": 8,
        "items": [
            {"desc": "Todos los proveedores cuentan con registro ICA vigente de lugar de producción o exportador (Art. 17.1.2)", "norma": "Art. 17.1.2"},
            {"desc": "Lista de proveedores actualizada en SimplifICA (Art. 17.1.13)", "norma": "Art. 17.1.13"},
            {"desc": "Cada envío respaldado con Certificado Fitosanitario o Constancia Fitosanitaria según país destino (Art. 17.1.8)", "norma": "Art. 17.1.8"},
            {"desc": "Material vegetal acompañado de solicitud de inspección ICA o constancia fitosanitaria del asistente técnico (Art. 17.1.10)", "norma": "Art. 17.1.10"},
            {"desc": "Empaques nuevos con etiqueta: nombre exportador, N° registro exportador, N° registro proveedor (Art. 17.1.14)", "norma": "Art. 17.1.14"},
            {"desc": "Constancias fitosanitarias que avalan movimiento de flores hacia exportación disponibles (Art. 17.1.17.4)", "norma": "Art. 17.1.17.4"},
            {"desc": "Actas de visitas del ICA al exportador disponibles y accesibles (Art. 17.1.17.1)", "norma": "Art. 17.1.17.1"},
            {"desc": "Resguardo fitosanitario garantizado durante transporte hacia aeropuertos o puertos (Art. 17.1.9)", "norma": "Art. 17.1.9"},
            {"desc": "Cumplimiento de la Convención CITES para las especies exportadas (Art. 17.1.15)", "norma": "Art. 17.1.15"},
        ]
    },
    {
        "nombre": "9. Capacitación y asistencia técnica (Art. 17.1.11)",
        "orden": 9,
        "items": [
            {"desc": "Programa de capacitación fitosanitaria del personal de poscosecha documentado y con seguimiento (Art. 17.1.17.3)", "norma": "Art. 17.1.17.3"},
            {"desc": "Todo el personal capacitado en fitosanidad según sus funciones en el proceso de exportación (Art. 17.1.11)", "norma": "Art. 17.1.11"},
            {"desc": "Bitácora de visitas del asistente técnico con recomendaciones fitosanitarias documentada (Art. 17.2.11)", "norma": "Art. 17.2.11"},
            {"desc": "Asistente técnico con contrato vigente y registro SV actualizado en SimplifICA (Art. 17.2.1)", "norma": "Art. 17.2.1"},
            {"desc": "Asistente técnico ha asistido a eventos programados por el ICA (Art. 17.2.4)", "norma": "Art. 17.2.4"},
        ]
    },
    {
        "nombre": "10. Planes de trabajo con ONPF países destino (Art. 17.1.6)",
        "orden": 10,
        "items": [
            {"desc": "Planes de trabajo fitosanitarios con ONPF de países de destino identificados y cumplidos (Art. 17.1.6)", "norma": "Art. 17.1.6"},
            {"desc": "Requisitos fitosanitarios adicionales de los países de destino verificados y cumplidos (Art. 25)", "norma": "Art. 25"},
            {"desc": "Informes trimestrales del estado fitosanitario presentados al ICA en el aplicativo correspondiente (Art. 17.1.12)", "norma": "Art. 17.1.12"},
        ]
    },
]

class Command(BaseCommand):
    help = 'Carga el checklist del Anexo 2 - Resolución ICA 2191/2024 (exportadores)'

    def handle(self, *args, **options):
        total_items = 0
        for fase_data in FASES:
            fase, created = FaseChecklist.objects.get_or_create(
                nombre=fase_data['nombre'],
                defaults={'orden': fase_data['orden']}
            )
            accion = 'Creada' if created else 'Ya existía'
            for item_data in fase_data['items']:
                _, item_created = ItemChecklist.objects.get_or_create(
                    fase=fase,
                    descripcion=item_data['desc'],
                    defaults={'norma_referencia': item_data['norma']}
                )
                if item_created:
                    total_items += 1
            self.stdout.write(f'  {accion}: {fase.nombre} ({len(fase_data["items"])} ítems)')

        self.stdout.write(self.style.SUCCESS(
            f'\nChecklist Anexo 2 cargado: {total_items} ítems nuevos en {len(FASES)} fases.'
        ))