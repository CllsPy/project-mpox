import streamlit as st
import numpy as np
import scipy.integrate as si
import matplotlib.pyplot as plt
from PIL import Image

# Set page config
icon = Image.open('files/icon.png')
st.set_page_config(
    page_title="Mpox Model Simulator",
    page_icon=icon, 
    layout="wide")

# Function for the model without vaccination
def mpoxWithout(x, T):
    S, E, I, R = x
    R0 = st.session_state.R0
    infectious_period = st.session_state.infectious_period
    incubation_period = st.session_state.incubation_period
    delta = st.session_state.delta
    death_rate = st.session_state.death_rate / 1000
    birth_rate = st.session_state.birth_rate / 1000

    pi = birth_rate / 365
    mu = death_rate / 365
    alpha = 1 / incubation_period
    gamma = 1 / infectious_period
    beta = R0 * (delta + gamma)

    dS = pi - beta * S * I - mu * S
    dE = beta * S * I - (alpha + mu) * E
    dI = alpha * E - (gamma + delta + mu) * I
    dR = gamma * I - mu * R

    return [dS, dE, dI, dR]

# Function for the model with vaccination
def mpoxWith(x, T):
    S, E, I, R, V = x
    R0 = st.session_state.R0
    infectious_period = st.session_state.infectious_period
    incubation_period = st.session_state.incubation_period
    delta = st.session_state.delta
    death_rate = st.session_state.death_rate / 1000
    birth_rate = st.session_state.birth_rate / 1000
    v = st.session_state.v
    e = st.session_state.e

    pi = birth_rate / 365
    mu = death_rate / 365
    alpha = 1 / incubation_period
    gamma = 1 / infectious_period
    beta = R0 * (delta + gamma)

    dS = pi - (beta * I + mu + v) * S
    dE = beta * S * I + (1 - e) * beta * V * I - (alpha + mu) * E
    dI = alpha * E - (gamma + delta + mu) * I
    dR = gamma * I - mu * R
    dV = v * S - (1 - e) * beta * V * I - mu * V

    return [dS, dE, dI, dR, dV]

# Function to run simulation without vaccination
def run_simulation_without_vaccination(T, initial_conditions):
    solution = si.odeint(mpoxWithout, initial_conditions, T)
    return solution.T

# Function to run simulation with vaccination
def run_simulation_with_vaccination(T, initial_conditions):
    solution = si.odeint(mpoxWith, initial_conditions, T)
    return solution.T

# Sidebar for page selection
page = st.sidebar.selectbox("Select Page", ["Introdução", "Descrição do Modelo Mpox", "Simulação", "Conclusão"])

if page == "Introdução":
    st.title("Varíola dos Macacos (Mpox) - Introdução")
    col1, col2 = st.columns([2, 2])
    
    with col1:
        st.write("""  A varíola dos macacos (mpox) é uma doença viral causada pelo vírus monkeypox, relacionado ao vírus da varíola, e encontrado principalmente na África Central e Ocidental. A doença geralmente dura de 2 a 4 semanas e é geralmente menos grave que a varíola. Embora não haja tratamento específico, a vacina contra varíola oferece cerca de 85% de proteção contra a varíola dos macacos.
                 \n Ela se espalha através do contato direto com animais infectados, humanos ou materiais contaminados. \n E seus sintomas incluem: febre, dor de cabeça, dores musculares e uma erupção cutânea que progride através de vários estágios antes de formar crostas. \n  """) 

    with col2:
        st.write(" ")
        st.markdown("*Caso de Mpox, República Democrática do Congo*")
        
        image_mpx = Image.open("files/imgs/th.jpeg") 
        st.image(image_mpx)

    st.markdown("---")
    
    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown("*Distribuição geográfica dos casos relatados de mpox, República Democrática do Congo, 1 de janeiro a 26 de maio de 2024 (n=7 851)*")
        image_map = Image.open("files/imgs/map.png")
        st.image(image_map)
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write("""
        - A Província de Equateur tem sido um ponto focal de preocupação, com mais de 4.000 casos e mais de 200 mortes relatadas até agosto de 2024.
        """)

    st.markdown("---")

    col1, col2 = st.columns([2, 2])
    with col1:
        st.write(" " * 6)
        st.write("- Os dados sugerem que o surto de Mpox afetou indivíduos de diferentes faixas etárias, mas a maioria dos casos está concentrada em adultos jovens, com homens ligeiramente mais afetados em algumas categorias. Essa distribuição fornece uma visão sobre a dinâmica da transmissão da Mpox na região.")
    with col2:
        st.markdown("*Distribuição por idade e sexo dos casos confirmados de mpox, República Democrática do Congo, 1 de janeiro a 26 de maio de 2024 (n=852)")
        image_age = Image.open("files/imgs/age.png")
        st.image(image_age)

    st.markdown("---")

    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown("*Curva epidêmica dos casos relatados de mpox e proporção de casos testados na República Democrática do Congo, 1 de janeiro a 26 de maio de 2024 (n=7 851)*")
        image_tested = Image.open("files/imgs/tested.png")
        st.image(image_tested)
    with col2:
        st.write(" " * 4)
        st.write("- O gráfico mostra que o número de casos suspeitos de Mpox flutuou durante o período de 20 semanas, com picos notáveis nas semanas 8 e 19. Apesar do alto número de casos suspeitos, a proporção de casos testados permaneceu baixa. Sugerindo que, embora o surto tenha sido generalizado, a capacidade de teste pode ter sido limitada, potencialmente impactando a capacidade de confirmar casos e responder efetivamente à epidemia.")


