import pandas as pd
import re
from difflib import get_close_matches
from app.clients.ollama_client import ollama_client
from app.core.settings import settings
from app.core.schemas import AgentState, IntentResult

class IntentClassification:
    def __init__(self):

        self.client = ollama_client
        self.model_name = settings.FINETUNED_MODEL
        self.mapping_path = "app/data/intent_mapping.csv"
        
        print(f"--- CONNECTING TO OLLAMA VIA PINGGY ---")    
        
        # Vẫn cần load mapping để thực hiện hậu xử lý (Normalize/Map label)
        self.class_list_str = self._get_class_intent(self.mapping_path)
        self.known_labels = self.class_list_str.split("\n")
        self.norm_map = {self._normalize_intent_label(l): l for l in self.known_labels}

    def _get_class_intent(self, mapping_path):
        try:
            df_label = pd.read_csv(mapping_path)
            return "\n".join(df_label['name_intent'].tolist())
        except Exception as e:
            print(f"Error load file mapping: {e}")
            return ""
        
    def _normalize_intent_label(self, text):
        cleaned_text = str(text).strip().lower()
        cleaned_text = re.sub(r"[^a-z0-9]+", "_", cleaned_text)
        cleaned_text = re.sub(r"_+", "_", cleaned_text).strip("_")
        return cleaned_text

    def _map_to_known_label(self, prediction):
        # Giữ nguyên logic map nhãn cũ của Ngân để đảm bảo độ chính xác
        normalized_prediction = self._normalize_intent_label(prediction)
        if normalized_prediction in self.norm_map:
            return self.norm_map[normalized_prediction]
        
        for normalized_label, original_label in self.norm_map.items():
            if normalized_label in normalized_prediction or normalized_prediction in normalized_label:
                return original_label

        close_matches = get_close_matches(normalized_prediction, list(self.norm_map.keys()), n=1, cutoff=0.8)
        return self.norm_map[close_matches[0]] if close_matches else "unknown"

    def predict(self, message):
        try:
            raw_prediction = self.client.generate(
                model=self.model_name,
                prompt=message
            )
            
            
            return self._map_to_known_label(raw_prediction)
        except Exception as e:
            print(f"Error in predict via OllamaClient: {e}")
            return "unknown"

classifier = IntentClassification()

def intent_node(state: AgentState) -> AgentState:
    print(f"\n--- [NODE] Intent Detection ---")
    predicted_intent = classifier.predict(state.customer_message)
    
    state.intent_data = IntentResult(intent=predicted_intent, confidence=1.0)
    state.trace.append(f"Intent: {predicted_intent}")
    print(f"Result: {predicted_intent}")
    return state