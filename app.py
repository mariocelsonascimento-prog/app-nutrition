import streamlit as st
from foods_db import FOODS_DB

st.set_page_config(page_title="Minha dieta - Nutri App", page_icon="💪")

st.title("🍽️ Minha dieta")
st.write(
    "Monte sua dieta diária por refeição usando a base de alimentos personalizada. "
    "Adicione refeições, selecione alimentos e quantidades, e veja os macros por refeição e no total."
)

# =========================
# Inicialização do estado
# =========================
if "meals" not in st.session_state:
    # meals = { nome_refeicao: [ {food, grams, kcal, protein, carb, fat}, ... ] }
    st.session_state["meals"] = {}

if "meal_input" not in st.session_state:
    st.session_state["meal_input"] = ""

if "meal_message" not in st.session_state:
    st.session_state["meal_message"] = ""


# =========================
# Função callback para adicionar refeição
# =========================
def add_meal_callback():
    name = st.session_state["meal_input"].strip()
    if not name:
        st.session_state["meal_message"] = "⚠️ Digite um nome válido para a refeição."
    elif name in st.session_state["meals"]:
        st.session_state["meal_message"] = "⚠️ Essa refeição já existe."
    else:
        st.session_state["meals"][name] = []
        st.session_state["meal_message"] = f"✅ Refeição **{name}** adicionada."
        # limpa o campo de texto
        st.session_state["meal_input"] = ""


# =========================
# Adicionar nova refeição
# =========================
st.subheader("➕ Adicionar refeição")

col_new1, col_new2 = st.columns([3, 1])
with col_new1:
    st.text_input(
        "Nome da refeição",
        placeholder="Ex: Café da manhã, Almoço, Lanche da tarde...",
        key="meal_input",
    )
with col_new2:
    st.button("Adicionar", use_container_width=True, on_click=add_meal_callback)

if st.session_state["meal_message"]:
    st.markdown(st.session_state["meal_message"])

st.markdown("---")

# =========================
# Listar refeições e permitir adicionar alimentos
# =========================
if not st.session_state["meals"]:
    st.info("Nenhuma refeição criada ainda. Adicione uma acima para começar.")
else:
    st.subheader("📋 Refeições do dia")

    total_kcal_day = 0.0
    total_prot_day = 0.0
    total_carb_day = 0.0
    total_fat_day = 0.0

    # Vamos guardar refeições para remover, se o usuário quiser
    meals_to_delete = []

    for meal_name, items in st.session_state["meals"].items():
        with st.expander(f"🍽️ {meal_name}", expanded=True):

            # Botão para remover refeição
            if st.button(f"Remover refeição '{meal_name}'", key=f"del_{meal_name}"):
                meals_to_delete.append(meal_name)
            else:
                # Seleção de alimento e quantidade para esta refeição
                c1, c2, c3 = st.columns([2, 1.2, 1])
                with c1:
                    food = st.selectbox(
                        "Alimento",
                        sorted(FOODS_DB.keys()),
                        key=f"food_{meal_name}",
                    )
                with c2:
                    grams = st.number_input(
                        "Quantidade (g)",
                        min_value=1,
                        max_value=2000,
                        value=100,
                        step=10,
                        key=f"grams_{meal_name}",
                    )
                with c3:
                    if st.button("Adicionar", key=f"add_{meal_name}", use_container_width=True):
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
                        st.session_state["meals"][meal_name].append(item)

                # Mostrar tabela da refeição
                if items:
                    st.write("**Alimentos desta refeição:**")
                    st.table(items)

                    meal_kcal = sum(i["kcal"] for i in items)
                    meal_prot = sum(i["protein"] for i in items)
                    meal_carb = sum(i["carb"] for i in items)
                    meal_fat = sum(i["fat"] for i in items)

                    total_kcal_day += meal_kcal
                    total_prot_day += meal_prot
                    total_carb_day += meal_carb
                    total_fat_day += meal_fat

                    st.markdown(
                        f"**Resumo:** {meal_kcal:.0f} kcal | "
                        f"{meal_prot:.1f} g proteína | "
                        f"{meal_carb:.1f} g carboidratos | "
                        f"{meal_fat:.1f} g gorduras"
                    )
                else:
                    st.caption("Nenhum alimento adicionado ainda para esta refeição.")

    # Remover refeições marcadas
    for m in meals_to_delete:
        del st.session_state["meals"][m]

    # =========================
    # Totais do dia
    # =========================
    st.markdown("---")
    st.subheader("📊 Total diário")

    if total_kcal_day == 0 and total_prot_day == 0 and total_carb_day == 0 and total_fat_day == 0:
        st.caption("Adicione alimentos às refeições para ver o total diário.")
    else:
        st.markdown(
            f"- **Calorias totais:** {total_kcal_day:.0f} kcal\n"
            f"- **Proteínas totais:** {total_prot_day:.1f} g\n"
            f"- **Carboidratos totais:** {total_carb_day:.1f} g\n"
            f"- **Gorduras totais:** {total_fat_day:.1f} g"
        )

    # Botão para limpar tudo
    if st.button("🗑️ Limpar todas as refeições"):
        st.session_state["meals"] = {}
        st.success("Todas as refeições foram limpas. Comece novamente.")
