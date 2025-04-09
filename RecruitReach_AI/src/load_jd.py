def load_jds_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split by the separator
    jd_blocks = content.split("=== JD START ===")
    
    # Remove empty entries and strip whitespace
    jds = [jd.strip() for jd in jd_blocks if jd.strip()]
    return jds


if __name__ == "__main__":
    # Example usage
    jd_list = load_jds_from_file("JD.txt")

    print(f"Total JDs found: {len(jd_list)}\n")
    print("First JD:\n", jd_list[0])
