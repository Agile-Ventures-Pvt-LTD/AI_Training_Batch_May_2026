import logging
from pathlib import Path
from langchain_community.document_loaders import TextLoader, PyPDFLoader
import config

logger = logging.getLogger(__name__)


def load_policy_documents():
    policy_path = Path(config.POLICY_DATA_PATH)
    if not policy_path.exists():
        raise FileNotFoundError(f"Policy folder not found: {policy_path}")

    docs = []
    for f in sorted(policy_path.iterdir()):
        if f.suffix.lower() not in {".md", ".txt", ".pdf"}:
            continue
        try:
            loader = PyPDFLoader(str(f)) if f.suffix.lower() == ".pdf" else TextLoader(str(f), encoding="utf-8")
            pages = loader.load()
            domain = next((v for k, v in config.POLICY_DOMAIN_MAP.items() if k in f.stem.lower()), "OTHER")
            for i, doc in enumerate(pages):
                doc.metadata.update({"source_file": f.name, "policy_domain": domain, "page_number": doc.metadata.get("page", i)})
            docs.extend(pages)
            logger.info("%s loaded (%d pages, domain=%s)", f.name, len(pages), domain)
        except Exception as e:
            logger.error("Skipping %s — %s", f.name, e)

    if not docs:
        raise ValueError(f"No policy documents found in {policy_path}")
    return docs
