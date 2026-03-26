import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ejercicio 3 - Diseño de Capacidad", layout="wide")

st.title("📊 Ejercicio 3 - Diseño Inverso (M/M/1)")
st.markdown("### Determinar capacidad mínima para cumplir nivel de servicio")

# INPUTS
st.sidebar.header("⚙️ Parámetros")

lam = st.sidebar.number_input("λ (clientes/hora)", value=30.0)
Wq_target_min = st.sidebar.number_input("Tiempo máximo en cola (min)", value=2.0)

# Convertir a horas
Wq_target = Wq_target_min / 60

# CALCULO DE μ MINIMO
def calcular_mu_min(lam, Wq):
    # Resolviendo: Wq = λ / (μ(μ-λ))
    # μ² - λμ - (λ / Wq) = 0
    a = 1
    b = -lam
    c = -(lam / Wq)

    mu = (-b + np.sqrt(b**2 - 4*a*c)) / (2*a)
    return mu

mu_min = calcular_mu_min(lam, Wq_target)

# Redondeo práctico
mu_practico = np.ceil(mu_min)

st.subheader("📌 Resultados de Capacidad")

st.write(f"μ mínimo teórico: {mu_min:.2f}")
st.write(f"μ recomendado (práctico): {mu_practico:.0f}")

# FUNCION MM1
def mm1(lam, mu):
    rho = lam / mu
    Lq = (lam**2) / (mu * (mu - lam))
    L = lam / (mu - lam)
    Wq = lam / (mu * (mu - lam))
    W = 1 / (mu - lam)
    return rho, Lq, L, Wq, W

rho, Lq, L, Wq, W = mm1(lam, mu_practico)

# RESULTADOS
st.subheader("📈 Indicadores del Sistema")

col1, col2 = st.columns(2)

with col1:
    st.write(f"Utilización (ρ): {rho:.4f}")
    st.write(f"Lq: {Lq:.4f}")
    st.write(f"L: {L:.4f}")

with col2:
    st.write(f"Wq: {Wq*60:.2f} min")
    st.write(f"W: {W*60:.2f} min")

# VERIFICACION
st.subheader("✅ Verificación")

if Wq*60 <= Wq_target_min:
    st.success("Se cumple el nivel de servicio")
else:
    st.error("No se cumple el nivel de servicio")

# GRAFICO SENSIBILIDAD
st.subheader("📊 Sensibilidad (Wq vs μ)")

mu_vals = np.linspace(lam+1, lam+50, 100)
Wq_vals = [lam / (m * (m - lam)) for m in mu_vals]

fig, ax = plt.subplots()
ax.plot(mu_vals, np.array(Wq_vals)*60)
ax.axhline(Wq_target_min)
ax.axvline(mu_practico)

ax.set_title("Tiempo en cola vs capacidad")
ax.set_xlabel("μ")
ax.set_ylabel("Wq (min)")

st.pyplot(fig)

# CONCLUSION
st.subheader("🧠 Conclusión")

st.markdown("""
- Para cumplir el nivel de servicio, se necesita aumentar la capacidad.
- El sistema requiere un margen entre λ y μ.
- Diseñar por intuición puede generar congestión.

✅ Se recomienda usar la capacidad calculada o superior.
""")
