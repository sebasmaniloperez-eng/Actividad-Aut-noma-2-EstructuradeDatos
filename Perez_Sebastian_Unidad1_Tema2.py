# AA2: Gestión logística. Ejecutar en Python 3.
# Basado en el notebook de clase; archivo TXT original sin modificar.

# 1. Leer el archivo TXT con la misma codificación de la captura.
archivo_origen = r"C:\Users\TALLER\Downloads\Data_Set_AA2.txt"
data_set = []  # Aquí se guardarán los registros de texto.

try:
    with open(archivo_origen, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()  # Leer todo: un registro ocupa varias líneas.

    # Unir las líneas sin cambiar el archivo original.
    contenido = contenido.replace("\n", " ").replace("\r", " ")

    # En este TXT, cada registro está encerrado entre comillas dobles.
    for parte in contenido.split('"'):
        linea = parte.strip().strip(",").strip()
        if linea.lower().startswith("id"):
            data_set.append(linea)

    print(f"Archivo leído con UTF-8. Registros encontrados: {len(data_set)}")

except FileNotFoundError:
    print("Archivo no encontrado. Revisa la ruta de archivo_origen.")


# 2. Limpiar los textos y crear una lista de diccionarios.
lista_paquetes = []  # Cada elemento tendrá las cinco llaves solicitadas.
lista_precios = []  # Guardar los precios originales, en el mismo orden.

for linea in data_set:
    # Quitar espacios exteriores y símbolos que aparecen al final.
    texto = linea.strip().rstrip("#?!").strip()

    # Unificar los separadores que hay entre los campos.
    texto = texto.replace(" - ", ";").replace(",", ";")

    # El guion junto a una etiqueta separa la llave de su valor.
    for etiqueta in ["id", "producto", "origen", "precio", "tasa"]:
        texto = texto.replace(etiqueta + "-", etiqueta + ":")
        texto = texto.replace(etiqueta.upper() + "-", etiqueta.upper() + ":")

    # Reparar las tasas sin separador de TRK902 y TRK906 en el TXT.
    texto = texto.replace("tasa0", "tasa:0").replace("TASA0", "TASA:0")
    cortes = texto.split(";")  # Separar los cinco campos del registro.
    datos = {}  # Diccionario temporal con los campos de entrada.

    for campo in cortes:
        clave, valor = campo.split(":", 1)  # Separar solo en el primer ':'.
        datos[clave.strip().lower()] = valor.strip()

    precio = float(datos["precio"])  # Convertir el precio a número.
    tasa = float(datos.get("tasa", 0))  # Usar 0 si falta la llave tasa.
    impuesto = precio * tasa  # Calcular sin redondear los valores intermedios.

    registro = {
        "id_rastreo": datos["id"],
        "item": datos["producto"].replace("_", " ").strip().title(),
        "pais_origen": datos["origen"].upper(),
        "impuesto_valor": impuesto,
        "total_pagar": precio + impuesto
    }

    lista_paquetes.append(registro)  # Agregar el diccionario a la lista.
    lista_precios.append(precio)  # Conservar el precio sin una sexta llave.

print(f"Registros procesados: {len(lista_paquetes)}")


# 3. Mostrar los campos de un registro para comprobar su estructura.
if lista_paquetes:
    print("EJEMPLO DE REGISTRO LIMPIO")
    for llave, valor in lista_paquetes[0].items():
        print(f"{llave}: {valor}")


# 4. Mostrar el resumen solicitado, como en la tabla del notebook de clase.
if lista_paquetes:
    print("RESUMEN DE PAQUETES (USD)")
    print(f"{'ID':<8}|{'PRODUCTO':<24}|{'TOTAL A PAGAR':>14}")
    print("-" * 48)
    for paquete in lista_paquetes:
        print(f"{paquete['id_rastreo']:<8}|{paquete['item']:<24}|"
              f"{paquete['total_pagar']:>14.3f}")


# 5. Buscar el mayor impuesto y calcular el promedio antes de impuestos.
if lista_paquetes:
    mayor_impuesto = lista_paquetes[0]  # Empezar por el primer paquete.
    for paquete in lista_paquetes:
        if paquete["impuesto_valor"] > mayor_impuesto["impuesto_valor"]:
            mayor_impuesto = paquete

    promedio = sum(lista_precios) / len(lista_precios)
    print(f"Mayor impuesto: {mayor_impuesto['item']}")
    print(f"ID: {mayor_impuesto['id_rastreo']}")
    print(f"Impuesto: ${mayor_impuesto['impuesto_valor']:.3f}")
    print(f"Promedio antes de impuestos: ${promedio:.2f}")
else:
    print("No hay registros para analizar. Revisa la carga del archivo.")


# 6. Función adicional: clasificar usando el precio original.
def filtro_prioridad(precio, limite=500):
    # El límite se puede cambiar al llamar a la función.
    if precio > limite:  # Exactamente $500 no supera el límite.
        return "Prioritario"
    else:
        return "Normal"


# 7. Aplicar el filtro y mostrar un pequeño resumen para el reparto.
if lista_paquetes:
    cantidad_prioritarios = 0
    total_prioritarios = 0
    print("FILTRO DE PRIORIDAD: PRECIO ORIGINAL > $500")
    print(f"{'ID':<8}|{'PRODUCTO':<24}|{'PRECIO':>9}|{'ESTADO':<12}")
    print("-" * 56)

    for i in range(len(lista_paquetes)):
        paquete = lista_paquetes[i]
        precio = lista_precios[i]  # Mismo índice: mismo paquete.
        estado = filtro_prioridad(precio)
        print(f"{paquete['id_rastreo']:<8}|{paquete['item']:<24}|"
              f"{precio:>9.2f}|{estado:<12}")
        if estado == "Prioritario":
            cantidad_prioritarios += 1
            total_prioritarios += paquete["total_pagar"]

    print(f"Paquetes prioritarios: {cantidad_prioritarios} de {len(lista_paquetes)}")
    print(f"Total a pagar de los prioritarios: ${total_prioritarios:.3f}")
