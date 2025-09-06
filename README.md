# Contest Insights GEN AI Pipeline

This project builds a **data-to-insight pipeline** that connects to PostgreSQL, fetches contest summary data, processes it into a structured format, and sends it to an **LLM (Llama/Gemini)** to generate **business insights**.


## Features
- PostgreSQL connection pooling with `psycopg2`.
- Efficient data fetching using `COPY TO STDOUT` into Pandas.
- Automatic logging with execution time tracking.
- Business insight generation from contest summary data.
- LLM-powered analysis with JSON validation and repair.
- Outputs structured insights both to file and Python dictionary.


## Setup

### 1. Clone Repo
```bash
git clone https://github.com/Abrahul-107/Luqta_ai_pipeline.git
cd ai_analysis
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```


---

### 3. Environment Variables

Create a `.env` file in the root folder:

```env
DB_NAME=your_db_name
DB_USER=your_username
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Usage

Run the pipeline:

```bash
python main.py
```

---

## Project Structure

```
├── contest_insights/
│   └── contestInsights.py         # Converts DataFrame → business JSON
├── llm_call/
│   └── call_llama_get_insight.py  # Sends JSON to LLM, repairs & parses insights
├── main.py                        # Pipeline entry point
├── requirements.txt
└── README.md
```

---

## 🔄 Workflow

1. **Fetch Data** → Query contest data from PostgreSQL into Pandas.
2. **Transform** → Convert DataFrame into structured JSON (`generate_business_insights`).
3. **LLM Insights** → Send JSON to LLM and repair/validate output JSON.
4. **Save & Return** → Save insights to `insights.json` and return as Python dict.

---

## Example

Query used in `main.py`:

```sql
SELECT * FROM public.x2_103_contest_summary_reportingcsv;
```

Example final log output:

```
2025-09-06 02:40:12 [INFO] contest_pipeline - Connection pool created successfully
2025-09-06 02:40:13 [INFO] contest_pipeline - Data fetched successfully (234 rows)
2025-09-06 02:40:13 [INFO] contest_pipeline - 📦 JSON prepared for LLM
2025-09-06 02:40:15 [INFO] contest_pipeline - Insights generated successfully
2025-09-06 02:40:15 [INFO] contest_pipeline - Final Insights: {...}
```

---

## Extending

* Swap the SQL query to fetch different contest datasets.
* Update `contestInsights.py` for new insight rules.
* Switch LLM provider in `llm_call/call_llama_get_insight.py`.

---

## Notes

* Requires Python 3.9+
* Optimized for **fast PostgreSQL reads** using `COPY TO STDOUT`.
* If LLM response JSON is malformed, it is auto-repaired with `json-repair`.
