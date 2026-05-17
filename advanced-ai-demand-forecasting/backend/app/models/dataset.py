from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.sql import func
from app.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)

    total_rows = Column(Integer, default=0)
    total_columns = Column(Integer, default=0)
    columns_info = Column(Text, nullable=True)

    product_category = Column(String(150), index=True, nullable=True)
    region = Column(String(150), index=True, nullable=True)

    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index("idx_dataset_category_region", "product_category", "region"),
    )