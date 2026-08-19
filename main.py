import streamlit as st
import pandas as pd
import io

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

# Inicializar Historial en la sesión si no existe
if "historial_apuestas" not in st.session_state:
    st.session_state["historial_apuestas"] = []

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
            <p style="color: #A32A2A; margin: 5px 0 0 0;">Generador Dinámico, Simulador Escenario por Escenario y Exportador Excel</p>
        </div>
        """,
        unsafe_allow_html=True
    )

tab1, tab2 = st.tabs(["🎯 Generador & Simulador", "📋 Historial & Exportación Excel"])

with tab1:
    st.header("1. Ingreso de Datos (3 Partidos / 6 Equipos y Cuotas)")

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
            
            # Algoritmo de recomendación
            prob1, probX, prob2 = 1/c1, 1/cX, 1/c2
            total_prob = prob1 + probX + prob2
            p1_real, pX_real, p2_real = (prob1/total_prob)*100, (probX/total_prob)*100, (prob2/total_prob)*100
            
            if c1 <= c2 and c1 <= cX:
                base_sugerida = f"1 ({p_local})"
                cuota_base = c1
            elif c2 <= c1 and c2 <= cX:
                base_sugerida = f"2 ({p_visitante})"
                cuota_base = c2
            else:
                base_sugerida = "X (Empate)"
                cuota_base = cX

            st.markdown(
                f"""
                <div style="background-color: #E8F5E9; border-radius: 8px; padding: 8px; margin-top: 10px; border: 1px solid #A5D6A7;">
                    <p style="margin:0; color:#2E7D32; font-weight:bold; font-size:13px;">🤖 Recomendación Base:</p>
                    <p style="margin:0; font-size:13px;"><b>{base_sugerida}</b> @ {cuota_base:.2f}</p>
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
    # BOLETOS 8 Y 9
    # ---------------------------------------------------------
    st.header("2. Boletos Libres (8 y 9)")
    auto_pilot = st.checkbox("🤖 Auto-Piloto IA para Boletos 8 y 9", value=True)
    
    opciones_p1 = [f"1 ({partidos[0]['local']})", "X (Empate)", f"2 ({partidos[0]['visitante']})"]
    opciones_p2 = [f"1 ({partidos[1]['local']})", "X (Empate)", f"2 ({partidos[1]['visitante']})"]
    opciones_p3 = [f"1 ({partidos[2]['local']})", "X (Empate)", f"2 ({partidos[2]['visitante']})"]

    if auto_pilot:
        b8_p1, b8_p2, b8_p3 = "X (Empate)", "X (Empate)", partidos[2]["opcion_base"]
        def op_sorpresa(p): return f"2 ({p['visitante']})" if "1" in p["opcion_base"] else f"1 ({p['local']})"
        b9_p1, b9_p2, b9_p3 = op_sorpresa(partidos[0]), op_sorpresa(partidos[1]), op_sorpresa(partidos[2])
    else:
        col_b8, col_b9 = st.columns(2)
        with col_b8:
            b8_p1 = st.selectbox("P1 (Boleto 8)", opciones_p1, index=1, key="b8_p1")
            b8_p2 = st.selectbox("P2 (Boleto 8)", opciones_p2, index=1, key="b8_p2")
            b8_p3 = st.selectbox("P3 (Boleto 8)", opciones_p3, index=0, key="b8_p3")
        with col_b9:
            b9_p1 = st.selectbox("P1 (Boleto 9)", opciones_p1, index=2, key="b9_p1")
            b9_p2 = st.selectbox("P2 (Boleto 9)", opciones_p2, index=2, key="b9_p2")
            b9_p3 = st.selectbox("P3 (Boleto 9)", opciones_p3, index=2, key="b9_p3")

    # STAKE
    st.header("3. Configuración del Stake")
    monto_por_boleto = st.number_input("Monto por Boleto (€)", min_value=1.0, value=10.0, step=1.0)
    stake_unidad = monto_por_boleto / 4.0
    inversion_total = monto_por_boleto * 9

    st.success(f"💡 Inversión Total (9 Boletos): *{inversion_total:.2f}€* ({stake_unidad:.2f}€ por apuesta individual)")

    # GENERAR MATRIZ
    if st.button("🚀 Calcular Matriz Completa y Simulador", use_container_width=True):
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
                "ID": num,
                "Boleto": f"Boleto {num}",
                "Estrategia": tipo,
                f"{partidos[0]['vs']}": f"{sel1} ({c1:.2f})",
                f"{partidos[1]['vs']}": f"{sel2} ({c2:.2f})",
                f"{partidos[2]['vs']}": f"{sel3} ({c3:.2f})",
                "Cobro 3 Dobles (€)": round(pago_dobles, 2),
                "Cobro Trixie Completo (€)": round(pago_trixie, 2),
                "c1": c1, "c2": c2, "c3": c3,
                "sel1": sel1, "sel2": sel2, "sel3": sel3
            })

        op_b1, op_b2, op_b3 = partidos[0]["opcion_base"], partidos[1]["opcion_base"], partidos[2]["opcion_base"]
        def inv_op(p): return f"2 ({p['visitante']})" if "1" in p["opcion_base"] else f"1 ({p['local']})"

        agregar_boleto(1, "🔥 BASE PRINCIPAL", op_b1, op_b2, op_b3)
        agregar_boleto(2, "🛡️ Cobertura Empate P1", "X (Empate)", op_b2, op_b3)
        agregar_boleto(3, "🛡️ Cobertura Empate P2", op_b1, "X (Empate)", op_b3)
        agregar_boleto(4, "🛡️ Cobertura Empate P3", op_b1, op_b2, "X (Empate)")
        agregar_boleto(5, "⚡ Cobertura Sorpresa P1", inv_op(partidos[0]), op_b2, op_b3)
        agregar_boleto(6, "⚡ Cobertura Sorpresa P2", op_b1, inv_op(partidos[1]), op_b3)
        agregar_boleto(7, "⚡ Cobertura Sorpresa P3", op_b1, op_b2, inv_op(partidos[2]))
        agregar_boleto(8, "🎯 Cierre Libre 1", b8_p1, b8_p2, b8_p3)
        agregar_boleto(9, "🚀 Cierre Libre 2", b9_p1, b9_p2, b9_p3)

        st.session_state["matriz_actual"] = boletos_data
        st.session_state["inversion_actual"] = inversion_total
        st.session_state["partidos_actuales"] = partidos

    # SI YA EXISTE UNA MATRIZ GENERADA
    if "matriz_actual" in st.session_state:
        df_matriz = pd.DataFrame(st.session_state["matriz_actual"])
        
        st.header("📋 Matriz de 9 Boletos Generada")
        st.dataframe(df_matriz.drop(columns=["c1", "c2", "c3", "sel1", "sel2", "sel3", "ID"]), use_container_width=True)

        # ---------------------------------------------------------
        # SIMULADOR DE CUALQUIER BOLETO GANADOR
        # ---------------------------------------------------------
        st.markdown("---")
        st.header("🔮 Simulador de Cobros según qué Boleto gane")
        st.markdown("Elige cuál boleto acierta los 3 partidos enteros para ver el *Cobro Total Real* sumando ese Trixie completo + las Dobles de rescate de los otros boletos:")

        boleto_ganador_id = st.selectbox(
            "Selecciona el Boleto Ganador a Simular:",
            options=[b["ID"] for b in st.session_state["matriz_actual"]],
            format_func=lambda x: f"Boleto {x} ({st.session_state['matriz_actual'][x-1]['Estrategia']})"
        )

        # Cálculo del escenario elegido
        b_ganador = st.session_state["matriz_actual"][boleto_ganador_id - 1]
        c1_g, c2_g, c3_g = b_ganador["c1"], b_ganador["c2"], b_ganador["c3"]
        
        # Cobro del boleto ganador en Trixie completo
        cobro_trixie_ganador = (c1_g*c2_g + c1_g*c3_g + c2_g*c3_g + c1_g*c2_g*c3_g) * stake_unidad

        # Suma de dobles en los demás boletos que compartan 2 aciertos
        suma_dobles_otros = 0.0
        for b in st.session_state["matriz_actual"]:
            if b["ID"] != boleto_ganador_id:
                # Comprobar cuántos partidos coinciden
                m1 = (b["sel1"] == b_ganador["sel1"])
                m2 = (b["sel2"] == b_ganador["sel2"])
                m3 = (b["sel3"] == b_ganador["sel3"])
                
                if m1 and m2: suma_dobles_otros += (b["c1"] * b["c2"]) * stake_unidad
                if m1 and m3: suma_dobles_otros += (b["c1"] * b["c3"]) * stake_unidad
                if m2 and m3: suma_dobles_otros += (b["c2"] * b["c3"]) * stake_unidad

        cobro_total_simulado = cobro_trixie_ganador + suma_dobles_otros
        neto_simulado = cobro_total_simulado - st.session_state["inversion_actual"]

        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric(f"Cobro Trixie (Boleto {boleto_ganador_id})", f"{cobro_trixie_ganador:.2f}€")
        col_s2.metric("Suma Dobles de Rescate (Otros Boletos)", f"{suma_dobles_otros:.2f}€")
        col_s3.metric("🔥 TOTAL RECAUDADO", f"{cobro_total_simulado:.2f}€", delta=f"{neto_simulado:+.2f}€ Neto")

        # BOTÓN PARA GUARDAR EN EL HISTORIAL
        st.markdown("---")
        st.subheader("💾 Guardar esta Jornada en tu Historial")
        col_g1, col_g2, col_g3 = st.columns(3)
        
        with col_g1:
            nombre_jornada = st.text_input("Nombre / Fecha de la Jornada", value="Jornada 1")
        with col_g2:
            resultado_final = st.selectbox("Resultado de la Apuesta", ["Ganada (Victoria)", "Perdida", "Recuperación Parcial"])
        with col_g3:
            monto_cobrado_real = st.number_input("Monto Real Cobrado (€)", value=float(round(cobro_total_simulado, 2)))

        if st.button("📌 Guardar en Historial"):
            st.session_state["historial_apuestas"].append({
                "Jornada": nombre_jornada,
                "Inversión (€)": st.session_state["inversion_actual"],
                "Cobrado (€)": monto_cobrado_real,
                "Beneficio (€)": round(monto_cobrado_real - st.session_state["inversion_actual"], 2),
                "Estado": resultado_final,
                "Detalles": st.session_state["matriz_actual"]
            })
            st.success("¡Jornada guardada correctamente en el historial!")

