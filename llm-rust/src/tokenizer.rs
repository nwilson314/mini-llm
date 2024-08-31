use regex::Regex;
use std::collections::{HashMap, HashSet};


const REGEX_PATTERN: &str = r"--|[,.!?':;]|[^\s,.!?':;-]+";

#[derive(Debug)]
pub struct Tokenizer {
    token_to_id: HashMap<String, usize>,
    id_to_token: HashMap<usize, String>,
}

impl Tokenizer {
    pub fn new(text: &str) -> Self {
        let re = Regex::new(REGEX_PATTERN).unwrap();

        let tokens: Vec<&str> = re.find_iter(text)
            .map(|mat| mat.as_str())
            .collect();

        let mut unique_tokens: HashSet<&str> = HashSet::new();

        for token in tokens {
            unique_tokens.insert(token);
        }

        let mut sorted_tokens: Vec<String> = unique_tokens.into_iter().map(String::from).collect();
        sorted_tokens.sort();

        let mut token_to_id = HashMap::new();
        let mut id_to_token = HashMap::new();

        for (index, token) in sorted_tokens.iter().enumerate() {
            token_to_id.insert(token.clone(), index);
            id_to_token.insert(index, token.clone());
        }

        Tokenizer {
            token_to_id,
            id_to_token,
        }
    }

    pub fn encode(&self, text: &str) -> Vec<usize> {
        let re = Regex::new(REGEX_PATTERN).unwrap();

        re.find_iter(text)
            .filter_map(|mat| self.token_to_id.get(mat.as_str()).cloned()) 
            .collect()
    }

    pub fn decode(&self, ids: Vec<usize>) -> String {
        let mut result = String::new();

        for id in ids {
            if let Some(token) = self.id_to_token.get(&id) {
                if result.is_empty() {
                    // First token, directly append
                    result.push_str(token);
                } else if [",", ".", "!", "?", ":", ";", "'", "--"].contains(&token.as_str()) {
                    // Punctuation marks should not have a space before them
                    result.push_str(token);
                } else {
                    // Regular word token, add space before appending
                    result.push(' ');
                    result.push_str(token);
                }
            }
        }

        result
    }
}