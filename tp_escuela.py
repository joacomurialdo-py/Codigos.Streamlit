
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Calificaciones",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Sistema de Calificaciones")
st.write("Registro y administración de notas de alumnos")

# Inicializar las listas en session_state
if "alumnos" not in st.session_state:
    st.session_state.alumnos = []

if "notas" not in st.session_state:
    st.session_state.notas = []


# --------------------------------
# REGISTRAR ALUMNOS
# --------------------------------

st.header("Registrar alumno")

nombre = st.text_input("Nombre del alumno")

nota = st.number_input(
    "Nota",
    min_value=1,
    max_value=10,
    step=1
)

if st.button("Registrar alumno"):

    nombre = nombre.strip()

    if nombre == "":
        st.error("El nombre no puede estar vacío.")

    elif nombre.lower() in [
        alumno.lower() for alumno in st.session_state.alumnos
    ]:
        st.error("Ese alumno ya está registrado.")

    else:
        st.session_state.alumnos.append(nombre)
        st.session_state.notas.append(int(nota))

        st.success("Alumno registrado correctamente.")


st.divider()


# --------------------------------
# MOSTRAR TABLA DE ALUMNOS
# --------------------------------

st.header("Listado de alumnos")

if len(st.session_state.alumnos) > 0:

    st.table({
        "Alumno": st.session_state.alumnos,
        "Nota": st.session_state.notas
    })

else:
    st.info("Todavía no hay alumnos registrados.")


st.divider()


# --------------------------------
# ESTADÍSTICAS
# --------------------------------

st.header("Estadísticas del curso")

if len(st.session_state.notas) > 0:

    promedio = sum(st.session_state.notas) / len(st.session_state.notas)

    nota_maxima = max(st.session_state.notas)
    nota_minima = min(st.session_state.notas)

    aprobados = 0
    desaprobados = 0

    for nota_alumno in st.session_state.notas:

        if nota_alumno >= 6:
            aprobados += 1
        else:
            desaprobados += 1

    col1, col2 = st.columns(2)

    col1.metric("Promedio general", f"{promedio:.2f}")
    col2.metric("Nota más alta", nota_maxima)

    col3, col4 = st.columns(2)

    col3.metric("Nota más baja", nota_minima)
    col4.metric("Cantidad de alumnos", len(st.session_state.alumnos))

    st.write("Aprobados:", aprobados)
    st.write("Desaprobados:", desaprobados)

    porcentaje = (aprobados / len(st.session_state.notas)) * 100

    st.write(f"Porcentaje de aprobados: {porcentaje:.2f}%")

else:
    st.warning("No hay notas para calcular estadísticas.")


st.divider()


# --------------------------------
# BUSCAR ALUMNO
# --------------------------------

st.header("Buscar alumno")

nombre_buscar = st.text_input("Ingrese el nombre que desea buscar")

if st.button("Buscar"):

    nombre_buscar = nombre_buscar.strip()

    encontrado = False

    for i in range(len(st.session_state.alumnos)):

        if st.session_state.alumnos[i].lower() == nombre_buscar.lower():

            st.success(
                f"Alumno: {st.session_state.alumnos[i]} "
                f"- Nota: {st.session_state.notas[i]}"
            )

            encontrado = True
            break

    if not encontrado:
        st.error("No se encontró el alumno.")


st.divider()


# --------------------------------
# ELIMINAR ALUMNO
# --------------------------------

st.header("Eliminar alumno")

if len(st.session_state.alumnos) > 0:

    alumno_eliminar = st.selectbox(
        "Seleccione el alumno que desea eliminar",
        st.session_state.alumnos
    )

    if st.button("Eliminar alumno"):

        indice = st.session_state.alumnos.index(alumno_eliminar)

        st.session_state.alumnos.pop(indice)
        st.session_state.notas.pop(indice)

        st.success("Alumno eliminado correctamente.")

else:
    st.info("No hay alumnos para eliminar.")


st.divider()


# --------------------------------
# MODIFICAR NOTA (OPCIONAL)
# --------------------------------

st.header("Modificar nota")

if len(st.session_state.alumnos) > 0:

    alumno_modificar = st.selectbox(
        "Seleccione un alumno",
        st.session_state.alumnos,
        key="alumno_modificar"
    )

    nueva_nota = st.number_input(
        "Nueva nota",
        min_value=1,
        max_value=10,
        step=1,
        key="nueva_nota"
    )

    if st.button("Actualizar nota"):

        indice = st.session_state.alumnos.index(alumno_modificar)

        st.session_state.notas[indice] = int(nueva_nota)

        st.success("Nota actualizada correctamente.")


st.divider()


# --------------------------------
# VACIAR TODOS LOS REGISTROS
# --------------------------------

st.header("Administrar registros")

if st.button("Vaciar todos los registros"):

    st.session_state.alumnos.clear()
    st.session_state.notas.clear()

    st.success("Todos los registros fueron eliminados.")
