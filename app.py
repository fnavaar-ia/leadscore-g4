"""Dashboard Streamlit local do Lead Scorer."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.filters import filter_queue
from src.ingest import load_and_prepare
from src.scoring import score_open_opportunities


st.set_page_config(page_title="Lead Scorer | Dashboard", page_icon="🎯", layout="wide")


@st.cache_data(show_spinner="Carregando dados reais e calculando a fila...")
def build_queue() -> pd.DataFrame:
    enriched = load_and_prepare().enriched
    scored = score_open_opportunities(enriched)
    dimensions = enriched[
        [
            "opportunity_id",
            "account",
            "sales_agent",
            "manager",
            "regional_office",
            "product",
            "deal_stage",
            "sales_price",
            "engage_date",
        ]
    ]
    return scored.merge(dimensions, on="opportunity_id", how="left", validate="one_to_one")


def _display_account(value: object) -> str:
    return "Não informada" if pd.isna(value) else str(value)


def _display_price(value: object) -> str:
    return "Indisponível" if pd.isna(value) else f"{float(value):,.2f}"


def _friendly_table(frame: pd.DataFrame) -> pd.DataFrame:
    table = frame.copy()
    table["account"] = table["account"].map(_display_account)
    table["sales_price"] = table["sales_price"].map(_display_price)
    return table.rename(
        columns={
            "rank": "Posição",
            "opportunity_id": "Oportunidade",
            "account": "Conta",
            "sales_agent": "Vendedor",
            "manager": "Manager",
            "regional_office": "Região",
            "deal_stage": "Estágio",
            "product": "Produto",
            "priority_score": "Score",
            "sales_price": "Preço referência",
        }
    )


def _reset_filters() -> None:
    for key in ("agents", "managers", "regions", "products", "stages", "score_range", "search"):
        st.session_state.pop(key, None)


def _render_sidebar(queue: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros da carteira")
    st.sidebar.caption("Combine filtros para explorar a fila. O score original é preservado.")
    if st.sidebar.button("Limpar filtros", use_container_width=True):
        _reset_filters()
        st.rerun()

    agents = st.sidebar.multiselect("Vendedor", sorted(queue["sales_agent"].dropna().unique()), key="agents")
    managers = st.sidebar.multiselect("Manager", sorted(queue["manager"].dropna().unique()), key="managers")
    regions = st.sidebar.multiselect("Região", sorted(queue["regional_office"].dropna().unique()), key="regions")
    stages = st.sidebar.multiselect("Estágio", ["Engaging", "Prospecting"], key="stages")
    products = st.sidebar.multiselect("Produto", sorted(queue["product"].dropna().unique()), key="products")
    score_range = st.sidebar.slider("Faixa de score", 0, 100, (0, 100), key="score_range")
    search = st.sidebar.text_input("Buscar oportunidade, conta ou vendedor", placeholder="Ex.: 021Z2J9L", key="search")
    return filter_queue(
        queue,
        sales_agents=agents,
        managers=managers,
        regional_offices=regions,
        products=products,
        stages=stages,
        min_score=score_range[0],
        max_score=score_range[1],
        search_text=search,
    )


def _render_kpis(queue: pd.DataFrame, filtered: pd.DataFrame) -> None:
    visible = len(filtered)
    total = len(queue)
    missing_accounts = int(filtered["account"].isna().sum()) if visible else 0
    engaging = int(filtered["deal_stage"].eq("Engaging").sum()) if visible else 0
    cards = st.columns(5)
    cards[0].metric("Deals abertos", f"{visible:,}", f"de {total:,}")
    cards[1].metric("Score médio", "—" if not visible else f"{filtered['priority_score'].mean():.1f}")
    cards[2].metric("Engaging", f"{engaging:,}", "maturidade heurística")
    cards[3].metric("Conta ausente", f"{missing_accounts:,}", "revisar contexto")
    cards[4].metric("Cobertura", "—" if not total else f"{visible / total:.0%}", "da fila original")


def _render_overview(filtered: pd.DataFrame) -> None:
    st.subheader("Visão executiva")
    left, right = st.columns(2)
    stage_counts = filtered["deal_stage"].value_counts().rename_axis("Estágio").reset_index(name="Deals")
    manager_counts = filtered["manager"].value_counts().head(10).rename_axis("Manager").reset_index(name="Deals")
    with left:
        st.markdown("**Deals por estágio**")
        st.bar_chart(stage_counts, x="Estágio", y="Deals", use_container_width=True)
    with right:
        st.markdown("**Top managers na seleção**")
        st.bar_chart(manager_counts, x="Manager", y="Deals", use_container_width=True)
    st.caption("Os gráficos são descritivos da seleção atual; não representam probabilidade de fechamento.")


def _render_queue(filtered: pd.DataFrame) -> None:
    st.subheader("Fila priorizada")
    show_all = st.checkbox("Mostrar todas as oportunidades", value=False)
    visible = filtered if show_all else filtered.head(100)
    if not show_all and len(filtered) > 100:
        st.caption("Exibindo as 100 primeiras posições globais. Ative a opção para ver toda a seleção.")
    st.dataframe(
        _friendly_table(visible)[
            ["Posição", "Oportunidade", "Conta", "Vendedor", "Estágio", "Produto", "Score", "Preço referência"]
        ],
        hide_index=True,
        use_container_width=True,
        height=520,
    )


def _render_detail(filtered: pd.DataFrame) -> None:
    st.subheader("Detalhe e explicação")
    options = filtered["opportunity_id"].astype(str).tolist()
    selected_id = st.selectbox("Selecione uma oportunidade", options)
    detail = filtered.loc[filtered["opportunity_id"].astype(str).eq(selected_id)].iloc[0]
    st.markdown(f"### Por que a oportunidade `{selected_id}` está nesta posição?")
    cols = st.columns(4)
    cols[0].metric("Score", int(detail["priority_score"]))
    cols[1].metric("Posição global", int(detail["rank"]))
    cols[2].metric("Estágio", str(detail["deal_stage"]))
    cols[3].metric("Preço referência", _display_price(detail["sales_price"]))
    detail_cols = st.columns(2)
    with detail_cols[0]:
        st.write(f"**Conta:** {_display_account(detail['account'])}")
        st.write(f"**Vendedor:** {detail['sales_agent']}")
        st.write(f"**Manager:** {detail['manager']}")
        st.write(f"**Região:** {detail['regional_office']}")
    with detail_cols[1]:
        st.write("**Contribuições do score**")
        st.json(detail["score_factors"])
    if detail["warnings"]:
        st.warning("; ".join(detail["warnings"]))
    else:
        st.success("Nenhum aviso de qualidade para esta oportunidade.")
    st.caption(
        f"Política {detail['policy_version']} · referência {detail['reference_date']} · score heurístico, não probabilidade nem receita esperada."
    )


def main() -> None:
    st.title("🎯 Lead Scorer")
    st.caption("Dashboard de priorização comercial com dados históricos reais")
    st.info("Demonstração offline · Data de referência: 31/12/2017 · Filtros alteram a visualização, não recalculam o score.")
    try:
        queue = build_queue()
        filtered = _render_sidebar(queue)
    except Exception as error:  # pragma: no cover - estado exibido pelo Streamlit
        st.error(f"Não foi possível carregar a fila: {error}")
        st.stop()

    _render_kpis(queue, filtered)
    if filtered.empty:
        st.warning("Nenhuma oportunidade corresponde aos filtros selecionados.")
        return

    overview, queue_tab, detail = st.tabs(["Visão geral", "Fila priorizada", "Detalhe da oportunidade"])
    with overview:
        _render_overview(filtered)
    with queue_tab:
        _render_queue(filtered)
    with detail:
        _render_detail(filtered)

    with st.expander("Como interpretar este dashboard"):
        st.markdown(
            "- **Score:** índice heurístico de prioridade, não percentual de chance de fechamento.\n"
            "- **Engaging/Prospecting:** regra comercial aprovada; não é taxa de conversão histórica.\n"
            "- **Preço referência:** valor de catálogo, usado como contexto e desempate; não é receita esperada.\n"
            "- **Conta ausente:** não reduz o score e aparece como aviso para revisão humana."
        )


if __name__ == "__main__":
    main()

