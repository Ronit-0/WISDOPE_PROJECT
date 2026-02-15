import streamlit as st
import os
from PIL import Image

# 1. Force Dark Mode & Page Config
st.set_page_config(page_title="Wisdope Academy", page_icon="🔬", layout="wide")

def set_custom_style():
    # DIRECT LINK OPTIMIZATION:
    # Replace the placeholders below with your actual GitHub username
    bg_image_url = "https://raw.githubusercontent.com/Ronit-0/WISDOPE_PROJECT/main/images/IMG_8098.PNG"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rakkas&display=swap');

        /* Optimized Background Loading */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                        url("{bg_image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}

        /* Targeted Rakkas Font for WISDOPE Title with Swap display */
        .wisdope-brand {{
            font-family: 'Rakkas', serif;
            font-display: swap; 
            font-size: 72px !important;
            font-weight: 400;
            color: white;
            margin-bottom: -10px;
            line-height: 1;
        }}
        
        .mentor-name {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stTabs [data-baseweb="tab-list"] button {{
            color: white !important;
        }}

        a {{
            color: #FFD700 !important;
            text-decoration: underline !important;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

# Call the style function (No longer needs the file path as an argument)
set_custom_style()

# 2. Header Section
st.markdown('<p class="wisdope-brand">WISDOPE</p>', unsafe_allow_html=True)
st.write(" ")
st.markdown('<p class="mentor-name">By Rishav Karar</p>', unsafe_allow_html=True)
st.write("**MSc. (Biotech), R.A. (Pharmacognosy)**")
st.write("Coaching Classes for Maths, Physics, Chemistry & Biology")
st.write("---")

# 3. Main Features & Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Why Join Us?", "Course Details", "Gallery", "Contact & Location", "Join Wisdope"])

with tab1:
    st.header("Why join WISDOPE?")
    features = [
        "Theoretical explanations with experimentations.",
        "Hands-on laboratory training and theory classes for VIII-X & XI-XII.",
        "Comprehensive coaching with specialized NEET (UG) preparation.",
        "Special exams conducted for all Boards (I.C.S.E., C.B.S.E. & W.B.).",
        "Study mats for all classes.",
        "Two times lab research field visits in a year.",
        "One-on-one doubt clearing classes.",
        "6+ years teaching experience associated with Bose Informatics."
    ]
    for feature in features:
        st.write(f"✅ {feature}")

with tab2:
    col_x, col_y = st.columns(2)
    with col_x:
        st.header("Class Details")
        st.write("**Subjects Offered:**")
        st.write("* **Classes VIII-X:** Physics, Chemistry, and Biology (Theory and Practical)")
        st.write("* **Classes XI-XII:** Chemistry and Biology (Theory and Practical), and Physics (Practical only)")

with tab3:
    st.header("Some Glimpses of Our Coaching Institute")
    img_path = "images/IMG_8148.PNG"
    if os.path.exists(img_path):
        img = Image.open(img_path)
        st.image(img, caption="Students during theory and practical session", use_container_width=True)
    else:
        st.error("Error: Image not found.")

with tab4:
    st.header("📍 Visit or Contact Us")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("**Address:** 37, Dinu Lane, Kadamtala, Howrah-01")
        st.write("**Landmark:** Opp. Kadamtala Bus Stand near S.B. Jewellers")
        map_embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3684.348398031383!2d88.30456187515153!3d22.56608553322049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a02794eb0f59967%3A0x111e1f2a32657579!2sKadamtala%20Bus%20Stand!5e0!3m2!1sen!2sin!4v1708000000000!5m2!1sen!2sin"
        st.components.v1.html(f'<iframe src="{map_embed_url}" width="100%" height="250" style="border:0;" allowfullscreen="" loading="lazy"></iframe>', height=260)
        st.link_button("🌐 Open in Google Maps", "https://maps.google.com/?cid=4692063799864552313&g_mp=CiVnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLkdldFBsYWNl")
    
    with c2:
        st.write("### 📞 Quick Connect")
        st.link_button("📞 Call Rishav Sir", "tel:+919051965176")
        whatsapp_url = "https://wa.me/917044443309?text=Hello!%20I%20am%20interested%20in%20joining%20Wisdope%20Academy."
        st.link_button("💬 WhatsApp Message", whatsapp_url)
        st.write("**Email Us:**")
        st.markdown('<div style="background-color:rgba(0,0,0,0.5); padding:10px; border-radius:5px;">📧 <a href="mailto:rishav9101999@gmail.com">rishav9101999@gmail.com</a></div>', unsafe_allow_html=True)

    with c3:
        st.header("Batch Timings")
        st.write("🌅 **Morning:** 7:00 AM - 10:00 AM")
        st.write("🌆 **Evening:** 5:00 PM - 10:00 PM")
        
    st.write("---")
    st.write("### Follow Us On:")
    s1, s2, s3, s4, s5 = st.columns(5)
    with s1: st.markdown("[![FB](https://img.icons8.com/color/48/facebook-new.png)](https://www.facebook.com/profile.php?id=61573780375951)")
    with s2: st.markdown("[![IG](https://img.icons8.com/color/48/instagram-new.png)](https://www.instagram.com/rishavkarar.09)")
    with s3: st.markdown("[![WA](https://img.icons8.com/color/48/whatsapp.png)](https://wa.me/917044443309)")
    with s4: st.markdown("[![LI](https://img.icons8.com/color/48/linkedin.png)](https://linkedin.com)")
    with s5: st.markdown("[![YT](https://img.icons8.com/color/48/youtube-play.png)](https://youtube.com)")

with tab5:
    st.header("📝 Student Registration")
    st.write("Ready to start? Fill out the form below.")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.link_button("🚀 Open Registration Form", "https://forms.gle/your-actual-google-form-link", use_container_width=True)
    with col2:
        st.link_button("💬 WhatsApp Support", whatsapp_url)

st.divider()
st.caption("© 2026 Wisdope Academy | Associated with Bose Informatics")
