import streamlit as st
from foods_db import FOODS_DB
from data_manager import load_plan, save_log, load_log, today_str

st.title("📅 Acompanhamento diário")
st.write(
    "Registre o que você consumiu ao longo do dia. Cada item é uma linha. "
    "Os dados ficam salvos por data em arquivos locais."
)

# =========================
# Meta (carregada da dieta salva)
# =========================
meals_plan = load_plan()

def calcular_totais_dieta(meals_dict):
    total_kcal = total_prot = total_carb = total_fat = 0.0
    for items in meals_dict.values():
        for i in items:
            total_kcal += i["kcal"]
            total_prot += i["protein"]
            total_carb += i["carb"]
            total_fat  += i["fat"]
    return total_kcal, total_prot, total_carb, total_fat

target_kcal, target_prot, target_carb, target_fat = calcular_totais_dieta(meals_plan)

st.markdown("### 🎯 Meta diária (vinda da página **Minha dieta**)")
if target_kcal == target_prot == target_carb == target_fat == 0:
    st.info("Nenhuma dieta base encontrada. Monte e salve na página **Minha dieta**.")
else:
    st.markdown(
        f"- **Calorias alvo:** {target_kcal:.0f} kcal\n"
        f"- **Proteínas alvo:** {target_prot:.1f} g\n"
        f"- **Carboidratos alvo:** {target_carb:.1f} g\n"
        f"- **Gorduras alvo:** {target_fat:.1f} g"
    )

st.markdown("---")

# =========================
# Dia selecionado
# =========================
st.subheader("🗓️ Selecione o dia")
default_day = today_str()
day = st.text_input("Data (YYYY-MM-DD)", value=default_day, key="log_day")

# =========================
# Estado do log do dia
# =========================
if "daily_log" not in st.session_state or st.session_state.get("loaded_day") != day:
    st.session_state["daily_log"] = load_log(day)
    st.session_state["loaded_day"] = day

st.subheader("✍️ Registrar consumo")
c1, c2, c3 = st.columns([2, 1.2, 1])
with c1:
    food = st.selectbox("Alimento consumido", sorted(FOODS_DB.keys()), key="log_food")
with c2:
    grams = st.number_input("Quantidade (g)", min_value=1, max_value=2000, value=100, step=10, key="log_grams")
with c3:
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
        save_log(day, st.session_state["daily_log"])  # salva a cada inserção
        st.success(f"Adicionado: {grams} g de {food}")

st.markdown("---")

# =========================
# Tabela de lançamentos + totais
# =========================
if not st.session_state["daily_log"]:
    st.info("Nenhum alimento registrado ainda para este dia. Adicione acima.")
else:
    st.subheader(f"📋 Consumos de {day}")
    st.table(st.session_state["daily_log"])

    total_kcal_cons = sum(i["kcal"] for i in st.session_state["daily_log"])
    total_prot_cons = sum(i["protein"] for i in st.session_state["daily_log"])
    total_carb_cons = sum(i["carb"] for i in st.session_state["daily_log"])
    total_fat_cons  = sum(i["fat"]  for i in st.session_state["daily_log"])

    st.subheader("📊 Totais consumidos")
    st.markdown(
        f"- **Calorias consumidas:** {total_kcal_cons:.0f} kcal\n"
        f"- **Proteínas consumidas:** {total_prot_cons:.1f} g\n"
        f"- **Carboidratos consumidos:** {total_carb_cons:.1f} g\n"
        f"- **Gorduras consumidas:** {total_fat_cons:.1f} g"
    )

    if target_kcal or target_prot or target_carb or target_fat:
        st.subheader("🧮 Diferença vs meta")
        st.markdown(
            f"- **Calorias restantes:** {target_kcal - total_kcal_cons:.0f} kcal\n"
            f"- **Proteína restante:** {target_prot - total_prot_cons:.1f} g\n"
            f"- **Carboidratos restantes:** {target_carb - total_carb_cons:.1f} g\n"
            f"- **Gorduras restantes:** {target_fat - total_fat_cons:.1f} g"
        )
        st.caption("Valores negativos = meta ultrapassada.")

    # Limpar
    if st.button("🗑️ Limpar registros do dia"):
        st.session_state["daily_log"] = []
        save_log(day, st.session_state["daily_log"])
        st.success("Registros do dia apagados.")
