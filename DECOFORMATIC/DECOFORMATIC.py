import time
import json
import os
from datetime import datetime

CONFIG_FILE = "config.json"

def cargar_sistema():
    """Carga los tokens y comprueba si toca la recarga mensual de 1500."""
    mes_actual = datetime.now().strftime("%Y-%m")
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            datos = json.load(f)
            
        if datos.get("ultimo_mes_recarga") != mes_actual:
            datos["decotokens"] += 1500
            datos["ultimo_mes_recarga"] = mes_actual
            guardar_sistema(datos)
            print("\n🎁 ¡SISTEMA: Se han ingresado tus 1500 DECOTOKENS mensuales gratuitos!")
            time.sleep(2)
        return datos
    else:
        # Estado inicial: 1500 tokens del primer mes y 20 usos iniciales
        nuevo_sistema = {
            "decotokens": 1500,
            "usos_codificar": 20,
            "usos_descodificar": 20,
            "ultimo_mes_recarga": mes_actual
        }
        guardar_sistema(nuevo_sistema)
        return nuevo_sistema

def guardar_sistema(datos):
    """Guarda el estado actual en el archivo local."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(datos, f, indent=4)

def auto_canjear_token(datos, tipo):
    """Comprueba si faltan créditos y canjea un token de forma automática."""
    if tipo == "codificar" and datos["usos_codificar"] <= 0:
        if datos["decotokens"] >= 1:
            datos["decotokens"] -= 1
            datos["usos_codificar"] += 20
            guardar_sistema(datos)
            print("\n🪙 ¡AUTO-REFRESH: 1 DECOTOKEN canjeado automáticamente (+20 COD)! ")
            time.sleep(1.5)
            return True
        return False
        
    elif tipo == "descodificar" and datos["usos_descodificar"] <= 0:
        if datos["decotokens"] >= 1:
            datos["decotokens"] -= 1
            datos["usos_descodificar"] += 20
            guardar_sistema(datos)
            print("\n🪙 ¡AUTO-REFRESH: 1 DECOTOKEN canjeado automáticamente (+20 DECOD)!")
            time.sleep(1.5)
            return True
        return False
    return True

def limpiar_pantalla():
    print("\033[H\033[2J", end="")

def texto_a_binario(texto):
    return ' '.join(format(ord(c), '08b') for c in texto)

def binario_a_texto(binario):
    try:
        bloques = binario.split()
        return ''.join(chr(int(b, 2)) for b in bloques)
    except ValueError:
        return None

def mostrar_interfaz(datos):
    print("=====================================================================")
    print("  ██████╗ ███████╗ ██████╗ ██████╗ ███████╗ ██████╗ ███╗   ███╗")
    print("  ██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔════╝██╔═══██╗████╗ ████║")
    print("  ██║  ██║█████╗  ██║     ██║   ██║█████╗  ██║   ██║██╔████╔██║")
    print("  ██║  ██║██╔══╝  ██║     ██║   ██║██╔══╝  ██║   ██║██║╚██╔╝██║")
    print("  ██████╔╝███████╗╚██████╗╚██████╔╝██║     ╚██████╔╝██║ ╚═╝ ██║")
    print("  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚═╝     ╚═╝")
    print("=====================================================================")
    info_tokens = f"🪙 WALLET: {datos['decotokens']} DECOTOKENS"
    info_creditos = f"⚡ BUFFER: [{datos['usos_codificar']} COD] | [{datos['usos_descodificar']} DECOD]"
    print(f"{info_tokens:>69}")
    print(f"{info_creditos:>69}")
    print("=====================================================================")

def app_principal():
    datos = cargar_sistema()

    while True:
        limpiar_pantalla()
        mostrar_interfaz(datos)
        print("\n[1] 🧠 CODIFICAR (Texto Plano ➔ Flujo Binario)")
        print("[2] 📟 DESCODIRICAR (Flujo Binario ➔ Texto Plano)")
        print("[3] 🔑 INTRODUCIR CÓDIGO DE RECARGA SECRETO")
        print("[4] 🔌 APAGAR SISTEMA")
        
        opcion = input("\n🖥️  Introduce comando (1-4): ").strip()
        
        if opcion == '1':
            limpiar_pantalla()
            mostrar_interfaz(datos)
            print("\n--- [ MODO CODIFICADOR ] ---")
            
            # Intenta el auto-canjeo si está a cero
            if not auto_canjear_token(datos, "codificar"):
                print("\n❌ ERROR: Sin créditos de codificación y sin DECOTOKENS en la Wallet.")
                time.sleep(2.5)
                continue
                
            texto = input("\n✍️  Suelta el texto a procesar:\n> ")
            if texto:
                datos['usos_codificar'] -= 1
                guardar_sistema(datos)
                
                resultado = texto_a_binario(texto)
                print("\n" + "=" * 69)
                print(resultado)
                print("-" * 69)
                print(f"📉 Créditos de codificación restantes: {datos['usos_codificar']}/20")
            else:
                print("\n⚠️ Entrada vacía. Cancelando...")
                
            input("\n⌨️  Pulsa ENTER para volver...")
            
        elif opcion == '2':
            limpiar_pantalla()
            mostrar_interfaz(datos)
            print("\n--- [ MODO DESCOFICADOR ] ---")
            
            # Intenta el auto-canjeo si está a cero
            if not auto_canjear_token(datos, "descodificar"):
                print("\n❌ ERROR: Sin créditos de descodificación y sin DECOTOKENS en la Wallet.")
                time.sleep(2.5)
                continue
                
            binario = input("\n📟 Pega el flujo binario:\n> ").strip()
            if binario:
                resultado = binario_a_texto(binario)
                print("\n" + "=" * 69)
                if resultado is not None:
                    datos['usos_descodificar'] -= 1
                    guardar_sistema(datos)
                    
                    print(resultado)
                    print("-" * 69)
                    print(f"📉 Créditos de descodificación restantes: {datos['usos_descodificar']}/20")
                else:
                    print("❌ ERROR: Flujo binario corrupto o inválido.")
                print("-" * 69)
            else:
                print("\n⚠️ Entrada vacía.")
                
            input("\n⌨️  Pulsa ENTER para volver...")
            
        elif opcion == '3':
            limpiar_pantalla()
            mostrar_interfaz(datos)
            print("\n--- [ TERMINAL DE RECARGA SECRETA ] ---")
            codigo = input("\n🔑 Introduce el código secreto:\n> ").strip()
            
            if codigo == "VIVAALVAROCODING813(!·":
                datos['decotokens'] += 1000000
                guardar_sistema(datos)
                print("\n🔥 ¡HACKEO LOGRADO! 1.000.000 DECOTOKENS INYECTADOS. REFRESCANDO WALLET...")
            else:
                print("\n❌ ACCESO DENEGADO. Código de inyección incorrecto.")
                
            time.sleep(2.5)
            
        elif opcion == '4':
            limpiar_pantalla()
            print("\n⚙️ Guardando estado de la Wallet... ¡Cerrando DECOFORMATIC!")
            time.sleep(1)
            break
        else:
            print("\n⚠️ Comando no reconocido.")
            time.sleep(1)

if __name__ == "__main__":
    app_principal()
