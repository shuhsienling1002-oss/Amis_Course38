import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 38: O Romi'ad", page_icon="🌤️", layout="centered")

# --- CSS 美化 (天空藍與晨曦黃) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #B3E5FC; color: #01579B; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #E1F5FE 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #03A9F4;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #0277BD; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #E1F5FE;
        border-left: 5px solid #29B6F6;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #B3E5FC; color: #01579B; border: 2px solid #03A9F4; padding: 12px;
    }
    .stButton>button:hover { background-color: #81D4FA; border-color: #0288D1; }
    .stProgress > div > div > div > div { background-color: #03A9F4; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 38: 18個單字 - 時間與天氣) ---
vocab_data = [
    {"amis": "Romi'ad", "chi": "日子 / 天氣 (詞根)", "icon": "📅", "source": "Row 1690", "morph": "Root"},
    {"amis": "Maromi'ad", "chi": "整天 / 度過一天", "icon": "⏳", "source": "Grammar", "morph": "Ma-Romi'ad"},
    {"amis": "'Orad", "chi": "雨 (詞根)", "icon": "💧", "source": "Row 3484", "morph": "Root"},
    {"amis": "Ma'orad", "chi": "下雨", "icon": "🌧️", "source": "Standard", "morph": "Ma-'Orad"},
    {"amis": "Cidal", "chi": "太陽 (詞根)", "icon": "☀️", "source": "Standard", "morph": "Root"},
    {"amis": "Macidal", "chi": "出太陽 / 晴天", "icon": "🌤️", "source": "Standard", "morph": "Ma-Cidal"},
    {"amis": "Fali", "chi": "風 (詞根)", "icon": "🍃", "source": "Row 555", "morph": "Root"},
    {"amis": "Mifali", "chi": "刮風", "icon": "💨", "source": "Standard", "morph": "Mi-Fali"},
    {"amis": "Heca", "chi": "年 / 歲 (詞根)", "icon": "🎂", "source": "Root", "morph": "Root"},
    {"amis": "Mihecaan", "chi": "年份 / 歲數", "icon": "🗓️", "source": "Row 321", "morph": "Mi-Heca-an"},
    {"amis": "Anini", "chi": "今天 / 現在", "icon": "👇", "source": "Row 1690", "morph": "Time"},
    {"amis": "Cila", "chi": "前/後一天 (詞根)", "icon": "📆", "source": "Root", "morph": "Root"},
    {"amis": "Nacila", "chi": "昨天", "icon": "⏪", "source": "Row 321", "morph": "Na-Cila (Past)"},
    {"amis": "Anocila", "chi": "明天", "icon": "⏩", "source": "Row 485", "morph": "Ano-Cila (Fut)"},
    {"amis": "Toki", "chi": "時間 / 鐘錶", "icon": "⌚", "source": "Row 676", "morph": "Loan"},
    {"amis": "Fulad", "chi": "月亮 / 月份", "icon": "🌙", "source": "Standard", "morph": "Noun"},
    {"amis": "Sananal", "chi": "早晨", "icon": "🌅", "source": "Standard", "morph": "Time"},
    {"amis": "Dadaya", "chi": "晚上", "icon": "🌃", "source": "Standard", "morph": "Time"},
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Ma'orad anini a romi'ad.", "chi": "今天是下雨天。", "icon": "🌧️", "source": "Standard Pattern"},
    {"amis": "Macidal i nacila.", "chi": "昨天是晴天。", "icon": "☀️", "source": "Standard Pattern"},
    {"amis": "Pina to ko mihecaan iso?", "chi": "你幾歲了？", "icon": "🎂", "source": "Standard Question"},
    {"amis": "Mifali to i papotal.", "chi": "外面在颳風了。", "icon": "💨", "source": "Standard Pattern"},
    {"amis": "Pina ko toki anini?", "chi": "現在幾點鐘？", "icon": "⌚", "source": "Row 676"},
    {"amis": "Malikat ko fulad i dadaya.", "chi": "晚上的月亮很亮。", "icon": "🌕", "source": "Standard Pattern"},
    {"amis": "Maromi'ad ciira a matayal.", "chi": "他工作了一整天。", "icon": "⏳", "source": "Standard Pattern"},
    {"amis": "Anocila a tayra kako i Taypak.", "chi": "我明天要去台北。", "icon": "🚄", "source": "Standard Pattern"},
    {"amis": "Mica'edongay kako to mi'acaan no miso a riko' i nacila a miheca.", "chi": "我穿著你去年買的衣服。", "icon": "👗", "source": "Row 321"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "Ma'orad anini a romi'ad.",
        "audio": "Ma'orad anini a romi'ad",
        "options": ["今天是下雨天", "今天是晴天", "今天是陰天"],
        "ans": "今天是下雨天",
        "hint": "Ma'orad (下雨) (Standard)"
    },
    {
        "q": "Pina to ko mihecaan iso?",
        "audio": "Pina to ko mihecaan iso",
        "options": ["你幾歲了？", "你有多少錢？", "你有幾個小孩？"],
        "ans": "你幾歲了？",
        "hint": "Mihecaan (歲數/年) (Standard)"
    },
    {
        "q": "單字測驗：Anocila",
        "audio": "Anocila",
        "options": ["明天", "昨天", "今天"],
        "ans": "明天",
        "hint": "Ano- (未來) + Cila"
    },
    {
        "q": "單字測驗：Nacila",
        "audio": "Nacila",
        "options": ["昨天", "明天", "後天"],
        "ans": "昨天",
        "hint": "Na- (過去) + Cila"
    },
    {
        "q": "Maromi'ad ciira a matayal.",
        "audio": "Maromi'ad ciira a matayal",
        "options": ["他工作了一整天", "他不想工作", "他剛開始工作"],
        "ans": "他工作了一整天",
        "hint": "Ma-romi'ad (度過一天/整天)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌 (5題)
    selected_questions = random.sample(raw_quiz_pool, 5)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #0277BD;'>Unit 38: O Romi'ad</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>時間與天氣 (Time & Weather)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #0277BD;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 5)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 5**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 20
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #B3E5FC; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #01579B;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會時間與天氣的說法了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 5)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
