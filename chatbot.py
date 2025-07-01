from textblob import TextBlob
from langdetect import detect
import re
import string

# Utility functions
def clean_text(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))

def contains_word(text, word):
    return re.search(rf'\b{re.escape(word)}\b', text) is not None

# Exit phrases
exit_phrases = [
    "exit", "quit", "bye", "goodbye", "see you",
    "thank you", "that's it",
    "no thanks", "i'm done", "done", "that's all",
    "nothing else", "no"
]

def is_exit_message(text):
    text = text.lower().strip()
    return any(phrase in text for phrase in exit_phrases)

# Greeting & small talk phrases
english_greetings = ["hi", "hello", "hey", "good morning", "good evening", "what's up", "yo", "greetings"]
hindi_greetings = ["नमस्ते", "नमस्कार", "हैलो", "हाय", "सलाम", "सुप्रभात", "राम राम"]
english_how_are_you = ["how are you", "how are you doing", "how are you today"]
hindi_how_are_you = ["कैसे हो", "कैसी हो", "कैसे हो बॉट", "आप कैसे हो", "तुम कैसे हो"]

# Intent database
intents = {
    "track_order": ["where is my order", "order status", "track my order", "order late", "tracking", "order not delivered"],
    "cancel_order": ["cancel my order", "i want to cancel", "stop my order", "order cancel"],
    "return_order": ["return product", "return item", "how to return", "product not good", "i want to return"],
    "refund": ["i want a refund", "money back", "refund not received", "get my money", "refund issue", "want a refund for my product"],
    "damaged_product": ["broken", "damaged", "not working", "received wrong item", "defective", "not functioning"],
    "replace_product": ["replace product", "i want a replacement", "need a replacement", "replace item", "exchange product", "product exchange", "want to exchange"],
    "thanks": ["thank you", "thanks", "shukriya", "dhanyawad"],
    "help": ["help", "i need help", "can you help me", "please help", "i want help", "madad karo", "mujhe madad chahiye"]
}

# Bot responses
responses = {
    "en": {
        "greeting": "Hello! How can I assist you today? 😊",
        "how_are_you": "I'm just a bot, but I'm happy to help you! 🤖",
        "thank_you": "You're most welcome! Let me know if you need anything else. 🙏",
        "bye": "Goodbye! Have a great day! 👋",
        "track_order": "You can track your order here: [Track Order Link]",
        "cancel_order": "To cancel your order, visit: [Cancel Order Link]",
        "return_order": "Here’s how to return your product: [Return Link]",
        "refund": "Refunds are processed in 3-5 business days. Check status here: [Refund Help]",
        "damaged_product": "I’m sorry to hear that! Please report the issue here: [Report Damage Link]",
        "replace_product": "You can request a replacement here: [Replacement Link]",
        "help": "Sure! I can assist you with orders, returns, refunds, or any issues you have. Please tell me more.",
        "default": "I'm here to help with any order-related issue. Could you tell me more?"
    },
    "hi": {
        "greeting": "नमस्ते! मैं आपकी कैसे मदद कर सकता हूँ? 😊",
        "how_are_you": "मैं एक बॉट हूँ, लेकिन आपकी मदद करके खुश हूँ! 🤖",
        "thank_you": "आपका स्वागत है! अगर कुछ और चाहिए हो तो बताएं। 🙏",
        "bye": "अलविदा! आपका दिन शुभ हो! 👋",
        "track_order": "आप अपना ऑर्डर यहाँ ट्रैक कर सकते हैं: [ऑर्डर ट्रैक लिंक]",
        "cancel_order": "ऑर्डर कैंसिल करने के लिए इस लिंक पर जाएं: [कैंसिल लिंक]",
        "return_order": "प्रोडक्ट रिटर्न करने का तरीका यहाँ है: [रिटर्न लिंक]",
        "refund": "रिफंड 3-5 दिनों में प्रोसेस होता है। यहाँ चेक करें: [रिफंड हेल्प]",
        "damaged_product": "हमें खेद है! आप यहाँ खराब प्रोडक्ट की रिपोर्ट कर सकते हैं: [समस्या रिपोर्ट लिंक]",
        "replace_product": "आप यहाँ से प्रोडक्ट रिप्लेसमेंट का अनुरोध कर सकते हैं: [रिप्लेसमेंट लिंक]",
        "help": "ज़रूर! मैं आपकी ऑर्डर, रिटर्न, रिफंड या किसी अन्य समस्या में मदद कर सकता हूँ। कृपया विस्तार से बताएं।",
        "default": "मैं आपकी ऑर्डर से जुड़ी किसी भी समस्या में मदद कर सकता हूँ। कृपया बताएं।"
    }
}

