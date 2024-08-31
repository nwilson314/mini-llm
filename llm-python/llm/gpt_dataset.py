from typing import TypeVar

import torch
from torch import Tensor
from torch.utils.data import Dataset, DataLoader

from llm.tokenizer import TokenizerBase


TTokenizer = TypeVar("TTokenizer", bound=TokenizerBase)


class GPTDataset(Dataset):
    def __init__(self, txt: str, tokenizer: TTokenizer, max_length: int, stride: int):
        self.input_ids: list[Tensor] = []
        self.target_ids: list[Tensor] = []

        token_ids = tokenizer.encode(txt)

        for i in range(0, len(token_ids) - max_length, stride):
            input_chunk = token_ids[i: i + max_length]
            target_chunk = token_ids[i + 1: i + max_length + 1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.target_ids[idx]