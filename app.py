import streamlit as st
import os
from PIL import Image
import requests
import base64
import pandas as pd
from streamlit_gsheets import GSheetsConnection

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
    from streamlit_gsheets import GSheetsConnection
    import pandas as pd
    from datetime import datetime, timedelta
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    news_df = conn.read(worksheet="News", ttl=60) 
    
    if not news_df.empty:
        msg = str(news_df.iloc[0]["Message"]).strip()
        exp_str = str(news_df.iloc[0]["Expiration"]).strip()
        
        if msg and msg.lower() != "nan" and exp_str and exp_str.lower() != "nan":
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
#       PERSISTENT SESSION MANAGER (10 MIN)
# ==========================================
import time
import json
import base64

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 1. Restore login if they refreshed the page within the 10-minute window
if not st.session_state.logged_in and "session_token" in st.query_params:
    try:
        token = st.query_params["session_token"]
        decoded_bytes = base64.b64decode(token.encode('utf-8'))
        session_data = json.loads(decoded_bytes.decode('utf-8'))
        
        # Check if current time is still before the expiry time
        if time.time() < session_data["expiry"]:
            st.session_state.logged_in = True
            st.session_state.user_name = session_data["name"]
            st.session_state.user_class = session_data["class"]
            st.session_state.user_dob = session_data.get("dob", "")
        else:
            # 10 minutes passed! Delete the token so they stay logged out
            del st.query_params["session_token"]
    except:
        del st.query_params["session_token"]

# 2. Keep refreshing the 10-minute timer as long as they are active
if st.session_state.logged_in:
    expiry_time = time.time() + 600 # 600 seconds = 10 minutes
    session_data = {
        "name": st.session_state.user_name,
        "class": st.session_state.user_class,
        "dob": st.session_state.get("user_dob", ""),
        "expiry": expiry_time
    }
    # Encode it so it looks like a professional, secure token in the URL
    token_bytes = json.dumps(session_data).encode('utf-8')
    st.query_params["session_token"] = base64.b64encode(token_bytes).decode('utf-8')

