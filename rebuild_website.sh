#!/bin/bash

# ---------------------------------------------------------------
# TODO 
# besoin de loop sur tous les book.toml
# bien faire les ln avec les scripts et les media sur tous les dossiers dans book/
# revoir les ./../media (qui ne marchent pas en local de toute facon) dans les fichier md > media/
# créer la version francaise et tester la redirection de langue (la page doit exister, obligatoire)

# ---------------------------------------------------------------
# variables declaration
ROOT=/home/www-data/rpgpowerforge

# ---------------------------------------------------------------
# virtual env creation
cd ${ROOT}
python3 -m venv venv
source venv/bin/activate

# ---------------------------------------------------------------
# requirements
pip install -r requirements.txt --no-input

# ---------------------------------------------------------------
# Save previous book
if [ -d "${ROOT}/book" ]; then
    rm -rf ${ROOT}/book.previous_build || true
    mv ${ROOT}/book ${ROOT}/book.previous_build
fi

# ---------------------------------------------------------------
# Pre-build script
echo " ======================= [ WEBSITE : PRE-BUILD SCRIPT ] ======================="
python3 ${ROOT}/scripts/pre_build.py

# ---------------------------------------------------------------
# BUILD SCRIPTS
echo " ======================= [ WEBSITE : BUILD ] ======================="
# find all folders under ./src
for folder in $(find src -mindepth 1 -maxdepth 1 -type d); do
    # find all the book.toml files and execute the build
    if [ -f "${folder}/book.toml" ]; then
        # Replace "src" with "book"
        output_dir="${folder/src/book}"
        echo "Building: ${ROOT}/${folder} -> ${ROOT}/${output_dir}"
        mdbook build "${ROOT}/${folder}" -d "${ROOT}/${output_dir}"
    fi
done

# ---------------------------------------------------------------
# HERO PAGE
cp ${ROOT}/resources/hero.html ${ROOT}/book/index.html

# ---------------------------------------------------------------
# MAKE RESOURCES AVAILABLE
ln -s ${ROOT}/custom-font ${ROOT}/book/custom-font
ln -s ${ROOT}/custom-css  ${ROOT}/book/custom-css
ln -s ${ROOT}/custom-js   ${ROOT}/book/custom-js
ln -s ${ROOT}/media       ${ROOT}/book/media
ln -s ${ROOT}/resources   ${ROOT}/book/resources

# ---------------------------------------------------------------
# POST BUILD SCRIPTS
echo " ======================= [ WEBSITE : POST-BUILD SCRIPT ] ======================="
python3 ${ROOT}/scripts/post_build.py
python3 ${ROOT}/scripts/generate_sitemap.py
python3 ${ROOT}/scripts/thumbnail.py

# ---------------------------------------------------------------
# desactivate venv
deactivate


## zip user manual resources files
#cd ${root_dir}/media/
#zip -r user_resources.zip user_resources || true

#cd ${root_dir}

# ---------------------------------------------------------------
# WHATS NEW MARKDOWN
#input_md=${root_dir}/src/doc/latest_news.md
#output_md=${root_dir}/book/doc/latest_news.md
#output_hash=${output_md}.sha256
#cp ${input_md} ${output_md}
#sha256sum ${output_md} | awk '{print $1}' > ${output_hash}

# ---------------------------------------------------------------
# WEBSITE METADATA
# Now the website is built, we can add metadata files
# robots.txt
#cp ${root_dir}/resources/robots.txt ${root_dir}/book/robots.txt
