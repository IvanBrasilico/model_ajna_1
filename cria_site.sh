jupyter nbconvert notebooks/*.ipynb
mv notebooks/*.html docs/docs/html
mkdocs build -f docs/mkdocs.yml