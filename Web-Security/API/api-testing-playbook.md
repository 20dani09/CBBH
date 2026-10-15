# Playbook práctico de seguridad de APIs

Comprobaciones ordenadas de **autenticación, autorización, integridad de objetos, paginación, errores y exposición de datos**. Ejemplos con servidor y cuentas ficticias de laboratorio.

![Matriz de autorización API](../../assets/diagrams/api-authorization.svg)

## 1. Antes de probar

| Dimensión | Pregunta principal |
|---|---|
| Autenticación | ¿Cookie de sesión, bearer token, API key, mTLS? |
| Autorización | ¿Servidor valida rol **y** pertenencia del objeto? |
| Propiedades | ¿Se muestran o aceptan campos no autorizados? |
| Recursos | ¿Se aplican límites por identidad y coste? |
| Errores | ¿Se exponen trazas, rutas internas o secretos? |
| Inventario | ¿Hay APIs antiguas accesibles fuera del front-end? |

## 2. Prueba BOLA con dos cuentas de laboratorio

Supongamos que A creó `invoice/101` y B creó `invoice/202`:

```text
A -> GET /api/invoices/101       [esperado: 200]
A -> GET /api/invoices/202       [esperado: 403/404, salvo objeto compartido]
B -> GET /api/invoices/202       [esperado: 200]
Anónimo -> GET /api/invoices/101 [esperado: 401/403, según diseño]
```

Los dos tokens se aportan como **variables de entorno** en el laboratorio:

```bash
BASE='https://api.lab.example.test'
curl -sS -i -H "Authorization: Bearer $TOKEN_A" "$BASE/api/invoices/101"
curl -sS -i -H "Authorization: Bearer $TOKEN_A" "$BASE/api/invoices/202"
curl -sS -i -H "Authorization: Bearer $TOKEN_B" "$BASE/api/invoices/202"
```

Si la respuesta devuelve HTTP 200, validar propiedad real, campos revelados y reglas de uso compartido. El código por sí solo no prueba un IDOR.

## 3. Matriz de pruebas

| Categoría | Cambio mínimo | Qué demuestra |
|---|---|---|
| BOLA | ID del objeto de B, token de A | Acceso efectivo a objeto de otra identidad |
| BFLA | Función de administración con usuario estándar | Control de autorización a nivel funcional |
| BOPLA lectura | Consultar campos internos | Información devuelta fuera de permiso |
| BOPLA escritura | Campo restringido en objeto propio de prueba | Cambio efectivo de estado |
| Sesiones | Repetir petición tras logout/expiración | Revocación efectiva |
| JWT | Comprobar expiración, issuer/audience y firma | Validez de la decisión del backend |
| Paginación | Valor de límite extremo, sin sobrecargar servicio | Validación y límites del backend |
| Errores | Entrada inválida no destructiva | Ausencia de trazas/secrets en respuesta |

## 4. Automatizar la comparación de códigos de respuesta

```python
import os
import requests

base = "https://api.lab.example.test"
cases = [
    ("A owns 101", os.environ["TOKEN_A"], 101),
    ("A requests B's 202", os.environ["TOKEN_A"], 202),
    ("B owns 202", os.environ["TOKEN_B"], 202),
]
for label, token, invoice_id in cases:
    r = requests.get(
        f"{base}/api/invoices/{invoice_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    print(label, r.status_code, len(r.content))
```

Este programa **no detecta vulnerabilidades automáticamente**; obliga a investigar los resultados con contexto de roles y propiedad.

## 5. Códigos HTTP y autorización

`401` indica que faltan credenciales válidas; `403` indica denegación; `404` también puede ocultar existencia para un usuario sin permisos. Ver [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html). Nunca inferir autorización a partir del status sin analizar la respuesta y el recurso.

## 6. Otras comprobaciones útiles

- **GraphQL:** autorización en resolvers y fields, no solo en el esquema; [notas](../../Tools/graphql-introspection.md).
- **Multitenancy:** validar `tenant_id` y autorización en el servidor; nunca fiarse del campo controlado por el cliente.
- **Mass assignment:** mantener lista de propiedades editables por rol y validar estado final con un objeto de laboratorio.
- **Caché:** confirmar que una respuesta privada no se sirve bajo la sesión de otro usuario.
- **Versionado:** comprobar controles equivalentes en endpoints legacy activos.

## Referencias

- [OWASP API1 — BOLA](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [OWASP API5 — BFLA](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

[Metodología](../../Methodologies/web-assessment-workflow.md) · [Seguridad web](../README.md)
