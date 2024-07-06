import spacy

nlp = spacy.load("en_core_web_sm")

def extract_intent_and_entities(user_input):
    doc = nlp(user_input)
    
    intents = {
        "schedule": ["schedule", "book", "set up"],
        "reminder": ["remind", "remember", "don't forget"],
        "information": ["what", "how", "when", "where", "why", "search"]
    }
    
    intent = "unknown"
    for key, words in intents.items():
        if any(word in user_input.lower() for word in words):
            intent = key
            break
    
    entities = {ent.label_: ent.text for ent in doc.ents}
    
    return intent, entities