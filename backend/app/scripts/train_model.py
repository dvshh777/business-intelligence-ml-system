from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.services.model_service import train_model


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        metrics = train_model(db)
    print(f"Training complete: {metrics}")


if __name__ == "__main__":
    main()
