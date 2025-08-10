import json
import os
from typing import Dict, List, Union

class DataManager:
    def __init__(self, base_dir='data'):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def load_data(self, filename: str) -> Union[Dict, List]:
        """Load data from JSON with fallback to TXT"""
        json_path = os.path.join(self.base_dir, f"{filename}.json")
        txt_path = os.path.join(self.base_dir, f"{filename}.txt")
        
        # Try loading JSON first
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading {json_path}: {str(e)}")
        
        # Fallback to TXT
        if os.path.exists(txt_path):
            return self._convert_txt_to_json(txt_path, json_path)
            
        return {}

    def _convert_txt_to_json(self, txt_path: str, json_path: str) -> dict:
        """Convert legacy TXT format to JSON"""
        data = {}
        
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if 'keywords' in txt_path:
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 3:
                            key = parts[0]
                            data[key] = {
                                "type": parts[1],
                                "response": parts[2],
                                "context": parts[3] if len(parts) > 3 else "general"
                            }
                    elif 'synonyms' in txt_path:
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 2:
                            base_word = parts[0]
                            synonyms = [s.strip() for s in parts[1].split(',')]
                            data[base_word] = synonyms
            
            # Save as JSON for future use
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(f"Converted {txt_path} to {json_path}")
            return data
            
        except Exception as e:
            print(f"Error converting {txt_path}: {str(e)}")
            return {}

    def save_data(self, filename: str, data: Union[Dict, List]):
        """Save data to JSON"""
        json_path = os.path.join(self.base_dir, f"{filename}.json")
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving {json_path}: {str(e)}")
            return False