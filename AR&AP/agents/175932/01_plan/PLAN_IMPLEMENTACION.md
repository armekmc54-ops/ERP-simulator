# Plan de implementación - 26/11/2026

Estado: preparación local autorizada hasta fase 3. No commits, no publicación de Issue, no PR, no ejecución de pruebas.

1. Investigación y plan: delimitar el problema acumulado, referencias y entregables en ISSUE_BORRADOR.md.
2. Diseño: contrato de evento, reglas, persistencia y límites en ../02_diseno/DISENO.md.
3. Implementación: esquema y función PostgreSQL, cliente Python, exportador de outbox, consultas Cypher y MongoDB.
4. Pendiente de autorización: preparar y ejecutar pruebas unitarias/integración/concurrencia; registrar resultados reales.
5. Pendiente: evidencia visual, PDF, commits por avances reales y PR hacia jesusrevilla/ERP-simulator.

## Mapa de archivos

- 03_implementacion/sql/schema.sql: esquema aislado, restricciones y función transaccional de decisión.
- 03_implementacion/agent.py: contrato Python, inicialización, registro de recepciones de demostración, evaluación y exportación.
- 03_implementacion/graph.cypher: proyección idempotente del evento y sus relaciones.
- 03_implementacion/consultas.cypher: inspección del grafo.
- 03_implementacion/consultas_mongo.js: validación y consultas de bitácora.
- 03_implementacion/examples/*.json: entradas sintéticas; no son evidencia de ejecución.

## Verificación futura

Las pruebas deben demostrar dos facturas contra la misma recepción, frontera exacta,
créditos parciales y excesivos, eventos repetidos y colisión de clave,
proveedor/recepción inválidos, bloqueo concurrente de capacidad y recuperación
del outbox cuando una base secundaria no está disponible.

No se afirma que esas pruebas hayan pasado.
