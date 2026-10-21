from datetime import date
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Fases da Lua - Verden", page_icon="🌙", layout="centered"
)

st.title("🌙 Rastreador Lunar de Verden")
st.write(
    "Acompanhe a fase atual da lua para as suas sessões de RPG no ano de"
    " **3020**."
)

# Constante do ciclo sinódico da lua (dias)
SYNODIC_MONTH = 29.53058867

# Data de referência fixa: 29 de julho de 3020 (Lua Cheia)
ref_date = date(3020, 7, 29)

st.sidebar.header("⚙️ Configurações do Mestre")
st.sidebar.write("**Referência de Lua Cheia:** 29/07/3020")

# Seleção da data atual no formato estrito Dia / Mês / Ano
st.subheader("📅 Data Atual da Campanha em Verden")

col_d, col_m, col_a = st.columns(3)
with col_d:
  dia = st.number_input("Dia", min_value=1, max_value=31, value=29, step=1)
with col_m:
  mes = st.number_input("Mês", min_value=1, max_value=12, value=7, step=1)
with col_a:
  ano = st.number_input(
      "Ano", min_value=1000, max_value=9999, value=3020, step=1
  )

# Validação se a data é real
try:
  current_date = date(int(ano), int(mes), int(dia))
  data_valida = True
except ValueError:
  data_valida = False
  st.error(
      "⚠️ A data informada é inválida (por exemplo, um dia que não existe neste"
      " mês). Ajuste os valores."
  )

if data_valida:
  # --- LÓGICA DE CÁLCULO CORRIGIDA ---
  delta_days = (current_date - ref_date).days

  # Como a referência é Lua Cheia (metade do ciclo), deslocamos o cálculo em 50%
  half_cycle = SYNODIC_MONTH / 2
  phase_cycle = (delta_days + half_cycle) % SYNODIC_MONTH

  interval = SYNODIC_MONTH / 8


  def get_moon_phase(cycle):
    if cycle < interval:
      return "Lua Nova", "🌑"
    elif cycle < interval * 2:
      return "Lua Crescente Côncava", "🌒"
    elif cycle < interval * 3:
      return "Quarto Crescente", "🌓"
    elif cycle < interval * 4:
      return "Lua Crescente Gibosa", "🌔"
    elif cycle < interval * 5:
      return "Lua Cheia", "🌕"
    elif cycle < interval * 6:
      return "Lua Minguante Gibosa", "🌖"
    elif cycle < interval * 7:
      return "Quarto Minguante", "🌗"
    else:
      return "Lua Minguante Côncava", "🌘"


  phase_name, phase_emoji = get_moon_phase(phase_cycle)

  # Formatação das datas para o padrão DD/MM/AAAA nas mensagens
  formatted_current = current_date.strftime("%d/%m/%Y")
  formatted_ref = ref_date.strftime("%d/%m/%Y")

  # --- EXIBIÇÃO NO APP ---
  st.markdown("---")
  st.metric(
      label=f"Fase da Lua em {formatted_current}",
      value=f"{phase_emoji} {phase_name}",
  )

  col1, col2 = st.columns(2)
  with col1:
    st.info(f"**Dias desde a referência ({formatted_ref}):** {delta_days} dias")
  with col2:
    st.info(
        f"**Progresso no ciclo:** {phase_cycle:.1f} / {SYNODIC_MONTH:.1f} dias"
    )
