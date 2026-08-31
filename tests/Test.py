# ==========================================
# SISTEMA DE REGISTRO DE USUARIOS
# Cantidad Máxima de usuarios: 10 usuarios
# ==========================================

# Lista donde se guardarán los usuarios
usuarios = []


# Mantiene el programa funcionando hasta elegir salir
while True:

    print("\n==============================")
    print("     SISTEMA DE USUARIOS")
    print("==============================")
    print("1. Registrar usuario")
    print("2. Consultar usuario")
    print("3. Mostrar todos los usuarios")
    print("4. Salir")

    opcion = input("\nSelecciona una opción: ")


    # ==========================================
    # 1. REGISTRAR USUARIO
    # ==========================================
    if opcion == "1":

        # Verificar que no existan ya 2 usuarios
        if len(usuarios) >= 10:
            print("\nYa se han registrado los 10 usuarios permitidos.")
            continue

        print("\n--- REGISTRO DE USUARIO ---")

        # Pedir información del usuario
        nombre = input("Nombre: ")
        edad = int(input("Edad: "))
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")
        empresa = input("Empresa donde trabaja: ")
        puesto = input("Puesto de trabajo: ")
        salario = float(input("Salario: "))

        # Crear un diccionario con los datos del usuario
        usuario = {
            "nombre": nombre,
            "edad": edad,
            "direccion": direccion,
            "telefono": telefono,
            "empresa": empresa,
            "puesto": puesto,
            "salario": salario
        }

        # Agregar el usuario a la lista
        usuarios.append(usuario)

        print("\nUsuario registrado correctamente.")


    # ==========================================
    # 2. CONSULTAR ALGUN USUARIO
    # ==========================================
    elif opcion == "2":

        # Comprobar si existen usuarios
        if len(usuarios) == 0:
            print("\nNo hay usuarios registrados.")
            continue

        # Pedir el nombre que queremos buscar
        nombre_buscar = input("\nEscribe el nombre del usuario: ")

        encontrado = False

        # Recorrer todos los usuarios registrados
        for usuario in usuarios:

            # Comparar el nombre introducido con los registrados
            if usuario["nombre"].lower() == nombre_buscar.lower():

                print("\n==============================")
                print("     INFORMACIÓN DEL USUARIO")
                print("==============================")

                # Mostrar información del usuario
                print(f"Nombre: {usuario['nombre']}")
                print(f"Edad: {usuario['edad']}")
                print(f"Dirección: {usuario['direccion']}")
                print(f"Teléfono: {usuario['telefono']}")
                print(f"Empresa: {usuario['empresa']}")
                print(f"Puesto: {usuario['puesto']}")
                print(f"Salario: ${usuario['salario']:.2f}")

                encontrado = True
                break

        # Mostrar mensaje si no se encontró el usuario
        if not encontrado:
            print("\nNo se encontró ese usuario.")


    # ==========================================
    # 3. MOSTRAR TODOS LOS USUARIOS
    # ==========================================
    elif opcion == "3":

        # Comprobar si existen usuarios
        if len(usuarios) == 0:
            print("\nNo hay usuarios registrados.")
            continue

        print("\n==============================")
        print("     USUARIOS REGISTRADOS")
        print("==============================")

        # Recorrer y mostrar todos los usuarios
        for numero, usuario in enumerate(usuarios, start=1):

            print(f"\n--- Usuario {numero} ---")
            print(f"Nombre: {usuario['nombre']}")
            print(f"Edad: {usuario['edad']}")
            print(f"Dirección: {usuario['direccion']}")
            print(f"Teléfono: {usuario['telefono']}")
            print(f"Empresa: {usuario['empresa']}")
            print(f"Puesto: {usuario['puesto']}")
            print(f"Salario: ${usuario['salario']:.2f}")


    # ==========================================
    # 4. SALIR
    # ==========================================
    elif opcion == "4":

        print("\nPrograma finalizado.")
        break


    # ==========================================
    # OPCIÓN NO VÁLIDA
    # ==========================================
    else:

        print("\nOpción no válida.")
