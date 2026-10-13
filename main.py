import streamlit as st
import requests
import json
import datetime

# Configure the Streamlit page
st.set_page_config(
    page_title="SoulBloom ♡",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap');

        /* Global Theme */
        html, body, [class*="css"] {
            font-family: 'Lora', serif;
            background-color: #fdfbf7;
            color: #4a4a4a;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Playfair Display', serif !important;
            color: #2d4a3e !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Bloom of the Day Banner */
        .bloom-banner {
            background-color: #f4e6eb;
            color: #2d4a3e;
            text-align: center;
            padding: 10px;
            font-style: italic;
            font-family: 'Playfair Display', serif;
            border-bottom: 1px solid rgba(244, 230, 235, 0.5);
            margin-top: -60px;
            margin-bottom: 30px;
            border-radius: 0 0 15px 15px;
        }

        /* Custom Card for Garden */
        .garden-card {
            background-color: white;
            border: 1px solid #f0f0f0;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease;
        }
        .garden-card:hover {
            transform: translateY(-5px);
        }
        
        /* Poem Text */
        .poem-box {
            background-color: #fdfbf7;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(210, 180, 140, 0.3);
            font-style: italic;
            color: #4a4a4a;
            margin-top: 15px;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #2d4a3e;
            color: white;
            border-radius: 30px;
            padding: 10px 24px;
            border: none;
            font-family: 'Lora', serif;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #1e332a;
            color: white;
            border-color: #1e332a;
            box-shadow: 0 4px 12px rgba(45, 74, 62, 0.2);
        }
        
        /* Text Areas */
        .stTextArea textarea {
            background-color: transparent !important;
            border: 1px solid #d2b48c !important;
            border-radius: 15px !important;
            font-family: 'Lora', serif !important;
            font-size: 1.1rem !important;
        }
        .stTextArea textarea:focus {
            border-color: #2d4a3e !important;
            box-shadow: 0 0 0 1px #2d4a3e !important;
        }
        </style>
    """, unsafe_allow_html=True)

def init_session_state():
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'Jardín'
    
    if 'garden_posts' not in st.session_state:
        # Default mock data to populate the garden
        st.session_state.garden_posts = [
            {
                "feeling": "Siento que el tiempo pasa muy rápido y no alcanzo a hacer todo.",
                "color": "#457b9d",
                "color_name": "Azul tormenta",
                "sensation": "pesa",
                "poem": "Hoy mi corazón se parece a un río apresurado,\nque olvida mirar las orillas por llegar al mar.",
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        ]
    
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1
    
    if 'wizard_data' not in st.session_state:
        st.session_state.wizard_data = {
            "feeling": "",
            "color_hex": "#e8f0eb",
            "color_name": "Verde calma",
            "sensation": "flota",
            "poem": ""
        }

def get_flower_svg(color_hex):
    """Generates an inline SVG string for the emotion flower."""
    return f"""
    <svg viewBox="0 0 100 100" width="100" height="100" style="filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.1));">
        <g transform="translate(50,50)">
            <path d="M0,0 C-20,-30 20,-30 0,0" fill="{color_hex}" stroke="rgba(0,0,0,0.1)" stroke-width="1" transform="rotate(0)" />
            <path d="M0,0 C-20,-30 20,-30 0,0" fill="{color_hex}" stroke="rgba(0,0,0,0.1)" stroke-width="1" transform="rotate(45)" />
            <path d="M0,0 C-20,-30 20,-30 0,0" fill="{color_hex}" stroke="rgba(0,0,0,0.1)" stroke-width="1" transform="rotate(90)" />
            <path d="M0,0 C-20,-30 20,-30 0,0" fill="{color_hex}" stroke="rgba(0,0,0,0.1)" stroke-width="1" transform="rotate(135)" />
            <path d="M0,0 C-20,-30 20,-30 0,0" fill="{color_hex}" stroke="rgba(0,0,0,0.1)" stroke-width="1" transform="rotate(180)" />
            <path d="M0,0 C-20,-30 20,-30 0,0" fill="{color_hex}" stroke="rgba(0,0,0,0.1)" stroke-width="1" transform="rotate(225)" />
            <path d="M0,0 C-20,-30 20,-30 0,0" fill="{color_hex}" stroke="rgba(0,0,0,0.1)" stroke-width="1" transform="rotate(270)" />
            <path d="M0,0 C-20,-30 20,-30 0,0" fill="{color_hex}" stroke="rgba(0,0,0,0.1)" stroke-width="1" transform="rotate(315)" />
            <circle cx="0" cy="0" r="8" fill="#d2b48c" stroke="rgba(0,0,0,0.1)" stroke-width="1"/>
        </g>
    </svg>
    """

def generate_soulpoem(feeling, color_name, sensation, api_key):
    """Calls Gemini API via REST to generate the poem."""
    if not api_key or api_key.strip() == "":
        return "Hoy mi corazón se parece a una hoja al viento,\nflotando suavemente hacia un lugar tranquilo."

    prompt = f"""Actúa como un poeta empático y sensible. Un adolescente está explorando sus emociones.
    Siente lo siguiente: "{feeling}".
    Asocia esta emoción con el color "{color_name}".
    Siente que su emoción "{sensation}".
    
    Escribe un "SoulPoem", un poema muy corto (máximo 4 líneas) que empiece estrictamente con la frase "Hoy mi corazón se parece a...". 
    Debe ser hermoso, reconfortante, validante y usar metáforas de la naturaleza o el clima. No uses comillas en la respuesta."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        data = response.json()
        if "candidates" in data and len(data["candidates"]) > 0:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip().replace('"', '')
        else:
            return "Hoy mi corazón se parece a un jardín en pausa,\nesperando la lluvia para volver a brotar."
    except Exception as e:
        return "Hoy mi corazón se parece a una nube pasajera,\nque pronto dejará ver el sol."

def render_sidebar():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>SoulBloom <span style='color:#f4e6eb'>♡</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888; font-style: italic; margin-bottom: 30px;'>Let your feelings bloom.</p>", unsafe_allow_html=True)
        
        # Navigation logic using buttons that update session state
        if st.button("🌸 Jardín (Mood Garden)", use_container_width=True):
            st.session_state.current_view = 'Jardín'
            st.rerun()
            
        if st.button("✨ Crear (SoulPoem)", use_container_width=True):
            st.session_state.current_view = 'Crear'
            st.session_state.wizard_step = 1  # Reset wizard on enter
            st.rerun()
            
        if st.button("✉️ Cartas (Letters)", use_container_width=True):
            st.session_state.current_view = 'Cartas'
            st.rerun()
            
        st.markdown("---")
        st.markdown("### Configuración IA")
        st.markdown("<small>Ingresa tu API Key de Gemini para generar poemas reales. Si la dejas vacía, se usará un poema de muestra.</small>", unsafe_allow_html=True)
        api_key = st.text_input("Gemini API Key", type="password")
        st.session_state.api_key = api_key

def render_garden():
    st.markdown("<h2 style='text-align: center; font-size: 2.5rem;'>Mood Garden</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-style: italic; margin-bottom: 40px;'>Cada emoción florece a su manera. Explora el jardín de emociones compartidas.</p>", unsafe_allow_html=True)

    if not st.session_state.garden_posts:
        st.info("El jardín está esperando que florezcan nuevas emociones...")
        return

    # Create a Masonry-like grid using columns
    cols = st.columns(2)
    for index, post in enumerate(reversed(st.session_state.garden_posts)):
        col = cols[index % 2]
        with col:
            svg_html = get_flower_svg(post["color"])
            card_html = f"""
            <div class="garden-card">
                <div style="height: 6px; background-color: {post["color"]}; width: calc(100% + 40px); margin: -20px -20px 15px -20px; border-radius: 20px 20px 0 0;"></div>
                <div style="display: flex; gap: 15px; align-items: center; margin-bottom: 15px;">
                    <div style="flex-shrink: 0;">
                        {svg_html}
                    </div>
                    <div>
                        <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: #888; margin-bottom: 5px;">
                            <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: {post["color"]}; margin-right: 5px;"></span>
                            Emoción que {post["sensation"]}
                        </div>
                        <div style="font-size: 0.95rem; color: #666; font-style: italic;">
                            "{post["feeling"]}"
                        </div>
                    </div>
                </div>
                <div class="poem-box">
                    {post["poem"].replace(chr(10), '<br>')}
                </div>
                <div style="text-align: right; font-size: 0.7rem; color: #aaa; margin-top: 10px;">
                    {post["date"]}
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

def render_create():
    st.markdown("<h2 style='text-align: center;'>De una emoción a una creación</h2>", unsafe_allow_html=True)
    
    # Progress Bar UI
    step = st.session_state.wizard_step
    colors = ['#2d4a3e' if i <= step else '#e0e0e0' for i in range(1, 5)]
    progress_html = f"""
    <div style="display: flex; justify-content: center; gap: 10px; margin: 20px 0 40px 0;">
        <div style="width: 12px; height: 12px; border-radius: 50%; background-color: {colors[0]};"></div>
        <div style="width: 12px; height: 12px; border-radius: 50%; background-color: {colors[1]};"></div>
        <div style="width: 12px; height: 12px; border-radius: 50%; background-color: {colors[2]};"></div>
        <div style="width: 12px; height: 12px; border-radius: 50%; background-color: {colors[3]};"></div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)

    # Step 1: Sentir
    if step == 1:
        st.markdown("<h3 style='text-align: center;'>1. Sentir</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>¿Qué estás experimentando en este momento? No lo pienses demasiado, solo déjalo salir.</p>", unsafe_allow_html=True)
        
        feeling = st.text_area("", placeholder="Siento como si una nube estuviera...", height=150, key="input_feeling", value=st.session_state.wizard_data["feeling"])
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("Explorar →", use_container_width=True):
                if feeling.strip() == "":
                    st.warning("Por favor, escribe un poco sobre cómo te sientes.")
                else:
                    st.session_state.wizard_data["feeling"] = feeling
                    st.session_state.wizard_step = 2
                    st.rerun()

    # Step 2: Explorar
    elif step == 2:
        st.markdown("<h3 style='text-align: center;'>2. Explorar</h3>", unsafe_allow_html=True)
        
        st.markdown("#### ¿Qué color tiene tu emoción?")
        color_options = {
            "Rosa tenue": "#f4e6eb",
            "Verde calma": "#e8f0eb",
            "Lila melancólico": "#e6e6fa",
            "Tierra cálida": "#d2b48c",
            "Olivo profundo": "#6b705c",
            "Azul tormenta": "#457b9d"
        }
        selected_color_name = st.radio("Selecciona un color:", list(color_options.keys()), horizontal=True)
        
        st.markdown("---")
        st.markdown("#### ¿Cómo se siente?")
        sensation_options = ["Pesa", "Flota", "Quema", "Tiembla"]
        selected_sensation = st.radio("Selecciona una sensación:", sensation_options, horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Volver", use_container_width=True):
                st.session_state.wizard_step = 1
                st.rerun()
        with col2:
            if st.button("Expresar (Generar Poema) ✨", use_container_width=True):
                st.session_state.wizard_data["color_name"] = selected_color_name
                st.session_state.wizard_data["color_hex"] = color_options[selected_color_name]
                st.session_state.wizard_data["sensation"] = selected_sensation.lower()
                st.session_state.wizard_step = 3
                st.rerun()

    # Step 3: Expresar (Loading AI)
    elif step == 3:
        st.markdown("<h3 style='text-align: center;'>3. Expresar</h3>", unsafe_allow_html=True)
        
        with st.spinner("Escuchando tus emociones... Creando tu SoulPoem único"):
            # Call AI
            generated_poem = generate_soulpoem(
                st.session_state.wizard_data["feeling"],
                st.session_state.wizard_data["color_name"],
                st.session_state.wizard_data["sensation"],
                st.session_state.api_key
            )
            st.session_state.wizard_data["poem"] = generated_poem
            st.session_state.wizard_step = 4
            st.rerun()

    # Step 4: Florecer
    elif step == 4:
        st.markdown("<h3 style='text-align: center;'>4. Florecer</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Tu emoción se ha transformado.</p>", unsafe_allow_html=True)
        
        # Display Final Flower and Poem
        col_flower, col_poem = st.columns([1, 2])
        
        with col_flower:
            st.markdown(f"<div style='text-align: center; margin-top: 20px;'>{get_flower_svg(st.session_state.wizard_data['color_hex'])}</div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style='background-color: #fcfaf5; padding: 10px; border-radius: 10px; border: 1px solid #e8e4d9; margin-top: 15px; text-align: center;'>
                    <span style='font-size: 0.7rem; text-transform: uppercase; color: #888;'>Tu Semilla</span><br>
                    <span style='font-style: italic; font-size: 0.9rem; color: #666;'>"{st.session_state.wizard_data['feeling'][:50]}..."</span>
                </div>
            """, unsafe_allow_html=True)
            
        with col_poem:
            st.markdown(f"""
                <div style='position: relative; background-color: #fdfbf7; padding: 30px; border-radius: 15px; border: 1px solid rgba(210, 180, 140, 0.4); margin-top: 10px;'>
                    <span style='position: absolute; top: 10px; left: 15px; font-size: 3rem; color: #d2b48c; opacity: 0.3; font-family: "Playfair Display", serif;'>“</span>
                    <p style='font-family: "Playfair Display", serif; font-size: 1.3rem; line-height: 1.8; color: #4a4a4a; font-style: italic; position: relative; z-index: 10; margin: 0 10px;'>
                        {st.session_state.wizard_data['poem'].replace(chr(10), '<br>')}
                    </p>
                    <span style='position: absolute; bottom: -10px; right: 15px; font-size: 3rem; color: #d2b48c; opacity: 0.3; font-family: "Playfair Display", serif;'>”</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Empezar de nuevo", use_container_width=True):
                st.session_state.wizard_step = 1
                st.session_state.wizard_data["feeling"] = ""
                st.rerun()
        with col2:
            if st.button("🌸 Plantar en el jardín", use_container_width=True):
                # Save to mock database
                new_post = {
                    "feeling": st.session_state.wizard_data["feeling"],
                    "color": st.session_state.wizard_data["color_hex"],
                    "color_name": st.session_state.wizard_data["color_name"],
                    "sensation": st.session_state.wizard_data["sensation"],
                    "poem": st.session_state.wizard_data["poem"],
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.garden_posts.append(new_post)
                st.success("¡Tu emoción ha florecido en el jardín!")
                
                # Navigate to garden
                st.session_state.current_view = 'Jardín'
                st.session_state.wizard_step = 1
                st.rerun()

def render_letters():
    st.markdown("<h2 style='text-align: center; font-size: 2.5rem;'>Letters I Never Sent</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-style: italic; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;'>Escribe aquello que necesitas soltar. No tienes que enviarlo a nadie. Solo escríbelo, siéntelo y déjalo ir.</p>", unsafe_allow_html=True)

    # Note Paper styling
    st.markdown("""
        <style>
        .letter-container {
            background-color: #fcfaf5;
            border: 1px solid #e8e4d9;
            border-radius: 10px;
            padding: 30px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.02);
            position: relative;
            background-image: repeating-linear-gradient(transparent, transparent 31px, rgba(210, 180, 140, 0.2) 31px, rgba(210, 180, 140, 0.2) 32px);
            background-position: 0 40px;
        }
        .stTextArea textarea {
            min-height: 400px !important;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
            font-size: 1.2rem !important;
            line-height: 32px !important;
            padding-top: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='letter-container'>", unsafe_allow_html=True)
    letter_content = st.text_area("", placeholder="Querido...", label_visibility="collapsed", key="letter_input")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌬️ Soltar al viento", use_container_width=True):
            if letter_content.strip():
                st.success("La carta se ha ido con el viento. Has soltado este sentimiento.")
                # Note: Streamlit state clearing requires widget key manipulation or rerun trick
                # We show success, next interaction clears it natively.
            else:
                st.warning("Escribe algo antes de soltar.")
    with col2:
        if st.button("Guardar para mí", use_container_width=True):
             if letter_content.strip():
                st.info("Carta guardada en tu espacio privado (Demo).")
             else:
                st.warning("Escribe algo antes de guardar.")

def main():
    inject_custom_css()
    init_session_state()
    render_sidebar()

    # Top Banner
    st.markdown("<div class='bloom-banner'>Bloom of the Day: \"Describe tu día utilizando solamente tres colores.\"</div>", unsafe_allow_html=True)

    # View Router
    if st.session_state.current_view == 'Jardín':
        render_garden()
    elif st.session_state.current_view == 'Crear':
        render_create()
    elif st.session_state.current_view == 'Cartas':
        render_letters()

if __name__ == "__main__":
    main()