from datetime import date, timedelta
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Fases da Lua - Verden", page_icon="🌙", layout="centered"
)

st.title("🌙 Rastreador Lunar de Verden")
st.write(
    "Acompanhe e gerencie as fases da lua para as suas sessões de RPG no ano"
    " de **3020**."
)

# Constante do ciclo sinódico da lua (dias)
SYNODIC_MONTH = 29.53058867
ref_date = date(3020, 7, 29)  # 29 de julho de 3020 é Lua Cheia
half_cycle = SYNODIC_MONTH / 2


# Função central para calcular a fase da lua de qualquer data
INVERVAL_CACHE = SYNODIC_MONTH / 8


def get_moon_phase(target_date):
  delta_days = (target_date - ref_date).days
  phase_cycle = (delta_days + half_cycle) % SYNODIC_MONTH
  interval = SYNODIC_MONTH / 8

  if phase_cycle < interval:
    return "Lua Nova", "🌑", delta_days, phase_cycle
  elif phase_cycle < interval * 2:
    return "Lua Crescente Côncava", "🌒", delta_days, phase_cycle
  elif phase_cycle < interval * 3:
    return "Quarto Crescente", "🌓", delta_days, phase_cycle
  elif phase_cycle < interval * 4:
    return "Lua Crescente Gibosa", "🌔", delta_days, phase_cycle
  elif phase_cycle < interval * 5:
    return "Lua Cheia", "🌕", delta_days, phase_cycle
  elif phase_cycle < interval * 6:
    return "Lua Minguante Gibosa", "🌖", delta_days, phase_cycle
  elif phase_cycle < interval * 7:
    return "Quarto Minguante", "🌗", delta_days, phase_cycle
  else:
    return "Lua Minguante Côncava", "🌘", delta_days, phase_cycle


# Criando abas para separar a consulta rápida e o controle de sessões
tab1, tab2 = st.tabs(
    ["📅 Consulta por Data Única", "🎲 Controle de Sessão (Vários Dias)"]
)

# --- ABA 1: CONSULTA ÚNICA ---
with tab1:
  st.subheader("Consultar um Dia Específico")
  col_d, col_m, col_a = st.columns(3)
  with col_d:
    dia1 = st.number_input(
        "Dia", min_value=1, max_value=31, value=29, step=1, key="d1"
    )
  with col_m:
    mes1 = st.number_input(
        "Mês", min_value=1, max_value=12, value=7, step=1, key="m1"
    )
  with col_a:
    ano1 = st.number_input(
        "Ano", min_value=1000, max_value=9999, value=3020, step=1, key="a1"
    )

  try:
    d_atual = date(int(ano1), int(mes1), int(dia1))
    nome, emoji, delta, cycle = get_moon_phase(d_atual)

    st.markdown("---")
    st.metric(
        label=f"Fase da Lua em {d_atual.strftime('%d/%m/%Y')}",
        value=f"{emoji} {nome}",
    )

    c1, c2 = st.columns(2)
    with c1:
      st.info(f"**Dias desde a referência (29/07/3020):** {delta} dias")
    with c2:
      st.info(f"**Progresso no ciclo:** {cycle:.1f} / {SYNODIC_MONTH:.1f} dias")
  except ValueError:
    st.error(
        "⚠️ A data informada é inválida (por exemplo, um dia que não existe"
        " neste mês)."
    )

# --- ABA 2: CONTROLE DE SESSÃO COM VÁRIOS DIAS ---
with tab2:
  st.subheader("Avançar Dias em uma Sessão")
  st.write(
      "Informe a data em que a sessão começou e quantos dias extras se"
      " passaram durante os eventos."
  )

  col_sd, col_sm, col_sa = st.columns(3)
  with col_sd:
    s_dia = st.number_input(
        "Dia Inicial", min_value=1, max_value=31, value=29, step=1, key="sd"
    )
  with col_sm:
    s_mes = st.number_input(
        "Mês Inicial", min_value=1, max_value=12, value=7, step=1, key="sm"
    )
  with col_sa:
    s_ano = st.number_input(
        "Ano Inicial", min_value=1000, max_value=9999, value=3020, step=1, key="sa"
    )

  dias_passados = st.number_input(
      "Quantos dias se passam após o início? (0 = sessão de um dia só)",
      min_value=0,
      value=0,
      step=1,
  )

  try:
    d_inicio = date(int(s_ano), int(s_mes), int(s_dia))
    d_fim = d_inicio + timedelta(days=int(dias_passados))

    nome_ini, emoji_ini, _, _ = get_moon_phase(d_inicio)
    nome_fim, emoji_fim, _, _ = get_moon_phase(d_fim)

    st.markdown("---")
    st.subheader("Resumo da Sessão")

    col_res1, col_res2 = st.columns(2)
    with col_res1:
      st.metric(
          label=f"Início ({d_inicio.strftime('%d/%m/%Y')})",
          value=f"{emoji_ini} {nome_ini}",
      )
    with col_res2:
      st.metric(
          label=f"Fim ({d_fim.strftime('%d/%m/%Y')})",
          value=f"{emoji_fim} {nome_fim}",
      )

    if dias_passados > 0:
      st.success(
          f"🗓️ A aventura cobriu **{dias_passados + 1} dias** no total"
          f" (começando em {d_inicio.strftime('%d/%m/%Y')} e encerrando em"
          f" {d_fim.strftime('%d/%m/%Y')})."
      )
    else:
      st.info("🗓️ Sessão de um único dia (sem passagem extra de tempo).")

  except ValueError:
    st.error("⚠️ A data inicial informada é inválida.")

st.markdown("---")
st.markdown(
    "*Dica de Mestre:* Salve o arquivo e atualize a página no navegador para"
    " ver o novo recurso funcionando!"
)
