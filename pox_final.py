import streamlit as st
import numpy as np
import scipy.integrate as si
import matplotlib.pyplot as plt
from PIL import Image

# Set page config
st.set_page_config(page_title="Mpox Model Simulator", layout="wide")

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
page = st.sidebar.radio("Select Page", ["Introduction", "Mpox Model Description", "Simulation", "Conclusion"])




if page == "Introduction":
    st.title("Monkey pox (Mpox) - Introduction")
    col1, col2 = st.columns([2, 2])
    
    with col1:
        st.write("""  Monkeypox (mpox) is a viral disease caused by the monkeypox virus, related to the smallpox virus, and primarily found in Central and West Africa. The disease typically lasts 2 to 4 weeks and is generally less severe than smallpox.  While there is no specific treatment, the smallpox vaccine offers about 85% protection against monkeypox.
                 \n It spreads through direct contact with,  infected animals,  humans or  contaminated materials. \n And its symptoms include:  fever,  headache,  muscle aches, and a rash that progresses through various stages before scabbing. \n  """) 

    with col2:
        st.write(" ")
        st.markdown("*Mpox case, Democratic Republic of the Congo*")
        
        image_mpx = Image.open("th.jpeg") 
        st.image(image_mpx)




    st.markdown("---")
    
    # Rest of the code remains the same...
    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown("*Geographic distribution of reported mpox cases, Democratic Republic of the Congo, 1 January to 26 May 2024 (n=7 851)*")
        image_map = Image.open("map.png")
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
        - The Equateur Province has been a focal point of concern, with over 4,000 cases and more than 200 deaths reported as of August 2024.
        """)

    st.markdown("---")

    col1, col2 = st.columns([2, 2])
    with col1:
        st.write(" " * 6)
        st.write("- Data suggests that the Mpox outbreak has impacted individuals across different age groups, but the majority of cases are concentrated in young adults, with males slightly more affected in some categories. This distribution provides insight into the dynamics of Mpox transmission in the region.")
    with col2:
        st.markdown("*Age and sex distribution of confirmed mpox cases, Democratic Republic of the Congo, 1 January to 26 May 2024 (n=852)")
        image_age = Image.open("age.png")
        st.image(image_age)

    st.markdown("---")

    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown("*Epidemic curve of reported mpox cases and the proportion of reported cases tested in the Democratic Republic of the Congo, 1 January to 26 May 2024 (n=7 851)*")
        image_tested = Image.open("tested.png")
        st.image(image_tested)
    with col2:
        st.write(" " * 4)
        st.write("- The graph shows that the number of suspected Mpox cases fluctuated over the 20-week period, with notable peaks in weeks 8 and 19. Despite the high number of suspected cases, the proportion of cases tested remained low. Suggesting that while the outbreak was widespread, testing capacity may have been limited, potentially impacting the ability to confirm cases and respond effectively to the epidemic.")


if page == "Mpox Model Description":
    st.title("Mpox Model Description")
    
    # Introductory text
    st.write("""
    The transmission dynamics of Mpox in Equateur Province are modeled using a SEIR framework. This model categorizes the population into four compartments: Susceptible (S), Exposed (E), Infectious (I), and Recovered (R) and for the model with intervention a new compartment is created called Vaccinated(V).
    """)

    # Create two columns for the model without vaccination
    st.subheader("Model Without Vaccination")
    col1, col2 = st.columns([3, 1])

    with col1:
        # Display the image for the model without vaccination
        image1 = Image.open("mpox without.jpg")
        st.image(image1, caption="Schematic diagram of Mpox dynamics without Vaccination")
            # Adding the formulas in LaTeX    
        st.write("""
        Without vaccination, the SEIR model is governed by the following equations:
        - dS/dt = π - βSI/N - μS
        - dE/dt = βSI/N - (α + μ) E
        - dI/dt = αE - (γ + δ + μ) I
        - dR/dt = γI - μR
        """)
        
    with col2:
        # Explanation for the model without vaccination
        st.write("""
        In this model: 
        - S: Susceptible individuals
        - E: Exposed individuals (infected but not yet infectious)
        - I: Infectious individuals
        - R: Recovered individuals

        Parameters:
        - π: Recruitment rate of susceptible individuals
        - β: Transmission rate
        - α: Rate at which exposed individuals become infectious
        - γ: Recovery rate
        - δ: Disease-induced death rate
        - μ: Natural death rate
        """)


   

    st.markdown("---")  # Separator between models
    

    # Create two columns for the model with vaccination
    st.subheader("Model With Vaccination")
    col1, col2 = st.columns([3, 1])

    with col1:
        # Display the image for the model with vaccination
        image2 = Image.open("mpox with.jpg")
        st.image(image2, caption="Schematic diagram of Mpox dynamics with Vaccination")
        # Adding the formulas in LaTeX for vaccination
        st.write("""
        With vaccination, the SEIR model is governed by the following equations:
        - dS/dt = π - βSI/N - μS - vS
        - dV/dt = vS - (1-e) βVI/N - μV
        - dE/dt = βSI/N + (1-e) βVI/N - (α + μ) E
        - dI/dt = αE - (γ + δ + μ) I
        - dR/dt = γI – μR
        """)

        
    with col2:
        # Explanation for the model with vaccination
        st.write("""
        This model includes an additional compartment:
        - V: Vaccinated individuals

        Additional parameters:
        - v: Vaccination rate
        - e: Vaccine efficacy
        """)



elif page == "Simulation":
    st.title("Mpox Model Simulation")
    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader("Model Parameters")
        st.session_state.R0 = st.number_input("Basic Reproduction Number (R0)", 1.0, 5.0, 2.4, 0.1)
        st.session_state.infectious_period = st.number_input("Infectious Period (days)", 1, 30, 14, 1)
        st.session_state.incubation_period = st.number_input("Incubation Period (days)", 1, 20, 8, 1)
        st.session_state.delta = st.number_input("Disease-induced Death Rate", 0.0, 0.2, 0.064, 0.001)
        st.session_state.birth_rate = st.number_input("Birth Rate (per 1000 per year)", 0, 100, 42, 1)
        st.session_state.death_rate = st.number_input("Death Rate (per 1000 per year)", 0, 50, 9, 1)

        show_vaccination = st.checkbox("Show Vaccination Scenario")
        if show_vaccination:
            st.session_state.v = st.number_input("Vaccination Rate", 0.0, 0.9, 0.005, 0.001)
            st.session_state.e = st.number_input("Vaccine Efficacy", 0.0, 1.0, 0.85, 0.01)
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
        ax.plot(T, S, label='Susceptible', linestyle='-.', color='blue')
        ax.plot(T, E, label='Exposed', linestyle='--', color='orange')
        ax.plot(T, I, label='Infectious', linestyle='-', color='red')
        ax.plot(T, R, label='Recovered', linestyle=':', color='green')
        if show_vaccination:
            ax.plot(T, V, label='Vaccinated', linestyle='-.', linewidth=3)
            ax.set_title('Mpox Model with Vaccination Simulation')
        else:
            ax.set_title('Mpox Model without Vaccination Simulation')

        # Add peak annotations
        # ax.annotate(f'E peak: {E_peak:.4f}', xy=(E_peak_time, E_peak), xytext=(10, 10),
        #             textcoords='offset points', ha='left', va='bottom',
        #             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        #             arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

        # ax.annotate(f'I peak: {I_peak:.4f}', xy=(I_peak_time, I_peak), xytext=(10, -10),
        #             textcoords='offset points', ha='left', va='top',
        #             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        #             arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

        ax.set_xlabel('Days')
        ax.set_ylabel('Population Proportion')
        ax.legend()
        st.pyplot(fig)

        st.subheader("Simulation Explanation")
        if show_vaccination:
            st.write("""
            The simulation displays the dynamics of the Mpox outbreak with vaccination. 
            Including vaccination reduces the peak of infectious individuals.
            """)
        else:
            st.write("""
            The simulation displays the dynamics of the Mpox outbreak without vaccination. 
            The peak of infectious individuals is higher without vaccination.
            """)
        
        st.subheader('Peak Values')
        st.write(f"""
                 - Peak Exposed: {E_peak:.4f} at day {E_peak_time},  
                 - Peak Infectious: {I_peak:.4f} at day {I_peak_time}""")

            
            
        st.subheader('Final Population Values')
        if show_vaccination:
            st.write(f"Susceptible: {S[-1]:.4f}, Exposed: {E[-1]:.4f}, Infectious: {I[-1]:.4f}, Recovered: {R[-1]:.4f}, Vaccinated: {V[-1]:.4f}")
        else:
            st.write(f"Susceptible: {S[-1]:.4f}, Exposed: {E[-1]:.4f}, Infectious: {I[-1]:.4f}, Recovered: {R[-1]:.4f}")

            
if page == "Conclusion":
    st.subheader("Limitations of the model")

    col1, col2 = st.columns([2, 2])
    with col1:
    # Introduction text
        st.write(""" 
            - Homogeneous Population: Assumes equal exposure risk for all individuals, ignoring population diversity and varying transmission rates.
            - Behavioral & Environmental Factors: Omits real-world dynamics like quarantine, behavior changes, and public health interventions.
            - Geographic Focus: Focuses on Equateur, overlooking regional differences like insecurity in other provinces.
            - Model Simplicity: May not work well in more complex, real-world epidemiological scenarios.
    """)
        st.subheader(" Model Improvement: ")
        st.write("""
            - A stochastic model, like an agent-based model (ABM), offers more accurate predictions by:
            - Modeling individual variability: Accounts for differences in behavior, location, and health.
            - Incorporating real-time interventions: Includes effects of quarantine, lockdowns, and vaccinations.""")
    with col2:
        
        # Adjust text to center align vertically with the image in col1

        st.markdown("*Schematic representation of the Mpox model with vaccination and vertical transmission.)")
        image_mpx = Image.open("cmplx.png")
        st.image(image_mpx)
    
    
    st.markdown("---")  # Separator between models
    # Create two columns
    col1, col2 = st.columns([2, 2])

    # Map image and explanation
    with col1:
        st.subheader("Treatment and Vaccinations")
        image_map = Image.open("vaccinex.jpg")
        st.image(image_map)
    with col2:
        # Adjust text to center align vertically with the image in col1
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write("""
                 - Monkeypox treatment focuses on symptom relief, with Tecovirimat (TPOXX) used for severe cases. Supportive care is also crucial for managing complications. 
                 - Vaccination options include the JYNNEOS vaccine, recommended for high-risk individuals, and ACAM2000, though it has more side effects.""")

    st.markdown("---")  # Separator between models
    # # Create two columns
    # col1, col2 = st.columns([2, 2])

    # # Age image and explanation
    # with col1:
    #     st.write(" ")
    #     st.write(" ")
    #     st.write(" ")
    #     st.write(" ")
    #     st.write(" ")
    #     st.write(" ")
    #     st.write("- Overall, the data suggests that the Mpox outbreak has impacted individuals across different age groups, but the majority of cases are concentrated in young adults. The spread of the disease appears somewhat balanced between males and females, with males slightly more affected in some categories. This distribution provides insight into the dynamics of Mpox transmission in the region.")

    # with col2:
    #     # Adjust text to center align vertically with the image in col1
    #     st.markdown("*Age and sex distribution of confirmed mpox cases, Democratic Republic of the Congo, 1 January to 26 May 2024 (n=852\\)")
    #     image_age = Image.open("age.png")
    #     st.image(image_age)
    # st.markdown("---")  # Separator between models
    # Create two columns
    col1, col2 = st.columns([2, 2])

    # Tested image and explanation
    with col2:
        st.subheader("Prevention and Self-care")
        image_tested = Image.open("care.jpg")
        st.image(image_tested)
    with col1:
        # Adjust text to center align vertically with the image in col1
        st.write(" ")
        st.write(" ")      
        st.write(" ")      
        st.write(" ")      
        st.write(" ")      
        st.write("""
                 Do 
                 - Wash hands regularly. 
                 - Wear a mask 
                 - cover sores. \n
                 Do not: 
                 - Use over-the-counter medications for pain. 
                 - Scratch sores or pop blisters. 
                 - Shave over sores.""")