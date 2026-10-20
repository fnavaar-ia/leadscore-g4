"""Dashboard Streamlit do Lead Scorer, orientado à decisão comercial."""

from __future__ import annotations

import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.filters import filter_queue
from src.ingest import load_and_prepare
from src.scoring import score_open_opportunities


st.set_page_config(page_title="Lead Scorer | Dashboard", page_icon="🎯", layout="wide")

COLORS = {
    "navy": "#102A43",
    "blue": "#1877F2",
    "teal": "#00A99D",
    "amber": "#F2A900",
    "red": "#D64545",
    "muted": "#627D98",
    "surface": "#F7FAFC",
}


@st.cache_data(show_spinner="Carregando dados reais e calculando a fila...")
def build_queue() -> pd.DataFrame:
    """Monta a visão da UI a partir de ingestão e scoring independentes."""

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


def _display_label(value: object) -> str:
    return "Não informado" if pd.isna(value) else str(value)


def _display_price(value: object) -> str:
    return "Indisponível" if pd.isna(value) else f"US$ {float(value):,.2f}"


def _priority_label(score: int | float) -> str:
    return "Prioridade elevada" if score >= 70 else "Prioridade em acompanhamento"


def _chart_layout(fig: go.Figure, *, height: int = 340) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=36, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["navy"], family="Arial"),
        hoverlabel=dict(bgcolor="white", font_color=COLORS["navy"]),
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#E6EDF5", zeroline=False)
    return fig


