import streamlit as st
import os
from dotenv import load_dotenv
from helpers.auth import auth
from helpers.summarization import summarization
from helpers.sentiment import sentiment
from helpers.tipo import tipo_class
from helpers.churn import churn_predict
from helpers.contestacion import res_contestacion

# Set page config to use wide mode by default
st.set_page_config(layout="wide")

load_dotenv()

apikey = os.getenv("APIKEY")
space_id_summarization = os.getenv("SPACE_ID_SUMMARIZATION")
space_id_sentiment = os.getenv("SPACE_ID_SENTIMENT")
space_id_tipo = os.getenv("SPACE_ID_TIPO")
space_id_churn = os.getenv("SPACE_ID_CHURN")
space_id_contestacion = os.getenv("SPACE_ID_CONTESTACION")
token = auth(apikey)["access_token"]

def main():

    xcol1, xcol2 = st.columns([2, 1])

    with xcol1:
        
        # Create a row of columns: one for the image and one for the title
        col1, col2 = st.columns([1, 5], gap="small")  # Adjust the ratio as needed
        
        with col1:
            # Display an image (replace 'image_path_or_url' with the actual path or URL to your image)
            st.image('images/watson.png', width=180)  # Adjust the width as needed
        
        with col2:
            # Display the title next to the image
            st.markdown("# GenIO: El sistema inteligente para la gestión de clientes")

        if 'selected_client' not in st.session_state:
            st.session_state['selected_client'] = None

        # Predefined texts for each client
        client_feedback = {
    "Cliente 1": {
        "queja": "¡Es inadmisible que me hayan asignado una silla de ruedas rota! Esto es un error grave de su parte y exijo que se corrija inmediatamente.",
        "Puntos": 656,
        "Geografia": "Germany",
        "Genero": "Female",
        "Edad": 49,
        "Antigüedad": 9,
        "KmAcompañante": 97092.87,
        "Acompañantes": 1,
        "TieneTarjetaClub": 1,
        "EsMiembroActivo": 0,
        "Km": 74771.22,
    },
    "Cliente 2": {
        "queja": "Estoy completamente frustrado porque al llegar a la estación no había operario disponible para asistirme a abordar el tren. Esto es inaceptable y necesito una solución inmediata. ¡Es mi derecho y no puedo acceder al servicio!",
        "Puntos": 580,
        "Geografia": "Germany",
        "Genero": "Female",
        "Edad": 38,
        "Antigüedad": 1,
        "KmAcompañante": 128218.47,
        "Acompañantes": 1,
        "TieneTarjetaClub": 1,
        "EsMiembroActivo": 0,
        "Km": 125953.83,
    },
    "Cliente 3": {
        "queja": "He notado que el ascensor de la estación estaba fuera de servicio sin previo aviso. Esto limita mi acceso al tren cuando más lo necesito.",
        "Puntos": 552,
        "Geografia": "Spain",
        "Genero": "Male",
        "Edad": 55,
        "Antigüedad": 3,
        "KmAcompañante": 0.0,
        "Acompañantes": 1,
        "TieneTarjetaClub": 1,
        "EsMiembroActivo": 1,
        "Km": 40333.94,
    },
    "Cliente 4": {
        "queja": "No puedo creer que aún no ofrezcan asistencia para discapacitados a través de su aplicación móvil. Esto me obliga a llamar por teléfono, lo cual es muy inconveniente.",
        "Puntos": 633,
        "Geografia": "Spain",
        "Genero": "Female",
        "Edad": 46,
        "Antigüedad": 3,
        "KmAcompañante": 0.0,
        "Acompañantes": 2,
        "TieneTarjetaClub": 1,
        "EsMiembroActivo": 0,
        "Km": 120250.58,
    },
    "Cliente 5": {
        "queja": "Quiero reportar un problema con el tren que no tenía rampas disponibles para mi silla de ruedas.",
        "Puntos": 687,
        "Geografia": "France",
        "Genero": "Female",
        "Edad": 36,
        "Antigüedad": 4,
        "KmAcompañante": 97157.96,
        "Acompañantes": 1,
        "TieneTarjetaClub": 0,
        "EsMiembroActivo": 1,
        "Km": 63185.05,
    }
}

        # Icons for each client
        client_icons = {
            "Cliente 1": "👩‍💼",
            "Cliente 2": "🙎",
            "Cliente 3": "🧑‍💼",
            "Cliente 4": "👩‍💼",
            "Cliente 5": "🧑‍🔧"
        }

        # Create a row of columns for client buttons
        cols = st.columns(len(client_icons))
        for idx, (client, icon) in enumerate(client_icons.items()):
            with cols[idx]:
                # Ensure each button takes the full width of its column
                if st.button(f"{client} {icon}", key=f"client_{idx}", use_container_width=True):
                    st.session_state['selected_client'] = client
                    st.session_state['client_details'] = client_feedback[client]
                    churn, conf = None, None

        # Determine the text to display based on the last pressed button
        if st.session_state['selected_client']:
            selected_text = client_feedback[st.session_state['selected_client']]["queja"]
            input_text = st.text_area("Feedback del cliente:", value=selected_text)

        else:
            input_text = st.text_area("Feedback del cliente:")

        if st.button("watsonx 🧠"):
            if input_text:
                senti = sentiment(token,space_id_sentiment,input_text)
                summari = summarization(token,space_id_summarization,input_text)
                tipo = tipo_class(token,space_id_tipo,input_text)
                contestacion = res_contestacion(token,space_id_contestacion,input_text)
                #senti = "XXX"
                #summari = "XXX"
                #tipo = "XXX"
                #contestacion = "XXX"

                col_analysis1, col_analysis2 = st.columns(2)

                # Improved results display with icons and markdown
                with col_analysis1:
                    st.markdown(f"### Análisis de sentimiento 🌡️")
                    st.markdown(f"* **Sentimiento:** {senti}")
                    
                    st.markdown(f"### Resumen de la queja 📝")
                    st.markdown(f"* **Resumen:** {summari}")

                    st.markdown(f"### Clasificación de queja por tipología 📊")
                    st.markdown(f"* **Tipo:** {tipo}")

                with col_analysis2:
                    st.markdown(f"### Contestación automática a la queja 🤖")
                    st.markdown(f"* **Contestación automática:** {contestacion}")

                if 'client_details' in st.session_state and st.session_state['client_details'] is not None:
                    # Retrieve and display the client details stored in session state
                    with xcol2:
                        churn,conf = churn_predict(token,space_id_churn,st.session_state['client_details'])
                else:
                    st.warning("No client details available.", icon="🚫")
                
            else:
                st.warning("Please enter some text.")

    detail_labels = [
            ("Puntos", "Puntos"),
            ("Geografia", "Geografía"),
            ("Genero", "Género"),
            ("Edad", "Edad"),
            ("Antigüedad", "Antigüedad"),
            ("KmAcompañante", "Km Acompañante"),
            ("Acompañantes", "Número de Acompañantes"),
            ("TieneTarjetaClub", "Tiene Tarjeta de Club"),
            ("EsMiembroActivo", "Es Miembro Activo"),
            ("Km", "Km")
        ]
    
    if 'client_details' in st.session_state and st.session_state['client_details'] is not None:
        client_details = st.session_state['client_details']
    else:
        client_details = {key: "" for key, _ in detail_labels}
    
    with xcol2:
        # New section for additional client details
        st.markdown("### Detalles del Cliente")

        # Define labels and keys for the new input fields

        # Organize the input fields in a 2x5 grid
        for i in range(0, len(detail_labels), 2):
            col1, col2 = st.columns(2)
            with col1:
                key, label = detail_labels[i]
                # Use the details from the session state to set the value of each input field
                st.text_input(label, value=str(client_details.get(key, "")), key=key, max_chars=20)
            if i + 1 < len(detail_labels):
                with col2:
                    key, label = detail_labels[i + 1]
                    st.text_input(label, value=str(client_details.get(key, "")), key=key, max_chars=20)
        
        if 'client_details' in st.session_state and st.session_state['client_details'] is not None and conf is not None:
            with st.container():  # Use a container to ensure it appears below xcol2
                st.markdown("### Predicción de abandono")
                if churn:
                    st.markdown(f"**Riesgo alto de abandono** ⚠️")
                    st.markdown(f"**Confianza de la decisión:** {1-conf}")
                else:
                    st.markdown(f"**No riesgo de abandono 😌**")
                    st.markdown(f"**Confianza de la decisión:** {conf}")
        else:
            with st.container():
                st.write()

    # Continue with the rest of your main() function...
    # Ensure you handle these input values appropriately in your application logic

if __name__ == "__main__":
    main()
