import streamlit as st
import pandas as pd

# Configuración de página con el tema visual de la captura
st.set_page_config(page_title="Strike Analytics Pro", page_icon="🐰", layout="wide")

# Fondo de color suave para la página (como en la captura)
st.markdown("""
<style>
.stApp {
    background-color: #E6F3EA; /* Color verde muy suave de fondo */
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENCABEZADO VISUAL (Conejo y Título)
# ---------------------------------------------------------
col_head1, col_head2 = st.columns([1, 4])

with col_head1:
    # Logotipo del conejo
    st.markdown(
        """
        <div style="text-align: center; background-color: white; border-radius: 50%; padding: 15px; width: 100px; height: 100px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: auto;">
            <span style="font-size: 60px;">🐰</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_head2:
    # Título y subtítulo con el estilo de color y tamaño
    st.markdown(
        """
        <div style="background-color: white; border-radius: 15px; padding: 15px; border: 1px solid #FFEBEB;">
            <h1 style="color: #A32A2A; margin: 0; font-size: 32px;">¡Hola! Strike Analytics Pro 👋</h1>
            <p style="color: #A32A2A; margin: 5px 0 0 0;">Generador Dinámico de 9 Boletos Tácticos</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# PESTAÑAS (Tabs)
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["🎯 Generador de Jornada", "📋 Historial Unificado"])

# =========================================================
# PESTAÑA 1: GENERADOR DE JORNADA
# =========================================================
with tab1:
    st.header("1. Configura tus Partidos y Cuotas")

    col1, col2, col3 = st.columns(3)
    partidos = []

    # Iterar para crear la interfaz de los 3 partidos
    for idx, col in enumerate([col1, col2, col3], start=1):
        with col:
            # Tarjeta de color suave para cada partido
            st.markdown(
                f"""
                <div style="background-color: #F3F9F6; border-radius: 10px; padding: 15px; border: 1px solid #C4E2D5;">
                    <h3 style="margin: 0; display: flex; align-items: center;">
                        <span style="font-size: 20px; margin-right: 10px;">⚽</span> Partido {idx}
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            p_nombre = st.text_input(f"Nombre del Partido {idx}", value=f"Partido {idx}", key=f"p_nom_{idx}")
            
            # Sub-tarjeta para cuotas
            st.markdown(
                f"""
                <div style="background-color: white; border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px solid #C4E2D5;">
                    <p style="margin: 0; font-weight: bold;">Cuotas Mercado 1X2:</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            c1 = st.number_input(f"Cuota 1 (Local) P{idx}", min_value=1.01, value=2.10, step=0.05, key=f"c1_{idx}")
            cX = st.number_input(f"Cuota X (Empate) P{idx}", min_value=1.01, value=3.20, step=0.05, key=f"cX_{idx}")
            c2 = st.number_input(f"Cuota 2 (Visitante) P{idx}", min_value=1.01, value=3.50, step=0.05, key=f"c2_{idx}")
            
            # Sub-tarjeta para factores cualitativos (Nueva Lógica)
            st.markdown(
                f"""
                <div style="background-color: white; border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px solid #C4E2D5;">
                    <p style="margin: 0; font-weight: bold;">Factores Cualitativos & Estadísticas:</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            bajas = st.selectbox(f"Bajas / Lesiones clave P{idx}", 
                                 ["Sin bajas importantes", "Baja clave en Local (-15% fav)", "Baja clave en Visitante (+15% fav local)"], 
                                 key=f"bajas_{idx}")
            tarjetas = st.selectbox(f"Sanciones / Tarjetas P{idx}", 
                                    ["Normal", "Alta tendencia amarillas/rojas", "Jugadores apercibidos"], 
                                    key=f"tarj_{idx}")
            racha = st.text_input(f"Últimos 5 partidos (ej. V-V-E-D-V) P{idx}", value="V-E-V-D-V", key=f"racha_{idx}")
            
            # Sub-tarjeta de visualización rápida de la base (con icono diana)
            adj_1 = c1
            adj_2 = c2
            if "Baja clave en Local" in bajas: adj_1 *= 1.15
            elif "Baja clave en Visitante" in bajas: adj_2 *= 1.15
            
            opcion_base = "1 (Local)" if adj_1 <= adj_2 else "2 (Visitante)"
            cuota_base = c1 if adj_1 <= adj_2 else c2
            
            st.markdown(
                f"""
                <div style="background-color: #E1F1F8; border-radius: 8px; padding: 10px; margin-top: 10px; border: 1px solid #AAD4E6; display: flex; align-items: center;">
                    <span style="font-size: 18px; margin-right: 10px;">🎯</span>
                    <p style="color: #0E5D7A; margin: 0;">Base Automática: Signo {opcion_base} (Cuota: {cuota_base:.2f})</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            partidos.append({
                "nombre": p_nombre,
                "c1": c1, "cX": cX, "c2": c2,
                "bajas": bajas, "tarjetas": tarjetas, "racha": racha,
                "opcion_base": opcion_base, "cuota_base": cuota_base
            })

    # ---------------------------------------------------------
    # SECCIÓN 2: CONFIGURACIÓN DE APUESTA
    # ---------------------------------------------------------
    st.header("2. Configuración del Stake")
    
    # Tarjeta visual para el stake (color suave)
    st.markdown(
        """
        <div style="background-color: white; border-radius: 10px; padding: 15px; border: 1px solid #FFEBEB; margin-bottom: 10px;">
            <h3 style="margin: 0; color: #A32A2A;">Inversión por Boleto</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    monto_por_boleto = st.number_input("Monto (€)", min_value=1.0, value=10.0, step=1.0, label_visibility="collapsed")
    inversion_total = monto_por_boleto * 9

    st.success(f"💡 Inversión Total para los 9 Boletos: *{inversion_total:.2f}€*")

    # Botón grande y colorido (Replicando estilo)
    if st.button("🚀 Calcular Matriz de 9 Boletos", use_container_width=True):
        
        # ---------------------------------------------------------
        # GENERACIÓN DE LOS 9 BOLETOS (Nueva Lógica)
        # ---------------------------------------------------------
        boletos_data = []

        def agregar_boleto(num, tipo, sel1, sel2, sel3, c1, c2, c3):
            c_comb = c1 * c2 * c3
            retorno = c_comb * monto_por_boleto
            ganancia = retorno - inversion_total
            boletos_data.append({
                "Boleto": f"Boleto {num}",
                "Tipo": tipo,
                f"{partidos[0]['nombre']}": f"{sel1} ({c1:.2f})",
                f"{partidos[1]['nombre']}": f"{sel2} ({c2:.2f})",
                f"{partidos[2]['nombre']}": f"{sel3} ({c3:.2f})",
                "Cuota Combinada": f"{c_comb:.2f}",
                "Retorno Potencial": f"{retorno:.2f}€",
                "Beneficio Neto": f"{ganancia:+.2f}€"
            })

        # Datos Base
        c_b1, c_b2, c_b3 = partidos[0]["cuota_base"], partidos[1]["cuota_base"], partidos[2]["cuota_base"]
        op_b1, op_b2, op_b3 = partidos[0]["opcion_base"], partidos[1]["opcion_base"], partidos[2]["opcion_base"]

        # Boleto 1: Base Principal
        agregar_boleto(1, "BASE PRINCIPAL", op_b1, op_b2, op_b3, c_b1, c_b2, c_b3)
        
        # Boletos 2 al 7: Núcleo Dobles/Trixie
        agregar_boleto(2, "COBERTURA 1: Empate P1", "X (Empate)", op_b2, op_b3, partidos[0]["cX"], c_b2, c_b3)
        agregar_boleto(3, "COBERTURA 2: Empate P2", op_b1, "X (Empate)", op_b3, c_b1, partidos[1]["cX"], c_b3)
        agregar_boleto(4, "COBERTURA 3: Empate P3", op_b1, op_b2, "X (Empate)", c_b1, c_b2, partidos[2]["cX"])
        
        def inv_op(p_dict): return "2 (Visitante)" if "1" in p_dict["opcion_base"] else "1 (Local)"
        def inv_c(p_dict): return p_dict["c2"] if "1" in p_dict["opcion_base"] else p_dict["c1"]

        agregar_boleto(5, "COBERTURA 4: Sorpresa P1", inv_op(partidos[0]), op_b2, op_b3, inv_c(partidos[0]), c_b2, c_b3)
        agregar_boleto(6, "COBERTURA 5: Sorpresa P2", op_b1, inv_op(partidos[1]), op_b3, c_b1, inv_c(partidos[1]), c_b3)
        agregar_boleto(7, "COBERTURA 6: Sorpresa P3", op_b1, op_b2, inv_op(partidos[2]), c_b1, c_b2, inv_c(partidos[2]))

        # Boletos 8 y 9: Remontada / Doble Empate
        agregar_boleto(8, "EXTRA 1: Fallo Doble", "X (Empate)", "X (Empate)", op_b3, partidos[0]["cX"], partidos[1]["cX"], c_b3)
        agregar_boleto(9, "EXTRA 2: Triple Remontada", inv_op(partidos[0]), inv_op(partidos[1]), inv_op(partidos[2]), inv_c(partidos[0]), inv_c(partidos[1]), inv_c(partidos[2]))

        # ---------------------------------------------------------
        # MOSTRAR RESULTADOS (Tabla y Tarjetas Replicadas)
        # ---------------------------------------------------------
        st.header("📋 Matriz Resultante de 9 Boletos")
        df_boletos = pd.DataFrame(boletos_data)
        st.dataframe(df_boletos, use_container_width=True)

        # Visualización en Tarjetas (Opcional, estilo antiguo)
        st.subheader("Visualización Individual de Boletos:")
        cols_b_show = st.columns(3)
        
        for idx, row in df_boletos.iterrows():
            with cols_b_show[idx % 3]:
                st.markdown(
                    f"""
                    <div style="background-color: white; border-radius: 8px; padding: 10px; margin-bottom: 10px; border: 1px solid #FFEBEB;">
                        <p style="color: #A32A2A; font-weight: bold; margin: 0;">{row['Boleto']} - {row['Tipo']}</p>
                        <p style="margin: 3px 0; font-size: 13px;">Combinada: {row[partidos[0]['nombre']]} | {row[partidos[1]['nombre']]} | {row[partidos[2]['nombre']]}</p>
                        <p style="margin: 0; color: #0E5D7A; font-weight: bold;">Cuota: {row['Cuota Combinada']}</p>
                        <p style="margin: 0; color: green; font-weight: bold;">Retorno: {row['Retorno Potencial']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# =========================================================
# PESTAÑA 2: HISTORIAL UNIFICADO (Vacío, como en captura)
# =========================================================
with tab2:
    st.info("Pestaña de Historial Unificado en desarrollo.")
