# Put This Website Online

This is a Flask website. It cannot fully work on GitHub Pages because GitHub Pages only serves static HTML, CSS, and JavaScript. Your site needs a Python server for:

- the admin login
- saving customer records to Excel
- the services database
- uploaded certificate images

Use a Python host such as Render, Railway, PythonAnywhere, or Fly.io. The files in this folder are ready for Render.

## Deploy With Render

1. Push this full project folder to GitHub.
2. Make sure these files are included in GitHub:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `render.yaml`
   - `runtime.txt`
   - `templates/`
   - `static/`
3. Go to Render and create a new **Blueprint** or **Web Service** from your GitHub repository.
4. If using a Web Service manually, set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variables:
   - `SECRET_KEY`: any long random text
   - `ADMIN_USERNAME`: your admin username
   - `ADMIN_PASSWORD`: your admin password
   - `PERSISTENT_DIR`: `/var/data`
6. Add a persistent disk mounted at `/var/data`.
7. Deploy.

After deployment, Render gives you a public link like:

```text
https://your-site-name.onrender.com
```

That link will work from the internet even when your computer is turned off.

## Important

Do not deploy only `templates/index.html`. The whole Flask project must be deployed.

The `.env` file should not be uploaded to GitHub. Set passwords in the hosting service environment variables instead.

## Save Excel On Your Windows Desktop

If the website is running on your Windows computer, add this to your local `.env` file:

```text
EXCEL_PATH=C:\Users\YourName\Desktop\records.xlsx
```

Replace `YourName` with your Windows user name.

This works only when the website is running on that computer. If the website is running on Render while your computer is off, customer details save on Render's server disk instead.
