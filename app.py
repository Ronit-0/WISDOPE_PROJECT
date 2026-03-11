# ==========================================
#  THE "GROQ AI" CHATBOT (GLOBAL INJECTOR)
# ==========================================
import streamlit.components.v1 as components

# Fetch the Groq API key securely from your secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

# --- ANTI-CHEAT PROTOCOL ---
in_focus_mode = st.session_state.get("exam_active", False)
in_practice_mode = st.session_state.get("practice_active", False)

if in_focus_mode or in_practice_mode:
    destroy_code = """
    <script>
    var existingContainer = window.parent.document.getElementById('wisdope-chatbot-container');
    if(existingContainer) existingContainer.remove();
    var existingStyle = window.parent.document.getElementById('wisdope-chatbot-style');
    if(existingStyle) existingStyle.remove();
    </script>
    """
    components.html(destroy_code, height=0, width=0)

else:
    user_type = st.session_state.get("user_class", "PUBLIC")
    if st.session_state.get("logged_in", False):
        if user_type == "ADMIN":
            first_name = "Rishav Sir"
            welcome_msg = "Welcome to the Command Center, Rishav Sir! Ask me about managing materials, exams, or fixing bugs."
        else:
            first_name = st.session_state.user_name.split()[0]
            welcome_msg = f"Welcome back to your portal, {first_name}! 🎓 Ask me about your exams, study materials, or technical help!"
    else:
        first_name = "Guest"
        welcome_msg = "Hello! I am the Wisdope AI Assistant. Ask me anything about admissions, fees, or our faculty!"

    # NOTE: Replace 'YOUR_PHONE_NUMBER_HERE' on line 1251 with your actual phone number
    custom_chat_code = f"""
    <script>
    (function() {{
        const currentUser = "{first_name}";
        const existingContainer = window.parent.document.getElementById('wisdope-chatbot-container');
        const existingStyle = window.parent.document.getElementById('wisdope-chatbot-style');
        
        if (existingContainer) {{
            if (existingContainer.getAttribute('data-user') === currentUser) return; 
            else {{ existingContainer.remove(); if (existingStyle) existingStyle.remove(); }}
        }}

        const style = window.parent.document.createElement('style');
        style.id = 'wisdope-chatbot-style';
        style.innerHTML = `
            #wisdope-chatbot-container {{ position: fixed; bottom: 90px; right: 25px; z-index: 999999; font-family: 'Segoe UI', Tahoma, sans-serif; }}
            #chat-fab {{ width: 65px; height: 65px; border-radius: 50%; background: linear-gradient(135deg, #8A2BE2, #4B0082); box-shadow: 0 4px 20px rgba(138, 43, 226, 0.6), 0 0 0 2px rgba(0, 229, 255, 0.8); display: flex; justify-content: center; align-items: center; cursor: pointer; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease; float: right; position: relative; }}
            #chat-fab:hover {{ transform: scale(1.1) rotate(-5deg); box-shadow: 0 6px 25px rgba(0, 229, 255, 0.8), 0 0 0 2px rgba(138, 43, 226, 1); }}
            #chat-fab svg {{ width: 32px; height: 32px; fill: white; transition: transform 0.3s ease; }}
            
            #chat-tooltip {{ position: absolute; right: 80px; bottom: 15px; background: linear-gradient(135deg, #FF416C, #FF4B2B); color: white; padding: 8px 14px; border-radius: 20px; border-bottom-right-radius: 0px; font-size: 13px; font-weight: bold; box-shadow: 0 4px 10px rgba(255, 65, 108, 0.4); opacity: 0; transform: translateX(20px) scale(0.9); transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); pointer-events: none; white-space: nowrap; }}
            #chat-tooltip.show {{ opacity: 1; transform: translateX(0) scale(1); }}

            #chat-window {{ display: none; width: 360px; max-width: 90vw; height: 520px; max-height: 80vh; background: linear-gradient(180deg, #13111C 0%, #1a1625 100%); border: 1px solid rgba(138, 43, 226, 0.5); border-radius: 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.8), 0 0 20px rgba(138, 43, 226, 0.2); margin-bottom: 20px; flex-direction: column; overflow: hidden; transform-origin: bottom right; transform: scale(0.1); opacity: 0; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.2); }}
            #chat-window.open {{ display: flex; transform: scale(1); opacity: 1; }}
            #chat-header {{ background: linear-gradient(90deg, #1C1829, #2a2438); padding: 16px 20px; color: #F8F9FA; font-weight: 800; font-size: 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #8A2BE2; box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 10; }}
            .header-title {{ display: flex; align-items: center; gap: 10px; }}
            .online-dot {{ width: 10px; height: 10px; background-color: #00FF00; border-radius: 50%; box-shadow: 0 0 8px #00FF00; animation: pulse 2s infinite; }}
            @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7); }} 70% {{ box-shadow: 0 0 0 6px rgba(0, 255, 0, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }} }}
            #chat-close {{ cursor: pointer; color: #B0A8B9; font-size: 20px; transition: color 0.2s, transform 0.2s; }}
            #chat-close:hover {{ color: #ff4b4b; transform: scale(1.2); }}
            #chat-messages {{ flex: 1; padding: 20px 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }}
            #chat-messages::-webkit-scrollbar {{ width: 6px; }}
            #chat-messages::-webkit-scrollbar-thumb {{ background: rgba(138, 43, 226, 0.5); border-radius: 3px; }}
            .msg-row {{ display: flex; align-items: flex-end; gap: 8px; animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; opacity: 0; transform: translateY(10px); max-width: 100%; }}
            .bot-row {{ justify-content: flex-start; }}
            .user-row {{ justify-content: flex-end; }}
            .avatar {{ width: 30px; height: 30px; background: #1C1829; border-radius: 50%; display: flex; justify-content: center; align-items: center; border: 1px solid #00E5FF; flex-shrink: 0; box-shadow: 0 0 8px rgba(0,229,255,0.3); }}
            .avatar svg {{ width: 16px; height: 16px; fill: #00E5FF; }}
            .msg-content {{ display: flex; flex-direction: column; max-width: 80%; }}
            .msg-bubble {{ padding: 12px 16px; font-size: 14px; line-height: 1.4; word-wrap: break-word; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }}
            .bot-msg {{ background: #2a2438; color: #E0E0E0; border-radius: 16px 16px 16px 4px; border: 1px solid rgba(138, 43, 226, 0.3); }}
            .user-msg {{ background: linear-gradient(135deg, #8A2BE2, #5a189a); color: white; border-radius: 16px 16px 4px 16px; border: 1px solid rgba(0, 229, 255, 0.3); }}
            .msg-time {{ font-size: 10px; color: #787088; margin-top: 4px; padding: 0 4px; }}
            .user-time {{ text-align: right; }}
            .bot-time {{ text-align: left; }}
            .bot-action-btn {{ display: inline-block; margin-top: 8px; padding: 8px 12px; background: linear-gradient(135deg, #25D366, #128C7E); color: white !important; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); transition: transform 0.2s; text-align: center; }}
            .bot-action-btn:hover {{ transform: scale(1.05); }}
            .typing-bubble {{ display: flex; align-items: center; gap: 5px; padding: 14px 16px; min-height: 20px; }}
            .dot {{ width: 7px; height: 7px; background-color: #00E5FF; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; }}
            .dot:nth-child(1) {{ animation-delay: -0.32s; }}
            .dot:nth-child(2) {{ animation-delay: -0.16s; }}
            @keyframes bounce {{ 0%, 80%, 100% {{ transform: scale(0); opacity: 0.5; }} 40% {{ transform: scale(1); opacity: 1; }} }}
            @keyframes popIn {{ to {{ opacity: 1; transform: translateY(0); }} }}
            #chat-input-area {{ display: flex; padding: 15px; background: #1C1829; border-top: 1px solid rgba(138, 43, 226, 0.3); align-items: center; gap: 10px; }}
            #chat-input {{ flex: 1; background: #13111C; border: 1px solid rgba(255,255,255,0.1); color: white; padding: 12px 18px; border-radius: 25px; outline: none; font-size: 14px; transition: all 0.3s; }}
            #chat-input:focus {{ border-color: #00E5FF; box-shadow: 0 0 10px rgba(0, 229, 255, 0.2); }}
            #chat-input:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            #send-btn {{ background: #8A2BE2; border: none; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; cursor: pointer; transition: transform 0.2s, background 0.2s; }}
            #send-btn:hover:not(:disabled) {{ transform: scale(1.1) rotate(15deg); background: #00E5FF; }}
            #send-btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            #send-btn svg {{ fill: white; width: 18px; height: 18px; }}
        `;
        window.parent.document.head.appendChild(style);

        const getTime = () => new Date().toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit' }});
        const botIcon = `<svg viewBox="0 0 24 24"><path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-1H1a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73A2 2 0 1 1 12 2zm-3 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm6 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/></svg>`;
        const userType = "{user_type}";
        const userName = "{first_name}";
        const groqKey = "{GROQ_API_KEY}";

        // --- GLOBAL MEMORY FOR AI ---
        window.parent.wisdopeChatHistory = [];
        
        // --- THE AI SYSTEM PROMPT ---
        const systemPrompt = `You are the Wisdope AI Assistant, a helpful and highly energetic virtual guide for Wisdope Academy. 
        RULES: Keep answers very short and concise (1-2 sentences maximum). Use emojis to be friendly. 
        FACTS TO KNOW: 
        - Founder: Rishav Karar Sir (MSc. Biotech, R.A. Pharmacognosy). 
        - Location: 37, Dinu Lane, Kadamtala, Howrah-01 (Opposite Kadamtala Bus Stand near S.B. Jewellers). 
        - Contact: Call 9051965176 or WhatsApp 7044443309. 
        - Subjects Taught: Physics, Chemistry, Biology (Theory and Practical labs). 
        - Boards: ICSE, ISC, CBSE, WB. 
        - Classes: VIII to XII. 
        - NEET prep is available. 
        - Timings: Morning (7AM-10AM) and Evening (5PM-10PM). 
        - Fees: Depend on the batch, users must contact Rishav Sir. 
        - Tech Architect: The website was built by Ronit Das.
        If a user asks about something you do not know, tell them to contact Rishav Sir directly on WhatsApp.`;

        const chatHTML = `
            <div id="chat-tooltip">Need help? 👋</div>
            <div id="chat-window">
                <div id="chat-header">
                    <div class="header-title"><div class="online-dot"></div> Wisdope AI</div>
                    <div id="chat-close" onclick="window.toggleWisdopeChat()">✖</div>
                </div>
                <div id="chat-messages">
                    <div class="msg-row bot-row">
                        <div class="avatar">${{botIcon}}</div>
                        <div class="msg-content">
                            <div class="msg-bubble bot-msg">{welcome_msg}</div>
                            <div class="msg-time bot-time">${{getTime()}}</div>
                        </div>
                    </div>
                </div>
                <div id="typing-indicator" class="msg-row bot-row" style="display: none;">
                    <div class="avatar">${{botIcon}}</div>
                    <div class="msg-content"><div class="msg-bubble bot-msg typing-bubble"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div></div>
                </div>
                <div id="chat-input-area">
                    <input type="text" id="chat-input" placeholder="Ask anything..." onkeypress="window.handleWisdopeEnter(event)" autocomplete="off">
                    <button id="send-btn" onclick="window.sendWisdopeMessage()">
                        <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>
                    </button>
                </div>
            </div>
            <div id="chat-fab" onclick="window.toggleWisdopeChat()">
                <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"></path></svg>
            </div>
        `;
        
        const container = window.parent.document.createElement('div');
        container.id = 'wisdope-chatbot-container';
        container.setAttribute('data-user', currentUser);
        container.innerHTML = chatHTML;
        window.parent.document.body.appendChild(container);

        function triggerTooltip() {{
            const tooltip = window.parent.document.getElementById('chat-tooltip');
            const chatWin = window.parent.document.getElementById('chat-window');
            if (tooltip && !chatWin.classList.contains('open')) {{
                tooltip.classList.add('show');
                setTimeout(() => {{ tooltip.classList.remove('show'); }}, 5000);
            }}
        }}
        setTimeout(triggerTooltip, 10000);
        setInterval(triggerTooltip, 300000);

        window.parent.toggleWisdopeChat = function() {{
            const chatWin = window.parent.document.getElementById('chat-window');
            const tooltip = window.parent.document.getElementById('chat-tooltip');
            if (chatWin.classList.contains('open')) {{
                chatWin.classList.remove('open');
                setTimeout(() => chatWin.style.display = 'none', 400); 
            }} else {{
                if(tooltip) tooltip.classList.remove('show'); 
                chatWin.style.display = 'flex';
                setTimeout(() => chatWin.classList.add('open'), 10);
                window.parent.document.getElementById('chat-input').focus();
            }}
        }};

        window.parent.handleWisdopeEnter = function(e) {{
            if (e.key === 'Enter') {{ window.parent.sendWisdopeMessage(); }}
        }};

        // HELPER: Adds bot message to UI
        function injectBotMessage(htmlContent) {{
            const msgBox = window.parent.document.getElementById('chat-messages');
            const typingInd = window.parent.document.getElementById('typing-indicator');
            const inputField = window.parent.document.getElementById('chat-input');
            const sendBtn = window.parent.document.getElementById('send-btn');
            
            typingInd.style.display = 'none';
            const botTime = getTime();
            msgBox.innerHTML += `
                <div class="msg-row bot-row">
                    <div class="avatar">${{botIcon}}</div>
                    <div class="msg-content">
                        <div class="msg-bubble bot-msg">${{htmlContent}}</div>
                        <div class="msg-time bot-time">${{botTime}}</div>
                    </div>
                </div>
            `;
            msgBox.scrollTop = msgBox.scrollHeight;
            inputField.disabled = false;
            sendBtn.disabled = false;
            inputField.focus();
        }}

        window.parent.sendWisdopeMessage = function() {{
            const inputField = window.parent.document.getElementById('chat-input');
            const sendBtn = window.parent.document.getElementById('send-btn');
            const msgBox = window.parent.document.getElementById('chat-messages');
            const typingInd = window.parent.document.getElementById('typing-indicator');
            const text = inputField.value.trim();
            
            if (!text) return;

            // Lock input & show user message
            inputField.disabled = true; sendBtn.disabled = true;
            const timeNow = getTime();
            msgBox.innerHTML += `
                <div class="msg-row user-row">
                    <div class="msg-content">
                        <div class="msg-bubble user-msg">${{text}}</div>
                        <div class="msg-time user-time">${{timeNow}}</div>
                    </div>
                </div>
            `;
            inputField.value = '';
            msgBox.scrollTop = msgBox.scrollHeight;

            msgBox.appendChild(typingInd); 
            typingInd.style.display = 'flex';
            msgBox.scrollTop = msgBox.scrollHeight;
            
            let tLower = text.toLowerCase();

            // ==========================================
            // 1. HARDCODED OVERRIDES (Security & Actions)
            // ==========================================
            if (tLower.includes('password') && (tLower.includes('admin') || tLower.includes('show') || tLower.includes('tell') || tLower.includes('database') || tLower.includes('secret'))) {{
                setTimeout(() => injectBotMessage("🛡️ <b>Security Alert:</b> I cannot reveal administrative passwords, database links, or sensitive credentials!"), 800);
                return;
            }}
            else if (tLower.includes('error') || tLower.includes('bug') || tLower.includes('crash') || tLower.includes('not working') || tLower.includes('glitch')) {{
                const bugText = encodeURIComponent(`Hi Ronit, I found a bug on the website. Here is what happened: `);
                let reply = `Uh oh, a technical glitch! 🛠️ Please take a screenshot and send it to our Digital Architect, Ronit Das.<br>
                <a href="https://wa.me/YOUR_PHONE_NUMBER_HERE?text=${{bugText}}" target="_blank" class="bot-action-btn" style="background: linear-gradient(135deg, #FF416C, #FF4B2B);">🛠️ Report Bug to Ronit</a>`;
                setTimeout(() => injectBotMessage(reply), 800);
                return;
            }}
            else if (userType === 'ADMIN' && (tLower.includes('help') || tLower.includes('portal') || tLower.includes('how to use') || tLower.includes('manage'))) {{
                let reply = "<b>Admin Command Center:</b> <br><br>📚 Materials: Add new PDFs/Links.<br>📸 Gallery: Upload photos.<br>👥 Directory: WhatsApp passwords to students.<br>🚨 News: Publish banners.<br>🌟 Star Student: Update leaderboard.<br>🧠 Manage Exams: Deploy live tests!";
                setTimeout(() => injectBotMessage(reply), 800);
                return;
            }}
            else if (userType === 'STUDENT' && (tLower.includes('help') || tLower.includes('portal') || tLower.includes('how to use') || tLower.includes('feature'))) {{
                let reply = `<b>Your Dashboard:</b><br><br>📚 Study Materials: Chapter notes.<br>🧠 Brain Drive: Live Exams & Practice.<br>📢 Notice Board: Latest updates from Rishav Sir.`;
                setTimeout(() => injectBotMessage(reply), 800);
                return;
            }}
            else if (tLower.includes('password') || tLower.includes('login') || tLower.includes('log in') || tLower.includes('can\\'t access') || tLower.includes('wrong') || tLower.includes('invalid')) {{
                const safePassText = encodeURIComponent(`Hi Rishav Sir, I forgot my Wisdope Academy portal password. Could you please help me retrieve it?`);
                let reply = `Did you know? <b>Passwords renew on the 10th of every month!</b> 🔄<br><br>If you cannot log in, please request a new one directly from Rishav Sir.<br>
                <a href="https://wa.me/917044443309?text=${{safePassText}}" target="_blank" class="bot-action-btn">📲 Request New Password</a>`;
                setTimeout(() => injectBotMessage(reply), 800);
                return;
            }}

            // ==========================================
            // 2. GROQ AI CONNECTION (Llama 3)
            // ==========================================
            if (!groqKey) {{
                setTimeout(() => injectBotMessage("⚠️ <b>API Key Missing:</b> Please add the Groq API Key to Streamlit secrets!"), 800);
                return;
            }}

            // Save to memory
            window.parent.wisdopeChatHistory.push({{ "role": "user", "content": text }});

            // Keep only the last 6 messages to save tokens and prevent overload
            let recentHistory = window.parent.wisdopeChatHistory.slice(-6);
            let apiPayload = [{{ "role": "system", "content": systemPrompt }}].concat(recentHistory);

            fetch('https://api.groq.com/openai/v1/chat/completions', {{
                method: 'POST',
                headers: {{
                    'Authorization': `Bearer ${{groqKey}}`,
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    model: 'llama3-8b-8192',
                    messages: apiPayload,
                    temperature: 0.6,
                    max_tokens: 150
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.choices && data.choices.length > 0) {{
                    let aiText = data.choices[0].message.content;
                    
                    // Save bot reply to memory
                    window.parent.wisdopeChatHistory.push({{ "role": "assistant", "content": aiText }});
                    
                    // Format Markdown (**bold** to <b>bold</b>, and newlines to <br>)
                    let formattedReply = aiText.replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>').replace(/\\n/g, '<br>');
                    
                    injectBotMessage(formattedReply);
                }} else {{
                    injectBotMessage("Sorry, my brain disconnected for a second! Please try asking again.");
                }}
            }})
            .catch(error => {{
                console.error("Groq Error:", error);
                injectBotMessage("⚠️ I'm having trouble connecting to my AI servers right now. Please try again later!");
            }});
            
        }};
    }})();
    </script>
    """

    components.html(custom_chat_code, height=0, width=0)
