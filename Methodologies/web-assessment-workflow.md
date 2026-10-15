# Metodología práctica de evaluación web y APIs

Guía de trabajo para **laboratorios y auditorías autorizadas**. Complementa las notas de [enumeración](../Enumeration/README.md), [herramientas](../Tools/README.md) y [seguridad web](../Web-Security/README.md).

![Proceso de investigación](../assets/diagrams/web-assessment-flow.svg)

## 0. Preparación y alcance

| Campo | Qué anotar |
|---|---|
| Objetivo | URL, hostnames y endpoints permitidos |
| Alcance | Dominio, cuentas de prueba y funciones evaluables |
| Restricciones | Tasas de petición, horario y operaciones prohibidas |
| Cuentas | Usuario A, usuario B, lector y administrador **solo si se suministran** |
| Evidencia | UTC, petición, respuesta, identificador, contexto, impacto |
| Criterio de parada | Riesgo de pérdida de datos, disponibilidad o exposición de terceros |

No subir a GitHub credenciales, tokens, cookies, datos reales de usuarios ni flags secretos.

## 1. Baseline del flujo normal

1. Abrir la aplicación con Burp Proxy, registrar el flujo normal.
2. Entender front-end, proxy, API y backend.
3. Identificar cookies, `Authorization`, `Content-Type` y controles CSRF.
4. Guardar primero una **petición autorizada** que permita comparar.

```bash
curl -i -sS 'https://app.lab.example.test/api/me'
curl -sS -o /dev/null \
  -w 'status=%{http_code} total=%{time_total}s ip=%{remote_ip}\n' \
  'https://app.lab.example.test/health'
```

Un `200` o `403` aislado **no confirma ni descarta** una vulnerabilidad.

## 2. Reconocimiento con contexto

| Qué | Herramienta o nota | Validación |
|---|---|---|
| DNS y dominios | [DNS](../Enumeration/Reconnaissance/dns.md) y [subdominios](../Enumeration/Reconnaissance/subdomains.md) | Resolver y comprobar propiedad |
| Puertos/servicios | [Nmap](../Tools/nmap-options.md) | Diferenciar banner de versión confirmada |
| Recursos web | [ffuf](../Tools/ffuf.md) | Baseline de errores y respuestas vacías |
| HTTP/TLS | [cURL](../Tools/curl.md) / [OpenSSL](../Tools/openssl-tls.md) | Cabeceras, redirecciones, certificado |
| API | [GraphQL](../Tools/graphql-introspection.md), OpenAPI y Burp | Endpoints accesibles por rol |

## 3. Matriz de autorización

Crear dos objetos de prueba, uno propio de A y otro propio de B:

| Prueba | A sobre su objeto | A sobre objeto B | Anónimo |
|---|---|---|---|
| Leer (GET) | Según diseño | **Denegar** salvo recurso compartido | Según diseño |
| Modificar (PATCH) | Según permisos | **Denegar** | Denegar |
| Eliminar (DELETE) | Según permisos | **Denegar** | Denegar |
| Función administrativa | Denegar a A | Denegar a A | Denegar |

- **BOLA/IDOR**: falta autorización sobre el objeto.
- **BFLA**: falta autorización sobre una función/endpoint.
- **BOPLA**: se leen o alteran propiedades fuera de permiso.

[Playbook completo para APIs](../Web-Security/API/api-testing-playbook.md).

## 4. Método de hipótesis y pruebas

Para cada hallazgo registrar: **comportamiento esperado → petición de control → único cambio → respuesta real → impacto → retest**.

Evitar confundir un error de aplicación o una diferencia estética con un problema explotable. Correlacionar método, ruta, rol, objeto y respuesta.

## 5. Plantilla de hallazgo

```markdown
# [Título] — [Endpoint]

**Severidad propuesta:** ...
**Alcance y prerrequisitos:** ...
**Comportamiento esperado:** ...
**Comportamiento observado:** ...
**Evidencia (UTC):** ...
**Pasos de reproducción:**
1. ...
2. ...
3. ...

**Impacto validado:** ...
**Limitaciones:** ...
**Recomendación:** ...
**Retest:** ...
```

## 6. Cierre

Revertir cambios de laboratorio, redactar secretos, preservar petición/respuesta mínimas y separar **observación**, **inferencia** y **no comprobado**.

## Referencias

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)

[Metodologías](./README.md) · [Inicio](../README.md)
