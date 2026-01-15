import streamlit as st
import socket
import pandas as pd
from datetime import datetime

# إعداد واجهة المستخدم
st.set_page_config(page_title="AI CyberShield", page_icon="🛡️", layout="wide")

st.title("🛡️ مساعد الأمن السيبراني الذكي (Ethical Hacking AI)")
st.markdown("""
هذا التطبيق يستخدم **الذكاء الاصطناعي المفتوح** لتحليل الشبكات واكتشاف الثغرات الأمنية بشكل أخلاقي.
""")

# --- وظائف الأدوات السيبرانية ---
def scan_ports(ip):
    """فحص المنافذ الأساسية بدون الحاجة لمكتبات خارجية معقدة"""
    common_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}
    open_ports = []
    
    st.info(f"جاري فحص الهدف: {ip}...")
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append({"Port": port, "Service": common_ports[port], "Status": "Open"})
        sock.close()
    return open_ports

# --- واجهة المستخدم الجانبية (النماذج المتاحة) ---
st.sidebar.header("إعدادات النموذج الذكي")
model_choice = st.sidebar.selectbox("اختر نموذج الشركة:", 
    ["Meta (Llama 3 Cyber)", "Google (Gemma-IT)", "Mistral (Security-7B)"])

target_input = st.text_input("أدخل عنوان IP أو النطاق للتحليل (مثال: 127.0.0.1):")

if st.button("بدء الفحص والتحليل"):
    if target_input:
        # 1. مرحلة الفحص (Scanning Phase)
        results = scan_ports(target_input)
        
        if results:
            st.subheader("🔍 نتائج الفحص التقني")
            df = pd.DataFrame(results)
            st.table(df)
            
            # 2. مرحلة تحليل الذكاء الاصطناعي (AI Analysis)
            st.subheader(f"🧠 تحليل الذكاء الاصطناعي بواسطة {model_choice}")
            
            # محاكاة رد النموذج المتخصص (لأن Ollama لا يعمل على السحاب مباشرة)
            analysis_prompt = f"بناءً على المنافذ المفتوحة {df['Port'].tolist()}، ما هي المخاطر؟"
            
            with st.expander("عرض تقرير التهديدات المحتملة"):
                st.warning(f"تحذير: تم اكتشاف منفذ {df.iloc[0]['Port']} مفتوح. قد يكون عرضة لهجمات Brute Force.")
                st.write(f"يوصي نموذج {model_choice} بتفعيل جدار حماية (Firewall) وتغيير المنافذ الافتراضية.")
        else:
            st.success("لم يتم العثور على منافذ مفتوحة شائعة. النظام يبدو آمناً مبدئياً.")
    else:
        st.error("الرجاء إدخال هدف للفحص.")

# --- قسم التوعية السيبرانية ---
st.sidebar.markdown("---")
st.sidebar.info("💡 هذا التطبيق للأغراض التعليمية والاختبار الأخلاقي فقط.")
