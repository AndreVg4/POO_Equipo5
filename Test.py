# Sistema sencillo de registro de usuarios
# Máximo: 2 usuarios

usuarios = []


while True:

    print("\n==============================")
    print("   SISTEMA DE USUARIOS")
    print("==============================")
    print("1. Registrar usuario")
    print("2. Consultar usuario")
    print("3. Mostrar todos los usuarios")
    print("4. Salir")

    opcion = input("\nSelecciona una opción: ")

    # --------------------------------
    # REGISTRAR USUARIO
    # --------------------------------
    if opcion == "1":

        if len(usuarios) >= 2:
            print("\nYa se han registrado los 2 usuarios permitidos.")
            continue

        print("\n--- REGISTRO DE USUARIO ---")

        nombre = input("Nombre: ")
        edad = int(input("Edad: "))
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")
        empresa = input("Empresa donde trabaja: ")
        puesto = input("Puesto de trabajo: ")
        salario = float(input("Salario: "))

        usuario = {
            "nombre": nombre,
            "edad": edad,
            "direccion": direccion,
            "telefono": telefono,
            "empresa": empresa,
            "puesto": puesto,
            "salario": salario
        }

        usuarios.append(usuario)

        print("\nUsuario registrado correctamente.")

    # --------------------------------
    # CONSULTAR USUARIO
    # --------------------------------
    elif opcion == "2":

        if len(usuarios) == 0:
            print("\nNo hay usuarios registrados.")
            continue

        nombre_buscar = input("\nEscribe el nombre del usuario: ")

        encontrado = False

        for usuario in usuarios:

            if usuario["nombre"].lower() == nombre_buscar.lower():

                print("\n==============================")
                print("     INFORMACIÓN DEL USUARIO")
                print("==============================")

                print(f"Nombre: {usuario['nombre']}")
                print(f"Edad: {usuario['edad']}")
                print(f"Dirección: {usuario['direccion']}")
                print(f"Teléfono: {usuario['telefono']}")
                print(f"Empresa: {usuario['empresa']}")
                print(f"Puesto: {usuario['puesto']}")
                print(f"Salario: ${usuario['salario']:.2f}")

                encontrado = True
                break

        if not encontrado:
            print("\nNo se encontró ese usuario.")

    # --------------------------------
    # MOSTRAR TODOS
    # --------------------------------
    elif opcion == "3":

        if len(usuarios) == 0:
            print("\nNo hay usuarios registrados.")
            continue

        print("\n==============================")
        print("     USUARIOS REGISTRADOS")
        print("==============================")

        for numero, usuario in enumerate(usuarios, start=1):

            print(f"\n--- Usuario {numero} ---")
            print(f"Nombre: {usuario['nombre']}")
            print(f"Edad: {usuario['edad']}")
            print(f"Dirección: {usuario['direccion']}")
            print(f"Teléfono: {usuario['telefono']}")
            print(f"Empresa: {usuario['empresa']}")
            print(f"Puesto: {usuario['puesto']}")
            print(f"Salario: ${usuario['salario']:.2f}")

    # --------------------------------
    # SALIR
    # --------------------------------
    elif opcion == "4":

        print("\nPrograma finalizado.")
        break

    else:
        print("\nOpción no válida.")