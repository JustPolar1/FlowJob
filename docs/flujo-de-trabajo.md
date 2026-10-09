# Flujo de trabajo y reglas de colaboración

## Flujo seleccionado

Se propone utilizar **GitHub Flow**. El equipo trabajará con una rama principal estable y ramas breves por cambio. Cada cambio se propondrá mediante un Pull/Merge Request (PR/MR), será revisado por otro integrante y se integrará después de su aprobación.

Este flujo es adecuado para FlowJob porque el proyecto se desarrollará de forma continua por funcionalidades y el equipo necesita que el historial muestre claramente la contribución y revisión de cada integrante.

## Nomenclatura de ramas

Las ramas de trabajo se crearán desde `main` y usarán minúsculas, guiones y un prefijo que indique el tipo de cambio:

| Prefijo | Uso | Ejemplo |
| --- | --- | --- |
| `feature/` | Nueva funcionalidad | `feature/crear-tareas` |
| `fix/` | Corrección de un defecto | `fix/validar-prioridad` |
| `docs/` | Documentación | `docs/flujo-colaborativo` |
| `chore/` | Configuración o mantenimiento | `chore/configurar-vite` |

Cada rama debe atender un cambio acotado. Cuando sea útil, se puede añadir un identificador de actividad al nombre, por ejemplo `feature/42-filtros-tareas`.

## Creación y eliminación de ramas

1. Antes de iniciar un cambio, actualizar la copia local de `main` desde el repositorio remoto.
2. Crear una rama nueva desde `main` para cada funcionalidad, corrección o tarea documental.
3. Trabajar y hacer push únicamente a la rama propia; no se permiten cambios directos en `main`.
4. Al integrar el PR/MR aprobado, eliminar la rama remota desde la plataforma. Eliminar también la rama local cuando ya no se necesite.
5. Si el PR/MR necesita cambios, continuar trabajando en la misma rama y actualizar la solicitud.

No reutilizar ramas ya integradas para trabajo nuevo: cada cambio nuevo debe partir de la versión actual de `main`.

## Acceso de los integrantes

- Todos los integrantes deben usar su propia cuenta de la plataforma y figurar como colaboradores del repositorio.
- Cada integrante debe tener permiso para crear ramas y abrir PR/MR. El permiso para integrar cambios se reserva a quienes el equipo designe como responsables de mantenimiento del repositorio.
- Las credenciales son personales y no se comparten.
- Las contribuciones deben quedar asociadas a la cuenta individual que las realizó; no se deben subir commits en nombre de otra persona.

## Políticas de commits

- Hacer commits pequeños que representen un cambio coherente y revisable.
- Usar mensajes en el formato `tipo: descripción breve`, con el tipo en minúsculas y la descripción en modo imperativo. Ejemplos: `feat: agregar creación de tareas`, `fix: validar el estado recibido`, `docs: describir el flujo de ramas`.
- Tipos recomendados: `feat`, `fix`, `docs`, `refactor`, `test` y `chore`.
- No incluir en un commit archivos generados, bases SQLite locales, secretos, contraseñas ni archivos `.env` con valores reales.
- Hacer push frecuente a la rama propia para respaldar el trabajo y mantener visible la participación individual.

## Políticas de combinación de ramas

- `main` debe permanecer en un estado integrado y ejecutable según las capacidades existentes del proyecto.
- Todo cambio a `main` debe llegar mediante un PR/MR aprobado; no se permiten pushes directos.
- Antes de integrar, actualizar la rama de trabajo si `main` avanzó y resolver los conflictos en la rama de trabajo.
- Integrar usando la opción **Create a merge commit** para conservar en el historial la rama y los commits revisados.
- La persona autora no debe integrar su propio PR/MR. La integración la realiza un integrante autorizado después de comprobar que se cumplieron las reglas de revisión.

## Políticas de Pull/Merge Requests

Cada PR/MR debe:

- Tener un título claro, idealmente con el mismo prefijo usado para los commits, por ejemplo `feat: crear y asignar tareas`.
- Explicar qué cambia y por qué; incluir instrucciones para revisar el cambio cuando no sea obvio.
- Referenciar la actividad o funcionalidad correspondiente, si el equipo usa un tablero o identificadores.
- Ser acotado a una funcionalidad o conjunto de cambios relacionados.
- Incluir capturas de pantalla cuando cambie la interfaz y estas ayuden a revisar el resultado.
- Indicar cualquier cambio de configuración o datos que se necesite para ejecutar la versión.

## Revisión y aprobación

1. La persona autora abre el PR/MR y solicita revisión a otro integrante.
2. El revisor examina el propósito del cambio, su legibilidad, su compatibilidad con la arquitectura y los efectos visibles en la aplicación.
3. El revisor aprueba o solicita cambios mediante comentarios concretos. La persona autora responde a las observaciones y actualiza su rama.
4. Las conversaciones deben quedar resueltas antes de integrar. La aprobación debe registrarse en la plataforma; no basta con una aprobación verbal o una captura.
5. Se requiere al menos **una aprobación de otro integrante**. La persona autora no puede aprobar su propia solicitud.
6. Tras la aprobación, una persona responsable distinta de la autora integra el PR/MR y elimina la rama de trabajo.

Si la plataforma permite proteger ramas, configurar `main` para exigir PR/MR y al menos una aprobación, y desactivar la integración de cambios no revisados.

## Evidencia de participación

Cada integrante debe contribuir desde su cuenta mediante una o más ramas, commits y PR/MR, y participar en la revisión del trabajo de otra persona. La tabla del reporte debe corresponder con el historial real de la plataforma (commits, solicitudes, revisiones e integraciones).

## Decisiones pendientes del equipo


- Herramientas de verificación automática que se incorporarán al proyecto.