# ---------------------------------------------------------
# PESTAÑA 2: HISTORIAL Y EXPORTACIÓN A EXCEL
# ---------------------------------------------------------
with tab2:
    st.header("📋 Historial Unificado y Registro de Apuestas")

    if len(st.session_state["historial_apuestas"]) == 0:
        st.info("Aún no has guardado ninguna jornada. Genera una matriz en la Pestaña 1 y haz clic en 'Guardar en Historial'.")
    else:
        df_historial = pd.DataFrame(st.session_state["historial_apuestas"]).drop(columns=["Detalles"])

        # Aplicar formato visual con colores al Historial
        def colorear_estado(val):
            if "Victoria" in str(val) or "Ganada" in str(val):
                return 'background-color: #C8E6C9; color: #2E7D32; font-weight: bold;'
            elif "Perdida" in str(val):
                return 'background-color: #FFCDD2; color: #C62828; font-weight: bold;'
            else:
                return 'background-color: #FFF9C4; color: #F57F17; font-weight: bold;'

        st.dataframe(df_historial.style.applymap(colorear_estado, subset=["Estado"]), use_container_width=True)

        st.subheader("📥 Exportar Matriz Actual o Historial a Excel")

        # Crear archivo Excel dinámico en memoria
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Hoja 1: Resumen de Historial
            df_historial.to_excel(writer, sheet_name='Historial Global', index=False)
            
            # Hoja 2: Matriz Actual Detallada (Equipos, Cuotas, Dobles y Trixie)
            if "matriz_actual" in st.session_state:
                df_mat = pd.DataFrame(st.session_state["matriz_actual"]).drop(columns=["c1", "c2", "c3", "sel1", "sel2", "sel3"])
                df_mat.to_excel(writer, sheet_name='Matriz_Detallada_Boletos', index=False)

        st.download_button(
            label="📊 Descargar Excel Completo con Formato",
            data=buffer.getvalue(),
            file_name="Strike_Analytics_Historial_Apuestas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
