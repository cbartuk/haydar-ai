"""
H.A.Y.D.A.R. AI - Ultra Deluxe JARVIS Style UI
3D Pulsating Sphere with Audio-Reactive Animation
"""

import streamlit as st
import streamlit.components.v1 as components
import time
import os
import numpy as np
import plotly.graph_objects as go
from audio_input import listen_and_transcribe, WHISPER_MODEL
from tts_output import synthesize
from haydar_persona import haydar

# Sayfa yapılandırması
st.set_page_config(
    page_title="H.A.Y.D.A.R. AI - JARVIS Interface",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - JARVIS Dark Theme
st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom button styling */
    .stButton > button {
        width: 100%;
        height: 80px;
        background: linear-gradient(135deg, #00d4ff 0%, #0080ff 100%);
        color: white;
        font-size: 24px;
        font-weight: bold;
        border: none;
        border-radius: 50px;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.6);
        transition: all 0.3s ease;
        letter-spacing: 2px;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 50px rgba(0, 212, 255, 0.9);
    }

    /* Status text */
    .status-text {
        text-align: center;
        font-size: 20px;
        color: #00d4ff;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.8);
        margin: 20px 0;
        font-weight: 500;
    }

    /* Title */
    h1 {
        color: #00d4ff !important;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.6);
        font-weight: 300;
        letter-spacing: 8px;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00d4ff;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }

    /* History expanders */
    .streamlit-expanderHeader {
        background-color: rgba(0, 212, 255, 0.1);
        border-radius: 10px;
        color: #00d4ff;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1729 0%, #1a1f3a 100%);
    }

    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #0080ff 100%);
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'status' not in st.session_state:
    st.session_state.status = "READY"
if 'sphere_size' not in st.session_state:
    st.session_state.sphere_size = 1.0

# Sidebar - Ayarlar
with st.sidebar:
    st.markdown("### ⚙️ SYSTEM CONFIGURATION")

    st.markdown("---")
    st.markdown("**🤖 LLM Settings**")

    llm_model = st.selectbox(
        "Model",
        ["qwen2.5:7b", "llama3.1:8b", "gemma2:9b"],
        index=0
    )

    temperature = st.slider(
        "Temperature",
        0.0, 2.0, 0.7, 0.1,
        help="🔥 0.0=Robot, 0.7=Balanced, 2.0=Creative"
    )
    st.caption("💡 Lower = More consistent, Higher = More creative")

    st.markdown("---")
    st.markdown("**🎙️ Audio Settings**")

    recording_duration = st.slider(
        "Recording Duration (s)",
        3, 10, 5, 1
    )

    whisper_model = st.selectbox(
        "Whisper Model",
        ["base", "small", "medium", "large"],
        index=2
    )

    st.markdown("---")
    st.markdown("**📊 System Info**")
    st.code(f"""
GPU: CPU Mode
Model: {llm_model}
Temp: {temperature}
STT: Whisper {whisper_model}
TTS: Piper TR
    """)

# 3D JARVIS Sphere Function - PREMIUM QUALITY
def create_jarvis_sphere(size=1.0, camera_angle=0):
    """Create HIGH QUALITY 3D JARVIS sphere with animated Saturn rings and camera rotation"""
    # High resolution sphere (100x100 for smooth surface)
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = size * np.outer(np.cos(u), np.sin(v))
    y = size * np.outer(np.sin(u), np.sin(v))
    z = size * np.outer(np.ones(np.size(u)), np.cos(v))

    fig = go.Figure()

    # Main sphere with enhanced lighting
    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        colorscale=[
            [0, '#000d1a'],
            [0.3, '#002b5c'],
            [0.6, '#0066cc'],
            [1, '#00d4ff']
        ],
        showscale=False,
        opacity=0.85,
        lighting=dict(
            ambient=0.6,
            diffuse=0.9,
            specular=1.0,
            roughness=0.05,
            fresnel=0.6
        ),
        lightposition=dict(x=100, y=100, z=150),
        name='sphere',
        hoverinfo='skip'
    ))

    # Enhanced Saturn rings with glow effect (multiple layers)
    ring_configs = [
        # Main rings
        {'radius': size * 1.5, 'tilt_x': 20, 'tilt_y': 10, 'width': 4, 'opacity': 0.8, 'segments': 200},
        {'radius': size * 1.58, 'tilt_x': 20, 'tilt_y': 10, 'width': 3, 'opacity': 0.7, 'segments': 200},
        {'radius': size * 1.65, 'tilt_x': 20, 'tilt_y': 10, 'width': 2, 'opacity': 0.6, 'segments': 200},
        # Secondary rings for depth
        {'radius': size * 1.45, 'tilt_x': -15, 'tilt_y': 25, 'width': 3, 'opacity': 0.5, 'segments': 150},
        {'radius': size * 1.7, 'tilt_x': 15, 'tilt_y': -20, 'width': 2, 'opacity': 0.4, 'segments': 150},
    ]

    for ring in ring_configs:
        theta = np.linspace(0, 2 * np.pi, ring['segments'])

        # Create ring in XY plane
        ring_x = ring['radius'] * np.cos(theta)
        ring_y = ring['radius'] * np.sin(theta)
        ring_z = np.zeros_like(theta)

        # Apply 3D rotations
        tilt_x_rad = np.radians(ring['tilt_x'])
        tilt_y_rad = np.radians(ring['tilt_y'])

        # Rotate around X axis
        ring_y_rot = ring_y * np.cos(tilt_x_rad) - ring_z * np.sin(tilt_x_rad)
        ring_z_rot = ring_y * np.sin(tilt_x_rad) + ring_z * np.cos(tilt_x_rad)

        # Rotate around Y axis
        ring_x_final = ring_x * np.cos(tilt_y_rad) + ring_z_rot * np.sin(tilt_y_rad)
        ring_z_final = -ring_x * np.sin(tilt_y_rad) + ring_z_rot * np.cos(tilt_y_rad)

        # Add ring with glow
        fig.add_trace(go.Scatter3d(
            x=ring_x_final,
            y=ring_y_rot,
            z=ring_z_final,
            mode='lines',
            line=dict(
                color='#00d4ff',
                width=ring['width']
            ),
            opacity=ring['opacity'],
            showlegend=False,
            hoverinfo='skip'
        ))

    # Camera rotation for smooth animation
    cam_distance = 2.2
    cam_x = cam_distance * np.cos(np.radians(camera_angle))
    cam_y = cam_distance * np.sin(np.radians(camera_angle))
    cam_z = 1.5

    # Perfect sphere aspect ratio - CRITICAL for non-ellipsoid shape
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False, range=[-3, 3]),
            yaxis=dict(visible=False, range=[-3, 3]),
            zaxis=dict(visible=False, range=[-3, 3]),
            aspectmode='cube',  # CRITICAL: Forces equal aspect ratios
            camera=dict(
                eye=dict(x=cam_x, y=cam_y, z=cam_z),
                center=dict(x=0, y=0, z=0)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        showlegend=False,
        uirevision='constant'  # Prevents jarring resets
    )

    return fig

