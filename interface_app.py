import streamlit as st
import google.generativeai as genai
import json

# --- Configuração da Página e Chave da API ---
st.set_page_config(page_title="Rapport.AI", page_icon="🧠")

# Usando o sistema de segredos do Streamlit para a chave do Google
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# --- A Lógica Principal (O "Cérebro") ---
PROMPT_MESTRE = """
Você é o 'Rapport.AI', um assistente de comunicação para aplicativos de relacionamento.
Sua missão é ajudar o usuário a criar conexões genuínas e marcar encontros, aplicando os princípios de dois livros:
'Manual de Persuasão do FBI' (Jack Schafer): Foco em criar confiança, fazer o outro se sentir bem consigo mesmo, usar perguntas abertas e validar sentimentos.
'Como Convencer em 90 Segundos' (Nicholas Boothman): Foco em espelhar o tom, ser positivo, curioso e quebrar o gelo de forma eficaz.
O usuário fornecerá a bio do 'match' e o histórico da conversa. Sua tarefa é analisar a última mensagem do 'match' e gerar três tipos de sugestões de resposta para o usuário.
As respostas devem ser:
Autênticas e leves, nunca robóticas ou manipuladoras.
Terminar com uma pergunta aberta para manter a conversa fluindo.
Adaptadas ao tom da conversa (se o match é engraçado, seja engraçado; se é sério, seja mais profundo).
Analise o contexto abaixo e retorne sua resposta EXCLUSIVAMENTE em formato JSON com a seguinte estrutura:
{
"analise_de_vibe": "Uma breve análise do sentimento e interesse do match.",
"termometro_de_interesse": um número de 0 a 100,
"sugestoes": {
"aprofundar_conexao": "Uma resposta focada em validar o que o match disse e aprofundar a conversa (Estilo FBI).",
"manter_interesse": "Uma resposta mais divertida, com humor ou uma provocação leve para manter a dinâmica (Estilo Boothman).",
"ponte_para_encontro": "Uma resposta que cria uma oportunidade para sugerir um encontro, SE o momento for apropriado. Se não for, deixe este campo como 'Ainda é cedo para um convite.'"
}
}
"""

def gerar_sugestao_resposta(bio_match, historico_conversa, ultima_mensagem_match):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        # A API do Gemini precisa que a instrução de formato JSON esteja no prompt.
        # Também precisamos limpar a resposta para garantir que seja um JSON válido.
        full_prompt = f"""
        {PROMPT_MESTRE}

        CONTEXTO:
        - Bio do Match: "{bio_match}"
        - Histórico da Conversa: "{historico_conversa}"
        - Última Mensagem do Match para eu responder: "{ultima_mensagem_match}"
        
        Por favor, gere as sugestões de resposta no formato JSON solicitado.
        """
        
        response = model.generate_content(full_prompt)
        
        # Limpa a saída da API para garantir que é apenas o JSON
        json_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        sugestoes_json = json.loads(json_text)
        return sugestoes_json
        
    except Exception as e:
        # Fornece um erro mais informativo para debugging
        error_message = f"Ocorreu um erro ao contatar a API do Google Gemini: {e}"
        print(error_message) # Isso aparecerá nos logs do Streamlit
        return {"error": error_message}

# --- O resto da Interface Gráfica com Streamlit (permanece igual) ---
st.title("🧠 Rapport.AI")
st.caption("Seu assistente de IA para criar conexões genuínas (Powered by Google Gemini)") # Adicionei uma menção ao Gemini!

st.header("Insira os dados da conversa:")
bio_do_match = st.text_area("Bio do Match", "Amante de viagens, viciada em café e tentando aprender a tocar violão. Não curto papo furado.")
historico_da_conversa = st.text_area("Histórico da Conversa", "Eu: Oi! Vi que vc tá aprendendo violão. Já conseguiu tirar alguma música ou só na parte dos dedos doendo? haha\nMatch: Hahaha por enquanto mais na parte dos dedos doendo mesmo! Mas já arrisco uns acordes de Legião Urbana.")
ultima_mensagem_do_match = st.text_input("Última Mensagem do Match (para você responder)", "Meu final de semana foi ótimo, descobri uma cafeteria nova no centro que tem um bolo de cenoura incrível.")

if st.button("Gerar Sugestões com IA"):
    with st.spinner('Analisando a conversa com Google Gemini...'):
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