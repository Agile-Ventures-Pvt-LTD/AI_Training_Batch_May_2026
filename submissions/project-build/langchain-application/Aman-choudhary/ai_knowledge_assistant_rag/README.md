##  Project Setup & Steps to Run

### Step 1: Create a Virtual Environment

```bash
uv venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / Mac**

```bash
source .venv/bin/activate
```

---

### Step 2: Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

### Step 3: Configure API Key

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

---