"""Interface Streamlit local do Lead Scorer."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.filters import filter_queue
from src.ingest import load_and_prepare
from src.scoring import score_open_opportunities


st.set_page_config(page_title="Lead Scorer", page_icon="🎯", layout="wide")


@st.cache_data(show_spinner="Carregando dados reais e calculando a fila...")
def build_queue() -> pd.DataFrame:
    enriched = load_and_prepare().enriched
    scored = score_open_opportunities(enriched)
    dimensions = enriched[
        ["opportunity_id", "account", "sales_agent", "manager", "regional_office", "product", "deal_stage", "sales_price", "engage_date"]
    ]
    return scored.merge(dimensions, on="opportunity_id", how="left", validate="one_to_one")


def _display_account(value: object) -> str:
    return "Não informada" if pd.isna(value) else str(value)


def _display_price(value: object) -> str:
    return "Indisponível" if pd.isna(value) else f"{float(value):,.2f}"


def main() -> None:
    st.title("🎯 Lead Scorer")
    st.caption("Demonstração offline com dados históricos reais. A pontuação é heurística, não é probabilidade de fechamento.")
    st.info("Data de referência: 31/12/2017. Filtros alteram apenas a visualização; não recalculam o score.")

    try:
        queue = build_queue()
    except Exception as error:  # pragma: no cover - estado exibido pelo Streamlit
        st.error(f"Não foi possível carregar a fila: {error}")
        st.stop()

    st.sidebar.header("Filtros da carteira")
    agents = st.sidebar.multiselect("Vendedor", sorted(queue["sales_agent"].dropna().unique()))
    managers = st.sidebar.multiselect("Manager", sorted(queue["manager"].dropna().unique()))
    regions = st.sidebar.multiselect("Região", sorted(queue["regional_office"].dropna().unique()))

    filtered = filter_queue(
        queue,
        sales_agents=agents,
        managers=managers,
        regional_offices=regions,
    )
    total, visible = len(queue), len(filtered)
    col1, col2, col3 = st.columns(3)
    col1.metric("Deals abertos", total)
    col2.metric("Na visualização", visible)
    col3.metric("Score médio visível", "—" if filtered.empty else f"{filtered['priority_score'].mean():.1f}")

    if filtered.empty:
        st.warning("Nenhuma oportunidade corresponde aos filtros selecionados.")
        return

    table = filtered.copy()
    table["account"] = table["account"].map(_display_account)
    table["sales_price"] = table["sales_price"].map(_display_price)
    st.subheader("Fila priorizada")
    st.dataframe(
        table[["rank", "opportunity_id", "account", "sales_agent", "deal_stage", "product", "priority_score", "sales_price"]],
        hide_index=True,
        use_container_width=True,
    )

    options = filtered["opportunity_id"].astype(str).tolist()
    selected_id = st.selectbox("Ver detalhes da oportunidade", options)
    detail = filtered.loc[filtered["opportunity_id"].astype(str).eq(selected_id)].iloc[0]
    st.subheader(f"Por que a oportunidade {selected_id} está nesta posição?")
    detail_cols = st.columns(3)
    detail_cols[0].metric("Score", int(detail["priority_score"]))
    detail_cols[1].metric("Posição global", int(detail["rank"]))
    detail_cols[2].metric("Stage", str(detail["deal_stage"]))
    st.write(f"**Conta:** {_display_account(detail['account'])}")
    st.write(f"**Preço de catálogo:** {_display_price(detail['sales_price'])}")
    st.write("**Contribuições:**")
    st.json(detail["score_factors"])
    if detail["warnings"]:
        st.warning("; ".join(detail["warnings"]))
    else:
        st.success("Nenhum aviso de qualidade para esta oportunidade.")
    st.caption(
        f"Política {detail['policy_version']}. O score prioriza por regra heurística; não estima probabilidade ou receita esperada."
    )


if __name__ == "__main__":
    main()


