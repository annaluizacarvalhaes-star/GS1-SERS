print("=" * 60)
print("HELIOS-7 — MONITORAMENTO ENERGÉTICO ESPACIAL")
print("=" * 60)
print("Missão: Helios Test Alpha")
print("Ciclos analisados: 6")
print("=" * 60)

# geracao(kW), eficiencia(%), bateria(%), reator(°C), consumo(kW)
dados_missao = [
    [4.2, 87, 78, 68, 3.3],  # ciclo 1
    [3.8, 75, 65, 72, 3.6],  # ciclo 2
    [2.1, 52, 40, 81, 4.0],  # ciclo 3
    [0.8, 30, 22, 89, 4.2],  # ciclo 4
    [0.4, 18, 10, 97, 3.9],  # ciclo 5
    [2.5, 60, 35, 75, 3.5],  # ciclo 6
]

pt_solar  = 0
pt_bat    = 0
pt_reator = 0
pt_consumo = 0


def analisar_solar(geracao):
    if geracao < 1.0:
        return "CRÍTICO", "Geração solar insuficiente", 2
    elif geracao < 3.0:
        return "ATENÇÃO", "Geração abaixo do ideal", 1
    else:
        return "NORMAL", "Geração estável", 0


def analisar_bateria(bat):
    if bat < 20:
        return "CRÍTICO", "Bateria em nível crítico", 2
    elif bat < 50:
        return "ATENÇÃO", "Bateria abaixo do recomendado", 1
    else:
        return "NORMAL", "Energia estável", 0


def analisar_reator(reator):
    if reator > 90:
        return "CRÍTICO", "Risco de superaquecimento", 2
    elif reator > 70:
        return "ATENÇÃO", "Temperatura elevada", 1
    else:
        return "NORMAL", "Temperatura estável", 0


def analisar_consumo(consumo, geracao):
    deficit = consumo - geracao
    if deficit > 2.5:
        return "CRÍTICO", "Consumo muito acima da geração", 2
    elif deficit > 0:
        return "ATENÇÃO", "Consumo acima da geração", 1
    else:
        return "NORMAL", "Consumo dentro do esperado", 0


def classificar_ciclo(risco):
    if risco <= 2:
        return "MISSÃO ESTÁVEL"
    elif risco < 6:
        return "MISSÃO EM ATENÇÃO"
    else:
        return "MISSÃO CRÍTICA"


def recomendacao_ciclo(risco, st_solar, st_bat, st_reator):
    if risco == 0:
        return "Manter operação normal e continuar monitoramento."

    tem_critico = "CRÍTICO" in (st_solar, st_bat, st_reator)

    if tem_critico:
        return "Ativar protocolo de emergência e reduzir consumo imediatamente."

    if st_reator == "ATENÇÃO":
        return "Verificar sistema de resfriamento do reator."

    return "Monitorar sistemas em atenção e preparar plano de contingência."


def calcular_media(coluna):
    return sum(d[coluna] for d in dados_missao) / len(dados_missao)


def calcular_tendencia(riscos):
    metade = len(riscos) // 2
    media_inicio = sum(riscos[:metade]) / metade
    media_fim    = sum(riscos[metade:]) / metade
    if media_fim > media_inicio:
        return "A missão apresentou tendência de piora."
    elif media_fim < media_inicio:
        return "A missão apresentou tendência de melhora."
    else:
        return "A missão manteve tendência estável."


def classificar_final(risco_medio):
    if risco_medio <= 2:
        return "MISSÃO ESTÁVEL"
    elif risco_medio < 6:
        return "MISSÃO EM ATENÇÃO"
    else:
        return "MISSÃO CRÍTICA"


def area_mais_afetada(pt_s, pt_b, pt_r, pt_c):
    areas = {
        "Geração solar":   pt_s,
        "Sistema de bateria": pt_b,
        "Reator térmico":  pt_r,
        "Consumo energético": pt_c,
    }
    return max(areas, key=areas.get)


