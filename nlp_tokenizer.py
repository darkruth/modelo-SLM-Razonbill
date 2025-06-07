#!/usr/bin/env python3
"""
Tokenizador NLP RazonbilstroOS
Sistema de tokenización compatible con LLaMA y cuantización int8
"""

import json
import re
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import struct

class RazonbilstroTokenizer:
    """Tokenizador personalizado para RazonbilstroOS"""
    
    def __init__(self, vocab_size: int = 32000):
        self.vocab_size = vocab_size
        self.vocab = {}
        self.inverse_vocab = {}
        self.special_tokens = {
            '<pad>': 0,
            '<unk>': 1,
            '<bos>': 2,
            '<eos>': 3,
            '<sys>': 4,
            '<cmd>': 5,
            '<usr>': 6,
            '<bot>': 7
        }
        self.init_vocab()
        
    def init_vocab(self):
        """Inicializar vocabulario base"""
        # Tokens especiales
        for token, idx in self.special_tokens.items():
            self.vocab[token] = idx
            self.inverse_vocab[idx] = token
        
        # Caracteres básicos
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        chars += ".,!?;:()[]{}\"'-+=/*@#$%^&_|\\~`<> \n\t"
        
        current_idx = len(self.special_tokens)
        for char in chars:
            if char not in self.vocab:
                self.vocab[char] = current_idx
                self.inverse_vocab[current_idx] = char
                current_idx += 1
        
        # Subpalabras comunes en español/inglés
        common_subwords = [
            'ing', 'tion', 'ness', 'ment', 'able', 'ible', 'less', 'ful',
            'er', 'ed', 'ly', 're', 'un', 'pre', 'dis', 'mis',
            'ando', 'endo', 'ción', 'dad', 'mente', 'able', 'ible',
            'ar', 'er', 'ir', 'ado', 'ido', 'ante', 'ente'
        ]
        
        for subword in common_subwords:
            if subword not in self.vocab and current_idx < self.vocab_size:
                self.vocab[subword] = current_idx
                self.inverse_vocab[current_idx] = subword
                current_idx += 1
        
        # Tokens de comando comunes
        command_tokens = [
            'sudo', 'ls', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'git', 'python',
            'pip', 'apt', 'docker', 'ssh', 'vim', 'nano', 'cat', 'echo',
            'grep', 'find', 'chmod', 'chown', 'ps', 'kill', 'top', 'df'
        ]
        
        for cmd in command_tokens:
            if cmd not in self.vocab and current_idx < self.vocab_size:
                self.vocab[cmd] = current_idx
                self.inverse_vocab[current_idx] = cmd
                current_idx += 1
        
        print(f"Vocabulario inicializado con {len(self.vocab)} tokens")
    
    def preprocess_text(self, text: str) -> str:
        """Preprocesar texto antes de tokenizar"""
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Separar puntuación
        text = re.sub(r'([.!?;:,()[\]{}])', r' \1 ', text)
        
        # Normalizar comandos
        text = re.sub(r'\$\s*', '<cmd> ', text)
        
        return text
    
    def tokenize(self, text: str) -> List[int]:
        """Tokenizar texto a lista de IDs"""
        text = self.preprocess_text(text)
        tokens = []
        
        words = text.split()
        for word in words:
            if word in self.vocab:
                tokens.append(self.vocab[word])
            else:
                # Tokenización por subpalabras
                subword_tokens = self.tokenize_subwords(word)
                tokens.extend(subword_tokens)
        
        return tokens
    
    def tokenize_subwords(self, word: str) -> List[int]:
        """Tokenizar palabra en subpalabras"""
        if not word:
            return [self.special_tokens['<unk>']]
        
        tokens = []
        i = 0
        
        while i < len(word):
            found = False
            # Buscar la subpalabra más larga posible
            for length in range(min(8, len(word) - i), 0, -1):
                subword = word[i:i+length]
                if subword in self.vocab:
                    tokens.append(self.vocab[subword])
                    i += length
                    found = True
                    break
            
            if not found:
                # Token de caracter individual
                char = word[i]
                if char in self.vocab:
                    tokens.append(self.vocab[char])
                else:
                    tokens.append(self.special_tokens['<unk>'])
                i += 1
        
        return tokens
    
    def detokenize(self, token_ids: List[int]) -> str:
        """Convertir IDs de tokens a texto"""
        tokens = []
        for token_id in token_ids:
            if token_id in self.inverse_vocab:
                token = self.inverse_vocab[token_id]
                if not token.startswith('<') or not token.endswith('>'):
                    tokens.append(token)
        
        text = ''.join(tokens)
        # Limpiar espacios extra
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def encode_conversation(self, messages: List[Dict]) -> List[int]:
        """Codificar conversación completa"""
        tokens = [self.special_tokens['<bos>']]
        
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            if role == 'system':
                tokens.append(self.special_tokens['<sys>'])
            elif role == 'user':
                tokens.append(self.special_tokens['<usr>'])
            elif role == 'assistant':
                tokens.append(self.special_tokens['<bot>'])
            
            content_tokens = self.tokenize(content)
            tokens.extend(content_tokens)
        
        tokens.append(self.special_tokens['<eos>'])
        return tokens
    
    def save_tokenizer(self, path: str):
        """Guardar tokenizador"""
        tokenizer_data = {
            'vocab': self.vocab,
            'inverse_vocab': self.inverse_vocab,
            'special_tokens': self.special_tokens,
            'vocab_size': self.vocab_size
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(tokenizer_data, f, ensure_ascii=False, indent=2)
        
        print(f"Tokenizador guardado en: {path}")
    
    def load_tokenizer(self, path: str):
        """Cargar tokenizador"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.vocab = data['vocab']
        self.inverse_vocab = {int(k): v for k, v in data['inverse_vocab'].items()}
        self.special_tokens = data['special_tokens']
        self.vocab_size = data['vocab_size']
        
        print(f"Tokenizador cargado desde: {path}")
    
    def export_for_llama_cpp(self, output_path: str):
        """Exportar tokenizador para llama.cpp"""
        # Crear formato compatible con llama.cpp
        llama_vocab = {
            'vocab': self.vocab,
            'model_type': 'razonbilstro',
            'vocab_size': self.vocab_size,
            'bos_token_id': self.special_tokens['<bos>'],
            'eos_token_id': self.special_tokens['<eos>'],
            'pad_token_id': self.special_tokens['<pad>'],
            'unk_token_id': self.special_tokens['<unk>']
        }
        
        with open(output_path, 'wb') as f:
            pickle.dump(llama_vocab, f)
        
        print(f"Tokenizador exportado para llama.cpp: {output_path}")
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas del tokenizador"""
        return {
            'vocab_size': len(self.vocab),
            'special_tokens': len(self.special_tokens),
            'character_tokens': sum(1 for token in self.vocab.keys() if len(token) == 1),
            'subword_tokens': sum(1 for token in self.vocab.keys() if len(token) > 1 and not token.startswith('<')),
            'command_tokens': sum(1 for token in self.vocab.keys() if token in ['sudo', 'ls', 'cd', 'git', 'python'])
        }

def main():
    """Demostración del tokenizador"""
    print("Tokenizador NLP RazonbilstroOS")
    print("=" * 40)
    
    # Crear tokenizador
    tokenizer = RazonbilstroTokenizer()
    
    # Textos de prueba
    test_texts = [
        "Hola, ¿cómo estás?",
        "sudo apt update && apt upgrade",
        "git clone https://github.com/usuario/proyecto.git",
        "Explícame qué es machine learning",
        "ls -la | grep python"
    ]
    
    print("\nPruebas de tokenización:")
    for i, text in enumerate(test_texts):
        print(f"\n[{i+1}] Texto: {text}")
        tokens = tokenizer.tokenize(text)
        print(f"Tokens: {tokens}")
        reconstructed = tokenizer.detokenize(tokens)
        print(f"Reconstruido: {reconstructed}")
    
    # Conversación completa
    conversation = [
        {"role": "user", "content": "Abre el terminal"},
        {"role": "assistant", "content": "Abriendo terminal del sistema"},
        {"role": "user", "content": "ls -la"}
    ]
    
    conv_tokens = tokenizer.encode_conversation(conversation)
    print(f"\nConversación tokenizada: {conv_tokens}")
    
    # Estadísticas
    stats = tokenizer.get_stats()
    print(f"\nEstadísticas del tokenizador:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Guardar tokenizador
    tokenizer.save_tokenizer("razonbilstro_tokenizer.json")
    tokenizer.export_for_llama_cpp("razonbilstro_tokenizer.pkl")

if __name__ == "__main__":
    main()