if page == "Descrição do Modelo Mpox":
    st.title("Descrição do Modelo Mpox")
    
    # Introductory text
    st.write("""
    A dinâmica de transmissão da Mpox na Província de Equateur é modelada usando uma estrutura SEIR. Este modelo categoriza a população em quatro compartimentos: Suscetível (S), Exposto (E), Infeccioso (I) e Recuperado (R), e para o modelo com intervenção, um novo compartimento é criado chamado Vacinado (V).
    """)

    # Create two columns for the model without vaccination
    st.subheader("Modelo Sem Vacinação")
    col1, col2 = st.columns([3, 1])

    with col1:
        # Display the image for the model without vaccination
        image1 = Image.open("files/imgs/mpox-without.jpg")
        st.image(image1, caption="Diagrama esquemático da dinâmica Mpox sem Vacinação")
        # Adding the formulas in LaTeX    
        st.write("""
        Sem vacinação, o modelo SEIR é governado pelas seguintes equações:
        - dS/dt = π - βSI/N - μS
        - dE/dt = βSI/N - (α + μ) E
        - dI/dt = αE - (γ + δ + μ) I
        - dR/dt = γI - μR
        """)
        
    with col2:
        # Explanation for the model without vaccination
        st.write("""
        Neste modelo: 
        - S: Indivíduos Suscetíveis
        - E: Indivíduos Expostos (infectados mas ainda não infecciosos)
        - I: Indivíduos Infecciosos
        - R: Indivíduos Recuperados

        Parâmetros:
        - π: Taxa de recrutamento de indivíduos suscetíveis
        - β: Taxa de transmissão
        - α: Taxa na qual indivíduos expostos se tornam infecciosos
        - γ: Taxa de recuperação
        - δ: Taxa de morte induzida pela doença
        - μ: Taxa de morte natural
        """)

    st.markdown("---")  # Separator between models

    # Create two columns for the model with vaccination
    st.subheader("Modelo Com Vacinação")
    col1, col2 = st.columns([3, 1])

    with col1:
        # Display the image for the model with vaccination
        image2 = Image.open("files/imgs/mpox-with.jpg")
        st.image(image2, caption="Diagrama esquemático da dinâmica Mpox com Vacinação")
        # Adding the formulas in LaTeX for vaccination
        st.write("""
        Com vacinação, o modelo SEIR é governado pelas seguintes equações:
        - dS/dt = π - βSI/N - μS - vS
        - dV/dt = vS - (1-e) βVI/N - μV
        - dE/dt = βSI/N + (1-e) βVI/N - (α + μ) E
        - dI/dt = αE - (γ + δ + μ) I
        - dR/dt = γI – μR
        """)

    with col2:
        # Explanation for the model with vaccination
        st.write("""
        Este modelo inclui um compartimento adicional:
        - V: Indivíduos Vacinados

        Parâmetros adicionais:
        - v: Taxa de vacinação
        - e: Eficácia da vacina
        """)