def conclusao_final(classificacao, tendencia):
    if classificacao == "MISSÃO ESTÁVEL":
        return ("A missão transcorreu dentro dos parâmetros normais. "
                "Todos os sistemas operaram de forma adequada.")
    elif classificacao == "MISSÃO EM ATENÇÃO":
        if "piora" in tendencia:
            return ("A missão apresentou instabilidade relevante. "
                    "A equipe deve manter o plano de contingência ativo.")
        else:
            return ("A missão apresentou instabilidade em alguns ciclos, "
                    "mas demonstrou tendência de recuperação.")
    else:
        return ("A missão atingiu níveis críticos em múltiplos sistemas. "
                "Intervenção imediata e protocolo de emergência necessários.")


# ANÁLISE DOS CICLOS

riscos_por_ciclo = []
total_ciclos = len(dados_missao)

for i in range(total_ciclos):
    geracao = dados_missao[i][0]
    efic    = dados_missao[i][1]
    bat     = dados_missao[i][2]
    reator  = dados_missao[i][3]
    consumo = dados_missao[i][4]

    st_solar,   desc_solar,   pts_solar   = analisar_solar(geracao)
    st_bat,     desc_bat,     pts_bat     = analisar_bateria(bat)
    st_reator,  desc_reator,  pts_reator  = analisar_reator(reator)
    st_consumo, desc_consumo, pts_consumo = analisar_consumo(consumo, geracao)

    risco = pts_solar + pts_bat + pts_reator + pts_consumo
    riscos_por_ciclo.append(risco)

    if i < total_ciclos - 1:
        pt_solar   += pts_solar
        pt_bat     += pts_bat
        pt_reator  += pts_reator
        pt_consumo += pts_consumo

    print("-" * 60)
    print(f"CICLO {i + 1}")
    print("-" * 60)
    print(f"Geração solar: {geracao} kW | {st_solar} | {desc_solar}")
    print(f"Eficiência:    {efic}%")
    print(f"Bateria:       {bat}% | {st_bat} | {desc_bat}")
    print(f"Reator:        {reator} °C | {st_reator} | {desc_reator}")
    print(f"Consumo:       {consumo} kW | {st_consumo} | {desc_consumo}")
    print(f"Pontuação de risco do ciclo: {risco}")
    print(f"Classificação do ciclo: {classificar_ciclo(risco)}")
    print(f"Recomendação: {recomendacao_ciclo(risco, st_solar, st_bat, st_reator)}")
    print()


# RELATÓRIO FINAL

ciclo_critico_idx = riscos_por_ciclo.index(max(riscos_por_ciclo))
maior_risco       = max(riscos_por_ciclo)
risco_medio       = sum(riscos_por_ciclo) / len(riscos_por_ciclo)
ciclos_criticos   = sum(1 for r in riscos_por_ciclo if r >= 6)
tendencia         = calcular_tendencia(riscos_por_ciclo)
classificacao_fim = classificar_final(risco_medio)
area_afetada      = area_mais_afetada(pt_solar, pt_bat, pt_reator, pt_consumo)
conclusao         = conclusao_final(classificacao_fim, tendencia)

print("=" * 60)
print("RELATÓRIO FINAL DA MISSÃO")
print("=" * 60)
print("Missão: Helios Test Alpha\n")
print(f"QUANTIDADE DE CICLOS ANALISADOS: {total_ciclos}\n")
print(f"Média de geração solar: {calcular_media(0):.2f} kW")
print(f"Média de eficiência:    {calcular_media(1):.2f}%")
print(f"Média de bateria:       {calcular_media(2):.2f}%")
print(f"Média do reator:        {calcular_media(3):.2f} °C")
print(f"Média de consumo:       {calcular_media(4):.2f} kW\n")
print(f"Ciclo mais crítico: Ciclo {ciclo_critico_idx + 1}")
print(f"Maior pontuação de risco: {maior_risco}\n")
print(f"Risco médio da missão: {risco_medio:.2f}")
print(f"Quantidade de ciclos críticos: {ciclos_criticos}")
print(f"Tendência da missão: {tendencia}\n")
print("PONTUAÇÃO ACUMULADA POR ÁREA:")
print(f"  Geração solar:        {pt_solar} pontos")
print(f"  Sistema de bateria:   {pt_bat} pontos")
print(f"  Reator térmico:       {pt_reator} pontos")
print(f"  Consumo energético:   {pt_consumo} pontos\n")
print(f"Área mais afetada: {area_afetada}\n")
print(f"Classificação final da missão: {classificacao_fim}\n")
print(f"CONCLUSÃO:\n{conclusao}")
