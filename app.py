import nmap
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

# --- الأدوات الذكية ---

def advanced_scanner(target):
    """يقوم بفحص الخدمات وإصداراتها لمحاولة توقع الثغرات"""
    nm = nmap.PortScanner()
    # -sV لمحاولة معرفة إصدار الخدمة (Version Detection)
    nm.scan(target, arguments='-sV --version-intensity 5')
    
    scan_results = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                service = nm[host][proto][port]
                info = f"Port: {port}, Service: {service['name']}, Version: {service['version']}"
                scan_results.append(info)
    
    return "\n".join(scan_results) if scan_results else "لم يتم العثور على خدمات مفتوحة."

# --- إعداد النماذج (متعددة الخيارات) ---
# يمكنك تغيير النموذج بناءً على ما قمت بتحميله في Ollama
# Meta: llama3 | Mistral: mistral | Google: gemma
llm = Ollama(model="llama3", temperature=0.1) # temperature منخفضة لضمان دقة التحليل التقني

tools = [
    Tool(
        name="Advanced Service Scanner",
        func=advanced_scanner,
        description="استخدم هذه الأداة للحصول على الخدمات وإصداراتها من الهدف."
    )
]

# --- تهيئة الوكيل السيبراني ---
cyber_agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True,
    handle_parsing_errors=True
)

# --- تجربة عملية ---
prompt = """
قم بفحص الهدف 127.0.0.1. 
بناءً على الخدمات المكتشفة وإصداراتها، اقترح ثغرات محتملة (CVEs) 
وقدم نصائح أمنية لغلق هذه الثغرات.
"""

# print(cyber_agent.run(prompt))
