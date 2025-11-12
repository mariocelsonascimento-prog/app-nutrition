import streamlit as st
from foods_db import FOODS_DB

st.title("📅 Acompanhamento diário")
st.write(
    "Registre tudo o que você consumiu ao longo do dia. "
    "Cada item lançado aparece em uma linha, com os macros correspondentes. "
    "Se você já montou sua dieta na página **Minha dieta**, aqui também verá "
    "quanto ainda falta (ou quanto passou) em relação ao plano."
)

# =========================
# 1) Recuperar totais da dieta (Minha dieta)
# =========================

def calcular_totais_dieta():
    if "meals" not in st.session_state or not st.session_state["meals"]:
        return 0.0, 0.0, 0.0, 0.0

    total_kcal = 0.0
    total_prot = 0.0
    total_carb = 0.0
    total_fat = 0.0

    for items in st.session_state["meals"].values():
        for i in items:
            total_kcal += i["kcal"]
            total_prot += i["protein"]
            total_carb += i["carb"]
            total_fat += i["fat"]

    return total_kcal, total_prot, total_carb, total_fat


target_kcal, target_prot, target_carb, target_fat = calcular_totais_dieta()

st.markdown("### 🎯 Meta diária baseada na página **Minha dieta**")

if target_kcal == 0 and target_prot == 0 and target_carb == 0 and target_fat == 0:
    st.info(
        "Nenhuma dieta base encontrada. Monte sua dieta na página **Minha dieta** "
        "para definir uma meta diária de macros."
    )
else:
    st.markdown(
        f"- **Calorias alvo:** {target_kcal:.0f} kcal\n"
        f"- **Proteínas alvo:** {target_prot:.1f} g\n"
        f"- **Carboidratos alvo:** {target_carb:.1f} g\n"
        f"- **Gorduras alvo:** {target_fat:.1f} g"
    )

st.markdown("---")

# =========================
# 2) Log diário de consumo
# =========================

if "daily_log" not in st.session_state:
    # Lista de registros do dia:
    # { food, grams, kcal, protein, carb, fat }
    st.session_state["daily_log"] = []

st.subheader("✍️ Registrar consumo do dia")

col1, col2, col3 = st.columns([2, 1.2, 1])
with col1:
    food = st.selectbox(
        "Alimento consumido",
        sorted(FOODS_DB.keys()),
        key="log_food"
    )
with col2:
    grams = st.number_input(
        "Quantidade (g)",
        min_value=1,
        max_value=2000,
        value=100,
        step=10,
        key="log_grams"
    )
with col3:
    if st.button("Adicionar consumo", use_container_width=True):
        data = FOODS_DB[food]
        factor = grams / 100.0
        entry = {
            "food": food,
            "grams": grams,
            "kcal": round(data["kcal"] * factor, 1),
            "protein": round(data["protein"] * factor, 1),
            "carb": round(data["carb"] * factor, 1),
            "fat": round(data["fat"] * factor, 1),
        }
        st.session_state["daily_log"].append(entry)
        st.success(f"Adicionado: {grams} g de {food}")

st.markdown("---")

# =========================
# 3) Exibir log em linhas + totais consumidos
# =========================

if not st.session_state["daily_log"]:
    st.info("Nenhum alimento registrado ainda para hoje. Adicione acima.")
else:
    st.subheader("📋 Consumos registrados (linha a linha)")
    # Cada item é uma linha separada (sem agrupar por refeição)
    st.table(st.session_state["daily_log"])

    total_kcal_cons = sum(i["kcal"] for i in st.session_state["daily_log"])
    total_prot_cons = sum(i["protein"] for i in st.session_state["daily_log"])
    total_carb_cons = sum(i["carb"] for i in st.session_state["daily_log"])
    total_fat_cons  = sum(i["fat"]  for i in st.session_state["daily_log"])

    st.subheader("📊 Totais consumidos no dia")
    st.markdown(
        f"- **Calorias consumidas:** {total_kcal_cons:.0f} kcal\n"
        f"- **Proteínas consumidas:** {total_prot_cons:.1f} g\n"
        f"- **Carboidratos consumidos:** {total_carb_cons:.1f} g\n"
        f"- **Gorduras consumidas:** {total_fat_cons:.1f} g"
    )

    # =========================
    # 4) Diferença em relação à meta (deduzir da dieta)
    # =========================
    if target_kcal > 0 or target_prot > 0 or target_carb > 0 or target_fat > 0:
        st.subheader("🧮 Diferença em relação à dieta planejada")

        diff_kcal = target_kcal - total_kcal_cons
        diff_prot = target_prot - total_prot_cons
        diff_carb = target_carb - total_carb_cons
        diff_fat  = target_fat - total_fat_cons

        st.markdown(
            f"- **Calorias restantes:** {diff_kcal:.0f} kcal\n"
            f"- **Proteína restante:** {diff_prot:.1f} g\n"
            f"- **Carboidratos restantes:** {diff_carb:.1f} g\n"
            f"- **Gorduras restantes:** {diff_fat:.1f} g"
        )
        st.caption("Valores negativos = você ultrapassou a meta daquele macro. 😉")

    # Botão para limpar o dia
    if st.button("🗑️ Limpar registros do dia"):
        st.session_state["daily_log"] = []
        st.success("Registros do dia apagados. Comece novamente.")
