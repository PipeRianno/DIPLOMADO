import streamlit as st
import pandas as pd

st.set_page_config(page_title="Misterio del Café", page_icon="☕", layout="centered")
st.title("🔍 Misterio de las Tazas de Café")
st.write("""
Cinco compañeros de oficina tienen cada uno un escritorio de color diferente, 
beben diferentes tipos de café, usan diferentes marcas de computadores, 
trabajan en diferentes proyectos y llegan a la oficina a diferentes horas.

**OBJETIVO:**  
Descubrir toda la disposición y responder:  
**¿Quién llega a las 7:00 y qué café toma?**

---

### Pistas:
1. El que trabaja en Marketing se sienta en el escritorio rojo.  
2. El de Desarrollo bebe espresso.  
3. El que llega a las 7:00 está al lado del que toma latte.  
4. El que usa Lenovo trabaja en Logística.  
5. El escritorio verde está inmediatamente a la izquierda del blanco.  
6. El que toma americano se sienta en el escritorio verde.  
7. El que usa HP llega a las 8:30.  
8. El que se sienta en el centro bebe capuchino.  
9. El que se sienta en el primer escritorio usa Apple.  
10. El que toma mocaccino está junto al que usa Asus.  
11. El que trabaja en Finanzas usa Dell.  
12. El que llega a las 9:00 está en el escritorio azul.  
---
""")

# Opciones posibles
escritorios = ["Rojo", "Azul", "Verde", "Blanco", "Amarillo"]
cafes = ["Espresso", "Latte", "Capuchino", "Americano", "Mocaccino"]
computadores = ["Apple", "Dell", "Lenovo", "HP", "Asus"]
proyectos = ["Marketing", "Ventas", "Finanzas", "Desarrollo", "Logística"]
horas = ["7:00", "7:30", "8:00", "8:30", "9:00"]

# Crear tabla interactiva
st.subheader("🔢 Completa la tabla")
data = []
for i in range(5):
    with st.expander(f"Persona {i+1}"):
        e = st.selectbox(f"Escritorio {i+1}", [""] + escritorios, key=f"e{i}")
        c = st.selectbox(f"Café {i+1}", [""] + cafes, key=f"c{i}")
        comp = st.selectbox(f"Computador {i+1}", [""] + computadores, key=f"comp{i}")
        p = st.selectbox(f"Proyecto {i+1}", [""] + proyectos, key=f"p{i}")
        h = st.selectbox(f"Hora {i+1}", [""] + horas, key=f"h{i}")
        data.append([e, c, comp, p, h])

# Botón para verificar
if st.button("✅ Verificar respuesta"):
    df_user = pd.DataFrame(data, columns=["Escritorio", "Café", "Computador", "Proyecto", "Hora"])

    # Solución correcta
    solucion = pd.DataFrame([
        ["Rojo", "Latte", "Apple", "Marketing", "7:30"],
        ["Azul", "Mocaccino", "Asus", "Ventas", "9:00"],
        ["Verde", "Americano", "Lenovo", "Logística", "8:00"],
        ["Blanco", "Capuchino", "HP", "Desarrollo", "8:30"],
        ["Amarillo", "Espresso", "Dell", "Finanzas", "7:00"]
    ], columns=["Escritorio", "Café", "Computador", "Proyecto", "Hora"])

    if df_user.equals(solucion):
        st.success("🎉 ¡Correcto! El que llega a las 7:00 es el del escritorio Amarillo, toma Espresso y trabaja en Finanzas.")
    else:
        st.error("❌ Aún no es correcto, revisa de nuevo las pistas.")
        st.write("Pista: Verifica las horas y la relación entre los cafés y los escritorios.")

# Mostrar solución final (solo para moderador)
if st.checkbox("Mostrar solución (moderador)"):
    st.dataframe(pd.DataFrame([
        ["Rojo", "Latte", "Apple", "Marketing", "7:30"],
        ["Azul", "Mocaccino", "Asus", "Ventas", "9:00"],
        ["Verde", "Americano", "Lenovo", "Logística", "8:00"],
        ["Blanco", "Capuchino", "HP", "Desarrollo", "8:30"],
        ["Amarillo", "Espresso", "Dell", "Finanzas", "7:00"]
    ], columns=["Escritorio", "Café", "Computador", "Proyecto", "Hora"]))
