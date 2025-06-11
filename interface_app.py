import streamlit as st
import openai
import json

# --- Configuração da Página e Chave da API ---
st.set_page_config(page_title="Rapport.AI", page_icon="🧠")

# ↓↓↓ COLOQUE SUA CHAVE DA API DA OPENAI AQUI DENTRO DAS ASPAS ↓↓↓
OPENAI_API_KEY = st.secrets["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"]

# --- A Lógica Principal (O "Cérebro") ---
PROMPT_MESTRE = """
Você é o 'Rapport.AI', um assistente de comunicação para aplicativos de relacionamento...
(O resto do prompt mestre que você já tem vai aqui, não precisa colar de novo, o código que você já tem está completo)
"""
# ... (cole o resto do código que te passei antes, da função gerar_sugestao_resposta até o final) ...
# Se precisar, aqui está ele completo de novo:

def gerar_sugestao_resposta(bio_match, historico_conversa, ultima_mensagem_match):
    if not OPENAI_API_KEY or OPENAI_API_KEY == "SUA_CHAVE_API_AQUI":
        return {"error": "Chave da API da OpenAI não configurada. Por favor, insira a chave no código acima."}
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": PROMPT_MESTRE},
                {"role": "user", "content": f"""
                CONTEXTO:
                - Bio do Match: "{bio_match}"
                - Histórico da Conversa: "{historico_conversa}"
                - Última Mensagem do Match para eu responder: "{ultima_mensagem_match}"
                Por favor, gere as sugestões de resposta no formato JSON solicitado.
                """}
            ]
        )
        sugestoes_json = json.loads(response.choices[0].message.content)
        return sugestoes_json
    except Exception as e:
        return {"error": f"Ocorreu um erro ao contatar a API da OpenAI: {e}"}

# --- A Interface Gráfica com Streamlit ---
st.title("🧠 Rapport.AI")
st.caption("Seu assistente de IA para criar conexões genuínas")

st.header("Insira os dados da conversa:")

bio_do_match = st.text_area("Bio do Match", "Amante de viagens, viciada em café e tentando aprender a tocar violão. Não curto papo furado.")
historico_da_conversa = st.text_area("Histórico da Conversa", "Eu: Oi! Vi que vc tá aprendendo violão. Já conseguiu tirar alguma música ou só na parte dos dedos doendo? haha\nMatch: Hahaha por enquanto mais na parte dos dedos doendo mesmo! Mas já arrisco uns acordes de Legião Urbana.")
ultima_mensagem_do_match = st.text_input("Última Mensagem do Match (para você responder)", "Meu final de semana foi ótimo, descobri uma cafeteria nova no centro que tem um bolo de cenoura incrível.")

if st.button("Gerar Sugestões com IA"):
    with st.spinner('Analisando a conversa e gerando sugestões...'):
        sugestoes = gerar_sugestao_resposta(bio_do_match, historico_da_conversa, ultima_mensagem_do_match)

    st.divider()

    if "error" in sugestoes:
        st.error(sugestoes["error"])
    else:
        st.header("Análise do Rapport.AI")
        interesse = sugestoes.get('termometro_de_interesse', 0)
        st.metric(label="Termômetro do Interesse", value=f"{interesse}/100")
        st.progress(interesse)
        st.info(f"**Análise de Vibe:** {sugestoes.get('analise_de_vibe', 'N/A')}")
        st.header("Suas Opções de Resposta")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("🤝 Aprofundar Conexão")
            st.write(sugestoes.get('sugestoes', {}).get('aprofundar_conexao', 'N/A'))
        with col2:
            st.subheader("🔥 Manter Interesse")
            st.write(sugestoes.get('sugestoes', {}).get('manter_interesse', 'N/A'))
        with col3:
            st.subheader("☕ Ponte para o Encontro")
            st.write(sugestoes.get('sugestoes', {}).get('ponte_para_encontro', 'N/A'))