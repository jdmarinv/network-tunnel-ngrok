# Network Tunnel con ngrok

Script interactivo en Python para compartir cualquier software o puerto local a través de internet usando ngrok.

## Ubicación
El proyecto está creado en: `~/Dev/network-tunnel-ngrok`

## Instalación rápida de dependencias

```bash
cd ~/Dev/network-tunnel-ngrok
pip install -r requirements.txt
```

## Uso

### Modo interactivo (asistido)
Simplemente ejecuta:
```bash
python share_tunnel.py
```
El script te preguntará:
1. Tu **Authtoken de ngrok** (solo la primera vez, luego lo recordará).
2. El **puerto local** de tu software (ej. `8080`, `3000`, `25565`).
3. El **tipo de tráfico**: HTTP (web/APIs) o TCP (juegos/sockets).

### Modo con argumentos (directo)
- Para compartir un servidor web en el puerto 8080:
  ```bash
  python share_tunnel.py -p 8080 -t http
  ```
- Para compartir un juego o socket TCP en el puerto 25565:
  ```bash
  python share_tunnel.py -p 25565 -t tcp
  ```
