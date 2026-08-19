import streamlit as st
import pandas as pd

# Configuración de página con la estética de Strike Analytics Pro
st.set_page_config(page_title="Strike Analytics Pro", page_icon="🐰", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #E6F3EA;
}
.stMetric {
    background-color: white;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENCABEZADO VISUAL
# ---------------------------------------------------------
col_head1, col_head2 = st.columns([1, 4])

with col_head1:
    st.markdown(
        """
        <div style="text-align: center; background-color: white; border-radius: 50%; padding: 15px; width: 100px; height: 100px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: auto;">
            <span style="font-size: 60px;">🐰</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_head2:
    st.markdown(
        """
        <div style="background-color: white; border-radius: 15px; padding: 15px; border: 1px solid #FFEBEB;">
            <h1 style="color: #A32A2A; margin: 0; font-size: 32px;">Strike Analytics Pro 👋</h1>
            <p style="color: #A32A2A; margin: 5px 0 0 0;">Motor Algorítmico de Optimización Dinámica y Generación de Boletos</p>
        </div>
        """,
        unsafe_allow_html=True
    )

tab1, tab2 = st.tabs(["🎯 Cerebro Analítico & Generador", "📋 Historial Unificado"])

with tab1:
    st.header("1. Ingreso de Datos (3 Partidos / 6 Equipos y Cuotas)")
    st.markdown("Ingresa los partidos y cuotas. *El algoritmo analizará el mercado y construirá la combinación óptima por sí solo.*")

    col1, col2, col3 = st.columns(3)
    partidos = []

    for idx, col in enumerate([col1, col2, col3], start=1):
        with col:
            st.markdown(
                f"""
                <div style="background-color: #F3F9F6; border-radius: 10px; padding: 10px; border: 1px solid #C4E2D5;">
                    <h3 style="margin: 0;">⚽ Partido {idx}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            p_local = st.text_input(f"Local P{idx}", value=f"Local {idx}", key=f"p_loc_{idx}")
            p_visitante = st.text_input(f"Visitante P{idx}", value=f"Visitante {idx}", key=f"p_vis_{idx}")
            
            c1 = st.number_input(f"Cuota 1 ({p_local})", min_value=1.01, value=2.10, step=0.05, key=f"c1_{idx}")
            cX = st.number_input(f"Cuota X (Empate)", min_value=1.01, value=3.20, step=0.05, key=f"cX_{idx}")
            c2 = st.number_input(f"Cuota 2 ({p_visitante})", min_value=1.01, value=3.50, step=0.05, key=f"c2_{idx}")
            
            # --- CEREBRO ANALÍTICO: Selección automática por cuotas ---
            prob1, probX, prob2 = 1/c1, 1/cX, 1/c2
            total_prob = prob1 + probX + prob2
            p1_real, pX_real, p2_real = (prob1/total_prob)*100, (probX/total_prob)*100, (prob2/total_prob)*100
            
            if c1 <= c2 and c1 <= cX:
                base_sugerida = f"1 ({p_local})"
                cuota_base = c1
                prob_base = p1_real
            elif c2 <= c1 and c2 <= cX:
                base_sugerida = f"2 ({p_visitante})"
                cuota_base = c2
                prob_base = p2_real
            else:
                base_sugerida = "X (Empate)"
                cuota_base = cX
                prob_base = pX_real

            st.markdown(
                f"""
                <div style="background-color: #E8F5E9; border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px solid #A5D6A7;">
                    <p style="margin:0; color:#2E7D32; font-weight:bold;">🤖 Recomendación Algorítmica:</p>
                    <p style="margin:0; font-size:14px;">Base: <b>{base_sugerida}</b> @ {cuota_base:.2f}</p>
                    <p style="margin:0; font-size:12px; color:#555;">Probabilidad Estimada: <b>{prob_base:.1f}%</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )

            partidos.append({
                "local": p_local, "visitante": p_visitante, "vs": f"{p_local} vs {p_visitante}",
                "c1": c1, "cX": cX, "c2": c2,
                "opcion_base": base_sugerida, "cuota_base": cuota_base,
                "p1_prob": p1_real, "pX_prob": pX_real, "p2_prob": p2_real
            })

    # ---------------------------------------------------------
    # CEREBRO AUTO-PILOTO PARA BOLETOS 8 Y 9
    # ---------------------------------------------------------
    st.header("2. Inteligencia para Boletos Libres (8 y 9)")
    
    auto_pilot = st.checkbox("🤖 Activar Modo Auto-Piloto (Dejar que la IA elija los Boletos 8 y 9 según valor matemático)", value=True)
    
    opciones_p1 = [f"1 ({partidos[0]['local']})", "X (Empate)", f"2 ({partidos[0]['visitante']})"]
    opciones_p2 = [f"1 ({partidos[1]['local']})", "X (Empate)", f"2 ({partidos[1]['visitante']})"]
    opciones_p3 = [f"1 ({partidos[2]['local']})", "X (Empate)", f"2 ({partidos[2]['visitante']})"]

    if auto_pilot:
        # Boleto 8: Cobertura Conservadora (Busca los empates con mayor probabilidad)
        b8_p1 = "X (Empate)" if partidos[0]["pX_prob"] >= 28 else partidos[0]["opcion_base"]
        b8_p2 = "X (Empate)" if partidos[1]["pX_prob"] >= 28 else partidos[1]["opcion_base"]
        b8_p3 = "X (Empate)"
        
        # Boleto 9: Sorpresa de Alto Rendimiento (Multiplica por cuotas altas no reflejadas)
        def op_sorpresa(p): return f"2 ({p['visitante']})" if "1" in p["opcion_base"] else f"1 ({p['local']})"
        b9_p1 = op_sorpresa(partidos[0])
        b9_p2 = op_sorpresa(partidos[1])
        b9_p3 = op_sorpresa(partidos[2])

        st.info("💡 *Auto-Piloto Activo:* La IA ha determinado que el *Boleto 8* debe actuar como Seguro de Empates y el *Boleto 9* como Multiplicador de Alto Impacto.")
    else:
        col_b8, col_b9 = st.columns(2)
        with col_b8:
            st.markdown("*📌 Boleto 8 (Personalizado)*")
            b8_p1 = st.selectbox("P1 (Boleto 8)", opciones_p1, index=1, key="b8_p1")
            b8_p2 = st.selectbox("P2 (Boleto 8)", opciones_p2, index=1, key="b8_p2")
            b8_p3 = st.selectbox("P3 (Boleto 8)", opciones_p3, index=0, key="b8_p3")

        with col_b9:
            st.markdown("*📌 Boleto 9 (Personalizado)*")
            b9_p1 = st.selectbox("P1 (Boleto 9)", opciones_p1, index=2, key="b9_p1")
            b9_p2 = st.selectbox("P2 (Boleto 9)", opciones_p2, index=2, key="b9_p2")
            b9_p3 = st.selectbox("P3 (Boleto 9)", opciones_p3, index=2, key="b9_p3")

    # ---------------------------------------------------------
    # CONFIGURACIÓN DEL STAKE
    # ---------------------------------------------------------
    st.header("3. Configuración del Stake")
    monto_por_boleto = st.number_input("Monto por Boleto (€)", min_value=1.0, value=10.0, step=1.0)
    stake_unidad = monto_por_boleto / 4.0
    inversion_total = monto_por_boleto * 9

    st.success(f"💡 Inversión Total (9 Boletos): *{inversion_total:.2f}€* ({stake_unidad:.2f}€ por combinación dentro del Trixie)")

    # ---------------------------------------------------------
    # PROCESAMIENTO Y EJECUCIÓN
    # ---------------------------------------------------------
    if st.button("🧠 Ejecutar Análisis y Generar Matriz Optimizada", use_container_width=True):
        boletos_data = []

        def obtener_cuota(p_dict, sel_texto):
            if "1" in sel_texto: return p_dict["c1"]
            elif "2" in sel_texto: return p_dict["c2"]
            else: return p_dict["cX"]

        def agregar_boleto(num, tipo, sel1, sel2, sel3):
            c1 = obtener_cuota(partidos[0], sel1)
            c2 = obtener_cuota(partidos[1], sel2)
            c3 = obtener_cuota(partidos[2], sel3)
            
            c_d12, c_d13, c_d23 = c1 * c2, c1 * c3, c2 * c3
            c_triple = c1 * c2 * c3
            
            pago_dobles = (c_d12 + c_d13 + c_d23) * stake_unidad
            pago_trixie = (c_d12 + c_d13 + c_d23 + c_triple) * stake_unidad
            
            boletos_data.append({
                "Boleto": f"Boleto {num}",
                "Estrategia / Tipo": tipo,
                f"{partidos[0]['vs']}": f"{sel1} ({c1:.2f})",
                f"{partidos[1]['vs']}": f"{sel2} ({c2:.2f})",
                f"{partidos[2]['vs']}": f"{sel3} ({c3:.2f})",
                "Cobro 3 Dobles": f"{pago_dobles:.2f}€",
                "Cobro Trixie Completo": f"{pago_trixie:.2f}€"
            })

        op_b1, op_b2, op_b3 = partidos[0]["opcion_base"], partidos[1]["opcion_base"], partidos[2]["opcion_base"]

        # Boletos del Sistema
        agregar_boleto(1, "🔥 BASE OPTIMIZADA", op_b1, op_b2, op_b3)
        agregar_boleto(2, "🛡️ Cobertura Empate P1", "X (Empate)", op_b2, op_b3)
        agregar_boleto(3, "🛡️ Cobertura Empate P2", op_b1, "X (Empate)", op_b3)
        agregar_boleto(4, "🛡️ Cobertura Empate P3", op_b1, op_b2, "X (Empate)")
        
        def inv_op(p): return f"2 ({p['visitante']})" if "1" in p["opcion_base"] else f"1 ({p['local']})"
        agregar_boleto(5, "⚡ Cobertura Sorpresa P1", inv_op(partidos[0]), op_b2, op_b3)
        agregar_boleto(6, "⚡ Cobertura Sorpresa P2", op_b1, inv_op(partidos[1]), op_b3)
        agregar_boleto(7, "⚡ Cobertura Sorpresa P3", op_b1, op_b2, inv_op(partidos[2]))

        agregar_boleto(8, "🎯 Cierre 1 (Empates/Personalizado)", b8_p1, b8_p2, b8_p3)
        agregar_boleto(9, "🚀 Cierre 2 (Sorpresas/Personalizado)", b9_p1, b9_p2, b9_p3)

        # Mostrar Matriz
        st.header("📋 Matriz Resultante Inteligente")
        df_boletos = pd.DataFrame(boletos_data)
        st.dataframe(df_boletos, use_container_width=True)

        # Cálculo de Cobros y Efecto Dominó
        c_b1, c_b2, c_b3 = partidos[0]["cuota_base"], partidos[1]["cuota_base"], partidos[2]["cuota_base"]
        cobro_b1_trixie = (c_b1*c_b2 + c_b1*c_b3 + c_b2*c_b3 + c_b1*c_b2*c_b3) * stake_unidad
        
        suma_dobles_otros = ((c_b2 * c_b3) + (c_b1 * c_b3) + (c_b1 * c_b2) + (c_b2 * c_b3) + (c_b1 * c_b3) + (c_b1 * c_b2)) * stake_unidad
        gran_total_cobro = cobro_b1_trixie + suma_dobles_otros
        beneficio_neto = gran_total_cobro - inversion_total

        st.markdown("---")
        st.header("💰 Evaluación Financiera del Sistema (Si entra la Base Principal)")
        
        c_res1, c_res2, c_res3 = st.columns(3)
        c_res1.metric("Cobro Boleto 1 (Base Entera)", f"{cobro_b1_trixie:.2f}€")
        c_res2.metric("Suma Dobles (Rescate Boletos 2 al 7)", f"{suma_dobles_otros:.2f}€")
        c_res3.metric("🔥 GRAN TOTAL A COBRAR", f"{gran_total_cobro:.2f}€", delta=f"{beneficio_neto:+.2f}€ Neto")

with tab2:
    st.info("Pestaña de Historial Unificado en desarrollo.")
