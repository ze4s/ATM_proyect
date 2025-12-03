MINIMO = 1.0  # monto mínimo aceptado para operaciones

def crear_cuenta(nombre, saldo_inicial=0.0):
    return {
        'nombre': nombre,
        'balance': float(saldo_inicial),
        'total_depositos': 0,
        'total_retiros': 0,
        'total_transferencias': 0,
    }

# Funciones obligatorias
def ver_balance(cuenta):
    print(f"Saldo de '{cuenta['nombre']}': ${cuenta['balance']:.2f}")

def validar_monto_raw(monto_raw):
    try:
        monto = float(monto_raw)
    except (ValueError, TypeError):
        print("Error: monto inválido (no es un número).")
        return None
    if monto <= 0:
        print("Error: el monto debe ser mayor que 0.")
        return None
    if monto < MINIMO:
        print(f"Error: el monto debe ser al menos ${MINIMO:.2f}.")
        return None
    return monto

def depositar(cuenta, monto_raw):
    monto = validar_monto_raw(monto_raw)
    if monto is None:
        return
    cuenta['balance'] += monto
    cuenta['total_depositos'] += 1
    print(f"Depósito realizado: ${monto:.2f}. Nuevo saldo: ${cuenta['balance']:.2f}")

def retirar(cuenta, monto_raw):
    monto = validar_monto_raw(monto_raw)
    if monto is None:
        return
    if monto > cuenta['balance']:
        print("Error: fondos insuficientes para retirar esa cantidad.")
        return
    cuenta['balance'] -= monto
    cuenta['total_retiros'] += 1
    print(f"Retiro realizado: ${monto:.2f}. Nuevo saldo: ${cuenta['balance']:.2f}")

def transferir(cuenta_origen, cuentas, origen_id, destino_id, monto_raw):
    if destino_id not in cuentas:
        print("Cuenta destino no encontrada. Transferencia cancelada.")
        return
    if origen_id == destino_id:
        print("Error: no puedes transferir a la misma cuenta.")
        return
    monto = validar_monto_raw(monto_raw)
    if monto is None:
        return
    if monto > cuenta_origen['balance']:
        print("Error: fondos insuficientes para transferir esa cantidad.")
        return
    cuenta_destino = cuentas[destino_id]
    cuenta_origen['balance'] -= monto
    cuenta_destino['balance'] += monto
    cuenta_origen['total_transferencias'] += 1
    print(f"Transferencia de ${monto:.2f} a '{cuenta_destino['nombre']}' realizada.")
    print(f"Tu nuevo saldo: ${cuenta_origen['balance']:.2f}")

def mostrar_reporte(cuenta):
    total = cuenta['total_depositos'] + cuenta['total_retiros'] + cuenta['total_transferencias']
    print("----- Reporte de transacciones -----")
    print(f"Depósitos realizados: {cuenta['total_depositos']}")
    print(f"Retiros realizados: {cuenta['total_retiros']}")
    print(f"Transferencias realizadas: {cuenta['total_transferencias']}")
    print(f"Total de transacciones: {total}")
    print("------------------------------------")

def menu():
    print("\n--- Cajero Automático (simulador) ---")
    print("1) Ver balance")
    print("2) Depositar")
    print("3) Retirar")
    print("4) Transferir (simulada)")
    print("5) Ver reporte de transacciones")
    print("6) Salir")

def main():
    # Creamos cuentas en memoria. '001' es la cuenta principal del usuario.
    cuentas = {
        '001': crear_cuenta("Mi Cuenta", saldo_inicial=1000.0),
        # cuentas destino adicionales para transferir
        '002': crear_cuenta("Gadiel", saldo_inicial=300.0),
        '003': crear_cuenta("caonabo", saldo_inicial=250.0),
        '004': crear_cuenta("Orlando", saldo_inicial=750.0),
    }

    mi_id = '001'
    mi_cuenta = cuentas[mi_id]

    print("Bienvenido al simulador de cajero.\n(No uses datos reales. Esto es solo una práctica simple.)")
    while True:
        menu()
        opcion = input("Elige una opción (1-6): ").strip()
        if opcion == '1':
            ver_balance(mi_cuenta)
        elif opcion == '2':
            monto = input("Ingrese monto a depositar: ").strip()
            depositar(mi_cuenta, monto)
        elif opcion == '3':
            monto = input("Ingrese monto a retirar: ").strip()
            retirar(mi_cuenta, monto)
        elif opcion == '4':
            print("Cuentas disponibles para transferir:")
            for cid, c in cuentas.items():
                if cid != mi_id:
                    print(f"- ID: {cid}  Nombre: {c['nombre']}  Saldo: ${c['balance']:.2f}")
            destino = input("Ingresa ID de cuenta destino: ").strip()
            monto = input("Ingrese monto a transferir: ").strip()
            transferir(mi_cuenta, cuentas, mi_id, destino, monto)
        elif opcion == '5':
            mostrar_reporte(mi_cuenta)
        elif opcion == '6':
            print("Saliendo. Gracias por usar el simulador.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()