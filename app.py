import streamlit as st
import os
from PIL import Image

# 1. Force Dark Mode & Page Config
st.set_page_config(page_title="Wisdope Academy", page_icon="🔬", layout="wide")

def set_custom_style():
    bg_image_url = "https://raw.githubusercontent.com/Ronit-0/WISDOPE_PROJECT/main/images/IMG_8098.PNG"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rakkas&display=swap');

        /* 1. Remove the Top Header (GitHub menu, Fork, etc.) */
        header {{visibility: hidden;}}
        
        /* 2. Remove the Bottom Footer (Made with Streamlit) */
        footer {{visibility: hidden;}}
        
        /* 3. Remove the padding at the top of the page */
        .block-container {{
            padding-top: 2rem;
        }}

        /* Existing background and font styles */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                        url("{bg_image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}

        .wisdope-brand {{
            font-family: 'Rakkas', serif;
            font-display: swap; 
            font-size: 72px !important;
            color: white;
            margin-bottom: -10px;
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Why Join Us?", "Course Details", "Gallery", "Contact & Location", "Join Wisdope" , "Student Login"])

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
        st.write("9051965176 (Call Only)")
        st.link_button("📞 Call Rishav Sir", "tel:+919051965176")
        whatsapp_url = "https://wa.me/917044443309?text=Hello!%20I%20am%20interested%20in%20joining%20Wisdope%20Academy."
        st.write("") # Add some spacing
        st.write("7044443309 (Whatsapp Only)")
        st.link_button("💬 WhatsApp Message", whatsapp_url)
        st.write("**Email Us:**")
        st.markdown('<div style="background-color:rgba(0,0,0,0.5); padding:10px; border-radius:5px;">📧 <a href="mailto:rishav9101999@gmail.com">rishav9101999@gmail.com</a></div>', unsafe_allow_html=True)

    with c3:
        st.header("Batch Timings")
        st.write("🌅 **Morning:** 7:00 AM - 10:00 AM")
        st.write("🌆 **Evening:** 5:00 PM - 10:00 PM")
        
    st.write("---")
    st.write("### Follow Us On:")
    s1, s2, s3, s4, s5, s6 = st.columns(6)
    with s1: st.markdown("[![FB](https://img.icons8.com/color/48/facebook-new.png)](https://www.facebook.com/profile.php?id=61573780375951)")
    with s2: st.markdown("[![IG](https://img.icons8.com/color/48/instagram-new.png)](https://www.instagram.com/rishavkarar.09/)")
    with s3: st.markdown("[![Threads](https://img.icons8.com/ios-filled/48/ffffff/threads.png)](https://www.threads.net/@rishavkarar.09)")
    with s4: st.markdown("[![WA](https://img.icons8.com/color/48/whatsapp.png)](https://wa.me/917044443309)")
    with s5: st.markdown("[![LI](https://img.icons8.com/color/48/linkedin.png)](https://linkedin.com)")
    with s6: st.markdown("[![YT](https://img.icons8.com/color/48/youtube-play.png)](https://youtube.com)")

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
        google_form_url = "https://forms.gle/ksZPZTy19kCnuPZg7"
        
        st.link_button("🚀 Open Registration Form", google_form_url, use_container_width=True)

    with col2:
        st.write("### Need Help?")
        st.write("If you face any issues while filling the form, contact us directly:")
        st.link_button("💬 WhatsApp Support", whatsapp_url)
# --- TAB 6: STUDENT PORTAL ---
with tab6:
    st.header("🔐 Student Portal")
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.info("Log in to access your study materials and NEET (UG) preparation guides.")
        
        with st.form("login_form"):
            # Force lowercase to prevent case-sensitive email errors
            login_email = st.text_input("Registered Email Address").strip().lower()
            login_pass = st.text_input("8-digit Password", type="password").strip()
            submit_button = st.form_submit_button("Access Portal")
            
            if submit_button:
                if login_email and login_pass:
                    try:
                        from streamlit_gsheets import GSheetsConnection
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        
                        df = conn.read(worksheet="Registration")
                        
                        # CLEANING 1: Remove accidental spaces from Google Form column names
                        df.columns = df.columns.str.strip()
                        
                        # CLEANING 2: Handle duplicate columns
                        df.columns = [f"{col}_{i}" if list(df.columns).count(col) > 1 else col for i, col in enumerate(df.columns)]
                        
                        # CLEANING 3: The "Invisible Decimal" Fix
                        # We force the sheet passwords to strings and cut off the ".0" if Python added it
                        sheet_emails = df['Email Address'].astype(str).str.strip().str.lower()
                        sheet_passwords = df['Password'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
                        
                        # Verify the user
                        user_match = df[
                            (sheet_emails == login_email) & 
                            (sheet_passwords == login_pass)
                        ]
                        
                        if not user_match.empty:
                            st.session_state.logged_in = True
                            st.session_state.user_name = user_match.iloc[0]["Student's Full Name"]
                            st.session_state.user_class = user_match.iloc[0]["Current Class/Grade Level"]
                            st.rerun()
                        else:
                            st.error("Invalid email or password. Please try again.")
                            
                    except Exception as e:
                        st.error(f"Debug Error: {str(e)}")
                else:
                    st.warning("Please enter both fields.")
    else:
        # Dashboard for logged-in students
        st.success(f"Welcome back to Wisdope Academy, {st.session_state.user_name}!")
        current_class = st.session_state.user_class
        st.write(f"**Batch:** {current_class}")
        st.write("---")
        # --- NEW: VIRTUAL NOTICE BOARD ---
        st.subheader("📢 Notice Board")
        st.caption("Latest updates and announcements from Rishav Sir.")
        
        # Your live Google Doc Notice Board link
        notice_board_url = "https://docs.google.com/document/d/e/2PACX-1vSG_rBv2zgRwC6orBZfr_mAoYVMjSJAOQYXdQlfkqsw6SdupJ78xo46rS4GTiJc4QmzPI1MplgRgIzQ/pub?embedded=true" 
        
        import streamlit.components.v1 as components
        # Height is set to 400 so students can scroll through announcements easily
        components.iframe(notice_board_url, width=1000, height=400, scrolling=True)
        
        st.write("---")
        # 1. Nested Dictionary: Class -> Subject -> Drive Link
        # Replace the "PASTE_LINK_HERE" with your actual Google Drive embed URLs
        course_materials = {
            "XII": {
                "Physics": "PASTE_XII_PHYSICS_LINK_HERE",
                "Chemistry": "PASTE_XII_CHEMISTRY_LINK_HERE",
                "Biology": "PASTE_XII_BIOLOGY_LINK_HERE",
                "Mathematics": "https://drive.google.com/file/d/1B58sglLGi7p05Aj6dudXx5YF7jmq449m/preview"
            },
            "XI": {
                "Physics": "PASTE_XI_PHYSICS_LINK_HERE",
                "Chemistry": "PASTE_XI_CHEMISTRY_LINK_HERE",
                "Biology": "PASTE_XI_BIOLOGY_LINK_HERE"
            },
            "X": {
                "Science": "PASTE_X_SCIENCE_LINK_HERE",
                "Mathematics": "PASTE_X_MATH_LINK_HERE",
                "English": "PASTE_X_ENGLISH_LINK_HERE"
            },
            "IX": {
                "Science": "PASTE_IX_SCIENCE_LINK_HERE",
                "Mathematics": "PASTE_IX_MATH_LINK_HERE"
            },
            "VIII": {
                "Science": "PASTE_VIII_SCIENCE_LINK_HERE",
                "Mathematics": "PASTE_VIII_MATH_LINK_HERE"
            }
        }
        
        # 2. Check if the student's class exists in our database
        if current_class in course_materials:
            st.subheader("📚 Select Your Subject")
            
            # Get the list of subjects available for this specific student's class
            available_subjects = list(course_materials[current_class].keys())
            
            # 3. Create a dropdown menu for the student to choose a subject
            selected_subject = st.selectbox("Choose a subject to view materials:", available_subjects)
            
            if selected_subject:
                st.write(f"### 📖 {selected_subject} Materials")
                st.caption("These materials are view-only and cannot be downloaded.")
                
                # Fetch the exact link for that Class + Subject combination
                embed_url = course_materials[current_class][selected_subject]
                
                # Embed the secure Google Drive file
                import streamlit.components.v1 as components
                components.iframe(embed_url, width=700, height=600)
                
        else:
            st.info(f"Study materials for Class {current_class} are currently being compiled.")
        
        st.write("---")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()
st.divider()
st.caption("© 2026 Wisdope Academy | Associated with Bose Informatics")
