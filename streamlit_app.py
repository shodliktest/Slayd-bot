"""
Streamlit Admin Panel for AI Slayd Bot
Web interface for monitoring and management
"""
import streamlit as st
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Slayd Bot - Admin Panel",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        padding: 20px;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Authentication
def check_password():
    """Simple password check"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        password = st.text_input("🔐 Admin Paroli", type="password")
        if st.button("Kirish"):
            if password == os.getenv("ADMIN_PASSWORD", "admin123"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Noto'g'ri parol!")
        return False
    return True

if not check_password():
    st.stop()

# Main interface
st.markdown('<div class="main-header">🎓 AI SLAYD BOT - Admin Panel</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f4e79/ffffff?text=AI+Slayd+Bot", use_container_width=True)
    st.markdown("---")
    
    page = st.radio(
        "📋 Menyu",
        ["📊 Dashboard", "📁 Kontent", "👥 Foydalanuvchilar", "⚙️ Sozlamalar", "📖 Yo'riqnoma"]
    )
    
    st.markdown("---")
    st.caption(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Dashboard
if page == "📊 Dashboard":
    st.header("📊 Statistika")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">0</div>
            <div>Jami Foydalanuvchilar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">0</div>
            <div>Yaratilgan Slaydlar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">0</div>
            <div>Bugungi So'rovlar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">✅</div>
            <div>Bot Holati</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📈 Oxirgi Faoliyat")
    st.info("Bot ishga tushgandan so'ng statistika bu yerda ko'rsatiladi.")

# Content page
elif page == "📁 Kontent":
    st.header("📁 Yaratilgan Kontent")
    
    tab1, tab2, tab3 = st.tabs(["📊 Slaydlar", "✍️ Esseylar", "❓ Testlar"])
    
    with tab1:
        st.info("Yaratilgan slaydlar bu yerda ko'rsatiladi.")
    
    with tab2:
        st.info("Yozilgan esseylar bu yerda ko'rsatiladi.")
    
    with tab3:
        st.info("Tuzilgan testlar bu yerda ko'rsatiladi.")

# Users page
elif page == "👥 Foydalanuvchilar":
    st.header("👥 Foydalanuvchilar")
    st.info("Foydalanuvchilar ro'yxati bu yerda ko'rsatiladi.")

# Settings page
elif page == "⚙️ Sozlamalar":
    st.header("⚙️ Sozlamalar")
    
    st.subheader("🤖 Bot Sozlamalari")
    st.text_input("Bot Token", value="***", type="password")
    st.text_input("Storage Channel ID", value="-1001234567890")
    
    st.subheader("🧠 AI Sozlamalari")
    ai_provider = st.selectbox("AI Provider", ["OpenAI", "Gemini"])
    st.text_input("API Key", type="password")
    
    if st.button("💾 Saqlash"):
        st.success("✅ Sozlamalar saqlandi!")

# Guide page
elif page == "📖 Yo'riqnoma":
    st.header("📖 Yo'riqnoma")
    
    st.markdown("""
    ### 🚀 Boshlash
    
    **1. Bot sozlash:**
    - `.streamlit/secrets.toml` faylida kerakli sozlamalarni kiriting
    - Bot tokenni [@BotFather](https://t.me/BotFather) dan oling
    - Storage channel yarating va bot'ni admin qiling
    
    **2. AI API sozlash:**
    - OpenAI API key: https://platform.openai.com/api-keys
    - Gemini API key: https://makersuite.google.com/app/apikey
    
    **3. Botni ishga tushirish:**
    ```bash
    python bot.py
    ```
    
    **4. Streamlit panelni ishga tushirish:**
    ```bash
    streamlit run streamlit_app.py
    ```
    
    ### 📚 Funksiyalar
    
    - ✅ **Slayd yaratish** - Professional PowerPoint taqdimotlar
    - ✅ **Essey yozish** - Akademik uslubda esseylar
    - ✅ **Test tuzish** - Savol-javobli testlar
    - ✅ **Referat** - To'liq strukturali referatlar
    - ✅ **Mustaqil ish** - Fan bo'yicha mustaqil ishlar
    - ✅ **Kurs ishi** - To'liq tadqiqot ishlari
    - ✅ **Maqola** - Ilmiy maqolalar
    - ✅ **Tezis** - Konferensiya tezislari
    
    ### 🆘 Yordam
    
    Savollar bo'lsa: @your_support
    """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: gray;">© 2024 AI Slayd Bot | Made with ❤️</div>',
    unsafe_allow_html=True
)
