# Migración del template de microservicio en NodeTS a Python (Parte 1)

## Introducción

La migración de un microservicio de NodeJS con TypeScript a Python busca aprovechar las capacidades y características que Python ofrece, optimizando el rendimiento, la escalabilidad y la mantenibilidad del servicio. Este documento detalla los objetivos principales de la migración y establece un plan de trabajo diario para asegurar una transición exitosa.

## Objetivos Principales

1. **Crear un README detallado para el nuevo proyecto en Python, siguiendo el formato del proyecto original en NodeTS.**
2. **Desarrollar una API en Python con todas las funciones y características equivalentes a la versión en NodeTS.**
3. **Realizar el despliegue de la aplicación en un entorno de producción.**
4. **Crear una imagen Docker del proyecto para facilitar su despliegue y escalabilidad en producción.**

### Nota importante sobre la organización del trabajo

Cada persona que siga este documento debe establecer sus propios subobjetivos de trabajo para cumplir con los objetivos principales. Es fundamental que cada lector divida las tareas en pasos alcanzables según su ritmo y necesidad, ajustándose a las metas descritas.

## Plan de Trabajo Diario

Para garantizar una migración organizada y eficiente, se seguirá un proceso diario que incluye el uso de GitHub para el control de versiones y la creación de commits específicos. A continuación, se detallan los pasos a seguir cada día:

### 1. Uso de GitHub

- **Repositorio Centralizado:** Todos los cambios y desarrollos se realizarán en un repositorio de GitHub, facilitando la colaboración y el seguimiento de las modificaciones. 
- **Ramas de Trabajo:** Se recomienda utilizar ramas específicas para cada objetivo o feature, permitiendo un desarrollo aislado y seguro antes de integrar los cambios a la rama development.

### 2. Creación de Commits

- **Commit por Objetivo:** Cada vez que se complete un objetivo o una funcionalidad específica, el lector debe realizar un commit describiendo detalladamente el trabajo realizado. Esto asegura un seguimiento claro del progreso y facilita la revisión de cambios.

```bash
    git add .
    git commit -m "Implementación de [descripción del objetivo/subobjetivo/funcionalidad]"
    git push origin [rama]
```

- **Commit por Día:** Cada vez que termine la jornada laboral se realizará un commit para ir detallando el trabajo por día.

```bash
    git add .
    git commit -m "Progreso del día [fecha]: [breve descripción de lo realizado]"
    git push origin [rama]
```
