# SSD33

## Springer
1. Search for `input string`
2. Figure out number of pages in search result
3. For each page in search result :
  - Fetch each items's landing page HTML
  - Grab each items's `DOI` number
  - Fecth BibTex (text format) from another link
---
- Parse each BibTex (text format) into a Dictionary and add to global list
- Convert global list into a json and write to the `output.json` file
