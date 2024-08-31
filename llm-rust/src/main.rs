mod tokenizer;

use std::fs;
use std::io;

use crate::tokenizer::*;

fn main() -> io::Result<()> {
    // Read the text file contents
    let file_path = "./data/tiny_shakespeare.txt";
    let file_content = fs::read_to_string(file_path)?;

    let tokenizer = Tokenizer::new(&file_content);

    let encoded_text = tokenizer.encode(&file_content);
    println!("Encoded: {:?}", encoded_text);
    let decoded_text = tokenizer.decode(encoded_text);
    println!("Decoded: {}", decoded_text);

    Ok(())
}
