import os, threading, pickle


class StateManager():
    
    def __init__(self, filename):
        self.filename = filename
        self.lock = threading.Lock()
        self._state = None
        
    def get(self):
        with self.lock:
            if self._state is None:
                self._state = self._load_state()
        return self._state

    def save(self):
        with self.lock:
            self._persist_state()
            
    def _load_state(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'rb') as f:
            return pickle.load(f)
        
    def _persist_state(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self._state, f)
            
