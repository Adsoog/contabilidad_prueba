def transformar_registros(registros):
    registros_transformados = []
    for registro in registros:
        # Desempaquetar cada registro, ignorando el último valor
        ruc_dni, nombre_proveedor, nombre_banco, nro_cuenta, moneda = registro[:-1]
        
        # Procesar nombre del banco y número de cuenta
        nombre_banco = nombre_banco if nombre_banco else ''
        nro_cuenta = nro_cuenta if nro_cuenta else ''
        
        # Convertir el valor de la moneda
        moneda = 'PEN' if moneda == 0 else 'USD' if moneda == 1 else ''
        
        # Agregar el registro transformado a la lista de resultados
        registros_transformados.append((ruc_dni, nombre_proveedor, nombre_banco, nro_cuenta, moneda))
    
    return registros_transformados

# Asegúrate de reemplazar el contenido de esta lista con tus propios datos
registros = [
    ('20605569936', 'HIGH SERVICE SPARES SAC', 'BBVA', '0011-0976-0100006771', 0, None),
    # Agrega aquí más registros según sea necesario
]

# Usar la función para transformar los registros
registros_transformados = transformar_registros(registros)

# Mostrar los registros transformados
for registro in registros_transformados:
    print(registro)
