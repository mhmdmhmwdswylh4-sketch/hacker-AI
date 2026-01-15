import streamlit as st
import socket
from langchain_groq import ChatGroq # سنستخدم Groq لأنه مجاني وسريع جداً
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

st.title("🛡️ مساعد الأمن السيبراني الذكي")

# إعداد مفتاح الـ API (يمكنك وضعه في Streamlit Secrets لاحقاً)
# للحصول على مفتاح مجاني: console.groq.com
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

def port_scanner(target):
    """فحص المنافذ الأساسية يدوياً بدون الحاجة لـ Nmap خارجي"""
    common_ports = [21, 22, 23, 25, 53, 80, 443, 3306, 8080]
    open_ports = []
    
    # محاولة فحص المنافذ
    target_ip = socket.gethostbyname(target)
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    
    return f"المنافذ المفتوحة على {target} هي: {open_ports}"

if api_key:
    # إعداد النموذج
    llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama3-8b-8192")

    # تعريف الأدوات
    tools = [
        Tool(
            name="Port Scanner",
            func=port_scanner,
            description="يستخدم لفحص المنافذ المفتوحة الشائعة على عنوان IP أو رابط."
        )
    ]

    # تهيئة العميل
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    user_input = st.text_input("ماذا تريد أن نفحص اليوم؟", placeholder="مثلاً: افحص localhost")

    if st.button("بدء التحليل"):
        with st.spinner("جاري الفحص والتحليل بالذكاء الاصطناعي..."):
            response = agent.run(user_input)
            st.success("النتيجة:")
            st.write(response)
else:
    st.warning("الرجاء إدخال مفتاح Groq API في الشريط الجانبي لتفعيل الذكاء الاصطناعي.")
