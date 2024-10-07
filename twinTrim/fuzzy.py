import os
from fuzzywuzzy import fuzz

def compare_file_content(file1, file2):
    """Compares the content of two files using fuzzy matching."""
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            content1 = f1.read()
            content2 = f2.read()
        
        # Calculate similarity score
        similarity_score = fuzz.ratio(content1, content2)
        return similarity_score
    
    except Exception as e:
        print(f"Error reading files {file1} or {file2}: {e}")
        return 0  # Return 0 if there’s an error

def find_fuzzy_duplicates(files, threshold=90):
    """Finds fuzzy duplicates in a list of file paths."""
    duplicates = []
    seen_files = {}

    for file_path in files:
        for existing_file in seen_files:
            similarity_score = compare_file_content(existing_file, file_path)
            if similarity_score >= threshold:
                duplicates.append((existing_file, file_path))
                break  # Stop checking once a duplicate is found
        else:
            # If no duplicates found, add the file to the seen_files
            seen_files[file_path] = file_path
            
    return duplicates
