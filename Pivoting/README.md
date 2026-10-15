# Pivoting, tunneling y port forwarding

Apuntes y referencias prácticas.

## Cómo funciona un pivot

El objetivo es alcanzar una red interna **desde un equipo al que ya se tiene acceso autorizado**. Antes de usar un túnel hay que conocer las interfaces, rutas, DNS y puertos accesibles desde ese equipo.

```mermaid
flowchart LR
    A["Equipo del operador"] --> B["Host de salto o foothold"]
    B --> C["Red interna"]
    A -. "Túnel SOCKS o túnel TUN" .-> B
```

| Técnica | Cuándo resulta útil | Nota relacionada |
|---|---|---|
| SOCKS / proxychains | Pasar aplicaciones compatibles con proxy a través del host intermedio | [Chisel](chisel.md) |
| Interfaz TUN y rutas | Conectar herramientas a subredes internas mediante routing | [Ligolo](ligolo.md) |
| Reenvío de puertos | Exponer un servicio concreto de forma controlada | [Port forwarding en Linux](../Privilege-Escalation/linux/port-forwarding.md) |

### Comprobaciones antes y después

```bash
ip -br addr                 # Interfaces disponibles
ip route                    # Rutas y redes alcanzables
ss -lntp                    # Puertos locales en escucha
getent hosts internal.lab   # Resolución DNS (si está configurada)
```

> Un túnel activo no garantiza que exista conectividad a todos los servicios. Revisar el enrutamiento, el firewall y la resolución DNS. Usar únicamente en redes de laboratorio o con autorización.

- [Chisel](chisel.md)
- [Copy1](copy1.md)
- [Ligolo](ligolo.md)

[Inicio](../README.md)
