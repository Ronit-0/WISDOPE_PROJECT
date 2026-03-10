import streamlit as st
import os
from PIL import Image
import requests
import base64
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time
import json

# 1. Force Dark Mode & Page Config
st.set_page_config(page_title="Wisdope Academy", page_icon="🔬", layout="wide")

def set_custom_style():
    bg_image_url = "https://raw.githubusercontent.com/Ronit-0/WISDOPE_PROJECT/main/images/IMG_8098.png"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rakkas&display=swap');

        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .block-container {{ padding-top: 2rem; }}

        [kind="primary"] p, [kind="primary"] span, [kind="primary"] div {{
            color: black !important;
            font-weight: 800 !important;
        }}

        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), url("{bg_image_url}");
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
    
set_custom_style()

# 2. Header Section
st.markdown('<p class="wisdope-brand">WISDOPE</p>', unsafe_allow_html=True)
st.write(" ")
st.markdown('<p class="mentor-name">By Rishav Karar</p>', unsafe_allow_html=True)
st.write("**MSc. (Biotech), R.A. (Pharmacognosy)**")
st.write("Coaching Classes for Maths, Physics, Chemistry & Biology")
st.write("---")

# ==========================================
#         URGENT NEWS TICKER (GLOBAL)
# ==========================================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # SMART CACHE: Remembers news for 60 seconds
    news_df = conn.read(worksheet="News", ttl=60) 
    
    if not news_df.empty:
        msg = str(news_df.iloc[0]["Message"]).strip()
        exp_str = str(news_df.iloc[0]["Expiration"]).strip()
        
        if msg and msg.lower() != "nan" and exp_str and exp_str.lower() != "nan":
            from datetime import datetime, timedelta
            exp_dt = pd.to_datetime(exp_str)
            ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
            
            if ist_now < exp_dt:
                st.markdown(f"""
                <div style="background-color: #ff0000; color: white; padding: 10px; font-size: 18px; font-weight: bold; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(255,0,0,0.4);">
                    <marquee behavior="scroll" direction="left" scrollamount="8">🚨 URGENT NEWS: {msg}</marquee>
                </div>
                """, unsafe_allow_html=True)
except Exception:
    pass 

# ==========================================
#       PERSISTENT SESSION MANAGER
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in and "session_token" in st.query_params:
    try:
        token = st.query_params["session_token"]
        decoded_bytes = base64.b64decode(token.encode('utf-8'))
        session_data = json.loads(decoded_bytes.decode('utf-8'))
        
        if time.time() < session_data["expiry"]:
            st.session_state.logged_in = True
            st.session_state.user_name = session_data["name"]
            st.session_state.user_class = session_data["class"]
            st.session_state.user_board = session_data.get("board", "")
            st.session_state.user_dob = session_data.get("dob", "")
        else:
            del st.query_params["session_token"]
    except:
        del st.query_params["session_token"]

if st.session_state.logged_in:
    expiry_time = time.time() + 600 
    session_data = {
        "name": st.session_state.user_name,
        "class": st.session_state.user_class,
        "board": st.session_state.get("user_board", ""),
        "dob": st.session_state.get("user_dob", ""),
        "expiry": expiry_time
    }
    token_bytes = json.dumps(session_data).encode('utf-8')
    st.query_params["session_token"] = base64.b64encode(token_bytes).decode('utf-8')

