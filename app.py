import streamlit as st
import os
import base64

# 1. Force Dark Mode & Page Config
st.set_page_config(page_title="Wisdope Academy", page_icon="🔬", layout="wide")

def set_custom_style(main_bg):
    # Convert image to base64 for background
    with open(main_bg, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rakkas&display=swap');

        /* Force Dark Mode UI */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                        url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}

        /* Targeted Rakkas Font for WISDOPE Title */
        .wisdope-brand {{
            font-family: 'Rakkas', serif;
            font-size: 72px !important;
            font-weight: 400;
            color: white;
            margin-bottom: -10px;
            line-height: 1;
        }}
        
        /* Subheader styling to match */
        .mentor-name {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        /* Fix visibility of tabs in dark mode */
        .stTabs [data-baseweb="tab-list"] button {{
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# Call the style function with your image
set_custom_style("images/IMG_8098.PNG")
# 2. Header Section (Cleaned up - no extra title)
st.markdown('<p class="wisdope-brand">WISDOPE</p>', unsafe_allow_html=True)
st.write(" ")
st.markdown('<p class="mentor-name">By Rishav Karar</p>', unsafe_allow_html=True)
st.write("**MSc. (Biotech), R.A. (Pharmacognosy)**")
st.write("Coaching Classes for Maths, Physics, Chemistry & Biology")
st.write("---")
# 3. Main Features & Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Why Join Us?", "Course Details", "Gallery", "Contact & Location","Join Wisdope"])

# --- TAB 1: WHY JOIN WISDOPE? (Detailed from Image 3) ---
with tab1:
    st.header("Why join WISDOPE?")
    features = [
        "Theoretical explanations with experimentations.",
        "Hands-on laboratory training and theory classes in Physics, Chemistry and Biology for classes VIII-X; Chemistry and Biology(Theory and Practical), and Physics(Practical Only) for classes XI-XII.",
        "Comprehensive coaching covering regular academic syllabus along with specialized NEET (UG) preparation.",
        "Special exams conducted for all Boards (I.C.S.E./I.S.C., C.B.S.E. & W.B.B.S.E./W.B.B.H.S.E.).",
        "Study mats for all classes.",
        "Two times lab research field visits in a year.",
        "Special and one-on-one doubt clearing classes are taken.",
        "Teaching experience of over 6 years and associated with Bose Informatics (Plant Chemistry)."
    ]
    for feature in features:
        st.write(f"✅ {feature}")

# --- TAB 2: CLASS DETAILS (Detailed from Images 1 & 3) ---
with tab2:
    col_x, col_y = st.columns(2)
    with col_x:
        st.header("Class Details")
        st.write("**Subjects Offered:**")
        st.write("* **Classes VIII-X:** Physics, Chemistry, and Biology (Theory and Practical)")
        st.write("* **Classes XI-XII:** Chemistry and Biology (Theory and Practical), and Physics (Practical only)")
    
from PIL import Image
import os

# --- TAB 3: GALLERY ---
with tab3:
    st.header("Some Glimpses of Our Coaching Institute")
    
    # Define the exact path
    img_path = "images/IMG_8148.PNG"
    
    if os.path.exists(img_path):
        # Open using PIL for better compatibility
        img = Image.open(img_path)
        st.image(img, caption="Students during theory and practical session", use_container_width=True)
    else:
        st.error(f"Error: Could not find image at {img_path}. Check your folder name and file case!")
# --- TAB 5: CONTACT & LOCATION (Detailed from Image 1) ---
with tab4:
    st.header("📍 Visit or Contact Us")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("**Address:**")
        st.write("37, Dinu Lane, Kadamtala, Howrah-01")
        st.write("**Landmark:**")
        st.write("Opp. Kadamtala Bus Stand near S.B. Jewellers")
        # --- FIXED MAP WINDOW ---
        st.write("**Location Map:**")
        # Direct embed link centered on Kadamtala Bus Stand area
        map_embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3684.348398031383!2d88.30456187515153!3d22.56608553322049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a02794eb0f59967%3A0x111e1f2a32657579!2sKadamtala%20Bus%20Stand!5e0!3m2!1sen!2sin!4v1708000000000!5m2!1sen!2sin"
        
        st.components.v1.html(f"""
            <iframe src="{map_embed_url}" 
            width="100%" height="250" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
        """, height=260)
        st.link_button("🌐 Open in Google Maps", "https://maps.google.com/?cid=4692063799864552313&g_mp=CiVnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLkdldFBsYWNl")
    
    
    with c2:
        st.write("### 📞 Quick Connect")
        st.write("9051965176 (Call Only)")
        # Call Button
        # The 'tel:' link opens the phone's dialer automatically
        st.link_button("📞 Call Rishav Sir", "tel:+919051965176")
        
        st.write("") # Add some spacing
        st.write("7044443309 (Whatsapp Only)")
        # WhatsApp Button
        # The 'wa.me' link opens WhatsApp with a pre-filled message
        whatsapp_msg = "Hello! I am interested in joining Wisdope Academy. Please provide more details."
        # We replace spaces with %20 for the URL to work correctly
        whatsapp_url = f"https://wa.me/917044443309?text={whatsapp_msg.replace(' ', '%20')}"
        st.link_button("💬 WhatsApp Message", whatsapp_url)
        
        
        st.write("**Email Us:**")
        # Wrapping in a div with background to ensure visibility
        st.markdown('<div style="background-color:rgba(0,0,0,0.5); padding:10px; border-radius:5px;">📧 <a href="mailto:rishav9101999@gmail.com">rishav9101999@gmail.com</a></div>', unsafe_allow_html=True)

    with c3:
        st.header("Batch Timings (Mon-Sat)")
        st.write("🌅 **Morning Batch:** 7:00 AM - 10:00 AM")
        st.write("🌆 **Evening Batch:** 5:00 PM - 10:00 PM")
    st.write("---")
    st.write("### Follow Us On:")
    
    # Creating 4 small columns for social icons
    s1, s2, s3, s4, s5 = st.columns(5)
    
    with s1:
        st.markdown("[![Facebook](https://img.icons8.com/color/48/facebook-new.png)](https://www.facebook.com/profile.php?id=61573780375951)")
    with s2:
        st.markdown("[![Instagram](https://img.icons8.com/color/48/instagram-new.png)](https://www.instagram.com/rishavkarar.09?igsh=MXVkYXdiN3B6amwybQ==)")
    with s3:
        st.markdown("[![WhatsApp](https://img.icons8.com/color/48/whatsapp.png)](https://wa.me/917044443309)")
    with s4:
        st.markdown("[![LinkedIn](https://img.icons8.com/color/48/linkedin.png)](https://linkedin.com/in/your-profile-link)")
    with s5:
        st.markdown("[![YouTube](https://img.icons8.com/color/48/youtube-play.png)](https://youtube.com/@your-channel-link)")

# --- TAB 6: REGISTRATION (NEW) ---
with tab5:
    st.header("📝 Student Registration")
    st.write("Ready to start your journey with Wisdope Academy? Please fill out the form below to secure your seat.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        **What happens next?**
        1. After you submit the form, Rishav Sir will review your details.
        2. You will receive a call or WhatsApp message within 24 hours.
        3. We will discuss batch availability and the start date.
        """)
        
        # Replace the URL below with your actual Google Form link
        google_form_url = "https://forms.gle/your-actual-google-form-link"
        
        st.link_button("🚀 Open Registration Form", google_form_url, use_container_width=True)

    with col2:
        st.write("### Need Help?")
        st.write("If you face any issues while filling the form, contact us directly:")
        st.link_button("💬 WhatsApp Support", whatsapp_url)
# 4. Footer
st.divider()
st.caption("© 2026 Wisdope Academy | Associated with Bose Informatics")
