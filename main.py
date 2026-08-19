import streamlit as st
import itertools
import pandas as pd
import json
import os
from datetime import datetime
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# --- ARCHIVOS DE CONTROL LOCAL ---
HISTORIAL_JSON = "historial_apuestas.json"
EXCEL_MASTER_FILE = "Historial_Apuestas_Master.xlsx"

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="STRIKE ANALYTICS | Predictor Pro 9 Boletos",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    /* Fondo General: Verde claro suave */
    .stApp {
        background-color: #DCEEE1;
        color: #2D3748;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Principal: Fondo Rojo Pastel Suave */
    .pastel-header {
        background: linear-gradient(135deg, #FFF5F5 0%, #FED7D7 100%);
        padding: 22px 30px;
        border-radius: 20px;
        border: 1px solid #FEB2B2;
        box-shadow: 0 4px 15px rgba(229, 115, 115, 0.12);
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .header-content {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    /* Mascota Bot Conejo Redondo con Tono Coral/Rojo Suave */
    .bunny-bot-avatar {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #E57373 0%, #EF5350 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(239, 83, 80, 0.3);
        animation: floatWave 3s infinite ease-in-out;
    }

    @keyframes floatWave {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-3px) rotate(5deg); }
        75% { transform: translateY(3px) rotate(-5deg); }
    }

    .pastel-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        color: #9B2C2C !important;
    }
    
    .pastel-header p {
        margin: 4px 0 0 0;
        font-size: 1rem;
        color: #742A2A;
    }
    
    /* Tarjetas de Contenedores Blancas y Limpias */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div {
        background-color: #FFFFFF;
        border-radius: 14px;
        border: 1px solid #C8E6C9;
        box-shadow: 0 3px 10px rgba(0,0,0,0.03);
    }
    
    /* Botones Rojo Pastel Elegante */
    .stButton > button {
        background: linear-gradient(135deg, #E57373 0%, #EF5350 100%);
        color: #FFFFFF !important;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 0.98rem;
        transition: all 0.25s ease;
        box-shadow: 0 3px 10px rgba(239, 83, 80, 0.25);
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #EF5350 0%, #E53935 100%);
        box-shadow: 0 5px 15px rgba(239, 83, 80, 0.4);
        transform: translateY(-1px);
    }
    
    /* Botón Descargar Verde Menta */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #66BB6A 0%, #4CAF50 100%);
        color: #FFFFFF !important;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        box-shadow: 0 3px 10px rgba(76, 175, 80, 0.25);
        width: 100%;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
        transform: translateY(-1px);
    }

    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #C8E6C9;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px;
        color: #1B5E20;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #9B2C2C !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# --- CABECERA EN ROJO PASTEL CON BOT-CONEJO ---
st.markdown("""
<div class="pastel-header">
    <div class="header-content">
        <div class="bunny-bot-avatar">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M8 9V3a1.5 1.5 0 0 1 3 0v6"></path>
                <path d="M13 9V3a1.5 1.5 0 0 1 3 0v6"></path>
                <circle cx="12" cy="14" r="6"></circle>
                <circle cx="10" cy="13" r="0.75" fill="white"></circle>
                <circle cx="14" cy="13" r="0.75" fill="white"></circle>
                <path d="M10.5 16c.8.5 2.2.5 3 0"></path>
                <line x1="12" y1="8" x2="12" y2="7"></line>
            </svg>
        </div>
        <div>
            <h1>¡Hola! Strike Analytics Pro 👋</h1>
            <p>Generador Dinámico de 9 Boletos Tácticos</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- MANEJO DE HISTORIAL Y EXCEL UNIFICADO ---
def cargar_historial():
    if os.path.exists(HISTORIAL_JSON):
        try:
            with open(HISTORIAL_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_historial(historial):
    with open(HISTORIAL_JSON, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)

def guardar_en_excel_master(df_boletos, num_jornada, fecha_str, partidos_info):
    if not os.path.exists(EXCEL_MASTER_FILE):
        wb = Workbook()
        ws = wb.active
        ws.title = "Historial Acumulado"
    else:
        wb = load_workbook(EXCEL_MASTER_FILE)
        ws = wb["Historial Acumulado"]

    fill_banner = PatternFill(start_color="C53030", end_color="C53030", fill_type="solid")
    font_banner = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    fill_header = PatternFill(start_color="2D3748", end_color="2D3748", fill_type="solid")
    font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    
    fill_even = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")
    fill_odd = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    border_thin = Side(border_style="thin", color="E2E8F0")
    cell_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

    start_row = ws.max_row + 2 if ws.max_row > 1 else 1

    ws.merge_cells(start_row=start_row, start_column=1, end_row=start_row, end_column=9)
    cell_b = ws.cell(row=start_row, column=1)
    p_summary = f"P1: {partidos_info[0]['local']} vs {partidos_info[0]['visitante']} | P2: {partidos_info[1]['local']} vs {partidos_info[1]['visitante']} | P3: {partidos_info[2]['local']} vs {partidos_info[2]['visitante']}"
    cell_b.value = f"📌 JORNADA #{num_jornada} [{fecha_str}] — {p_summary}"
    cell_b.fill = fill_banner
    cell_b.font = font_banner
    cell_b.alignment = Alignment(horizontal="left", vertical="center")

    headers = list(df_boletos.columns)
    header_row = start_row + 1
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=header_row, column=col_idx, value=h)
        cell.fill = fill_header
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center", vertical="center")

    data_start = header_row + 1
    for r_idx, row in enumerate(df_boletos.itertuples(index=False), start=data_start):
        row_fill = fill_even if r_idx % 2 == 0 else fill_odd
        for c_idx, val in enumerate(row, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.fill = row_fill
            cell.border = cell_border
            cell.alignment = Alignment(horizontal="center", vertical="center")

    ws.views.sheetView[0].showGridLines = True
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            if cell.value is not None:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max(max_len + 3, 14)

    wb.save(EXCEL_MASTER_FILE)

# --- PESTAÑAS DE LA APLICACIÓN ---
tab_gen, tab_hist, tab_stats = st.tabs(["🎯 Generador de Jornada", "📋 Historial Unificado", "📈 Métricas & ROI"])

# ==========================================
# PESTAÑA 1: GENERADOR
# ==========================================
with tab_gen:
    st.markdown("##### 1. Configura tus Partidos y Cuotas")
    
    partidos_defecto = [
        {"local": "Equipo A", "visitante": "Equipo B", "c1": 2.45, "cx": 3.20, "c2": 2.80},
        {"local": "Equipo C", "visitante": "Equipo D", "c1": 3.40, "cx": 3.00, "c2": 2.55},
        {"local": "Equipo E", "visitante": "Equipo F", "c1": 2.35, "cx": 3.10, "c2": 2.95}
    ]

    cols = st.columns(3)
    partidos_analizados = []

    for i, p in enumerate(partidos_defecto):
        with cols[i]:
            st.markdown(f"*⚽ Partido {i+1}*")
            nom_loc = st.text_input(f"Local P{i+1}", value=p["local"], key=f"loc_{i}")
            nom_vis = st.text_input(f"Visitante P{i+1}", value=p["visitante"], key=f"vis_{i}")
            
            c1 = st.number_input(f"Cuota 1 ({nom_loc})", min_value=1.01, value=p["c1"], step=0.05, key=f"c1_{i}")
            cx = st.number_input(f"Cuota X (Empate)", min_value=1.01, value=p["cx"], step=0.05, key=f"cx_{i}")
            c2 = st.number_input(f"Cuota 2 ({nom_vis})", min_value=1.01, value=p["c2"], step=0.05, key=f"c2_{i}")
            
            opciones_cuotas = {"1": c1, "X": cx, "2": c2}
            validas = {k: v for k, v in opciones_cuotas.items() if v >= 2.30}
            
            if len(validas) > 0:
                base_auto = max(validas, key=validas.get)
                cuota_val = validas[base_auto]
            else:
                base_auto = max(opciones_cuotas, key=opciones_cuotas.get)
                cuota_val = opciones_cuotas[base_auto]
                st.caption("⚠️ Ninguna cuota supera 2.30")

            st.info(f"🎯 *Base Automática:* Signo {base_auto} (Cuota: {cuota_val:.2f})")

            partidos_analizados.append({
                "local": nom_loc, "visitante": nom_vis,
                "c1": c1, "cx": cx, "c2": c2,
                "base_sel": base_auto
            })

    st.markdown("---")
    st.markdown("##### 2. Asignación de Presupuesto")

    c_p1, c_p2 = st.columns(2)
    with c_p1:
        presupuesto = st.number_input("Presupuesto Total de la Jornada (€):", min_value=10.0, value=100.0, step=10.0)
    with c_p2:
        pct_base = st.slider("Porcentaje para Apuesta Base (%)", 20, 60, 36) / 100.0

    top_base = (partidos_analizados[0]["base_sel"], partidos_analizados[1]["base_sel"], partidos_analizados[2]["base_sel"])

    def obtener_cuotas_indiv(comb):
        c_list = []
        c_tot = 1.0
        for idx, res in enumerate(comb):
            p = partidos_analizados[idx]
            val = p["c1"] if res == "1" else (p["cx"] if res == "X" else p["c2"])
            c_list.append(val)
            c_tot *= val
        return c_list, round(c_tot, 2)

    boletos_generados = [{"comb": top_base, "tipo": "APUESTA BASE"}]
    opciones = ["1", "X", "2"]
    todas_comb = list(itertools.product(opciones, repeat=3))
    coberturas_1_fallo = [comb for comb in todas_comb if sum(1 for a, b in zip(top_base, comb) if a != b) == 1]

    for idx, cob in enumerate(coberturas_1_fallo):
        boletos_generados.append({"comb": cob, "tipo": f"COBERTURA {idx+1}"})

    boletos_generados.append({"comb": ("1", "X", "1"), "tipo": "EXTRA 1 (Fallo Doble)"})
    boletos_generados.append({"comb": ("X", "X", "X"), "tipo": "EXTRA 2 (Triple Empate)"})

    monto_base = round(presupuesto * pct_base, 2)
    num_coberturas = len(boletos_generados) - 1
    monto_cobertura = round((presupuesto * (1 - pct_base)) / num_coberturas, 2)

    boletos_finales = []
    p1_str = f"{partidos_analizados[0]['local']} vs {partidos_analizados[0]['visitante']}"
    p2_str = f"{partidos_analizados[1]['local']} vs {partidos_analizados[1]['visitante']}"
    p3_str = f"{partidos_analizados[2]['local']} vs {partidos_analizados[2]['visitante']}"

    for idx, b in enumerate(boletos_generados):
        monto = monto_base if idx == 0 else monto_cobertura
        c_indiv, c_tot = obtener_cuotas_indiv(b["comb"])
        retorno = round(monto * c_tot, 2)

        boletos_finales.append({
            "Boleto #": idx + 1,
            "Tipo": b["tipo"],
            f"P1: {p1_str}": f"{b['comb'][0]} ({c_indiv[0]})",
            f"P2: {p2_str}": f"{b['comb'][1]} ({c_indiv[1]})",
            f"P3: {p3_str}": f"{b['comb'][2]} ({c_indiv[2]})",
            "Cuota Total": c_tot,
            "Inversión (€)": monto,
            "Retorno (€)": retorno,
            "Beneficio (€)": round(retorno - presupuesto, 2)
        })

    df_boletos = pd.DataFrame(boletos_finales)
    
    st.markdown("##### 📋 Matriz Resultante de 9 Boletos")
    st.dataframe(df_boletos, use_container_width=True)

    st.markdown("---")
    btn_c1, btn_c2 = st.columns(2)
    
    with btn_c1:
        if st.button("➕ Registrar e Incrementar en Excel Master"):
            historial = cargar_historial()
            num_j = len(historial) + 1
            f_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            nueva_j = {
                "id": num_j, "fecha": f_str, "inversion_total": presupuesto,
                "boletos": boletos_finales, "estado": "Pendiente", "retorno_real": 0.0
            }
            historial.append(nueva_j)
            guardar_historial(historial)
            
            guardar_en_excel_master(df_boletos, num_j, f_str, partidos_analizados)
            st.success(f"¡Jornada #{num_j} añadida al Excel Master unificado!")

    with btn_c2:
        if os.path.exists(EXCEL_MASTER_FILE):
            with open(EXCEL_MASTER_FILE, "rb") as f:
                st.download_button(
                    label="📥 Descargar Libro de Excel Unificado (.xlsx)",
                    data=f,
                    file_name=EXCEL_MASTER_FILE,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# ==========================================
# PESTAÑA 2: HISTORIAL UNIFICADO
# ==========================================
with tab_hist:
    st.markdown("##### 📋 Histórico de Jornadas")
    historial = cargar_historial()
    
    if not historial:
        st.info("Aún no has registrado jornadas. Agrega una desde el generador.")
    else:
        for j in reversed(historial):
            j_id = j.get("id", 1)
            with st.expander(f"📌 JORNADA #{j_id} [{j.get('fecha')}] — Inversión: {j.get('inversion_total')} € | Estado: {j.get('estado')}"):
                df_j = pd.DataFrame(j["boletos"])
                st.dataframe(df_j, use_container_width=True)
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    nuevo_est = st.selectbox("Resultado:", ["Pendiente", "Ganada 🟢", "Perdida 🔴"], index=["Pendiente", "Ganada 🟢", "Perdida 🔴"].index(j.get("estado", "Pendiente")), key=f"est_sel_{j_id}")
                with col_e2:
                    monto_ganado = st.number_input("Cobro Efectivo Real (€):", value=float(j.get("retorno_real", 0.0)), key=f"monto_in_{j_id}")
                
                if st.button(f"Guardar Cambios J#{j_id}", key=f"save_btn_{j_id}"):
                    j["estado"] = nuevo_est
                    j["retorno_real"] = monto_ganado if nuevo_est == "Ganada 🟢" else 0.0
                    guardar_historial(historial)
                    st.rerun()

# ==========================================
# PESTAÑA 3: MÉTRICAS & ROI
# ==========================================
with tab_stats:
    st.markdown("##### 📈 Rendimiento Financiero")
    historial = cargar_historial()
    
    if historial:
        total_inv = sum(float(j.get("inversion_total", 0.0)) for j in historial)
        total_ret = sum(float(j.get("retorno_real", 0.0)) for j in historial if j.get("estado") == "Ganada 🟢")
        bal = total_ret - total_inv
        roi = ((bal / total_inv) * 100) if total_inv > 0 else 0.0

        m1, m2, m3 = st.columns(3)
        m1.metric("Capital Invertido Total", f"{total_inv:.2f} €")
        m2.metric("Balance Neto Real", f"{bal:.2f} €", delta=f"{bal:.2f} €")
        m3.metric("ROI Rendimiento %", f"{roi:.2f}%", delta=f"{roi:.2f}%")
    else:
        st.write("Sin datos guardados aún.")