def _inject_style() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #F7FAFC; }
        [data-testid="stSidebar"] { background: #102A43; }
        [data-testid="stSidebar"] * { color: #F7FAFC; }
        [data-testid="stSidebar"] [data-baseweb="select"] * { color: #102A43; }
        [data-testid="stSidebar"] input { color: #102A43 !important; }
        [data-testid="stMetric"] {
            background: #FFFFFF; border: 1px solid #E6EDF5; border-radius: 14px;
            padding: 16px; box-shadow: 0 4px 16px rgba(16,42,67,.06);
        }
        [data-testid="stMetricLabel"] { color: #627D98; }
        [data-testid="stMetricValue"] { color: #102A43; }
        .hero { background: linear-gradient(115deg, #102A43, #1877F2); border-radius: 18px;
                color: white; padding: 26px 30px; margin-bottom: 18px; }
        .hero h1 { color: white; margin: 0 0 4px 0; font-size: 2rem; }
        .hero p { color: #D9EAFB; margin: 0; font-size: 1rem; }
        .eyebrow { color: #9FB3C8; font-size: .8rem; font-weight: 700; letter-spacing: .08em;
                   text-transform: uppercase; }
        .section-note { color: #627D98; margin-top: -8px; }
        div[data-testid="stTabs"] button { font-weight: 600; }
        .stDownloadButton button { border-radius: 8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _reset_filters() -> None:
    for key in ("agents", "managers", "regions", "products", "stages", "score_range", "search"):
        st.session_state.pop(key, None)


def _render_sidebar(queue: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("## Explorar carteira")
    st.sidebar.caption("Os filtros mudam a visão, nunca a pontuação ou a posição global.")
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
    visible, total = len(filtered), len(queue)
    engaging = int(filtered["deal_stage"].eq("Engaging").sum()) if visible else 0
    missing_accounts = int(filtered["account"].isna().sum()) if visible else 0
    catalog_total = filtered["sales_price"].sum(min_count=1) if visible else None
    cards = st.columns(5)
    cards[0].metric("Deals na seleção", f"{visible:,}", f"de {total:,} abertos")
    cards[1].metric("Score médio", "—" if not visible else f"{filtered['priority_score'].mean():.1f}", "índice heurístico")
    cards[2].metric("Prioridade elevada", f"{engaging:,}", "deals Engaging")
    cards[3].metric("Valor de catálogo", "—" if pd.isna(catalog_total) else f"US$ {catalog_total:,.0f}", "referência, não receita")
    cards[4].metric("Dados a revisar", f"{missing_accounts:,}", "contas não informadas")


def _render_overview(filtered: pd.DataFrame) -> None:
    st.markdown("#### Leitura rápida da seleção")
    st.caption("Use esta visão para decidir onde investigar primeiro; ela descreve a carteira filtrada.")
    viz = filtered.assign(
        manager_label=filtered["manager"].map(_display_label),
        region_label=filtered["regional_office"].map(_display_label),
        priority_band=filtered["priority_score"].map(_priority_label),
    )
    left, right = st.columns(2)
    with left:
        stages = viz["deal_stage"].value_counts().rename_axis("Estágio").reset_index(name="Deals")
        fig = px.pie(stages, names="Estágio", values="Deals", hole=.62, color="Estágio", color_discrete_map={"Engaging": COLORS["teal"], "Prospecting": COLORS["amber"]})
        fig.update_traces(textinfo="label+percent", hovertemplate="%{label}<br>%{value:,} deals<extra></extra>")
        st.plotly_chart(_chart_layout(fig), use_container_width=True, config={"displayModeBar": False})
    with right:
        by_region = viz["region_label"].value_counts().rename_axis("Região").reset_index(name="Deals")
        fig = px.bar(by_region, x="Deals", y="Região", orientation="h", color_discrete_sequence=[COLORS["blue"]])
        fig.update_traces(hovertemplate="%{y}<br>%{x:,} deals<extra></extra>")
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(_chart_layout(fig), use_container_width=True, config={"displayModeBar": False})

    left, right = st.columns(2)
    with left:
        manager_counts = viz["manager_label"].value_counts().head(10).rename_axis("Manager").reset_index(name="Deals")
        fig = px.bar(manager_counts, x="Deals", y="Manager", orientation="h", color_discrete_sequence=[COLORS["teal"]])
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(_chart_layout(fig), use_container_width=True, config={"displayModeBar": False})
    with right:
        product_counts = viz["product"].value_counts().head(7).rename_axis("Produto").reset_index(name="Deals")
        fig = px.bar(product_counts, x="Produto", y="Deals", color_discrete_sequence=[COLORS["amber"]])
        st.plotly_chart(_chart_layout(fig), use_container_width=True, config={"displayModeBar": False})
    st.info("O score é uma prioridade heurística aprovada por estágio. Ele não é probabilidade de fechamento, nem previsão de receita.")


def _friendly_table(frame: pd.DataFrame) -> pd.DataFrame:
    table = frame.copy()
    table["Faixa"] = table["priority_score"].map(_priority_label)
    table["account"] = table["account"].map(_display_account)
    table["sales_price"] = table["sales_price"].map(_display_price)
    return table.rename(
        columns={
            "rank": "Posição global",
            "opportunity_id": "Oportunidade",
            "account": "Conta",
            "sales_agent": "Vendedor",
            "deal_stage": "Estágio",
            "product": "Produto",
            "priority_score": "Score",
            "sales_price": "Preço de referência",
        }
    )


def _export_selection(filtered: pd.DataFrame) -> bytes:
    export_columns = ["rank", "opportunity_id", "priority_score", "deal_stage", "account", "sales_agent", "manager", "regional_office", "product", "sales_price", "warnings"]
    export = filtered[export_columns].copy()
    export["warnings"] = export["warnings"].map(json.dumps)
    return export.to_csv(index=False).encode("utf-8-sig")


def _render_queue(filtered: pd.DataFrame) -> None:
    st.markdown("#### Fila para ação")
    controls, export = st.columns([2, 1])
    with controls:
        show_all = st.checkbox("Mostrar todas as oportunidades", value=False)
    with export:
        st.download_button("Baixar seleção em CSV", _export_selection(filtered), "leadscore-selecao.csv", "text/csv", use_container_width=True)
    visible = filtered if show_all else filtered.head(100)
    if not show_all and len(filtered) > 100:
        st.caption("Exibindo as 100 primeiras posições globais. O ranking não é recalculado após os filtros.")
    table = _friendly_table(visible)
    st.dataframe(
        table[["Posição global", "Oportunidade", "Faixa", "Conta", "Vendedor", "Estágio", "Produto", "Score", "Preço de referência"]],
        hide_index=True,
        use_container_width=True,
        height=540,
        column_config={"Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d")},
    )


def _render_detail(filtered: pd.DataFrame) -> None:
    st.markdown("#### Ficha da oportunidade")
    options = filtered["opportunity_id"].astype(str).tolist()
    selected_id = st.selectbox("Selecione uma oportunidade para entender sua posição", options)
    detail = filtered.loc[filtered["opportunity_id"].astype(str).eq(selected_id)].iloc[0]
    left, right = st.columns([1, 1.5])
    with left:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=int(detail["priority_score"]),
            number={"suffix": " / 100", "font": {"color": COLORS["navy"]}},
            title={"text": _priority_label(detail["priority_score"]), "font": {"color": COLORS["navy"]}},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": COLORS["teal"] if detail["priority_score"] >= 70 else COLORS["amber"]}, "bgcolor": "#E6EDF5", "steps": [{"range": [0, 40], "color": "#F7FAFC"}, {"range": [40, 70], "color": "#FFF7E0"}]},
        ))
        st.plotly_chart(_chart_layout(gauge, height=300), use_container_width=True, config={"displayModeBar": False})
    with right:
        st.markdown(f"### {selected_id}")
        st.caption(f"Posição global #{int(detail['rank'])} · {detail['deal_stage']} · {_display_price(detail['sales_price'])}")
        a, b = st.columns(2)
        a.write(f"**Conta**  \n{_display_account(detail['account'])}")
        b.write(f"**Produto**  \n{_display_label(detail['product'])}")
        a.write(f"**Vendedor**  \n{_display_label(detail['sales_agent'])}")
        b.write(f"**Manager / Região**  \n{_display_label(detail['manager'])} · {_display_label(detail['regional_office'])}")
        st.markdown("**Como o score foi composto**")
        for factor in detail["score_factors"]:
            st.write(f"`+{factor['contribution']}` **{factor['name']}** — {factor['reason']}")
        if detail["warnings"]:
            st.warning("Avisos: " + "; ".join(detail["warnings"]))
        else:
            st.success("Nenhum aviso de qualidade para esta oportunidade.")
        st.caption(f"Política {detail['policy_version']} · Referência demonstrativa: {detail['reference_date']}")


def _render_data_quality(filtered: pd.DataFrame) -> None:
    st.markdown("#### Qualidade e cobertura dos dados")
    fields = pd.DataFrame(
        {
            "Campo": ["Conta", "Data de engajamento", "Preço de catálogo", "Manager", "Região"],
            "Preenchidos": [
                filtered["account"].notna().sum(), filtered["engage_date"].notna().sum(), filtered["sales_price"].notna().sum(), filtered["manager"].notna().sum(), filtered["regional_office"].notna().sum(),
            ],
        }
    )
    fields["Cobertura"] = fields["Preenchidos"] / len(filtered)
    fig = px.bar(fields, x="Campo", y="Cobertura", text=fields["Cobertura"].map("{:.0%}".format), range_y=[0, 1], color_discrete_sequence=[COLORS["blue"]])
    fig.update_traces(textposition="outside", hovertemplate="%{x}<br>Cobertura: %{y:.0%}<extra></extra>")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(_chart_layout(fig, height=330), use_container_width=True, config={"displayModeBar": False})
    st.caption("Ausências são preservadas e sinalizadas; não são preenchidas artificialmente nem reduzem o score por si só.")


def main() -> None:
    _inject_style()
    st.markdown("""<div class="hero"><div class="eyebrow">RevOps · priorização de carteira</div><h1>🎯 Lead Scorer</h1><p>Uma visão operacional para encontrar as oportunidades abertas que merecem atenção primeiro.</p></div>""", unsafe_allow_html=True)
    try:
        queue = build_queue()
        filtered = _render_sidebar(queue)
    except Exception as error:  # pragma: no cover - estado exibido pelo Streamlit
        st.error(f"Não foi possível carregar a fila: {error}")
        st.stop()

    _render_kpis(queue, filtered)
    st.caption("Demonstração offline com dados históricos reais · referência: 31/12/2017 · filtros não recalculam o score.")
    if filtered.empty:
        st.warning("Nenhuma oportunidade corresponde aos filtros selecionados. Ajuste ou limpe os filtros na lateral.")
        return

    overview, queue_tab, detail, quality = st.tabs(["Visão executiva", "Fila priorizada", "Detalhe do deal", "Qualidade dos dados"])
    with overview:
        _render_overview(filtered)
    with queue_tab:
        _render_queue(filtered)
    with detail:
        _render_detail(filtered)
    with quality:
        _render_data_quality(filtered)

    with st.expander("Como interpretar este dashboard"):
        st.markdown(
            "- **Score:** índice heurístico de prioridade, não percentual de chance de fechamento.\n"
            "- **Estágio:** única regra comercial ponderada na política aprovada.\n"
            "- **Preço de referência:** preço de catálogo, exibido como contexto e usado apenas no desempate estável; não é receita esperada.\n"
            "- **Dados ausentes:** permanecem visíveis como avisos para a revisão humana."
        )


if __name__ == "__main__":
    main()
