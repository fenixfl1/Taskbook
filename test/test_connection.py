import os
import pytest
from config.default import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine


@pytest.fixture
def test_db_connection():
    
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    assert engine