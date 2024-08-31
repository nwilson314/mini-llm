from llm.tokenizer import SimpleTokenizer, TikTokenizer

def main():
    with open("data/the-verdict.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()

    # tokenizer = SimpleTokenizer(raw_text)
    # ids = tokenizer.encode(raw_text)

    tik_tokenizer = TikTokenizer()
    enc_text = tik_tokenizer.encode(raw_text)

    enc_sample = enc_text[50:]

    context_size = 4
    x = enc_sample[:context_size]
    y = enc_sample[1:context_size+1]

if __name__ == "__main__":
    main()