# Language detection
def detect_language(text):
    try:
        lang = detect(text)
        if lang != "hi":
            return "en"
        return "hi"
    except:
        return "en"

# Emotion detection
def detect_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity < -0.2:
        return "negative"
    elif polarity > 0.2:
        return "positive"
    else:
        return "neutral"

# Intent detection
def detect_intent(text):
    text = text.lower()
    for intent, keywords in intents.items():
        for keyword in keywords:
            if all(word in text for word in keyword.split()):
                return intent
    return "default"

# Main reply logic
def generate_reply(text):
    text_clean = clean_text(text)
    lang = detect_language(text)
    reply_set = responses.get(lang, responses["en"])

    if any(phrase in text_clean for phrase in english_how_are_you) and lang == "en":
        return reply_set["how_are_you"]
    if any(phrase in text_clean for phrase in hindi_how_are_you) and lang == "hi":
        return reply_set["how_are_you"]

    if any(contains_word(text_clean, greet) for greet in english_greetings + hindi_greetings):
        return reply_set["greeting"]

    if any(phrase in text_clean for phrase in intents["thanks"]):
        return reply_set["thank_you"]

    if any(phrase in text_clean for phrase in ["bye", "goodbye", "अलविदा", "बाय"]):
        return reply_set["bye"]

    intent = detect_intent(text_clean)
    emotion = detect_emotion(text_clean) if lang == "en" else "neutral"
    base_reply = reply_set.get(intent, reply_set["default"])

    if emotion == "negative":
        empathy = "I'm really sorry to hear that. " if lang == "en" else "हमें खेद है कि आपको परेशानी हुई। "
        return empathy + base_reply
    else:
        return base_reply

# Chatbot conversation loop
last_intent = None
awaiting_exit_confirmation = False

print("\n🤖 Welcome to Customer Assistant! Type 'exit' or 'thank you, that’s it' to end.\n")

while True:
    user_input = input("You: ")
    clean_input = clean_text(user_input)
    lang = detect_language(user_input)

    if awaiting_exit_confirmation:
        if clean_input in ["yes", "yeah", "yep", "sure", "i have a question", "another question"]:
            print("Customer Assistant: Sure! Please go ahead.")
            awaiting_exit_confirmation = False
            continue
        elif clean_input in ["no", "no thanks", "nothing", "nothing else", "exit", "quit", "done", "that's all"]:
            goodbye = responses[lang]["bye"] if lang in responses else "Goodbye!"
            print("Customer Assistant:", goodbye)
            break
        else:
            print("Customer Assistant: I'm here if you have another question, or you can type 'exit' to leave. 😊")
            continue

    if is_exit_message(user_input):
        goodbye = responses[lang]["bye"] if lang in responses else "Goodbye!"
        print("Customer Assistant:", goodbye)
        break

    intent = detect_intent(clean_input)

    if intent == "thanks" and last_intent and last_intent != "thanks":
        if lang == "hi":
            print("Customer Assistant: आपका स्वागत है! क्या आपके पास और कोई सवाल है, या आप बातचीत समाप्त करना चाहते हैं?")
        else:
            print("Customer Assistant: You're welcome! Do you have another question, or would you like to end the conversation?")
        awaiting_exit_confirmation = True
        last_intent = intent
        continue

    bot_reply = generate_reply(user_input)
    print("Customer Assistant:", bot_reply)
    last_intent = intent
    awaiting_exit_confirmation = False