# Auto-play audio function
def autoplay_audio(file_path):
    """Auto-play audio using JavaScript"""
    import base64
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay>
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
        components.html(md, height=0)

# Main Layout
st.markdown("<h1>H.A.Y.D.A.R.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00d4ff; opacity: 0.7; letter-spacing: 4px;'>HAYATIN AKIŞINA YÖN VEREN DİNAMİK AKILLI REHBER</p>", unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("CONVERSATIONS", len(st.session_state.conversation_history))
with col2:
    st.metric("MODEL", llm_model.upper())
with col3:
    st.metric("STATUS", st.session_state.status)
with col4:
    st.metric("MODE", "ONLINE" if True else "OFFLINE")

st.markdown("---")

# Main content area
col_sphere, col_history = st.columns([2, 1])

with col_sphere:
    # JARVIS Sphere
    sphere_placeholder = st.empty()

    # Determine sphere size based on status (larger sizes for better visibility)
    if st.session_state.status == "LISTENING":
        sphere_size = 2.2
    elif st.session_state.status == "THINKING":
        sphere_size = 2.8
    elif st.session_state.status == "SPEAKING":
        sphere_size = 2.5
    else:
        sphere_size = 1.8

    sphere_fig = create_jarvis_sphere(size=sphere_size)
    sphere_placeholder.plotly_chart(sphere_fig, width='stretch', key='sphere_main')

    # Status text
    status_color = {
        "READY": "#00d4ff",
        "LISTENING": "#00ff88",
        "THINKING": "#ffaa00",
        "SPEAKING": "#ff00ff"
    }

    status_placeholder = st.empty()
    status_placeholder.markdown(f"<div class='status-text' style='color: {status_color.get(st.session_state.status, '#00d4ff')};'>{st.session_state.status}</div>", unsafe_allow_html=True)

    # Main button
    if st.button("🎙️  SPEAK TO HAYDAR", key="main_button"):
        try:
            # Update status to LISTENING
            st.session_state.status = "LISTENING"
            status_placeholder.markdown(f"<div class='status-text' style='color: {status_color.get('LISTENING', '#00ff88')};'>LISTENING</div>", unsafe_allow_html=True)
            sphere_placeholder.plotly_chart(create_jarvis_sphere(size=2.2), width='stretch', key='sphere_listening')
            # Record audio
            start_time = time.time()
            transcript = listen_and_transcribe()
            stt_duration = time.time() - start_time

            if not transcript or len(transcript.strip()) == 0:
                st.session_state.status = "READY"
                status_placeholder.markdown(f"<div class='status-text' style='color: {status_color.get('READY', '#00d4ff')};'>READY</div>", unsafe_allow_html=True)
                sphere_placeholder.plotly_chart(create_jarvis_sphere(size=1.8), width='stretch', key='sphere_ready_noaudio')
                st.warning("⚠️ No audio detected")
            else:
                # Update to THINKING
                st.session_state.status = "THINKING"
                status_placeholder.markdown(f"<div class='status-text' style='color: {status_color.get('THINKING', '#ffaa00')};'>THINKING</div>", unsafe_allow_html=True)
                sphere_placeholder.plotly_chart(create_jarvis_sphere(size=2.8), width='stretch', key='sphere_thinking')

                # Get LLM response
                llm_start = time.time()
                intent = haydar.detect_intent(transcript)
                canned = haydar.get_canned_response(intent)

                if canned:
                    response = canned
                    llm_duration = 0.0
                else:
                    try:
                        import ollama
                        messages = [{'role': 'system', 'content': haydar.get_system_prompt()}]
                        messages.extend(haydar.get_conversation_context())
                        messages.append({'role': 'user', 'content': transcript})

                        llm_response = ollama.chat(
                            model=llm_model,
                            messages=messages,
                            options={
                                'temperature': temperature,
                                'num_ctx': 2048  # Context window
                            }
                        )
                        response = llm_response['message']['content']
                        llm_duration = time.time() - llm_start

                    except Exception as e:
                        print(f"❌ LLM EXCEPTION: {type(e).__name__}: {e}")
                        import traceback
                        traceback.print_exc()
                        st.error(f"❌ LLM Error: {type(e).__name__}: {str(e)}")
                        response = "Üzgünüm efendim, bir hata oluştu. Lütfen tekrar deneyin."
                        llm_duration = time.time() - llm_start

                haydar.add_to_history(transcript, response)

                # Update to SPEAKING
                st.session_state.status = "SPEAKING"
                status_placeholder.markdown(f"<div class='status-text' style='color: {status_color.get('SPEAKING', '#ff00ff')};'>SPEAKING</div>", unsafe_allow_html=True)

                # Generate TTS
                try:
                    audio_path = synthesize(response, play_audio=False)
                except Exception as e:
                    st.error(f"❌ TTS Error: {e}")
                    audio_path = None

                # Add to history
                st.session_state.conversation_history.append({
                    'user': transcript,
                    'haydar': response,
                    'stt_duration': stt_duration,
                    'llm_duration': llm_duration,
                    'audio_path': audio_path
                })

                # Auto-play audio with smooth rotation + pulsing animation
                if audio_path and os.path.exists(audio_path):
                    autoplay_audio(audio_path)

                    # Smooth rotation animation with size pulsing
                    angles = [0, 30, 60, 90, 120, 150]
                    sizes = [2.5, 2.7, 2.6, 2.8, 2.6, 2.5]

                    for i, (angle, size) in enumerate(zip(angles, sizes)):
                        sphere_placeholder.plotly_chart(
                            create_jarvis_sphere(size=size, camera_angle=angle),
                            key=f'sphere_speaking_anim_{i}'
                        )
                        time.sleep(0.5)  # Smooth 360° rotation over 3 seconds

                # Reset status to READY
                st.session_state.status = "READY"
                status_placeholder.markdown(f"<div class='status-text' style='color: {status_color.get('READY', '#00d4ff')};'>READY</div>", unsafe_allow_html=True)
                sphere_placeholder.plotly_chart(create_jarvis_sphere(size=1.8), width='stretch', key='sphere_ready_final')

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state.status = "READY"
            status_placeholder.markdown(f"<div class='status-text' style='color: {status_color.get('READY', '#00d4ff')};'>READY</div>", unsafe_allow_html=True)
            sphere_placeholder.plotly_chart(create_jarvis_sphere(size=1.8), width='stretch', key='sphere_ready_error')

with col_history:
    st.markdown("### 📜 CONVERSATION LOG")

    if len(st.session_state.conversation_history) == 0:
        st.info("No conversations yet.\nSpeak to start.")
    else:
        # Show last 5 conversations
        for idx, conv in enumerate(reversed(st.session_state.conversation_history[-5:])):
            with st.expander(f"#{len(st.session_state.conversation_history) - idx}", expanded=(idx==0)):
                st.markdown(f"**YOU:** {conv['user']}")
                st.markdown(f"**HAYDAR:** {conv['haydar']}")
                st.caption(f"⏱️ {conv['stt_duration']:.1f}s + {conv['llm_duration']:.1f}s")

                # Audio replay
                if 'audio_path' in conv and conv['audio_path'] and os.path.exists(conv['audio_path']):
                    st.audio(conv['audio_path'], format='audio/wav')

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #00d4ff; opacity: 0.5; font-size: 12px;'>H.A.Y.D.A.R. v1.1 ULTRA | JARVIS INTERFACE | DESIGNED FOR EXCELLENCE</p>", unsafe_allow_html=True)
