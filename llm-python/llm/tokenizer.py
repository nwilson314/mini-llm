import re

import tiktoken

UNK = "<|unk|>"
EOF = "<|eof|>"

REGEX_STR = r'([,.:;?_!"()\']|--|\s)'


class TokenizerBase:
    def encode(self, text: str, *args, **kwargs) -> list[int]:
        raise NotImplementedError

    def decode(self, ids: list[int], *args, **kwargs) -> str:
        raise NotImplementedError
    

class TikTokenizer(TokenizerBase):
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("gpt2")

    def encode(self, text):
        return self.tokenizer.encode(text)

    def decode(self, ids):
        return self.tokenizer.decode(ids)


class SimpleTokenizer(TokenizerBase):
    def __init__(self, raw_text: str):

        preprocessed = re.split(REGEX_STR, raw_text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]

        all_tokens = sorted(list(set(preprocessed)))
        all_tokens.extend([UNK, EOF])

        self.str_to_int = {token:integer for integer,token in enumerate(all_tokens)}
        self.int_to_str = {i:s for s,i in self.str_to_int.items()}

    def encode(self, text):
        preprocessed = re.split(REGEX_STR, text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        preprocessed = [item if item in self.str_to_int else UNK for item in preprocessed]
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids
    
    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text