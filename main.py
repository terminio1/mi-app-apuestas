import streamlit as st
import pandas as pd

# Configuración de página con la estética de Strike Analytics Pro
st.set_page_config(page_title="Strike Analytics Pro", page_icon="🐰", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #E6F3EA;
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
            <h1 style="color: #A32A2A; margin: 0; font-size: 32px;">¡Hola! Strike Analytics Pro 👋</h1>
            <p style="color: #A32A2A; margin: 5px 0 0 0;">Sistema Dinámico de 9 Boletos (Base + Coberturas Libres)</p>
        </div>
        """,
        unsafe_allow_html=True
    )

tab1, tab2 = st.tabs(["🎯 Generador de Jornada", "📋 Historial Unificado"])

with tab1:
    st.header("1. Configura tus Partidos, Cuotas y Selección Base")

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
            
            p_local = st.text_input(f"Equipo Local P{idx}", value=f"Local {idx}", key=f"p_loc_{idx}")
            p_visitante = st.text_input(f"Equipo Visitante P{idx}", value=f"Visitante {idx}", key=f"p_vis_{idx}")
            
            st.markdown("*Cuotas Mercado 1X2:*")
            c1 = st.number_input(f"Cuota 1 ({p_local})", min_value=1.01, value=2.10, step=0.05, key=f"c1_{idx}")
            cX = st.number_input(f"Cuota X (Empate)", min_value=1.01, value=3.20, step=0.05, key=f"cX_{idx}")
            c2 = st.number_input(f"Cuota 2 ({p_visitante})", min_value=1.01, value=3.50, step=0.05, key=f"c2_{idx}")
            
            # Elección de la Base (Sugerida por cuota, modificable por el usuario)
            sugerencia_idx = 0 if c1 <= c2 else 1
            opciones = [f"1 ({p_local})", f"2 ({p_visitante})", "X (Empate)"]
            
            st.markdown("*Selección para Apuesta Base:*")
            sel_base = st.selectbox(
                f"Base Elegida P{idx}", 
                opciones, 
                index=sugerencia_idx, 
                key=f"base_sel_{idx}"
            )
            
            # Asignar cuota según la base seleccionada
            if "1" in sel_base:
                cuota_base = c1
            elif "2" in sel_base:
                cuota_base = c2
            else:
                cuota_base = cX
            
            partidos.append({
                "local": p_local, "visitante": p_visitante, "vs": f"{p_local} vs {p_visitante}",
                "c1": c1, "cX": cX, "c2": c2,
                "opcion_base": sel_base, "cuota_base": cuota_base
            })

    # ---------------------------------------------------------
    # SECCIÓN DE BOLETOS LIBRES (8 Y 9)
    # ---------------------------------------------------------
    st.header("2. Boletos Libres (8 y 9)")
    st.markdown("Elige libremente los resultados que quieres cubrir para los boletos de cierre:")
    
    col_b8, col_b9 = st.columns(2)
    
    opciones_p1 = [f"1 ({partidos[0]['local']})", "X (Empate)", f"2 ({partidos[0]['visitante']})"]
    opciones_p2 = [f"1 ({partidos[1]['local']})", "X (Empate)", f"2 ({partidos[1]['visitante']})"]
    opciones_p3 = [f"1 ({partidos[2]['local']})", "X (Empate)", f"2 ({partidos[2]['visitante']})"]

    with col_b8:
        st.markdown("*📌 Boleto 8 (Cobertura Personalizada 1)*")
        b8_p1 = st.selectbox("Selección P1 (Boleto 8)", opciones_p1, index=1, key="b8_p1")
        b8_p2 = st.selectbox("Selección P2 (Boleto 8)", opciones_p2, index=1, key="b8_p2")
        b8_p3 = st.selectbox("Selección P3 (Boleto 8)", opciones_p3, index=0, key="b8_p3")

    with col_b9:
        st.markdown("*📌 Boleto 9 (Cobertura Personalizada 2)*")
        b9_p1 = st.selectbox("Selección P1 (Boleto 9)", opciones_p1, index=2, key="b9_p1")
        b9_p2 = st.selectbox("Selección P2 (Boleto 9)", opciones_p2, index=2, key="b9_p2")
        b9_p3 = st.selectbox("Selección P3 (Boleto 9)", opciones_p3, index=2, key="b9_p3")

    # ---------------------------------------------------------
    # CONFIGURACIÓN DEL STAKE
    # ---------------------------------------------------------
    st.header("3. Configuración del Stake")
    monto_por_boleto = st.number_input("Monto por Boleto (€)", min_value=1.0, value=10.0, step=1.0)
    stake_unidad = monto_por_boleto / 4.0
    inversion_total = monto_por_boleto * 9

    st.success(f"💡 Inversión Total (9 Boletos): *{inversion_total:.2f}€* ({stake_unidad:.2f}€ por combinación dentro del Trixie)")

    # ---------------------------------------------------------
    # CÁLCULO DE LA MATRIZ DE 9 BOLETOS
    # ---------------------------------------------------------
    if st.button("🚀 Calcular Matriz de 9 Boletos", use_container_width=True):
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
                "Tipo": tipo,
                f"{partidos[0]['vs']}": f"{sel1} ({c1:.2f})",
                f"{partidos[1]['vs']}": f"{sel2} ({c2:.2f})",
                f"{partidos[2]['vs']}": f"{sel3} ({c3:.2f})",
                "Pago 3 Dobles": f"{pago_dobles:.2f}€",
                "Pago Trixie Completo": f"{pago_trixie:.2f}€"
            })

        op_b1, op_b2, op_b3 = partidos[0]["opcion_base"], partidos[1]["opcion_base"], partidos[2]["opcion_base"]

        # Boleto 1: Base
        agregar_boleto(1, "BASE PRINCIPAL", op_b1, op_b2, op_b3)
        
        # Boletos 2 al 4: Variantes Empate
        agregar_boleto(2, "COBERTURA 1: Empate P1", "X (Empate)", op_b2, op_b3)
        agregar_boleto(3, "COBERTURA 2: Empate P2", op_b1, "X (Empate)", op_b3)
        agregar_boleto(4, "COBERTURA 3: Empate P3", op_b1, op_b2, "X (Empate)")
        
        # Boletos 5 al 7: Variantes Sorpresa
        def inv_op(p_dict): return f"2 ({p_dict['visitante']})" if "1" in p_dict["opcion_base"] else f"1 ({p_dict['local']})"
        agregar_boleto(5, "COBERTURA 4: Sorpresa P1", inv_op(partidos[0]), op_b2, op_b3)
        agregar_boleto(6, "COBERTURA 5: Sorpresa P2", op_b1, inv_op(partidos[1]), op_b3)
        agregar_boleto(7, "COBERTURA 6: Sorpresa P3", op_b1, op_b2, inv_op(partidos[2]))

        # Boletos 8 y 9: Configurados libremente por el usuario
        agregar_boleto(8, "LIBRE 1 (Personalizado)", b8_p1, b8_p2, b8_p3)
        agregar_boleto(9, "LIBRE 2 (Personalizado)", b9_p1, b9_p2, b9_p3)

        # Mostrar Tabla Resultante
        st.header("📋 Matriz Resultante de 9 Boletos")
        df_boletos = pd.DataFrame(boletos_data)
        st.dataframe(df_boletos, use_container_width=True)

        # Cálculo de Cobro Global si entra la Base
        c_b1, c_b2, c_b3 = partidos[0]["cuota_base"], partidos[1]["cuota_base"], partidos[2]["cuota_base"]
        cobro_b1_trixie = (c_b1*c_b2 + c_b1*c_b3 + c_b2*c_b3 + c_b1*c_b2*c_b3) * stake_unidad
        
        suma_dobles_otros = ((c_b2 * c_b3) + (c_b1 * c_b3) + (c_b1 * c_b2) + (c_b2 * c_b3) + (c_b1 * c_b3) + (c_b1 * c_b2)) * stake_unidad
        gran_total_cobro = cobro_b1_trixie + suma_dobles_otros
        beneficio_neto = gran_total_cobro - inversion_total

        st.markdown("---")
        st.header("💰 Resumen de Cobro Global (Si entra la Base Completa)")
        
        c_res1, c_res2, c_res3 = st.columns(3)
        c_res1.metric("Cobro Boleto 1 (Trixie Base)", f"{cobro_b1_trixie:.2f}€")
        c_res2.metric("Suma Dobles (Boletos 2 al 7)", f"{suma_dobles_otros:.2f}€")
        c_res3.metric("🔥 GRAN TOTAL COBRADO", f"{gran_total_cobro:.2f}€", delta=f"{beneficio_neto:+.2f}€ Neto")

with tab2:
    st.info("Pestaña de Historial Unificado en desarrollo.")
