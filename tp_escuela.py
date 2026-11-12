
import streamlit as st

st.set_page_config(page_title="Sistema de Calificaciones")

st.title("Sistema de Calificaciones")

# Listas de alumnos y notas
if "alumnos" not in st.session_state:
    st.session_state.alumnos = []
    st.session_state.notas = []

alumnos = st.session_state.alumnos
notas = st.session_state.notas

# REGISTRAR ALUMNO
st.header("Registrar alumno")

nombre = st.text_input("Nombre")
nota = st.number_input("Nota", 1, 10, 1)

if st.button("Registrar"):
    nombre = nombre.strip()

    if not nombre:
        st.error("Ingrese un nombre.")
    elif nombre.lower() in [a.lower() for a in alumnos]:
        st.error("El alumno ya existe.")
    else:
        alumnos.append(nombre)
        notas.append(nota)
        st.success("Alumno registrado.")

# LISTADO
st.header("Listado de alumnos")

if alumnos:
    st.table({"Alumno": alumnos, "Nota": notas})
else:
    st.info("No hay alumnos registrados.")

# ESTADÍSTICAS
st.header("Estadísticas")

if notas:
    aprobados = sum(n >= 6 for n in notas)

    st.write("Promedio:", round(sum(notas) / len(notas), 2))
    st.write("Nota máxima:", max(notas))
    st.write("Nota mínima:", min(notas))
    st.write("Cantidad de alumnos:", len(alumnos))
    st.write("Aprobados:", aprobados)
    st.write("Desaprobados:", len(notas) - aprobados)
    st.write("Porcentaje de aprobados:", round(aprobados / len(notas) * 100, 2), "%")
else:
    st.warning("No hay notas.")

# BUSCAR ALUMNO
st.header("Buscar alumno")

buscar = st.text_input("Nombre a buscar")

if st.button("Buscar"):
    if buscar.lower().strip() in [a.lower() for a in alumnos]:
        i = [a.lower() for a in alumnos].index(buscar.lower().strip())
        st.success(f"{alumnos[i]} - Nota: {notas[i]}")
    else:
        st.error("Alumno no encontrado.")

# MODIFICAR NOTA
st.header("Modificar nota")

if alumnos:
    alumno = st.selectbox("Seleccione alumno", alumnos)
    nueva_nota = st.number_input("Nueva nota", 1, 10, 1)

    if st.button("Actualizar"):
        i = alumnos.index(alumno)
        notas[i] = nueva_nota
        st.success("Nota actualizada.")

# ELIMINAR ALUMNO
st.header("Eliminar alumno")

if alumnos:
    eliminar = st.selectbox("Alumno a eliminar", alumnos, key="eliminar")

    if st.button("Eliminar"):
        i = alumnos.index(eliminar)
        alumnos.pop(i)
        notas.pop(i)
        st.success("Alumno eliminado.")

# VACIAR REGISTROS
st.header("Administrar registros")

if st.button("Vaciar todos los registros"):
    alumnos.clear()
    notas.clear()
    st.success("Registros eliminados.")
