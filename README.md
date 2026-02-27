# Resume as Code
- The main goal of this project is to treat my CV as a software project. 
Instead of using word or doing manual PDF exports, I use my experience in `YAML`, template it in `Jinja2` and automate the PDF generation using GitHub Actions.


# Workflow 
1. `Data Layer`: All my career details live here in `data/resume.yaml`
2. `logic Layer:` A Python script (`src/build.py`) injects data into a HTLM template
3. `Automation`: Every `git push` triggers github actions that spins up a headless browser and renders the resume and saves the pilex perfect PDF 

# Project Structure
`data/`: contains the `resume.yaml` that contains base data such as my experiences, certificates. The infomation can be overriden by editing the `variants/`
`templates/`: The HTML/Jinja2 source file that defines the layout and ATS-Friendly stying. 
    > You can style this using CSS according to your preference
`src/` contains the python script which is the brain handlin the PDF rendering and variant merging
`.github/workflows/`: The CI/CD instructions for GitHub

# Setup and usage
### 1. Update the content:
- To change resume content, edit `data/resume.yaml`
- Tailor the resume for a specific company using the company name e.g safaricom.yaml
- create the file in the `variants/safaricom.yaml` containing only the fields you want to make edits to 

### 2. Run Locally
- If you wnat to run the build locally on your machine:
 > make sure you have python3 and pip installed

 ```sh
$ pip install -r requirements.txt

# This is the headless browser that does the rendering
$ playwright install chromium

# Run the script for the base resume
$ python3 src/build.py

# run the script for the variant resume
$ python3 src/build.py variant/safaricom.yaml

```
- The PDF file will be generated in the `/dis` file



### Deploy(Auomated)
- Simply push your changes to github
```sh
$ git add .
$ git commit -m "feat: AWS Cloud Practitioner"
$ git push
```
- GitHub Actions will automatically:
 * Validate your YAMl
 * Build the PDF
 * Upload the final resume as an artifact in the `Actions` tab


# ATS Optimisation
- The template is built using sematic HTML using standard `<header>`, `<section>`, `<ul>` tags
- Uses standard fonts(Arial)
