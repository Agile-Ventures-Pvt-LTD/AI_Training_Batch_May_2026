import kagglehub
import shutil
from pathlib import Path

dataset_path = Path(
    kagglehub.dataset_download(
        "terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database"
    )
)

source_db = dataset_path / "olist.sqlite"

target_db = Path("data/ecommerce.db")

target_db.parent.mkdir(
    exist_ok=True
)

shutil.copy(
    source_db,
    target_db
)

print("Database created successfully")