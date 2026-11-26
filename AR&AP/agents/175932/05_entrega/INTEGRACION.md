# Entrega final

- Alumno: José Armando Palomo Cerda.
- Matrícula: 175932.
- Tema: A/R y A/P; capacidad acumulada de cuentas por pagar.
- Rama: feature/175932 en armekmc54-ops/ERP-simulator.
- Issue: https://github.com/jesusrevilla/ERP-simulator/issues/301
- PR: https://github.com/jesusrevilla/ERP-simulator/pull/302
- Pruebas: https://github.com/armekmc54-ops/ERP-simulator/actions/runs/45907283467

El plan se preparó localmente antes del código final. El Issue se publicó por
interfaz web después de los primeros commits porque el conector devolvió 403;
se conserva esta cronología real, sin simular avances de fechas anteriores.

El PR propone integrar el agente y sus evidencias al repositorio original.
La publicación del PR no equivale a aprobación ni merge. No se ejecuta una
fusión automática ni se afirma que los documentos productivos del ERP estén
ya conectados al adaptador de demostración.

El workflow propio APReceiptCapacityAgent pasa. En el repositorio original,
el control heredado Neo4j Tutorial Pipeline CI falla por URI de conexión vacía
y luego driver no definido en ingest_football_data.py. Ver run 45908209213.
No se afirma que todos los controles generales del repositorio estén en verde.

## Explicación breve para clase

El agente vigila cuántas piezas de una recepción ya están facturadas. Si recibo
10 y acepto una factura de 6, solo quedan 4 por facturar: por eso otra de 6 se
bloquea. Un crédito de cantidad de 2 libera capacidad y permite aceptar después
una nueva solicitud de 6. PostgreSQL decide con bloqueo de fila para proteger
operaciones simultáneas, Neo4j muestra las relaciones entre decisiones y
documentos y MongoDB guarda la bitácora. El outbox permite recuperar reportes
cuando falla una base secundaria sin duplicar el efecto de la factura.
