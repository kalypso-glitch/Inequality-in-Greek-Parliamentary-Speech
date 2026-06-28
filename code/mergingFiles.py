
#match a 4-digit year at the beginning of filename
pattern = re.compile(r"^(\d{4}).*\.txt$")
groups = defaultdict(list)

#collect files by year
for file in Path(".").glob("*.txt"):
    match = pattern.match(file.name)

    if match:
        year = match.group(1)

        #skipping already merged files like 1989.txt
        if file.name == f"{year}.txt":
            continue

        groups[year].append(file)

#merge files
for year, files in groups.items():
    output_file = Path(f"{year}.txt")

    #stable order
    files.sort(key=lambda f: f.name)

    with output_file.open("w", encoding="utf-8") as outfile:
        for file in files:
            outfile.write(file.read_text(encoding="utf-8"))
            outfile.write(f"\n--- {file.name} ---\n")

    #delete originals
    for file in files:
        file.unlink()


