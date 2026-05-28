# ==========================================
# ENGINE DE SINAIS
# ==========================================

def gerar_sinal(

    zscore,
    correlacao,
    half_life,
    pvalor

):

    sinal = "NEUTRO"

    confianca = 0

    motivo = []

    # ==========================================
    # CORRELAÇÃO
    # ==========================================

    if correlacao >= 0.80:

        confianca += 1

        motivo.append(

            "Correlação Forte"

        )

    # ==========================================
    # HALF LIFE
    # ==========================================

    if half_life <= 30:

        confianca += 1

        motivo.append(

            "Reversão Rápida"

        )

    # ==========================================
    # COINTEGRAÇÃO
    # ==========================================

    if pvalor <= 0.05:

        confianca += 1

        motivo.append(

            "Cointegração Ativa"

        )

    # ==========================================
    # ZSCORE
    # ==========================================

    if zscore >= 2:

        sinal = "🔴 SELL SPREAD"

        confianca += 1

        motivo.append(

            "Spread Esticado"

        )

    elif zscore <= -2:

        sinal = "🟢 BUY SPREAD"

        confianca += 1

        motivo.append(

            "Spread Descontado"

        )

    else:

        sinal = "⚪ NO TRADE"

    return {

        "sinal": sinal,

        "confianca": confianca,

        "motivo": motivo

    }
