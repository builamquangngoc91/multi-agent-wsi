# Multi-Agent WSI — CrewAI sample project

This repository contains the **create-wsi-kl** crew generated with the
[crewAI `crewai create` CLI](https://docs.crewai.com). The crew is wired to
Google Gemini, enriched with a PDF knowledge base and runs on Python 3.11.

---

## 1. Quick start

```bash
# 1. Clone the repo
$ git clone https://github.com/<your-org>/multi-agent-wsi.git
$ cd multi-agent-wsi/create_wsi_kl

# 2. Create & activate a Python 3.11 virtual-env (any tool works)
$ python3.11 -m venv .venv
$ source .venv/bin/activate

# 3. Install dependencies (editable mode so you can change the code)
$ pip install -e .

# 4. Extra libraries for knowledge & embeddings
$ pip install docling google-generativeai

# 5. Export your Gemini key (or put it in .env)
$ export GEMINI_API_KEY="<your-key>"

# 6. Run the crew 🎉
$ crewai run          # alias for  python -m create_wsi_kl.main
```

The run streams each agent's thoughts/results to the console and writes the
final markdown report to `report.md`.

---

## 2. Project layout

```text
multi-agent-wsi/
├── README.md            ← this file
└── create_wsi_kl/
    ├── pyproject.toml    ← package & dependency list
    ├── .env             ← place secrets here (GEMINI_API_KEY=…)
    ├── knowledge/
    │   └── sodapdf-converted.pdf   ← searchable PDF
    └── src/create_wsi_kl/
        ├── crew.py      ← agents, tasks, crew definition *(edit me)*
        ├── init_llm.py  ← central Gemini LLM config
        ├── main.py      ← entry-points (run / train / replay / test)
        └── …
```

---

## 3. Environment variables

| Variable         | Purpose                                 |
| ---------------- | --------------------------------------- |
| `GEMINI_API_KEY` | Google AI Studio API key (text + embed) |
| `OPENAI_API_KEY` | Optional – only if you swap to OpenAI   |

You can keep them in `create_wsi_kl/.env` so they're picked up automatically.

---

## 4. Common commands

```bash
# run agents with verbose output
activate-env
crewai run

# train the crew for 10 iterations and save logs
train 10 train_log.pkl

# replay a previous execution starting from task id 3
replay 3

# automated testing (5 runs, eval with Gemini flash model)
test 5 gemini/gemini-1.5-flash
```

---

## 5. Updating the knowledge base

Drop additional PDFs (or other Docling-supported formats) into
`create_wsi_kl/knowledge/` and point to them in `crew.py`:

```python
pdf_source = CrewDoclingSource(
    file_paths=["knowledge/another-file.pdf"],
)
```

The next run will embed & index the new content automatically.

---

## 6. Troubleshooting

- **`ImportError: google-generativeai`** – install it: `pip install google-generativeai`.
- **`FileNotFoundError` for knowledge** – make sure the relative path you pass
  in `CrewDoclingSource` matches the location _inside the package_, e.g.
  `knowledge/your.pdf`.
- **API quota / 429 errors** – Gemini embedding uses the same key as chat.
  If you hit quotas consider switching the embedder to an open-source model.

---

## 7. License

MIT (see `LICENSE`).
