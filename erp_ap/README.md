# 175932 — grafo ERP de cuentas por pagar (AP)

## Problema y alcance

Evitar autorizar una factura sin comprobar la orden de compra y la recepción.
Es una demostración de conciliación de tres vías con datos sintéticos: cada
documento tiene un artículo CPU, moneda MXN y una recepción como máximo.
No ejecuta pagos bancarios ni sustituye la contabilidad SQL.

El grafo conecta Supplier → PurchaseOrder ← Invoice → Receipt → PurchaseOrder.
Los nodos llevan la etiqueta APDemo para separar la práctica de los datos de fútbol.
Los importes se representan en centavos enteros, sin errores de punto flotante.

## Reglas y validación

Se basan en `AR&AP/AR&AP-Req.md` y
`AR&AP/Flowchart and requirements APAR 181779.md`:
proveedor activo, existencia de recepción, cantidades positivas, precios no
negativos, recepción no superior a la OC, factura no superior a lo recibido y
precio coincidente. Se usa tolerancia cero como decisión explícita para esta
práctica; la documentación general deja la tolerancia a Finanzas.

`schema.cypher` crea una restricción de identidad.
`load.cypher` crea nodos y relaciones mediante MERGE.
`validate.cypher` devuelve la decisión y el motivo de cada factura.
`rules.py` proporciona una referencia independiente y `test_rules.py` cubre
siete escenarios. `run_graph.py` compara las decisiones reales de Cypher
contra esa referencia y comprueba que recargar no duplica nodos ni relaciones.

Dos casos deben autorizarse (factura completa y parcial); cinco deben bloquearse:
cantidad excesiva, precio distinto, recepción ausente, proveedor inactivo y
cantidad cero. Un caso rechazado correctamente es una prueba exitosa.

## Reporte del agente y evidencia

APValidationAgent registra una actividad THREE_WAY_MATCH por factura, con
identificador, decisión, permiso de pago y fecha. AgentReport se enlaza a Invoice.
Los resultados reales se escriben en `evidence/results.json` y en el resumen del job.

Ejecutar con Python 3.12 y las dependencias de `tutorial_175932/requirements.txt`:

```sh
python -m unittest discover -s erp_ap -p test_rules.py
python erp_ap/run_graph.py
```

La segunda orden requiere NEO4J_URI, NEO4J_USERNAME y NEO4J_PASSWORD.
El pipeline usa un Neo4j temporal sin secretos de Aura y publica el artefacto
`neo4j-and-erp-ap-evidence`. Revisar todos los controles antes de solicitar el merge.
No se modificaron los esquemas SQL ni se automatizó el merge.
