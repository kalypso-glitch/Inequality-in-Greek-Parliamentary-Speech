from pathlib import Path
import re
import html
from termSearching import term_searching
import argostranslate.translate

#same pattern as in termSearching.py
pattern= r'στερεότυπ.*\b|στερεοτύπ.*\b|στερεοτυπ.*\b'

#translating function
def translate_text(text):

    return argostranslate.translate.translate(
        text,
        "el",
        "en"
    )

#highlight searched term
def highlight_term(text):

    escaped_text = html.escape(text)

    return re.sub(
        pattern,
        lambda match: f"<mark>{match.group(0)}</mark>",
        escaped_text,
        flags=re.IGNORECASE
    )


#creating html files
def main():

    output_file = Path(
        "STEREOTYPE_context.html"
    )

    html_output = []

    # --------------------------------------------------
    # HTML HEADER
    # --------------------------------------------------

    html_output.append("""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<title>'Stereotype' in Greek Parliamentary Speech</title>

<style>

body {
    font-family: Arial, sans-serif;
    margin: 40px;
    background-color: #f5f5f5;
}

h1 {
    text-align: center;
    margin-bottom: 50px;
}

.year {
    margin-top: 60px;
    padding: 10px;
    background-color: #333;
    color: white;
}

table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    margin-bottom: 40px;
    background-color: white;
}

th,
td {
    width: 50%;
}

th {
    background-color: #ddd;
    padding: 12px;
    border: 1px solid #aaa;
    font-size: 18px;
}

td {
    padding: 15px;
    border: 1px solid #aaa;
    vertical-align: top;
    line-height: 1.6;
    word-wrap: break-word;
}

.greek {
    font-family: Arial, sans-serif;
}

.english {
    font-family: Arial, sans-serif;
}

mark {
    background-color: yellow;
    font-weight: bold;
}

tr:hover td {
    background-color: #fafafa;
}

</style>

</head>

<body>

<h1>
'Stereotype' in Greek Parliamentary Speech
</h1>
""")

    # --------------------------------------------------
    # PROCESS FILES
    # --------------------------------------------------

    for file in sorted(Path("data").glob("*.txt")):

        # get year from filename
        year = file.stem[:4]

        # use term_searching function
        results = term_searching(file)

        # skip files where term was not found
        if not results:
            continue

        # --------------------------------------------------
        # YEAR
        # --------------------------------------------------

        html_output.append(
            f'<h2 class="year">{year}</h2>'
        )

        # --------------------------------------------------
        # TABLE
        # --------------------------------------------------

        html_output.append("""
<table>

<tr>
<th>Greek</th>
<th>English</th>
</tr>
""")

        # --------------------------------------------------
        # TRANSLATE EACH MATCH
        # --------------------------------------------------

        for greek_text in results:

            # translate Greek
            english_text = translate_text(
                greek_text
            )

            # highlight term in Greek
            greek_html = highlight_term(
                greek_text
            )

            
            # escape English HTML characters
            english_html = html.escape(
                english_text
            )

            # add row
            html_output.append(f"""
<tr>

<td class="greek">
{greek_html}
</td>

<td class="english">
{english_html}
</td>

</tr>
""")

        # close table
        html_output.append("""
</table>
""")

    # --------------------------------------------------
    # CLOSE HTML
    # --------------------------------------------------

    html_output.append("""
</body>
</html>
""")

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    output_file.write_text(
        "".join(html_output),
        encoding="utf-8"
    )

    print(
        f"\nSaved to: {output_file}"
    )


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    main()