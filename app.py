import streamlit as st
from foods_db import FOODS_DB

st.set_page_config(page_title="Nutri App - Mario", page_icon="💪")

st.title("💪 Nutri App - Cálculo de Macronutrientes")
st.write("Baseado na sua dieta de hipertrofia (off-season). Valores por 100 g, com cálculo automático por porção.")

if "items" not in st.session_state:
    st.session_state.items = []

# Seleção de alimento
col1, col2 = st.columns([2, 1])
with col1:
    food = st.selectbox("Escolha o alimento:", sorted(FOODS_DB.keys()))
with col2:
    grams = st.number_input("Quantidade (g):", min_value=1, max_value=1000, value=100, step=10)

if st.button("Adicionar alimento"):
    data = FOODS_DB[food]
    factor = grams / 100.0
    item = {
        "food": food,
        "grams": grams,
        "kcal": round(data["kcal"] * factor, 1),
        "protein": round(data["protein"] * factor, 1),
        "carb": round(data["carb"] * factor, 1),
        "fat": round(data["fat"] * factor, 1),
    }
    st.session_state.items.append(item)

# Tabela dos itens adicionados
if st.session_state.items:
    st.subheader("Refeição / Dia atual")
    st.table(st.session_state.items)

    total_kcal = sum(i["kcal"] for i in st.session_state.items)
    total_prot = sum(i["protein"] for i in st.session_state.items)
    total_carb = sum(i["carb"] for i in st.session_state.items)
    total_fat  = sum(i["fat"]  for i in st.session_state.items)

    st.markdown(f"### 🔢 Totais")
    st.write(f"**Calorias:** {total_kcal:.0f} kcal")
    st.write(f"**Proteínas:** {total_prot:.1f} g")
    st.write(f"**Carboidratos:** {total_carb:.1f} g")
    st.write(f"**Gorduras:** {total_fat:.1f} g")

    if st.button("Limpar tudo"):
        st.session_state.items = []
else:
    st.info("Adicione um alimento acima para iniciar os cálculos.")
