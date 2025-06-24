from flask import Flask, render_template, request, jsonify
import sys
import traceback

# Try different import methods for LangChain compatibility
try:
    from langchain_community.chat_models import Ollama
    from langchain_core.messages import SystemMessage, HumanMessage
    print("✅ Using langchain-community imports")
except ImportError:
    try:
        from langchain_community.llms import Ollama
        from langchain_core.messages import SystemMessage, HumanMessage
        print("✅ Using langchain-community LLMs imports")
    except ImportError:
        try:
            from langchain.chat_models import Ollama
            from langchain.schema import SystemMessage, HumanMessage
            print("⚠️ Using deprecated langchain imports")
        except ImportError as e:
            print(f"❌ Error importing LangChain: {e}")
            print("Please install: pip install langchain-community langchain-core")
            sys.exit(1)

app = Flask(__name__)

# Initialize your Ollama model with error handling
try:
    llm = Ollama(model="llama3.1")
    print("✅ Ollama model initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Ollama: {e}")
    print("Make sure Ollama is running: ollama run llama3.1")
    llm = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if llm is None:
        return jsonify({"error": "Ollama model not available. Please check your Ollama installation."}), 500
    
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        
        # Create system message for Bengali responses
        system_message = SystemMessage(
            content="তুমি একজন জ্ঞানী এবং ভদ্র বাংলা সহকারী। সব প্রশ্নের উত্তর শুধুমাত্র বাংলায় দাও। তুমি সাহায্যকারী, ক্ষতিকর নও।"
        )
        human_message = HumanMessage(content=user_input)
        
        # Get response from Ollama
        response = llm.invoke([system_message, human_message])
        
        # Handle different response types
        if hasattr(response, 'content'):
            reply = response.content
        else:
            reply = str(response)
        
        return jsonify({"reply": reply})
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        traceback.print_exc()
        return jsonify({"error": f"একটি ত্রুটি হয়েছে: {str(e)}"}), 500

@app.route("/health")
def health():
    """Health check endpoint"""
    status = "healthy" if llm is not None else "unhealthy"
    return jsonify({"status": status})

if __name__ == "__main__":
    print("🚀 Starting Bengali ChatBot...")
    print("📍 Make sure Ollama is running: ollama run llama3.1")
    print("🌐 App will be available at: http://localhost:5000")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
