# Egg Production Tracker (Web Interface)

A small web app that lets a poultry farm manager log daily egg production per shed
from a browser, and see the totals update on the same page without a reload.

Day 18 of my AI masterclass. It builds on the Day 17 REST API by adding a browser
interface: an HTML form that calls the Flask API with JavaScript `fetch()`.

## Live demo

**https://egg-production-tracker.onrender.com/**

Open the link, enter a shed name, a date and an egg count, and click Submit. The table and totals update on the same page without a reload.

> **Please note:**
> - This demo runs on a free hosting plan, so **the first visit can take up to 50 seconds** while the app wakes up. After that it responds normally.
> - Records are stored in memory, so **they are cleared whenever the app restarts or goes idle**. A production version would use a database.

## What it does

- A form for the shed name, date and egg count
- On **Submit**, the page sends the record to the API (`POST /api/eggs`)
- It then fetches all records (`GET /api/eggs`) and redraws the table and totals
- The page never reloads
- Shows the overall total, a total per shed, and a running total on every row
- Shows a clear message if the input is invalid or the server is not reachable

## How it works

```
Browser (templates/index.html)              Flask (app.py)
  form submit  --- POST /api/eggs ------->  validate, store in list
  redraw table <-- GET  /api/eggs --------  records + running totals
```

Flask serves the page itself at `/`. Because the page and the API share one address,
the JavaScript calls `/api/eggs` directly and no CORS setup is needed.

## API

### `POST /api/eggs`

| Field   | Type    | Rules                               |
|---------|---------|-------------------------------------|
| `shed`  | text    | required, cannot be blank           |
| `date`  | text    | required, real date as `YYYY-MM-DD` |
| `count` | integer | required, whole number, 0 or more   |

Returns `201` with the stored record, or `400` with `{"error": "..."}`.

### `GET /api/eggs`

```json
{
  "records": [
    { "id": 1, "shed": "Shed A", "date": "2026-11-04", "count": 420, "running_total": 420 }
  ],
  "total_eggs": 420,
  "totals_by_shed": { "Shed A": 420 }
}
```

## Setup

Requires Python 3.9 or newer.

```powershell
git clone <your-repo-url>
cd egg-tracker-ui
pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

Open it through that address. Double-clicking `index.html` will not work, because the
page needs Flask running to serve it and to answer its requests.

## Try it

1. Enter `Shed A`, today's date and `420`, then click **Submit**.
2. Enter `Shed B`, the same date and `380`, then **Submit**.
3. Enter `Shed A`, tomorrow's date and `410`, then **Submit**.
4. Enter `Shed B`, tomorrow's date and `395`, then **Submit**.

After each submit, the table gains a row and the totals change without the page
reloading. After the four records you should see running totals of 420, 800, 1210
and 1605, with Shed A at 830 and Shed B at 775.

To see the validation, clear the shed name or enter a decimal such as `12.5` and submit.

## Project structure

```
egg-tracker-ui/
  app.py              Flask backend (API and page route)
  templates/
    index.html        the browser interface
  requirements.txt    dependencies
  .gitignore
  README.md
```

## Limitations

- **Records are kept in memory.** Restarting the server erases them.
- **No login.** Anyone who can reach the address can view and add records.
- **No edit or delete.** A wrongly typed record cannot be corrected yet.

## Who could use a tool like this, and at what price

The tool does one thing: record a number per location per day, and add it up. Many
small businesses in Kenya do exactly that today on WhatsApp, in an exercise book or
on a calculator. The table below shows who could use it and what I would charge. All
prices are in Kenya shillings (KES), and they are my estimates, to be adjusted for each
client.

| Business | What they would log | Setup (one-time) | Monthly |
|----------|---------------------|------------------|---------|
| Poultry and egg farmers | Eggs per shed per day | 25,000 - 35,000 | 2,000 - 3,000 |
| Dairy farmers | Litres of milk per cow or per milking | 25,000 - 40,000 | 2,000 - 3,500 |
| Fish farmers | Kilograms harvested per pond | 20,000 - 30,000 | 1,500 - 2,500 |
| Greenhouse and horticulture growers | Kilograms picked per greenhouse per day | 25,000 - 40,000 | 2,000 - 3,500 |
| Boda boda and matatu owners | Daily takings per bike or vehicle | 20,000 - 35,000 | 2,000 - 3,000 |
| Butcheries, kiosks and small shops | Daily sales or stock count per outlet | 15,000 - 30,000 | 1,500 - 2,500 |
| Salons and barbershops with several chairs | Clients served per chair per day | 15,000 - 25,000 | 1,500 - 2,000 |

How I set the prices:

- **Setup** covers customising the form for the business (for example "pond" instead
  of "shed", or "KES" instead of "eggs"), replacing the in-memory list with a database
  so records survive restarts, adding a login, deploying with HTTPS, and showing the
  owner how to use it.
- **Monthly** covers hosting, daily backups, fixing problems and small changes.
- Businesses with several locations or more daily records sit at the top of each range.
  A farmer with one shed and a single user sits at the bottom.
- The in-memory version in this repository is a demo. The prices above assume the
  database and login are included.
- Monthly fees are easy to collect through M-Pesa, which most of these clients already use.