# ==========================================
#               PUBLIC WEBSITE
# ==========================================
if not st.session_state.logged_in:
    tab1, tab2, tab3, tab_team, tab_leader, tab4, tab5, tab6 = st.tabs([
        "🌟 Why Join Us?", 
        "📚 Course Details", 
        "📸 Gallery", 
        "🔮 Our Team",
        "🏆 Leaderboard", 
        "📍 Contact & Location", 
        "🚀 Join Wisdope", 
        "🔐 Student Login"
    ])

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
        st.header("📸 Some Glimpses of Our Coaching Institute")
        st.write("---")
        try:
            # THIS IS FIXED: Moved outside the HTML string
            import streamlit.components.v1 as components 
            conn = st.connection("gsheets", type=GSheetsConnection)
            gallery_df = conn.read(worksheet="Gallery", usecols=[0], ttl=60)
            gallery_images = gallery_df["Image_URL"].dropna().tolist()
            
            if len(gallery_images) == 0:
                st.info("No photos uploaded yet. Check back soon!")
            else:
                slides_html = ""
                for i, img_url in enumerate(gallery_images):
                    slides_html += f'''
                    <div class="mySlides fade">
                        <img src="{img_url}" style="width:100%; max-height: 500px; object-fit: contain; border-radius: 8px;">
                        <div class="numbertext" style="color: white; padding: 8px; position: absolute; top: 0; background: rgba(0,0,0,0.5); border-radius: 8px;">{i+1} / {len(gallery_images)}</div>
                    </div>
                    '''
                
                full_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                * {{box-sizing: border-box; font-family: sans-serif;}}
                body {{ margin: 0; background-color: transparent; }}
                .slideshow-container {{ max-width: 1000px; position: relative; margin: auto; }}
                .mySlides {{ display: none; text-align: center; }}
                .prev, .next {{ cursor: pointer; position: absolute; top: 50%; width: auto; padding: 16px; margin-top: -22px; color: white; font-weight: bold; font-size: 24px; transition: 0.3s ease; border-radius: 0 3px 3px 0; user-select: none; background-color: rgba(0,0,0,0.6); text-decoration: none;}}
                .next {{ right: 0; border-radius: 3px 0 0 3px; }}
                .prev {{ left: 0; }}
                .prev:hover, .next:hover {{ background-color: rgba(0,0,0,0.9); }}
                .fade {{ animation-name: fade; animation-duration: 1.5s; }}
                @keyframes fade {{ from {{opacity: .4}} to {{opacity: 1}} }}
                </style>
                </head>
                <body>
                <div class="slideshow-container">
                  {slides_html}
                  <a class="prev" onclick="plusSlides(-1)">❮</a>
                  <a class="next" onclick="plusSlides(1)">❯</a>
                </div>
                <script>
                let slideIndex = 1; let timer; showSlides(slideIndex);
                function plusSlides(n) {{ clearTimeout(timer); showSlides(slideIndex += n); }}
                function showSlides(n) {{
                  let i; let slides = document.getElementsByClassName("mySlides");
                  if (!slides.length) return;
                  if (n > slides.length) {{slideIndex = 1}}    
                  if (n < 1) {{slideIndex = slides.length}}
                  for (i = 0; i < slides.length; i++) {{ slides[i].style.display = "none"; }}
                  slides[slideIndex-1].style.display = "block";  
                  timer = setTimeout(() => plusSlides(1), 10000); 
                }}
                </script>
                </body>
                </html>
                """
                components.html(full_html, height=550)
        except Exception as e:
            img_path = "images/IMG_8148.PNG"
            import os
            from PIL import Image
            if os.path.exists(img_path):
                st.image(Image.open(img_path), caption="Students during theory and practical session", use_container_width=True)
                
    with tab_team:
        st.header("🔮 Meet the Wisdope Team")
        st.write("The elite professionals working behind the scenes to bring you the best education.")
        st.write("---")
        
        team_html = """
        <style>
        .team-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 25px;
            padding: 20px 10px;
        }
        .team-card {
            background: linear-gradient(145deg, #13111C, #1C1829);
            border-radius: 16px;
            padding: 25px 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(138, 43, 226, 0.15);
            border: 1px solid rgba(138, 43, 226, 0.3);
            border-top: 4px solid #8A2BE2;
            width: 250px;
            transition: transform 0.4s ease, box-shadow 0.4s ease, border-color 0.4s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }
        .team-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 25px rgba(138, 43, 226, 0.5);
            border-color: #8A2BE2;
        }
        .team-img {
            width: 110px;
            height: 110px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #00E5FF;
            margin-bottom: 15px;
            background-color: #0f0f1b;
            transition: transform 0.4s ease, box-shadow 0.4s ease;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
        }
        .team-card:hover .team-img {
            transform: scale(1.08) rotate(3deg);
            box-shadow: 0 0 25px rgba(0, 229, 255, 0.6);
        }
        .team-name {
            color: #F8F9FA;
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 5px;
            margin-top: 0;
            letter-spacing: 0.5px;
        }
        .team-role {
            color: #00E5FF;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0px;
            margin-top: 0;
            min-height: 40px; 
            display: flex;
            align-items: center;
            justify-content: center;
            transition: margin-bottom 0.4s ease;
        }
        .team-card:hover .team-role {
            margin-bottom: 12px;
        }
        .team-desc {
            color: #B0A8B9;
            font-size: 14px;
            line-height: 1.5;
            max-height: 0;
            opacity: 0;
            overflow: hidden;
            margin: 0;
            transition: all 0.4s ease-in-out;
        }
        .team-card:hover .team-desc {
            max-height: 150px;
            opacity: 1;
            margin-top: 0px;
        }
        </style>
        <div class="team-container">
            <div class="team-card">
                <img class="team-img" src="https://img.icons8.com/3d-fluency/150/businessman.png" alt="Rishav Sir">
                <h3 class="team-name">Rishav Karar</h3>
                <div class="team-role">Founder & Lead Educator</div>
                <p class="team-desc">R.A. (Pharmacognosy). 6+ years of teaching experience, guiding students to excellence.</p>
            </div>
            <div class="team-card">
                <img class="team-img" src="https://img.icons8.com/3d-fluency/150/stethoscope.png" alt="Doctor">
                <h3 class="team-name">Soumyadeep Mondal</h3>
                <div class="team-role">Medical Advisor</div>
                <p class="team-desc">Doctor at Jadavpur Hospital. Bringing real-world medical insights and expert guidance.</p>
            </div>
            <div class="team-card">
                <img class="team-img" src="https://img.icons8.com/3d-fluency/150/manager.png" alt="Secretary">
                <h3 class="team-name">Gouranga Biswas</h3>
                <div class="team-role">Academy Secretary</div>
                <p class="team-desc">Managing operations, administration, and ensuring the academy runs smoothly day-to-day.</p>
            </div>
            <div class="team-card">
                <img class="team-img" src="https://img.icons8.com/3d-fluency/150/commercial.png" alt="Media Consultant">
                <h3 class="team-name">Suhina Karar</h3>
                <div class="team-role">Media Consultant</div>
                <p class="team-desc">Handling social media, digital presence, and connecting Wisdope Academy with the world.</p>
            </div>
            <div class="team-card">
                <img class="team-img" src="https://img.icons8.com/3d-fluency/150/user-male-circle.png" alt="Ronit Das">
                <h3 class="team-name">Ronit Das</h3>
                <div class="team-role">Digital Architect</div>
                <p class="team-desc">The technical mastermind behind the Wisdope digital platform and Learning Management System.</p>
            </div>
        </div>
        """
        st.markdown(team_html, unsafe_allow_html=True)
        
    with tab_leader:
        st.header("🌟 Wisdope Hall of Fame")
        st.write("Recognizing outstanding performance, hard work, and dedication!")
        st.write("---")
        
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            leader_df = conn.read(worksheet="Leaderboard", ttl=60) 
            
            if not leader_df.empty and str(leader_df.iloc[0]["Name"]).lower() not in ["nan", "none", ""]:
                star_name = str(leader_df.iloc[0]["Name"]).strip()
                star_batch = str(leader_df.iloc[0]["Batch"]).strip()
                star_msg = str(leader_df.iloc[0]["Message"]).strip()
                
                star_img = ""
                if "Image_URL" in leader_df.columns:
                    val = str(leader_df.iloc[0]["Image_URL"]).strip()
                    if val.lower() not in ["nan", "none", ""]:
                        star_img = val
                
                img_html = f'<img src="{star_img}" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 4px solid #FFD700; margin-bottom: 10px;">' if star_img else '<h1 style="margin-bottom: 0px; font-size: 60px;">🏆</h1>'
                
                st.markdown(f"""
                <div style="display: flex; justify-content: center; margin-top: 20px;">
                    <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 4px; border-radius: 15px; width: 100%; max-width: 600px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.5);">
                        <div style="background-color: #262626; padding: 40px 20px; border-radius: 12px;">
                            {img_html}
                            <h2 style="color: white; margin-top: 10px; margin-bottom: 5px; font-size: 32px;">{star_name}</h2>
                            <h4 style="color: #FFD700; margin-top: 0px; font-size: 18px;">Batch: {star_batch}</h4>
                            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255,215,0,0.3);">
                                <p style="color: #E0E0E0; font-size: 18px; font-style: italic; margin-bottom: 0px;">"{star_msg}"</p>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("The Star Student of the month will be announced soon! Keep studying hard. 📚")
        except Exception:
            st.info("The Star Student of the month will be announced soon! Keep studying hard. 📚")
    
    with tab4:
        st.header("📍 Visit or Contact Us")
        st.write("**Address:** 37, Dinu Lane, Kadamtala, Howrah-01")
        st.write("**Landmark:** Opp. Kadamtala Bus Stand near S.B. Jewellers")
        
        map_embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3684.348398031383!2d88.30456187515153!3d22.56608553322049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a02794eb0f59967%3A0x111e1f2a32657579!2sKadamtala%20Bus%20Stand!5e0!3m2!1sen!2sin!4v1708000000000!5m2!1sen!2sin"
        st.markdown(
            f'''
            <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                <iframe src="{map_embed_url}" style="width: 100%; max-width: 800px; height: 350px; border:none; border-radius: 8px;" allowfullscreen="" loading="lazy"></iframe>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        st.link_button("🌐 Open in Google Maps", "https://maps.google.com/?cid=4692063799864552313&g_mp=CiVnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLkdldFBsYWNl", use_container_width=True)
        st.write("---")
        st.write("### 📞 Quick Connect")
        st.write("9051965176 (Call Only)")
        st.link_button("📞 Call Rishav Sir", "tel:+919051965176", use_container_width=True)
        st.write("") 
        st.write("7044443309 (Whatsapp Only)")
        whatsapp_url = "https://wa.me/917044443309?text=Hello!%20I%20am%20interested%20in%20joining%20Wisdope%20Academy."
        st.link_button("💬 WhatsApp Message", whatsapp_url, use_container_width=True)
        st.write("**Email Us:**")
        st.markdown('<div style="background-color:rgba(0,0,0,0.5); padding:10px; border-radius:5px;">📧 <a href="mailto:rishav9101999@gmail.com" style="color: white; text-decoration: none;">rishav9101999@gmail.com</a></div>', unsafe_allow_html=True)
        st.write("---")
        st.write("### ⏳ Batch Timings")
        st.write("🌅 **Morning:** 7:00 AM - 10:00 AM")
        st.write("🌆 **Evening:** 5:00 PM - 10:00 PM")

    with tab5:
        st.header("📝 Student Registration")
        st.write("Ready to start your journey with Wisdope Academy? Please fill out the form below to secure your seat.")
        st.write("") 
        st.write("""
        **What happens next?**
        1. After you submit the form, Rishav Sir will review your details.
        2. You will receive a call or WhatsApp message within 24 hours.
        3. We will discuss batch availability and the start date.
        """)
        st.write("") 
        google_form_url = "https://forms.gle/ksZPZTy19kCnuPZg7"
        st.link_button("🚀 Open Registration Form", google_form_url, type="primary", use_container_width=True)
        st.write("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write("### Need Help?")
            st.write("If you face any issues while filling the form, contact us directly:")
            st.link_button("💬 WhatsApp Support", whatsapp_url, use_container_width=True)

    with tab6:
        st.header("🔐 Student Login")
        st.info("Log in to access your private portal and study materials.")
        
        with st.form("login_form"):
            login_email = st.text_input("Registered Email Address").strip().lower()
            login_pass = st.text_input("Password", type="password").strip()
            submit_button = st.form_submit_button("Access Portal")
            
            if submit_button:
                if login_email and login_pass:
                    if login_email == st.secrets["admin"]["email"] and login_pass == st.secrets["admin"]["password"]:
                        st.session_state.logged_in = True
                        st.session_state.user_name = "Rishav Sir"
                        st.session_state.user_class = "ADMIN"
                        st.session_state.user_board = "ADMIN"
                        st.rerun()
                    else:
                        try:
                            conn = st.connection("gsheets", type=GSheetsConnection)
                            df = conn.read(worksheet="Students", ttl=60) 
                            df.columns = df.columns.str.strip()
                            
                            sheet_emails = df['Email Address'].astype(str).str.strip().str.lower()
                            sheet_passwords = df['Password'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
                            user_match = df[(sheet_emails == login_email) & (sheet_passwords == login_pass)]
                            
                            if not user_match.empty:
                                st.session_state.logged_in = True
                                st.session_state.user_name = str(user_match.iloc[0]["Student Name"]).strip()
                                st.session_state.user_class = str(user_match.iloc[0]["Class"]).strip()
                                
                                if "Board" in df.columns:
                                    st.session_state.user_board = str(user_match.iloc[0]["Board"]).strip()
                                else:
                                    st.session_state.user_board = "ALL"
                                    
                                if "Date of Birth" in df.columns:
                                    st.session_state.user_dob = str(user_match.iloc[0]["Date of Birth"]).strip()
                                else:
                                    st.session_state.user_dob = ""
                                st.rerun()
                            else:
                                st.error("Invalid email or password.")
                        except Exception as e:
                            st.error(f"Login Error (Make sure 'Students' tab exists with Board column): {str(e)}")
                else:
                    st.warning("Please enter both fields.")

# ==========================================
#              PRIVATE PORTAL
# ==========================================
else:
    # --- Top Action Bar ---
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.header(f"Welcome, {st.session_state.user_name}!")
    with top_col2:
        if st.button("🚪 Log Out", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            if "session_token" in st.query_params:
                del st.query_params["session_token"]
            st.rerun()
            
    st.write("---")

    # ------------------------------------------
    #             ADMIN DASHBOARD
    # ------------------------------------------
    if st.session_state.user_class == "ADMIN":
        admin_tab1, admin_tab2, admin_tab3, admin_tab4, admin_tab5, admin_tab6 = st.tabs([
            "📚 Materials", "📸 Gallery", "💬 Directory", "🚨 News", "🏆 Star Student", "🧠 Manage Exams"
        ])

        with admin_tab1:
            st.write("Add new subjects, chapters, and PDF/Video links here.")
            if "reset_key" not in st.session_state:
                st.session_state.reset_key = 0
            
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_mat = conn.read(worksheet="Materials", ttl=60) 
            except Exception:
                df_mat = pd.DataFrame(columns=["Class", "Board", "Subject", "Chapter", "Link"])

            default_classes = ["XII", "XI", "X", "IX", "VIII"]
            db_classes = df_mat["Class"].dropna().unique().tolist() if not df_mat.empty else []
            admin_class_options = sorted(list(set(default_classes + db_classes))) + ["+ Add New Class"]
            selected_class = st.selectbox("1. Target Class", admin_class_options, key=f"c_drop_{st.session_state.reset_key}")
            final_class = st.text_input("Enter New Class", key=f"c_t_{st.session_state.reset_key}").strip() if selected_class == "+ Add New Class" else selected_class
            
            default_boards = ["CBSE", "ICSE/ISC", "WB", "ALL"]
            db_boards = df_mat["Board"].dropna().unique().tolist() if "Board" in df_mat.columns else []
            admin_board_options = sorted(list(set(default_boards + db_boards))) + ["+ Add New Board"]
            selected_board = st.selectbox("2. Target Board", admin_board_options, key=f"b_drop_{st.session_state.reset_key}")
            final_board = st.text_input("Enter New Board", key=f"b_t_{st.session_state.reset_key}").strip() if selected_board == "+ Add New Board" else selected_board

            default_subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "Science", "English"]
            db_subjects = df_mat["Subject"].dropna().unique().tolist() if "Subject" in df_mat.columns else []
            admin_subject_options = sorted(list(set(default_subjects + db_subjects))) + ["+ Add New Subject"]
            selected_subject = st.selectbox("3. Subject Name", admin_subject_options, key=f"s_drop_{st.session_state.reset_key}")
            final_subject = st.text_input("Enter New Subject", key=f"s_t_{st.session_state.reset_key}").strip() if selected_subject == "+ Add New Subject" else selected_subject
            
            final_chapter = st.text_input("4. Chapter / Topic Name", key=f"ch_t_{st.session_state.reset_key}").strip() 
            raw_link = st.text_input("5. Google Drive Share Link", key=f"l_{st.session_state.reset_key}").strip()
            final_link = raw_link.replace("/view", "/preview").replace("/edit", "/preview") if raw_link else "Pending"

            if st.button("Publish Material", type="primary"):
                if final_class and final_board and final_subject and final_chapter:
                    try:
                        mask = (df_mat.get("Class", pd.Series(dtype=str)).astype(str).str.strip() == final_class) & \
                               (df_mat.get("Board", pd.Series(dtype=str)).astype(str).str.strip() == final_board) & \
                               (df_mat.get("Subject", pd.Series(dtype=str)).astype(str).str.strip() == final_subject) & \
                               (df_mat.get("Chapter", pd.Series(dtype=str)).astype(str).str.strip() == final_chapter)
                        if mask.any():
                            idx = df_mat[mask].index[0]
                            df_mat.at[idx, "Link"] = final_link
                            conn.update(worksheet="Materials", data=df_mat)
                        else:
                            new_data = pd.DataFrame([{"Class": final_class, "Board": final_board, "Subject": final_subject, "Chapter": final_chapter, "Link": final_link}])
                            updated_df = pd.concat([df_mat, new_data], ignore_index=True)
                            conn.update(worksheet="Materials", data=updated_df)
                            
                        st.success(f"✅ Published {final_chapter} for {final_board} ({final_class})!")
                        st.session_state.reset_key += 1 
                        time.sleep(2)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please fill out Class, Board, Subject, and Chapter.")

        with admin_tab2:
            st.subheader("Add Photos to Gallery")
            uploaded_photos = st.file_uploader("Select Photos (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            compress_image = st.checkbox("Compress photos for faster loading?", value=True)
            
            if st.button("Publish to Gallery", type="primary") and uploaded_photos:
                with st.spinner(f"Processing and Uploading {len(uploaded_photos)} photo(s)..."):
                    try:
                        import io
                        new_urls = []
                        for photo in uploaded_photos:
                            if compress_image:
                                img = Image.open(photo)
                                if img.mode != 'RGB': img = img.convert('RGB')
                                img.thumbnail((800, 800))
                                buffer = io.BytesIO()
                                img.save(buffer, format="JPEG", quality=70, optimize=True)
                                final_bytes = buffer.getvalue()
                            else:
                                final_bytes = photo.getvalue()

                            payload = {"key": st.secrets["IMGBB_API_KEY"], "image": base64.b64encode(final_bytes).decode('utf-8')}
                            res = requests.post("https://api.imgbb.com/1/upload", data=payload)
                            if res.status_code == 200: new_urls.append({"Image_URL": res.json()["data"]["url"]})
                        
                        if new_urls:
                            conn = st.connection("gsheets", type=GSheetsConnection)
                            gallery_df = conn.read(worksheet="Gallery", usecols=[0], ttl=60)
                            updated_df = pd.concat([gallery_df, pd.DataFrame(new_urls)], ignore_index=True)
                            conn.update(worksheet="Gallery", data=updated_df)
                            st.success(f"✅ Successfully published {len(new_urls)} photo(s)!")
                        else:
                            st.error("Upload failed.")
                    except Exception as e:
                        st.error(f"Error: {e}")

        with admin_tab3:
            st.subheader("👥 Active Student Directory")
            try:
                import urllib.parse
                conn = st.connection("gsheets", type=GSheetsConnection)
                reg_df = conn.read(worksheet="Students", ttl=60)
                reg_df.columns = reg_df.columns.str.strip()
                
                required_cols = ["Student Name", "WhatsApp Number", "Password"]
                if all(col in reg_df.columns for col in required_cols):
                    display_df = reg_df.dropna(subset=["Student Name"]).copy()
                    whatsapp_links = []
                    for index, row in display_df.iterrows():
                        student_name = str(row["Student Name"]).strip()
                        student_pass = str(row["Password"]).replace(".0", "").strip()
                        raw_number = str(row["WhatsApp Number"]).strip()
                        if raw_number.endswith(".0"): raw_number = raw_number[:-2]
                        clean_number = ''.join(filter(str.isdigit, raw_number))
                        
                        if len(clean_number) == 10: clean_number = "91" + clean_number
                        elif len(clean_number) == 11 and clean_number.startswith("0"): clean_number = "91" + clean_number[1:]
                        
                        msg = f"Hello {student_name}, your Wisdope Academy fee is received. Your password for this month is: {student_pass}"
                        encoded_msg = urllib.parse.quote(msg)
                        whatsapp_links.append(f"https://wa.me/{clean_number}?text={encoded_msg}")
                        
                    display_df["Action"] = whatsapp_links
                    st.dataframe(
                        display_df,
                        column_config={"Action": st.column_config.LinkColumn("Send Password", display_text="📲 Send WhatsApp")},
                        hide_index=True, use_container_width=True
                    )
                else:
                    st.warning("Missing required columns in 'Students' tab.")
            except Exception as e:
                st.error(f"Error loading directory: {str(e)}")

        with admin_tab4:
            st.subheader("🚨 Publish Urgent News")
            news_input = st.text_input("Enter the Urgent Message:")
            duration = st.selectbox("Display for how long?", ["1 Hour", "3 Hours", "6 Hours", "12 Hours", "24 Hours", "2 Days", "3 Days", "1 Week"])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📢 Publish News Banner", type="primary"):
                    if news_input:
                        try:
                            from datetime import datetime, timedelta
                            num = int(duration.split()[0])
                            if "Hour" in duration: time_delta = timedelta(hours=num)
                            elif "Day" in duration: time_delta = timedelta(days=num)
                            elif "Week" in duration: time_delta = timedelta(weeks=num)
                            
                            ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
                            exp_dt = ist_now + time_delta
                            
                            new_news = pd.DataFrame([{"Message": news_input, "Expiration": exp_dt.strftime("%Y-%m-%d %H:%M:%S")}])
                            conn.update(worksheet="News", data=new_news)
                            st.success(f"✅ News published! It will automatically disappear in {duration}.")
                        except Exception as e:
                            st.error(f"Database Error: {e}")
                    else:
                        st.warning("Please enter a message first.")
            with col2:
                if st.button("🗑️ Clear Active News"):
                    try:
                        empty_news = pd.DataFrame([{"Message": "", "Expiration": ""}])
                        conn.update(worksheet="News", data=empty_news)
                        st.success("✅ News banner removed immediately!")
                    except Exception as e:
                        st.error(f"Database Error: {e}")

        with admin_tab5:
            st.subheader("🌟 Update Star Student")
            star_input = st.text_input("Student Name (e.g., Ronit Das):")
            batch_input = st.text_input("Batch/Class (e.g., Class XII):")
            msg_input = st.text_area("Achievement / Custom Message (e.g., 'Highest score in the Physics mock test!'):")
            star_photo = st.file_uploader("Upload Student Photo (Optional)", type=["jpg", "jpeg", "png"])
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🏅 Publish Star Student", type="primary"):
                    if star_input and batch_input:
                        with st.spinner("Uploading and publishing to Leaderboard..."):
                            try:
                                conn = st.connection("gsheets", type=GSheetsConnection)
                                img_url = ""
                                if star_photo:
                                    payload = {"key": st.secrets["IMGBB_API_KEY"], "image": base64.b64encode(star_photo.getvalue()).decode('utf-8')}
                                    res = requests.post("https://api.imgbb.com/1/upload", data=payload)
                                    if res.status_code == 200: img_url = res.json()["data"]["url"]
                                
                                new_leader = pd.DataFrame([{"Name": star_input, "Batch": batch_input, "Message": msg_input, "Image_URL": img_url}])
                                conn.update(worksheet="Leaderboard", data=new_leader)
                                st.success(f"✅ {star_input} is now live on the public Leaderboard!")
                            except Exception as e:
                                st.error(f"Database Error: {e}")
                    else:
                        st.warning("Please enter at least the Student Name and Batch.")
            with col_b:
                if st.button("🗑️ Hide Leaderboard"):
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        empty_leader = pd.DataFrame([{"Name": "", "Batch": "", "Message": "", "Image_URL": ""}])
                        conn.update(worksheet="Leaderboard", data=empty_leader)
                        st.success("✅ Leaderboard has been cleared and hidden from the public.")
                    except Exception as e:
                        st.error(f"Database Error: {e}")

        # --- NEW: API OPTIMIZED EXAM DEPLOYER ---
        with admin_tab6:
            st.subheader("🧠 Deploy Brain Drive Exam")
            
            try:
                from datetime import datetime, timedelta
                conn = st.connection("gsheets", type=GSheetsConnection)
                ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
                
                # Fetch every 15 seconds to prevent Quota Crashes
                try:
                    settings_df = conn.read(worksheet="Exam_Settings", ttl=15)
                except:
                    st.error("Please add 'Board' and 'Class' columns to your Exam_Settings sheet!")
                    settings_df = pd.DataFrame()
                
                if not settings_df.empty and str(settings_df.iloc[0].get("Status", "")) == "Active":
                    exp_str = str(settings_df.iloc[0].get("Expires_At", ""))
                    exam_sub = str(settings_df.iloc[0].get("Subject", ""))
                    exam_cls = str(settings_df.iloc[0].get("Class", ""))
                    exam_brd = str(settings_df.iloc[0].get("Board", ""))
                    try:
                        exp_dt = pd.to_datetime(exp_str)
                        if ist_now < exp_dt:
                            rem_mins = int((exp_dt - ist_now).total_seconds() / 60)
                            st.markdown(f"""
                            <div style="background-color: rgba(0, 255, 0, 0.1); border: 2px solid #00FF00; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                                <h3 style="color: #00FF00; margin-top: 0px;">✅ ACTIVE EXAM: {exam_sub}</h3>
                                <p style="font-size: 16px; margin-bottom: 5px;">Targeting: <b>Class {exam_cls} | {exam_brd}</b></p>
                                <p style="font-size: 14px; margin-bottom: 0px; color: #B0A8B9;">Link disappears from student portals in: <b>{rem_mins} Minutes</b> (At {exp_dt.strftime('%I:%M %p')})</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button("🛑 Force Stop Exam Early"):
                                conn.update(worksheet="Exam_Settings", data=pd.DataFrame([{"Status": "Inactive", "Board":"", "Class":"", "Subject": "", "Duration": "", "Retake": "", "Expires_At": "", "Question_Limit": ""}]))
                                st.success("🛑 Exam forcefully stopped! Waiting for database to sync...")
                                time.sleep(2)
                                st.rerun()
                    except:
                        pass
                
                st.write("---")
                brain_df = conn.read(worksheet="Brain_Drive", ttl=15)
                
                if "Exam Type" not in brain_df.columns:
                    brain_df["Exam Type"] = "Practice"
                
                vault_q = brain_df[brain_df["Exam Type"].astype(str).str.strip().str.title() == "Final"]
                
                col_c, col_b = st.columns(2)
                with col_c:
                    avail_classes = vault_q["Class"].dropna().unique().tolist() if not vault_q.empty else []
                    set_cls = st.selectbox("Target Class:", avail_classes + ["ALL"]) if avail_classes else None
                with col_b:
                    avail_boards = vault_q["Board"].dropna().unique().tolist() if not vault_q.empty else []
                    set_brd = st.selectbox("Target Board:", avail_boards + ["ALL"]) if avail_boards else None
                
                if set_cls and set_brd:
                    # FIX: Handle "ALL" logic properly so it doesn't crash
                    if set_cls == "ALL" and set_brd == "ALL":
                        filtered_q = vault_q
                    elif set_cls == "ALL":
                        filtered_q = vault_q[vault_q["Board"] == set_brd]
                    elif set_brd == "ALL":
                        filtered_q = vault_q[vault_q["Class"] == set_cls]
                    else:
                        filtered_q = vault_q[(vault_q["Class"] == set_cls) & (vault_q["Board"] == set_brd)]
                    
                    avail_subs = filtered_q["Subject"].dropna().unique().tolist()
                    
                    if avail_subs:
                        set_sub = st.selectbox("Select Subject to Test:", avail_subs)
                        max_q = len(filtered_q[filtered_q["Subject"] == set_sub])
                        max_val = max_q if max_q > 0 else 1
                        
                        exam_limit = st.number_input(f"Questions to ask? (Max available: {max_q})", min_value=1, max_value=max_val, value=min(10, max_val))
                        exam_time = st.number_input("Time limit for student (Minutes):", min_value=1, max_value=60, value=20)
                        exam_window = st.number_input("Exam link visibility window (Minutes):", min_value=1, max_value=1440, value=60)
                        exam_retake = st.checkbox("Allow students to retake the exam?", value=False)
                        
                        if st.button("🚀 Deploy Targeted Exam", type="primary"):
                            expires_at = ist_now + timedelta(minutes=exam_window)
                            settings = pd.DataFrame([{
                                "Status": "Active", 
                                "Board": set_brd,
                                "Class": set_cls,
                                "Subject": set_sub, 
                                "Duration": exam_time, 
                                "Retake": str(exam_retake),
                                "Expires_At": expires_at.strftime("%Y-%m-%d %H:%M:%S"),
                                "Question_Limit": exam_limit
                            }])
                            conn.update(worksheet="Exam_Settings", data=settings)
                            st.success(f"✅ Exam Deployed Successfully! Students will see it in ~15 seconds.")
                            time.sleep(2)
                            st.rerun()
                    else:
                        st.warning(f"No Final Exam questions found for Class {set_cls} ({set_brd}).")
                else:
                    st.warning("No Final Exam questions found in the Vault. Please add rows with 'Exam Type' set to 'Final'.")
                
                st.write("---")
                st.subheader("📊 Live Exam Scores")
                scores_df = conn.read(worksheet="Scores", ttl=15)
                if not scores_df.empty and "Name" in scores_df.columns:
                    st.dataframe(scores_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No scores recorded yet.")
            except Exception as e:
                st.error(f"Error fetching data: {e}")


    # ------------------------------------------
    #            STUDENT DASHBOARD
    # ------------------------------------------
    else:
        st.markdown(f"🎓 **Class:** {st.session_state.user_class} | 🏫 **Board:** {st.session_state.user_board}")
        
        if st.session_state.get("user_dob") and st.session_state.user_dob.lower() not in ["nan", "none", ""]:
            try:
                from datetime import datetime, timedelta
                dob_dt = pd.to_datetime(st.session_state.user_dob, dayfirst=True)
                ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
                if dob_dt.month == ist_now.month and dob_dt.day == ist_now.day:
                    if "bday_celebrated" not in st.session_state:
                        st.balloons()
                        st.session_state.bday_celebrated = True
                    st.markdown(f"""
                    <div style="background-color: rgba(255, 215, 0, 0.15); padding: 15px; border-radius: 10px; border: 2px solid gold; text-align: center; margin-bottom: 20px;">
                        <h2 style="color: gold; margin-top: 0px;">🎉 Happy Birthday, {st.session_state.user_name}! 🎂</h2>
                        <p style="font-size: 16px; margin-bottom: 0px;">Wishing you a fantastic day and a wonderful year ahead! Keep shining and keep learning.<br><b>- Rishav Sir & The Wisdope Team</b></p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception:
                pass
        
        st.write("---")

        # ==========================================
        #   ANTI-CHEAT FOCUS MODE (ASSIGNED EXAM)
        # ==========================================
        if st.session_state.get("exam_active", False):
            st.warning("🚨 **EXAM IN PROGRESS - FOCUS MODE ACTIVE** 🚨")
            
            if st.session_state.get("exam_completed", False):
                st.success("✅ Exam Submitted Successfully!")
                st.info("📊 Your exam has been securely saved. Results will be announced soon by Rishav Sir.")
                if st.button("🚪 Exit Focus Mode", type="primary", use_container_width=True):
                    st.session_state.exam_active = False
                    st.session_state.exam_completed = False
                    st.rerun()
            else:
                st.write("All study materials and tabs are locked until you submit this exam.")
                try:
                    from datetime import datetime, timedelta
                    import streamlit.components.v1 as components
                    
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
                    settings_df = conn.read(worksheet="Exam_Settings", ttl=15)
                    
                    active_sub = str(settings_df.iloc[0]["Subject"])
                    time_limit = int(settings_df.iloc[0]["Duration"])
                    end_time = st.session_state.exam_start_time + timedelta(minutes=time_limit)
                    rem_sec = int((end_time - ist_now).total_seconds())
                    
                    if rem_sec > 0:
                        # FIX: THE JAVASCRIPT AUTO-SUBMIT HACK
                        timer_html = f"""
                        <div style="font-family: 'Courier New', monospace; font-size: 28px; font-weight: bold; color: #fff; background-color: #ff4b4b; text-align: center; padding: 10px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); margin-bottom: 15px;">
                            ⏳ <span id="timer">{rem_sec // 60:02d}:{rem_sec % 60:02d}</span>
                        </div>
                        <script>
                            var timeleft = {rem_sec};
                            var timerInterval = setInterval(function() {{
                                timeleft--;
                                if (timeleft <= 0) {{
                                    clearInterval(timerInterval);
                                    document.getElementById("timer").innerHTML = "00:00 (AUTO-SUBMITTING...)";
                                    
                                    // Hack: Finds and physically clicks the Streamlit 'Submit' button
                                    var buttons = window.parent.document.querySelectorAll('button[kind="primaryFormSubmit"]');
                                    if (buttons.length > 0) {{
                                        buttons[0].click();
                                    }} else {{
                                        var allBtns = window.parent.document.querySelectorAll('button');
                                        for (var i=0; i<allBtns.length; i++) {{
                                            if(allBtns[i].innerText.includes('Submit Exam')) {{
                                                allBtns[i].click();
                                                break;
                                            }}
                                        }}
                                    }}
                                }} else {{
                                    var m = Math.floor(timeleft / 60);
                                    var s = timeleft % 60;
                                    document.getElementById("timer").innerHTML = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
                                }}
                            }}, 1000);
                        </script>
                        """
                        components.html(timer_html, height=75)
                        
                        with st.form("exam_form"):
                            user_answers = {}
                            for i, q in enumerate(st.session_state.exam_questions):
                                st.write(f"**Q{i+1}: {q['Question']}**")
                                options = [str(q['Option A']), str(q['Option B']), str(q['Option C']), str(q['Option D'])]
                                options = [opt for opt in options if opt.lower() != 'nan']
                                
                                user_answers[i] = st.radio("Select an answer:", options, key=f"q_{i}", index=None)
                                st.write("---")
                                
                            submitted = st.form_submit_button("Submit Exam", type="primary")
                            
                            if submitted:
                                ist_submit = datetime.utcnow() + timedelta(hours=5, minutes=30)
                                # Grace period allows the auto-submit to register as "On Time"
                                is_late = (ist_submit - end_time).total_seconds() > 15
                                
                                score = 0
                                total_q = len(st.session_state.exam_questions)
                                for i, q in enumerate(st.session_state.exam_questions):
                                    correct_ans = str(q['Correct Answer']).strip().lower()
                                    chosen_ans = str(user_answers[i]).strip().lower() if user_answers[i] else ""
                                    if chosen_ans == correct_ans: score += 1
                                        
                                percentage = round((score / total_q) * 100, 2)
                                pct_str = f"{percentage}% (Late)" if is_late else f"{percentage}%"
                                
                                scores_df = conn.read(worksheet="Scores", ttl=0)
                                new_score = pd.DataFrame([{
                                    "Name": st.session_state.user_name,
                                    "Batch": st.session_state.user_class,
                                    "Subject": active_sub,
                                    "Start Time": st.session_state.exam_start_time.strftime("%Y-%m-%d %I:%M %p"),
                                    "Submit Time": ist_submit.strftime("%Y-%m-%d %I:%M %p"),
                                    "Score": f"{score}/{total_q}",
                                    "Percentage": pct_str
                                }])
                                
                                updated_scores = pd.concat([scores_df, new_score], ignore_index=True) if not scores_df.empty else new_score
                                conn.update(worksheet="Scores", data=updated_scores)
                                
                                st.session_state.exam_completed = True
                                del st.session_state.exam_questions
                                st.rerun()
                    else:
                        st.error("🚨 TIME IS UP! You must submit your exam immediately.")
                        if st.button("Submit Now (Late)", type="primary"):
                            ist_submit = datetime.utcnow() + timedelta(hours=5, minutes=30)
                            scores_df = conn.read(worksheet="Scores", ttl=0)
                            new_score = pd.DataFrame([{
                                    "Name": st.session_state.user_name,
                                    "Batch": st.session_state.user_class,
                                    "Subject": active_sub,
                                    "Start Time": st.session_state.exam_start_time.strftime("%Y-%m-%d %I:%M %p"),
                                    "Submit Time": ist_submit.strftime("%Y-%m-%d %I:%M %p"),
                                    "Score": "0 (Forced Auto-Submit)",
                                    "Percentage": "0% (Late)"
                                }])
                            updated_scores = pd.concat([scores_df, new_score], ignore_index=True) if not scores_df.empty else new_score
                            conn.update(worksheet="Scores", data=updated_scores)
                            
                            st.session_state.exam_completed = True
                            del st.session_state.exam_questions
                            st.rerun()
                except Exception as e:
                    st.error(f"Exam Rendering Error: {e}")
                    
        # ==========================================
        #   SELF-ASSESSMENT PRACTICE MODE
        # ==========================================
        elif st.session_state.get("practice_active", False):
            st.info("🧠 **PRACTICE MODE ACTIVE** - Test your knowledge at your own pace.")
            
            if st.session_state.get("practice_completed", False):
                score = st.session_state.practice_score
                total = st.session_state.practice_total
                st.success(f"🎉 Practice Complete! You scored **{score} out of {total}**!")
                
                if score >= (total * 0.8):
                    st.balloons()
                    
                if st.button("🔄 Retake This Subject"):
                    with st.spinner("Shuffling new questions..."):
                        try:
                            from datetime import datetime, timedelta
                            conn = st.connection("gsheets", type=GSheetsConnection)
                            brain_df = conn.read(worksheet="Brain_Drive", ttl=15)
                            
                            if "Exam Type" not in brain_df.columns:
                                brain_df["Exam Type"] = "Practice"
                                
                            e_col = brain_df["Exam Type"].astype(str).str.strip().str.title()
                            b_col = brain_df["Board"].astype(str).str.strip().str.upper()
                            user_b = str(st.session_state.user_board).strip().upper()
                            
                            my_class_q = brain_df[(brain_df["Class"].astype(str).str.strip() == str(st.session_state.user_class).strip()) &
                                                  ((b_col == user_b) | (b_col == "ALL") | (b_col == "")) &
                                                  (e_col == "Practice")]
                                                  
                            sub_pool = my_class_q[my_class_q["Subject"] == st.session_state.practice_sub]
                            sample_size = min(10, len(sub_pool))
                            
                            st.session_state.practice_questions = sub_pool.sample(n=sample_size).to_dict('records')
                            st.session_state.practice_completed = False
                            st.session_state.practice_start_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
                            st.rerun()
                        except Exception as e:
                            st.error("Error loading new questions. Please exit and try again.")
                            
                if st.button("🚪 Exit Practice Mode"):
                    st.session_state.practice_active = False
                    st.session_state.practice_completed = False
                    if 'practice_questions' in st.session_state:
                        del st.session_state.practice_questions
                    st.rerun()
            else:
                with st.form("practice_form"):
                    user_answers = {}
                    for i, q in enumerate(st.session_state.practice_questions):
                        st.write(f"**Q{i+1}: {q['Question']}**")
                        options = [str(q['Option A']), str(q['Option B']), str(q['Option C']), str(q['Option D'])]
                        options = [opt for opt in options if opt.lower() != 'nan']
                        
                        user_answers[i] = st.radio("Select an answer:", options, key=f"p_{i}", index=None)
                        st.write("---")
                        
                    submitted = st.form_submit_button("Submit Practice", type="primary")
                    if submitted:
                        from datetime import datetime, timedelta
                        ist_submit = datetime.utcnow() + timedelta(hours=5, minutes=30)
                        
                        score = 0
                        total = len(st.session_state.practice_questions)
                        for i, q in enumerate(st.session_state.practice_questions):
                            correct_ans = str(q['Correct Answer']).strip().lower()
                            chosen_ans = str(user_answers[i]).strip().lower() if user_answers[i] else ""
                            if chosen_ans == correct_ans: score += 1
                        
                        percentage = round((score / total) * 100, 2)
                        
                        try:
                            conn = st.connection("gsheets", type=GSheetsConnection)
                            scores_df = conn.read(worksheet="Scores", ttl=0)
                            
                            new_score = pd.DataFrame([{
                                "Name": st.session_state.user_name,
                                "Batch": st.session_state.user_class,
                                "Subject": f"{st.session_state.practice_sub} (Practice)",
                                "Start Time": st.session_state.practice_start_time.strftime("%Y-%m-%d %I:%M %p"),
                                "Submit Time": ist_submit.strftime("%Y-%m-%d %I:%M %p"),
                                "Score": f"{score}/{total}",
                                "Percentage": f"{percentage}%"
                            }])
                            updated_scores = pd.concat([scores_df, new_score], ignore_index=True) if not scores_df.empty else new_score
                            conn.update(worksheet="Scores", data=updated_scores)
                        except Exception as e:
                            st.error(f"Could not save score: {e}")

                        st.session_state.practice_score = score
                        st.session_state.practice_total = total
                        st.session_state.practice_completed = True
                        st.rerun()

        # ==========================================
        #       NORMAL STUDENT DASHBOARD (TABS)
        # ==========================================
        else:
            stud_tab1, stud_tab2, stud_tab3 = st.tabs(["📚 Study Materials", "🧠 Brain Drive", "📢 Notice Board"])
            
            with stud_tab1:
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    m_df = conn.read(worksheet="Materials", ttl=60) 
                    
                    if 'Chapter' not in m_df.columns: m_df['Chapter'] = "General"
                    if 'Board' not in m_df.columns: m_df['Board'] = "ALL"
                        
                    b_col = m_df["Board"].astype(str).str.strip().str.upper()
                    user_b = str(st.session_state.user_board).strip().upper()
                    
                    c_mat = m_df[(m_df["Class"].astype(str).str.strip() == str(st.session_state.user_class).strip()) & 
                                 ((b_col == user_b) | (b_col == "ALL") | (b_col == ""))]
                    
                    student_subs = sorted(list(set(c_mat["Subject"].tolist() if not c_mat.empty else [])))
                    
                    if not student_subs:
                        st.info(f"No study materials available for {st.session_state.user_class} ({st.session_state.user_board}) yet.")
                    else:
                        sel_sub = st.selectbox("1. Choose a subject:", student_subs)
                        if sel_sub:
                            sub_match = c_mat[c_mat["Subject"] == sel_sub]
                            chapter_list = sorted(list(set(sub_match["Chapter"].tolist() if not sub_match.empty else [])))
                            sel_chap = st.selectbox("2. Choose a chapter/topic:", chapter_list)
                            if sel_chap:
                                final_match = sub_match[sub_match["Chapter"] == sel_chap]
                                if not final_match.empty and str(final_match.iloc[0]["Link"]).startswith("http"):
                                    st.markdown(f'<iframe src="{final_match.iloc[0]["Link"]}" style="width: 100%; height: 700px; border:none; border-radius: 8px;"></iframe>', unsafe_allow_html=True)
                                else:
                                    st.info("Materials for this chapter are coming soon!")
                except Exception as e:
                    st.error(f"Database Error: {e}")

            with stud_tab2:
                st.subheader("🧠 Brain Drive")
                
                try:
                    from datetime import datetime, timedelta
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
                    
                    # 1. CHECK FOR ASSIGNED FINAL EXAMS
                    settings_df = conn.read(worksheet="Exam_Settings", ttl=15)
                    exam_available = False
                    
                    if not settings_df.empty and str(settings_df.iloc[0].get("Status", "")) == "Active":
                        exam_cls = str(settings_df.iloc[0].get("Class", "")).strip()
                        exam_brd = str(settings_df.iloc[0].get("Board", "")).strip()
                        
                        if (exam_cls == st.session_state.user_class or exam_cls == "ALL") and \
                           (exam_brd == st.session_state.user_board or exam_brd == "ALL"):
                            exp_str = str(settings_df.iloc[0].get("Expires_At", ""))
                            try:
                                exp_dt = pd.to_datetime(exp_str)
                                if ist_now < exp_dt:
                                    exam_available = True
                                    active_sub = str(settings_df.iloc[0]["Subject"])
                                    time_limit = int(settings_df.iloc[0]["Duration"])
                                    allow_retake = str(settings_df.iloc[0]["Retake"]).lower() == "true"
                                    
                                    q_limit_raw = settings_df.iloc[0].get("Question_Limit", 10)
                                    q_limit = int(q_limit_raw) if pd.notna(q_limit_raw) and str(q_limit_raw).strip() != "" else 10
                            except:
                                pass

                    if exam_available:
                        scores_df = conn.read(worksheet="Scores", ttl=15)
                        already_taken = False
                        if not scores_df.empty and "Name" in scores_df.columns:
                            mask = (scores_df["Name"] == st.session_state.user_name) & (scores_df["Subject"] == active_sub)
                            if mask.any(): already_taken = True

                        if already_taken and not allow_retake:
                            st.warning("You have already completed this exam. Retakes are currently disabled by Rishav Sir.")
                        else:
                            st.markdown(f"""
                            <div style="background-color: rgba(255, 0, 0, 0.1); border-left: 5px solid red; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                                <h3 style="color: red; margin-top: 0px;">🚨 ASSIGNED EXAM: {active_sub}</h3>
                                <p style="font-size: 16px; margin-bottom: 0px;"><b>Time Limit:</b> {time_limit} Mins | <b>Questions:</b> {q_limit}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.write("When you are ready, click Start. The timer will begin immediately and you will enter Focus Mode.")
                            
                            if st.button("🚀 Start Final Exam", type="primary"):
                                brain_df = conn.read(worksheet="Brain_Drive", ttl=15)
                                
                                if "Exam Type" not in brain_df.columns:
                                    brain_df["Exam Type"] = "Practice"
                                e_col = brain_df["Exam Type"].astype(str).str.strip().str.title()
                                
                                # FIX: Also handle "ALL" logic for question grabbing
                                if exam_cls == "ALL" and exam_brd == "ALL":
                                    subject_questions = brain_df[(brain_df["Subject"] == active_sub) & (e_col == "Final")]
                                elif exam_cls == "ALL":
                                    subject_questions = brain_df[(brain_df["Board"] == exam_brd) & (brain_df["Subject"] == active_sub) & (e_col == "Final")]
                                elif exam_brd == "ALL":
                                    subject_questions = brain_df[(brain_df["Class"] == exam_cls) & (brain_df["Subject"] == active_sub) & (e_col == "Final")]
                                else:
                                    subject_questions = brain_df[(brain_df["Class"] == exam_cls) & (brain_df["Board"] == exam_brd) & (brain_df["Subject"] == active_sub) & (e_col == "Final")]
                                
                                if len(subject_questions) > 0:
                                    sample_size = min(q_limit, len(subject_questions))
                                    st.session_state.exam_questions = subject_questions.sample(n=sample_size).to_dict('records')
                                    st.session_state.exam_active = True
                                    st.session_state.exam_start_time = ist_now
                                    st.rerun()
                                else:
                                    st.error("Error: No 'Final' questions found in the vault for this subject.")
                    
                    # 2. SELF ASSESSMENT (PRACTICE)
                    else:
                        st.write("No active final exams. Take a self-assessment practice quiz to test your readiness!")
                        st.write("---")
                        
                        brain_df = conn.read(worksheet="Brain_Drive", ttl=15)
                        if "Class" in brain_df.columns and "Board" in brain_df.columns:
                            if "Exam Type" not in brain_df.columns:
                                brain_df["Exam Type"] = "Practice"
                            
                            e_col = brain_df["Exam Type"].astype(str).str.strip().str.title()
                            b_col = brain_df["Board"].astype(str).str.strip().str.upper()
                            user_b = str(st.session_state.user_board).strip().upper()
                            
                            my_class_q = brain_df[(brain_df["Class"].astype(str).str.strip() == str(st.session_state.user_class).strip()) &
                                                  ((b_col == user_b) | (b_col == "ALL") | (b_col == "")) &
                                                  (e_col == "Practice")]
                            
                            if my_class_q.empty:
                                st.info(f"No practice questions available yet for Class {st.session_state.user_class} ({st.session_state.user_board}).")
                            else:
                                p_subs = my_class_q["Subject"].dropna().unique().tolist()
                                prac_sub = st.selectbox("Select Subject to Practice:", p_subs) if p_subs else None
                                        
                                if prac_sub:
                                    if st.button("📝 Start 10-Question Practice"):
                                        sub_pool = my_class_q[my_class_q["Subject"] == prac_sub]
                                        sample_size = min(10, len(sub_pool))
                                        st.session_state.practice_questions = sub_pool.sample(n=sample_size).to_dict('records')
                                        st.session_state.practice_active = True
                                        st.session_state.practice_completed = False
                                        st.session_state.practice_sub = prac_sub
                                        st.session_state.practice_start_time = ist_now
                                        st.rerun()
                        else:
                            st.info("Brain Drive is currently undergoing database updates.")
                        
                        st.write("---")
                        st.subheader("📊 My Past Scores")
                        try:
                            scores_df = conn.read(worksheet="Scores", ttl=15)
                            if not scores_df.empty and "Name" in scores_df.columns:
                                my_scores = scores_df[scores_df["Name"] == st.session_state.user_name]
                                if not my_scores.empty:
                                    display_scores = my_scores[["Subject", "Start Time", "Score", "Percentage"]].copy()
                                    st.dataframe(display_scores, hide_index=True, use_container_width=True)
                                else:
                                    st.info("You haven't taken any exams or practice tests yet.")
                        except:
                            st.info("Scores database not available yet.")
                        
                except Exception as e:
                    st.info(f"Brain Drive Error: {e}")

            # --- TAB 3: NOTICE BOARD ---
            with stud_tab3:
                st.subheader("📢 Notice Board")
                st.write("If using smartphone, use desktop site for better view.")
                notice_url = st.secrets["admin"]["notice_board"]
                st.markdown(
                    f'''
                    <style>
                    .notice-wrapper {{ display: flex; justify-content: center; width: 100%; margin-bottom: 20px; }}
                    .notice-iframe {{ width: 100%; max-width: 700px; height: 250px; border: 2px solid rgba(255,255,255,0.1); border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); background-color: #595959; overflow-y: scroll !important; -webkit-overflow-scrolling: touch !important; overscroll-behavior: contain; }}
                    @media (min-width: 768px) {{ .notice-iframe {{ height: 380px; }} }}
                    </style>
                    <div class="notice-wrapper">
                        <iframe class="notice-iframe" src="{notice_url}" scrolling="yes"></iframe>
                    </div>
                    ''', unsafe_allow_html=True
                )            
# ==========================================
#               GLOBAL FOOTER
# ==========================================
st.divider()
st.write("### Follow Us On:")
st.markdown(
    """
    <div style="display: flex; justify-content: center; flex-wrap: nowrap; gap: 10px; margin-bottom: 20px;">
        <a href="https://www.facebook.com/profile.php?id=61573780375951" target="_blank">
            <img src="https://img.icons8.com/color/48/facebook-new.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://www.instagram.com/rishavkarar.09?igsh=MXFmazF1d2xzc3Bhcg==" target="_blank">
            <img src="https://img.icons8.com/color/48/instagram-new.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://www.threads.net/@rishavkarar.09" target="_blank">
            <img src="https://img.icons8.com/ios-filled/48/ffffff/threads.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://wa.me/917044443309" target="_blank">
            <img src="https://img.icons8.com/color/48/whatsapp.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://www.linkedin.com/in/rishav-karar-56849b3b4" target="_blank">
            <img src="https://img.icons8.com/color/48/linkedin.png" width="40" style="transition: transform 0.2s;">
        </a>
        <a href="https://youtube.com/@rishavkarar7470" target="_blank">
            <img src="https://img.icons8.com/color/48/youtube-play.png" width="40" style="transition: transform 0.2s;">
        </a>
    </div>
    """, 
    unsafe_allow_html=True
)
st.write("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>© 2026 Wisdope Academy | Associated with Bose Informatics</p>", 
    unsafe_allow_html=True
)
