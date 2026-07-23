# IntelliRAG 

**AI-Powered Workspace for Structured Research and Retrieval**

IntelliRAG is a Retrieval-Augmented Generation (RAG) application that allows users to build an AI-powered knowledge base from **PDF documents** or **public GitHub repositories** and interact with the indexed content using natural-language questions.

The application processes the selected source, splits its content into chunks, generates semantic embeddings, stores them in a vector database, and retrieves relevant context to generate grounded answers.

🌐 **Live Demo:**  
https://intellirag-rag.streamlit.app/

---

## ✨ Features

### 📄 PDF Knowledge Base
- Upload PDF documents
- Extract and process document text
- Split documents into manageable chunks
- Generate semantic embeddings
- Store embeddings for similarity-based retrieval
- Ask questions directly about uploaded documents

### 💻 GitHub Repository Analysis
- Enter the URL of a public GitHub repository
- Clone and process the repository automatically
- Extract supported source-code and documentation files
- Convert repository content into searchable chunks
- Ask natural-language questions about the codebase

### 🔎 Semantic Search
IntelliRAG uses vector embeddings to retrieve information based on semantic similarity rather than simple keyword matching.

### 🤖 RAG-Powered Question Answering
Relevant chunks are retrieved from the vector database and supplied to the LLM as context, allowing IntelliRAG to generate answers grounded in the indexed source.

### 🗑️ Workspace Management
Users can clear the current workspace and create a new knowledge base whenever required.

---

## 🏗️ How IntelliRAG Works

```text
             ┌──────────────────────┐
             │    User selects      │
             │   knowledge source   │
             └──────────┬───────────┘
                        │
              ┌─────────┴─────────┐
              │                   │
           PDF File        GitHub Repository
              │                   │
              └─────────┬─────────┘
                        │
                        ▼
               Content Extraction
                        │
                        ▼
                  Text Chunking
                        │
                        ▼
              HuggingFace Embeddings
                        │
                        ▼
                  ChromaDB
                 Vector Store
                        │
                        ▼
                Similarity Search
                        │
                        ▼
                 Relevant Context
                        │
                        ▼
                   Groq LLM
                        │
                        ▼
                 Generated Answer
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application language |
| Streamlit | Web application and user interface |
| LangChain | RAG pipeline and LLM integration |
| ChromaDB | Vector database |
| Hugging Face | Embedding model integration |
| BAAI/bge-small-en-v1.5 | Semantic embedding model |
| Groq | LLM inference |
| Llama 3.3 70B | Language model |
| GitPython | GitHub repository cloning and processing |
| PyPDF | PDF text extraction |
| BeautifulSoup | Content processing utilities |
| python-dotenv | Environment variable management |

---

## 🧠 Models

### Embedding Model

```text
BAAI/bge-small-en-v1.5
```

The embedding model converts document and source-code chunks into numerical vectors that enable semantic similarity search.

### LLM

```text
llama-3.3-70b-versatile
```

The LLM is accessed through Groq and generates responses using the context retrieved from the vector database.

---

## 📁 Project Structure

```text
IntelliRAG/
│
├── app/
│   ├── database.py
│   ├── file_manager.py
│   └── ...
│
├── rag/
│   ├── config.py
│   ├── ingest.py
│   ├── vectorstore.py
│   ├── github_reader.py
│   ├── query_engine.py
│   └── ...
│
├── utils/
│   ├── github_loader.py
│   └── ...
│
├── data/
│
├── docs/
│
├── app.py
├── chat.py
├── ingest.py
├── developer.py
├── requirements.txt
├── runtime.txt
├── Procfile
├── secrets.toml.example
├── .gitignore
└── README.md
```

> The exact contents of temporary data directories may differ between local and cloud environments.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_INTELLIRAG_GITHUB_REPOSITORY_URL>
cd IntelliRAG
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

IntelliRAG requires a **Groq API key**.

Create a `.env` file in the project root for local development:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Alternatively, when deploying with Streamlit Community Cloud, add the key through **Streamlit Secrets**.

Example:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

> ⚠️ Never commit your actual `.env` file or API keys to GitHub.

---

## ▶️ Running Locally

Start the application with:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 📖 Usage

### Using a PDF

1. Select **PDF** from the Workspace Source.
2. Upload a PDF document.
3. Click **Build Knowledge Base**.
4. Wait for the document to be processed and indexed.
5. Ask questions about the uploaded content.

### Using a GitHub Repository

1. Select **GitHub Repository**.
2. Paste the URL of a **public GitHub repository**.

Example:

```text
https://github.com/username/repository
```

3. Click **Build Knowledge Base**.
4. IntelliRAG clones and processes the repository.
5. The source files are converted into searchable chunks.
6. Ask questions about the repository using natural language.

---

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

The project includes cloud-compatible handling for temporary files and ChromaDB storage so that writable directories can be used correctly in the deployed Linux environment.

Deployment configuration includes:

```text
requirements.txt
runtime.txt
Streamlit Secrets
```

The Groq API key should be configured through Streamlit's secret management rather than committed to the repository.

---

## 🔄 RAG Pipeline

IntelliRAG follows a standard Retrieval-Augmented Generation workflow:

```text
Source
  ↓
Content Extraction
  ↓
Chunking
  ↓
Embedding Generation
  ↓
Vector Storage
  ↓
User Question
  ↓
Query Embedding
  ↓
Similarity Search
  ↓
Relevant Chunks
  ↓
LLM + Retrieved Context
  ↓
Grounded Response
```

This architecture allows the model to answer questions using information retrieved from the user's selected knowledge source.

---

## 🔒 Security

IntelliRAG follows basic secret-management practices:

- API keys are not hardcoded in application code
- Local secrets can be stored using `.env`
- Production secrets are managed using Streamlit Secrets
- `.env` should remain excluded through `.gitignore`
- Public GitHub repositories can be processed without exposing private credentials

---

## 🚀 Future Improvements

Potential improvements include:

- Support for private GitHub repositories
- Repository branch selection
- Multiple-document knowledge bases
- Additional document formats such as DOCX and TXT
- Conversation history
- Source citations in generated responses
- Persistent cloud vector storage
- Repository architecture visualization
- Code dependency analysis
- Improved retrieval and reranking
- User authentication
- Multiple independent workspaces

---

## 🎯 Use Cases

IntelliRAG can be used for:

- Understanding unfamiliar codebases
- Exploring GitHub repositories
- Researching large PDF documents
- Technical documentation Q&A
- Codebase onboarding
- Academic research
- Document-based knowledge assistants
- Semantic information retrieval

---

## 👩‍💻 Author

**Pranavi Jain**

Computer Science & Engineering Student

Interested in Software Development, AI, Generative AI, and building intelligent developer tools.

---

## ⭐ Support

If you find IntelliRAG useful, consider giving the repository a ⭐.

Contributions, suggestions, and feedback are welcome.
