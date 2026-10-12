# API de integrantes

El Member Service administra los integrantes y sus datos en su propia base SQLite. Los endpoints se exponen directamente en el servicio, que por defecto escucha en el puerto `8002`.

## Registrar un integrante

`POST /members`

Solicitud:

```json
{
  "name": "Ada Lovelace"
}
```

Respuesta `201 Created`:

```json
{
  "id": 1,
  "name": "Ada Lovelace"
}
```

El nombre se recorta en los extremos y debe contener entre 1 y 120 caracteres después del recorte. Una solicitud inválida recibe `422 Unprocessable Entity`.

## Consultar integrantes

`GET /members`

Respuesta `200 OK`: arreglo de integrantes ordenado por identificador ascendente. Si todavía no hay integrantes, devuelve un arreglo vacío.

## Consultar un integrante

`GET /members/{member_id}`

Respuesta `200 OK`: objeto del integrante solicitado. Si el identificador no existe, devuelve `404 Not Found` con el detalle `Integrante no encontrado`.
