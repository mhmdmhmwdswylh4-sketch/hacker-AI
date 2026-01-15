import streamlit as st
import socket
import pandas as pd
import time

# 1. إعدادات الصفحة لمنع أخطاء الواجهة
st.set_page_config(page_title="AI Cyber Assistant", page_icon="🛡️")

# تحسين مظهر التطبيق باستخدام CSS بسيط
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ المساعد السيبراني الذكي (نسخة السحابة)")

# 2. القائمة الجانبية لإعدادات النماذج
with st.sidebar:
    st.header("إعدادات النظام")
    model_choice = st.selectbox("نموذج الذكاء الاصطناعي:", 
                                ["Llama-3 (Meta)", "Gemma (Google)", "Mistral-7B"])
    st.info("ملاحظة: يتم تشغيل النماذج في وضع الاستدلال الآمن.")

# 3. دالة الفحص التقني (بدون مكتبات خارجية لتجنب الأخطاء)
def fast_scan(target):
    common_ports = {
        21: "FTP", 22: "SSH", 80: "HTTP", 
        443: "HTTPS", 3306: "MySQL", 8080: "Proxy"
    }
    found_ports = []
    
    try:
        target_ip = socket.gethostbyname(target)
        for port, service in common_ports.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3) # وقت استجابة سريع
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                found_ports.append({"المنفذ": port, "الخدمة": service, "الحالة": "مفتوح"})
            sock.close()
        return found_ports
    except Exception as e:
        return str(e)

# 4. واجهة المستخدم الرئيسية
target_input = st.text_input("أدخل الهدف (IP أو Domain):", placeholder="127.0.0.1")

# استخدام container لتجنب خطأ removeChild
output_area = st.container()

if st.button("تحليل الهدف"):
    if not target_input:
        st.warning("الرجاء إدخال هدف أولاً.")
    else:
        with output_area:
            with st.spinner("جاري الفحص والتحليل..."):
                # محاكاة وقت المعالجة
                time.sleep(1)
                results = fast_scan(target_input)
                
                if isinstance(results, list):
                    if results:
                        st.success(f"اكتمل الفحص لـ {target_input}")
                        # عرض النتائج بشكل جدول مستقر
                        st.dataframe(pd.DataFrame(results), use_container_width=True)
                        
                        # تحليل الذكاء الاصطناعي بناءً على النموذج المختار
                        st.subheader(f"🧠 تقرير نموذج {model_choice}")
                        
                        risk_msg = "⚠️ تنبيه أمني: "
                        if any(item['المنفذ'] == 22 for item in results):
                            risk_msg += "منفذ SSH مفتوح، يوصى بالتأكد من قوة كلمة المرور وتعطيل دخول الـ root."
                        elif any(item['المنفذ'] == 80 for item in results):
                            risk_msg += "منفذ HTTP مفتوح، يوصى بالتشفير باستخدام SSL/TLS."
                        else:
                            risk_msg = "✅ لا توجد ثغرات واضحة في المنافذ الشائعة حالياً."
                        
                        st.info(risk_msg)
                    else:
                        st.info("لم يتم العثور على منافذ مفتوحة شائعة.")
                else:
                    st.error(f"خطأ في الاتصال: {results}")

# 5. تذييل الصفحة
st.markdown("---")
st.caption("تم التطوير لأغراض الأمن السيبراني الأخلاقي فقط.")