# ==========================================
#               PUBLIC WEBSITE
# ==========================================
if not st.session_state.logged_in:
    # --- ADDED THE LEADERBOARD TAB HERE ---
    tab1, tab2, tab3, tab_leader, tab4, tab5, tab6 = st.tabs([
        "🌟 Why Join Us?", 
        "📚 Course Details", 
        "📸 Gallery", 
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
            from streamlit_gsheets import GSheetsConnection
            import pandas as pd
            import streamlit.components.v1 as components
            
            conn = st.connection("gsheets", type=GSheetsConnection)
            gallery_df = conn.read(worksheet="Gallery", usecols=[0], ttl=0)
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

    # --- NEW: LEADERBOARD TAB (4th Position) ---
    with tab_leader:
        st.header("🌟 Wisdope Hall of Fame")
        st.write("Recognizing outstanding performance, hard work, and dedication!")
        st.write("---")
        
        try:
            from streamlit_gsheets import GSheetsConnection
            conn = st.connection("gsheets", type=GSheetsConnection)
            leader_df = conn.read(worksheet="Leaderboard", ttl=60) # Refreshes every 60 seconds
            
            # Check if there's actually a winner listed
            if not leader_df.empty and str(leader_df.iloc[0]["Name"]).lower() not in ["nan", "none", ""]:
                star_name = str(leader_df.iloc[0]["Name"]).strip()
                star_batch = str(leader_df.iloc[0]["Batch"]).strip()
                star_msg = str(leader_df.iloc[0]["Message"]).strip()
                
                # Safely extract the Image URL if it exists
                star_img = ""
                if "Image_URL" in leader_df.columns:
                    val = str(leader_df.iloc[0]["Image_URL"]).strip()
                    if val.lower() not in ["nan", "none", ""]:
                        star_img = val
                
                # If there is an image, make a circular profile pic. If not, use the Trophy icon.
                img_html = f'<img src="{star_img}" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 4px solid #FFD700; margin-bottom: 10px;">' if star_img else '<h1 style="margin-bottom: 0px; font-size: 60px;">🏆</h1>'
                
                # A beautiful gold-bordered card for the winner
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
                        st.rerun()
                    else:
                        try:
                            from streamlit_gsheets import GSheetsConnection
                            import pandas as pd
                            conn = st.connection("gsheets", type=GSheetsConnection)
                            df = conn.read(worksheet="Students", ttl=0) 
                            df.columns = df.columns.str.strip()
                            
                            sheet_emails = df['Email Address'].astype(str).str.strip().str.lower()
                            sheet_passwords = df['Password'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
                            user_match = df[(sheet_emails == login_email) & (sheet_passwords == login_pass)]
                            
                            if not user_match.empty:
                                st.session_state.logged_in = True
                                st.session_state.user_name = user_match.iloc[0]["Student Name"]
                                st.session_state.user_class = user_match.iloc[0]["Class"]
                                if "Date of Birth" in df.columns:
                                    st.session_state.user_dob = str(user_match.iloc[0]["Date of Birth"]).strip()
                                else:
                                    st.session_state.user_dob = ""
                                st.rerun()
                            else:
                                st.error("Invalid email or password.")
                        except Exception as e:
                            st.error(f"Login Error (Make sure 'Students' tab exists): {str(e)}")
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
            # Destroy the URL token instantly
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
            if "publish_msg" in st.session_state:
                st.success(st.session_state.publish_msg)
                del st.session_state.publish_msg 
            if "reset_key" not in st.session_state:
                st.session_state.reset_key = 0
            
            import pandas as pd
            try:
                from streamlit_gsheets import GSheetsConnection
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_mat = conn.read(worksheet="Materials", ttl=0) 
                if 'Chapter' not in df_mat.columns: df_mat['Chapter'] = "General"
            except Exception:
                df_mat = pd.DataFrame(columns=["Class", "Subject", "Chapter", "Link"])

            default_classes = ["XII", "XI", "X", "IX", "VIII"]
            db_classes = df_mat["Class"].dropna().unique().tolist() if not df_mat.empty else []
            admin_class_options = sorted(list(set(default_classes + db_classes))) + ["+ Add New Class"]
            selected_class = st.selectbox("1. Target Class", admin_class_options, key=f"c_drop_{st.session_state.reset_key}")
            final_class = st.text_input("Enter New Class", key=f"c_t_{st.session_state.reset_key}").strip() if selected_class == "+ Add New Class" else selected_class
            
            default_subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "Science", "English"]
            db_subjects = df_mat["Subject"].dropna().unique().tolist() if not df_mat.empty else []
            admin_subject_options = sorted(list(set(default_subjects + db_subjects))) + ["+ Add New Subject"]
            selected_subject = st.selectbox("2. Subject Name", admin_subject_options, key=f"s_drop_{st.session_state.reset_key}")
            final_subject = st.text_input("Enter New Subject", key=f"s_t_{st.session_state.reset_key}").strip() if selected_subject == "+ Add New Subject" else selected_subject
            
            db_chapters = df_mat[(df_mat["Class"] == final_class) & (df_mat["Subject"] == final_subject)]["Chapter"].dropna().unique().tolist() if not df_mat.empty else []
            admin_chapter_options = sorted(list(set(db_chapters))) + ["+ Add New Chapter"]
            selected_chapter = st.selectbox("3. Chapter / Topic Name", admin_chapter_options, key=f"ch_drop_{st.session_state.reset_key}")
            final_chapter = st.text_input("Enter New Chapter Name", key=f"ch_t_{st.session_state.reset_key}").strip() if selected_chapter == "+ Add New Chapter" else selected_chapter
            
            raw_link = st.text_input("4. Google Drive Share Link", key=f"l_{st.session_state.reset_key}").strip()
            final_link = raw_link.replace("/view", "/preview").replace("/edit", "/preview") if raw_link else "Pending"

            if st.button("Publish Material", type="primary"):
                if final_class and final_subject and final_chapter:
                    try:
                        mask = (df_mat["Class"].astype(str).str.strip() == final_class) & (df_mat["Subject"].astype(str).str.strip() == final_subject) & (df_mat["Chapter"].astype(str).str.strip() == final_chapter)
                        if mask.any():
                            idx = df_mat[mask].index[0]
                            df_mat.at[idx, "Link"] = final_link
                            conn.update(worksheet="Materials", data=df_mat)
                        else:
                            new_data = pd.DataFrame([{"Class": final_class, "Subject": final_subject, "Chapter": final_chapter, "Link": final_link}])
                            updated_df = pd.concat([df_mat, new_data], ignore_index=True)
                            conn.update(worksheet="Materials", data=updated_df)
                        st.session_state.publish_msg = f"✅ Published {final_chapter}!"
                        st.session_state.reset_key += 1 
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please fill out Class, Subject, and Chapter.")

        with admin_tab2:
            st.subheader("Add Photos to Gallery")
            uploaded_photos = st.file_uploader("Select Photos (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            compress_image = st.checkbox("Compress photos for faster loading?", value=True)
            
            if st.button("Publish to Gallery", type="primary") and uploaded_photos:
                with st.spinner(f"Processing and Uploading {len(uploaded_photos)} photo(s)..."):
                    try:
                        import requests, base64, io
                        from PIL import Image
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
                            gallery_df = conn.read(worksheet="Gallery", usecols=[0], ttl=0)
                            updated_df = pd.concat([gallery_df, pd.DataFrame(new_urls)], ignore_index=True)
                            conn.update(worksheet="Gallery", data=updated_df)
                            st.success(f"✅ Successfully published {len(new_urls)} photo(s)!")
                        else:
                            st.error("Upload failed.")
                    except Exception as e:
                        st.error(f"Error: {e}")

        with admin_tab3:
            st.subheader("👥 Active Student Directory")
            st.write("Click the button next to their name to automatically send their monthly password via WhatsApp.")
            try:
                from streamlit_gsheets import GSheetsConnection
                import urllib.parse
                conn = st.connection("gsheets", type=GSheetsConnection)
                reg_df = conn.read(worksheet="Students", ttl=0)
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
                        elif len(clean_number) == 12 and clean_number.startswith("91"): pass
                        
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
                            import pandas as pd
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
                        import pandas as pd
                        empty_news = pd.DataFrame([{"Message": "", "Expiration": ""}])
                        conn.update(worksheet="News", data=empty_news)
                        st.success("✅ News banner removed immediately!")
                    except Exception as e:
                        st.error(f"Database Error: {e}")

        with admin_tab5:
            st.subheader("🌟 Update Star Student")
            st.write("Feature a top-performing student on the public Leaderboard.")
            
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
                                import pandas as pd
                                import requests, base64
                                from streamlit_gsheets import GSheetsConnection
                                conn = st.connection("gsheets", type=GSheetsConnection)
                                
                                img_url = ""
                                if star_photo:
                                    payload = {
                                        "key": st.secrets["IMGBB_API_KEY"],
                                        "image": base64.b64encode(star_photo.getvalue()).decode('utf-8')
                                    }
                                    res = requests.post("https://api.imgbb.com/1/upload", data=payload)
                                    if res.status_code == 200:
                                        img_url = res.json()["data"]["url"]
                                
                                new_leader = pd.DataFrame([{
                                    "Name": star_input, 
                                    "Batch": batch_input, 
                                    "Message": msg_input,
                                    "Image_URL": img_url
                                }])
                                conn.update(worksheet="Leaderboard", data=new_leader)
                                st.success(f"✅ {star_input} is now live on the public Leaderboard!")
                            except Exception as e:
                                st.error(f"Database Error: {e}")
                    else:
                        st.warning("Please enter at least the Student Name and Batch.")
            with col_b:
                if st.button("🗑️ Hide Leaderboard"):
                    try:
                        import pandas as pd
                        from streamlit_gsheets import GSheetsConnection
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        
                        empty_leader = pd.DataFrame([{"Name": "", "Batch": "", "Message": "", "Image_URL": ""}])
                        conn.update(worksheet="Leaderboard", data=empty_leader)
                        st.success("✅ Leaderboard has been cleared and hidden from the public.")
                    except Exception as e:
                        st.error(f"Database Error: {e}")

        # --- NEW: ADMIN EXAM PANEL WITH DYNAMIC QUESTION LIMIT ---
        with admin_tab6:
            st.subheader("🧠 Deploy Brain Drive Exam")
            try:
                from streamlit_gsheets import GSheetsConnection
                import pandas as pd
                from datetime import datetime, timedelta
                conn = st.connection("gsheets", type=GSheetsConnection)
                
                ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
                settings_df = conn.read(worksheet="Exam_Settings", ttl=0)
                
                # Check for currently active exams and show countdown for the link
                if not settings_df.empty and str(settings_df.iloc[0]["Status"]) == "Active":
                    exp_str = str(settings_df.iloc[0].get("Expires_At", ""))
                    try:
                        exp_dt = pd.to_datetime(exp_str)
                        if ist_now < exp_dt:
                            rem_mins = int((exp_dt - ist_now).total_seconds() / 60)
                            st.markdown(f"""
                            <div style="background-color: rgba(0, 255, 0, 0.1); border: 2px solid #00FF00; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                                <h3 style="color: #00FF00; margin-top: 0px;">✅ ACTIVE EXAM: {settings_df.iloc[0]["Subject"]}</h3>
                                <p style="font-size: 16px; margin-bottom: 0px;">Link disappears from student portals in: <b>{rem_mins} Minutes</b> (At {exp_dt.strftime('%I:%M %p')})</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button("🛑 Force Stop Exam Early"):
                                conn.update(worksheet="Exam_Settings", data=pd.DataFrame([{"Status": "Inactive", "Subject": "", "Duration": "", "Retake": "", "Expires_At": "", "Question_Limit": ""}]))
                                st.rerun()
                    except:
                        pass
                
                st.write("---")
                # Fetch available subjects
                brain_df = conn.read(worksheet="Brain_Drive", ttl=0)
                available_subjects = brain_df["Subject"].dropna().unique().tolist() if "Subject" in brain_df.columns else []
                
                if available_subjects:
                    st.write("**Deploy a New Exam**")
                    exam_sub = st.selectbox("Select Subject to Test:", available_subjects)
                    
                    # DYNAMIC LOGIC: Automatically count how many questions exist for the selected subject
                    max_q = len(brain_df[brain_df["Subject"] == exam_sub])
                    max_val = max_q if max_q > 0 else 1
                    default_val = min(10, max_val)
                    
                    exam_limit = st.number_input(f"How many questions should be asked? (Max available: {max_q})", min_value=1, max_value=max_val, value=default_val)
                    exam_time = st.number_input("Time limit for student to write (Minutes):", min_value=1, max_value=60, value=20)
                    exam_window = st.number_input("How long should the exam link stay open? (Minutes):", min_value=1, max_value=1440, value=60)
                    exam_retake = st.checkbox("Allow students to retake the exam?", value=False)
                    
                    if st.button("🚀 Deploy Exam", type="primary"):
                        expires_at = ist_now + timedelta(minutes=exam_window)
                        settings = pd.DataFrame([{
                            "Status": "Active", 
                            "Subject": exam_sub, 
                            "Duration": exam_time, 
                            "Retake": str(exam_retake),
                            "Expires_At": expires_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "Question_Limit": exam_limit
                        }])
                        conn.update(worksheet="Exam_Settings", data=settings)
                        st.success(f"✅ Exam Deployed Successfully! It will automatically vanish at {expires_at.strftime('%I:%M %p')}.")
                        st.rerun()
                else:
                    st.warning("No subjects found in the 'Brain_Drive' sheet. Please add questions first!")
                
                st.write("---")
                st.subheader("📊 Live Exam Scores")
                scores_df = conn.read(worksheet="Scores", ttl=0)
                if not scores_df.empty and "Name" in scores_df.columns:
                    st.dataframe(scores_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No scores recorded yet.")
            except Exception as e:
                st.error(f"Please create the 'Exam_Settings' and 'Scores' sheets first. Error: {e}")

    # ------------------------------------------
    #            STUDENT DASHBOARD
    # ------------------------------------------
    else:
        st.write(f"🎓 **Batch:** {st.session_state.user_class}")
        
        if st.session_state.get("user_dob") and st.session_state.user_dob.lower() not in ["nan", "none", ""]:
            try:
                import pandas as pd
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
        #   ANTI-CHEAT FOCUS MODE (ACTIVE EXAM)
        # ==========================================
        if st.session_state.get("exam_active", False):
            st.warning("🚨 **EXAM IN PROGRESS - FOCUS MODE ACTIVE** 🚨")
            
            # --- THE NEW POST-SUBMIT SCREEN ---
            if st.session_state.get("exam_completed", False):
                st.success("✅ Exam Submitted Successfully!")
                st.info("📊 Your exam has been securely saved. Results will be announced soon by Rishav Sir.")
                
                # Locks them here until they click this button
                if st.button("🚪 Exit Focus Mode", type="primary", use_container_width=True):
                    st.session_state.exam_active = False
                    st.session_state.exam_completed = False
                    st.rerun()
            
            # --- THE LIVE EXAM ENGINE ---
            else:
                st.write("All study materials and tabs are locked until you submit this exam.")
                
                try:
                    from streamlit_gsheets import GSheetsConnection
                    import pandas as pd
                    from datetime import datetime, timedelta
                    import streamlit.components.v1 as components
                    
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
                    
                    settings_df = conn.read(worksheet="Exam_Settings", ttl=0)
                    active_sub = str(settings_df.iloc[0]["Subject"])
                    time_limit = int(settings_df.iloc[0]["Duration"])
                    
                    end_time = st.session_state.exam_start_time + timedelta(minutes=time_limit)
                    rem_sec = int((end_time - ist_now).total_seconds())
                    
                    if rem_sec > 0:
                        # Live Javascript countdown
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
                                    document.getElementById("timer").innerHTML = "00:00 (TIME UP!)";
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
                                
                                # Do NOT exit focus mode yet. Just trigger the completion screen.
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
        #       NORMAL STUDENT DASHBOARD (TABS)
        # ==========================================
        else:
            stud_tab1, stud_tab2, stud_tab3 = st.tabs(["📚 Study Materials", "🧠 Brain Drive", "📢 Notice Board"])
            
            with stud_tab1:
                try:
                    from streamlit_gsheets import GSheetsConnection
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    m_df = conn.read(worksheet="Materials", ttl=0) 
                    if 'Chapter' not in m_df.columns: m_df['Chapter'] = "General"
                        
                    c_mat = m_df[m_df["Class"].astype(str).str.strip() == str(st.session_state.user_class).strip()]
                    student_subs = sorted(list(set(c_mat["Subject"].tolist() if not c_mat.empty else [])))
                    
                    if not student_subs:
                        st.info("No materials available for your class yet.")
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
                except Exception:
                    st.error("Database Error. Please contact Rishav Sir.")

            # --- TAB 2: BRAIN DRIVE WAITING ROOM ---
            with stud_tab2:
                st.subheader("🧠 Brain Drive")
                
                try:
                    from streamlit_gsheets import GSheetsConnection
                    import pandas as pd
                    from datetime import datetime, timedelta
                    
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
                    
                    settings_df = conn.read(worksheet="Exam_Settings", ttl=0)
                    exam_available = False
                    
                    if not settings_df.empty and str(settings_df.iloc[0]["Status"]) == "Active":
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
                        scores_df = conn.read(worksheet="Scores", ttl=0)
                        already_taken = False
                        if not scores_df.empty and "Name" in scores_df.columns:
                            mask = (scores_df["Name"] == st.session_state.user_name) & (scores_df["Subject"] == active_sub)
                            if mask.any(): already_taken = True

                        if already_taken and not allow_retake:
                            st.warning("You have already completed this exam. Retakes are currently disabled by Rishav Sir.")
                        else:
                            st.info(f"📝 **New Exam Assigned:** {active_sub} | ⏱️ **Time Limit:** {time_limit} Mins | ❓ **Questions:** {q_limit}")
                            st.write("When you are ready, click Start. The timer will begin immediately and you will not be able to access your study materials.")
                            
                            if st.button("🚀 Start Exam", type="primary"):
                                brain_df = conn.read(worksheet="Brain_Drive", ttl=0)
                                subject_questions = brain_df[brain_df["Subject"] == active_sub]
                                
                                if len(subject_questions) > 0:
                                    sample_size = min(q_limit, len(subject_questions))
                                    st.session_state.exam_questions = subject_questions.sample(n=sample_size).to_dict('records')
                                    st.session_state.exam_active = True
                                    st.session_state.exam_start_time = ist_now
                                    st.rerun()
                                else:
                                    st.error("Error: No questions found for this subject.")
                    else:
                        st.info("No active exams right now. Take a break and study your materials!")
                        
                except Exception as e:
                    st.info("The Brain Drive module is being setup by Rishav Sir. Check back later.")

            # --- TAB 3: NOTICE BOARD ---
            with stud_tab3:
                st.subheader("📢 Notice Board")
                st.write("If using samrtphone use desktop site for better view")
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
