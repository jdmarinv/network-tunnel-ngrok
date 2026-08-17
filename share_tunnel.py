#!/usr/bin/env python3
import sys
import os
import argparse
from pathlib import Path
from pyngrok import ngrok, conf

CONFIG_FILE = Path(__file__).parent / ".ngrok_token"

def get_saved_token():
    if CONFIG_FILE.exists():
        return CONFIG_FILE.read_text().strip()
    return os.environ.get("NGROK_AUTHTOKEN", "")

def save_token(token):
    CONFIG_FILE.write_text(token.strip())

def main():
    parser = argparse.ArgumentParser(
        description="Comparte un puerto local usando ngrok para conectarte con otra persona."
    )
    parser.add_argument("-p", "--port", type=int, help="Puerto local del software (ej. 8080, 25565, 3000)")
    parser.add_argument("-t", "--type", choices=["http", "tcp"], help="Tipo de tráfico ('http' para web/apps, 'tcp' para juegos/sockets directos)")
    parser.add_argument("--token", type=str, help="Tu Authtoken de ngrok (solo necesario la primera vez)")

    args = parser.parse_args()

    # 1. Obtener o solicitar Authtoken
    token = args.token or get_saved_token()
    if not token:
        print("\n🔑 No se encontró un authtoken de ngrok guardado.")
        print("Obtén tu token gratis en: https://dashboard.ngrok.com/get-started/your-authtoken")
        token = input("Pega tu Authtoken de ngrok aquí: ").strip()
        if not token:
            print("❌ El token no puede estar vacío.")
            sys.exit(1)
        save_token(token)
        print("💾 Token guardado para futuras sesiones.\n")

    conf.get_default().auth_token = token

    # 2. Obtener puerto
    port = args.port
    if not port:
        while True:
            port_input = input("👉 Introduce el puerto del software local (ej. 8080): ").strip()
            if port_input.isdigit():
                port = int(port_input)
                break
            print("❌ Por favor ingresa un número de puerto válido.")

    # 3. Obtener tipo de tráfico
    proto = args.type
    if not proto:
        print("\n¿Qué tipo de software van a usar?")
        print("  1) HTTP/Web (Páginas web, APIs, paneles, dashboards)")
        print("  2) TCP (Juegos, servidores de sockets directos, bases de datos)")
        choice = input("Selecciona una opción (1 o 2) [1]: ").strip()
        proto = "tcp" if choice == "2" else "http"

    print(f"\n🚀 Iniciando túnel ngrok para el puerto {port} ({proto.upper()})...")

    try:
        tunnel = ngrok.connect(port, proto)
        print("\n" + "=" * 60)
        print("🎉 ¡TÚNEL CONECTADO EXITOSAMENTE!")
        print("=" * 60)
        print(f"\n🔗 Dirección pública para compartir:")
        print(f"   >>>  {tunnel.public_url}  <<<")
        print("\nℹ️  Instrucciones para tu novio:")
        if proto == "http":
            print(f"   • Debe abrir en su navegador: {tunnel.public_url}")
        else:
            # Ejemplo: tcp://4.tcp.ngrok.io:12345
            url_clean = tunnel.public_url.replace("tcp://", "")
            host, tcp_port = url_clean.split(":")
            print(f"   • Servidor / Host: {host}")
            print(f"   • Puerto:          {tcp_port}")
            print(f"   • O poner la dirección completa: {tunnel.public_url}")
        
        print("\n" + "=" * 60)
        print("⏳ El túnel se mantendrá abierto mientras este script esté corriendo.")
        print("👉 Presiona Ctrl + C para cerrarlo cuando terminen.")
        print("=" * 60 + "\n")

        ngrok_process = ngrok.get_ngrok_process()
        ngrok_process.proc.wait()

    except KeyboardInterrupt:
        print("\n\n🛑 Cerrando túnel...")
        ngrok.kill()
        print("👋 Conexión cerrada. ¡Hasta la próxima!")
    except Exception as e:
        print(f"\n❌ Ocurrió un error al abrir el túnel: {e}")
        print("💡 Verifica que tu Authtoken sea válido y que el puerto esté libre.")

if __name__ == "__main__":
    main()
