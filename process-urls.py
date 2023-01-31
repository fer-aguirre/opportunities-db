# Import modules
import opportunities_db.data.analyze as analyze
import opportunities_db.data.load as load

# Load data
data = load.data
data_processed = load.data_processed

url = 'https://socialcomquant.ku.edu.tr/2023-summer-school/'


text = analyze.extract_text(url)
title = analyze.extract_title(url)
deadline = analyze.extract_deadline(text)
summary = analyze.extract_summary(text)

print(title)
print(deadline)
print(summary)