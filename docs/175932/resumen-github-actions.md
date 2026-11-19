# Introducción a GitHub Actions — resumen del primer módulo

GitHub Actions automatiza tareas del repositorio mediante archivos YAML en
`.github/workflows/`. Un evento inicia un workflow, que contiene trabajos
(`jobs`); cada trabajo se ejecuta en un runner y contiene pasos (`steps`).

## Conceptos para la evaluación

- `on`: eventos, por ejemplo push, pull_request o workflow_dispatch (manual).
- `runs-on`: tipo de runner que ejecuta el trabajo.
- `run`: ejecuta un comando; `uses`: utiliza una acción.
- `needs`: establece dependencias; los trabajos independientes pueden ejecutarse en paralelo.
- `if`: condiciona la ejecución.
- `env`: variables de configuración. Las credenciales personales pertenecen a secrets.
- Los registros permiten revisar errores por trabajo y paso.
- Los artefactos conservan resultados; la caché evita descargar dependencias repetidamente.

## Práctica en este repositorio

`github-actions-demo.yml` adapta el inicio rápido oficial: muestra el evento,
identifica el runner, descarga el código y lista los archivos.
El pipeline de Neo4j añade comprobaciones previas y un trabajo dependiente con
`needs`, un servicio de base de datos y evidencia descargable.

Fuentes:
- [Resumen de Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/introduction-to-github-actions/11-summary)
- [Inicio rápido de GitHub](https://docs.github.com/es/actions/get-started/quickstart)

Este documento resume el contenido y la práctica; no acredita por sí mismo la
finalización del módulo en una cuenta de Microsoft Learn.