elif page == "Simulação":
    st.title("Simulação do Modelo Mpox")
    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader("Parâmetros do Modelo")
        st.session_state.R0 = st.number_input("Número Básico de Reprodução (R0)", 1.0, 5.0, 2.4, 0.1)
        st.session_state.infectious_period = st.number_input("Período Infeccioso (dias)", 1, 30, 14, 1)
        st.session_state.incubation_period = st.number_input("Período de Incubação (dias)", 1, 20, 8, 1)
        st.session_state.delta = st.number_input("Taxa de Morte Induzida pela Doença", 0.0, 0.2, 0.064, 0.001)
        st.session_state.birth_rate = st.number_input("Taxa de Natalidade (por 1000 por ano)", 0, 100, 42, 1)
        st.session_state.death_rate = st.number_input("Taxa de Mortalidade (por 1000 por ano)", 0, 50, 9, 1)

        show_vaccination = st.checkbox("Mostrar Cenário com Vacinação")
        if show_vaccination:
            st.session_state.v = st.number_input("Taxa de Vacinação", 0.0, 0.9, 0.005, 0.001)
            st.session_state.e = st.number_input("Eficácia da Vacina", 0.0, 1.0, 0.85, 0.01)
        else:
            st.session_state.v = 0.0
            st.session_state.e = 0.0

    with col1:
        T = np.linspace(0, 365, 366)

        if show_vaccination:
            initial_conditions = [0.95, 0.03, 0.02, 0.0, 0.0]
            solution = run_simulation_with_vaccination(T, initial_conditions)
            S, E, I, R, V = solution
        else:
            initial_conditions = [0.95, 0.03, 0.02, 0.0]
            solution = run_simulation_without_vaccination(T, initial_conditions)
            S, E, I, R = solution

        # Calculate peaks
        E_peak = max(E)
        I_peak = max(I)
        E_peak_time = np.argmax(E)
        I_peak_time = np.argmax(I)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(T, S, label='Suscetíveis', linestyle='-.', color='blue')
        ax.plot(T, E, label='Expostos', linestyle='--', color='orange')
        ax.plot(T, I, label='Infecciosos', linestyle='-', color='red')
        ax.plot(T, R, label='Recuperados', linestyle=':', color='green')
        if show_vaccination:
            ax.plot(T, V, label='Vacinados', linestyle='-.', linewidth=3)
            ax.set_title('Simulação do Modelo Mpox com Vacinação')
        else:
            ax.set_title('Simulação do Modelo Mpox sem Vacinação')

        ax.set_xlabel('Dias')
        ax.set_ylabel('Proporção da População')
        ax.legend()
        st.pyplot(fig)

        st.subheader("Explicação da Simulação")
        if show_vaccination:
            st.write("""
            A simulação mostra a dinâmica do surto de Mpox com vacinação. 
            Incluir a vacinação reduz o pico de indivíduos infecciosos.
            """)
        else:
            st.write("""
            A simulação mostra a dinâmica do surto de Mpox sem vacinação. 
            O pico de indivíduos infecciosos é maior sem vacinação.
            """)
        
        st.subheader('Valores de Pico')
        st.write(f"""
                 - Pico de Expostos: {E_peak:.4f} no dia {E_peak_time},  
                 - Pico de Infecciosos: {I_peak:.4f} no dia {I_peak_time}""")
            
        st.subheader('Valores Finais da População')
        if show_vaccination:
            st.write(f"Suscetíveis: {S[-1]:.4f}, Expostos: {E[-1]:.4f}, Infecciosos: {I[-1]:.4f}, Recuperados: {R[-1]:.4f}, Vacinados: {V[-1]:.4f}")
        else:
            st.write(f"Suscetíveis: {S[-1]:.4f}, Expostos: {E[-1]:.4f}, Infecciosos: {I[-1]:.4f}, Recuperados: {R[-1]:.4f}")

            
if page == "Conclusão":
    st.subheader("Limitações do modelo")

    col1, col2 = st.columns([2, 2])
    with col1:
    # Introduction text
        st.write(""" 
            - População Homogênea: Assume risco de exposição igual para todos os indivíduos, ignorando a diversidade populacional e taxas de transmissão variáveis.
            - Fatores Comportamentais e Ambientais: Omite dinâmicas do mundo real como quarentena, mudanças de comportamento e intervenções de saúde pública.
            - Foco Geográfico: Concentra-se em Equateur, desconsiderando diferenças regionais como insegurança em outras províncias.
            - Simplicidade do Modelo: Pode não funcionar bem em cenários epidemiológicos mais complexos do mundo real.
    """)
        st.subheader("Melhoria do Modelo:")
        st.write("""
            - Um modelo estocástico, como um modelo baseado em agentes (ABM), oferece previsões mais precisas ao:
            - Modelar variabilidade individual: Considera diferenças em comportamento, localização e saúde.
            - Incorporar intervenções em tempo real: Inclui efeitos de quarentena, lockdowns e vacinações.""")
    with col2:
        st.markdown("*Representação esquemática do modelo Mpox com vacinação e transmissão vertical.*")
        image_mpx = Image.open("files/imgs/cmplx.png")
        st.image(image_mpx)
    
    st.markdown("---")  
    
    col1, col2 = st.columns([2, 2])

    with col1:
        st.subheader("Tratamento e Vacinações")
        image_map = Image.open("files/imgs/vaccinex.jpg")
        st.image(image_map)
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write("""
                 - O tratamento da varíola dos macacos concentra-se no alívio dos sintomas, com Tecovirimat (TPOXX) usado para casos graves. O cuidado de suporte também é crucial para gerenciar complicações. 
                 - As opções de vacinação incluem a vacina JYNNEOS, recomendada para indivíduos de alto risco, e ACAM2000, embora tenha mais efeitos colaterais.""")

    st.markdown("---")
    
    col1, col2 = st.columns([2, 2])

    with col2:
        st.subheader("Prevenção e Autocuidado")
        image_tested = Image.open("files/imgs/care.jpg")
        st.image(image_tested)
    with col1:
        st.write(" ")
        st.write(" ")      
        st.write(" ")      
        st.write(" ")      
        st.write(" ")      
        st.write("""
                 Fazer: 
                 - Lavar as mãos regularmente 
                 - Usar máscara 
                 - Cobrir as feridas \n
                 Não fazer: 
                 - Usar medicamentos sem prescrição para dor 
                 - Coçar feridas ou estourar bolhas 
                 - Fazer a barba sobre as feridas""")

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Desenvolvido com ❤ por <a style='display: block; text-align: center;' href="https://github.com/Camillia18" target="_blank">Camillia</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

