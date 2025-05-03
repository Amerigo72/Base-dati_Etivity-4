from sqlalchemy import create_engine, Column, Integer, String, CHAR, TEXT, BLOB, DECIMAL, Date, SmallInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import exc

# Definizione della stringa di connessione al database MySQL
DB_USER = 'root'
DB_PASSWORD = 'Manta_1200'
DB_HOST = 'localhost'
DB_NAME = 'etivity 4'
DB_CHARSET = 'utf8mb4'
# DB_USER = 'root'
# DB_PASSWORD = 'root'
# DB_HOST = '127.0.0.1'
# DB_NAME = 'etivity4'
# DB_CHARSET = 'utf8mb4'

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset={DB_CHARSET}"
#DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3310/{DB_NAME}?charset={DB_CHARSET}"
     
#DATABASE_URL = "sqlite:///./mydatabase.db"  # Using SQLite for simplicity

engine = create_engine(DATABASE_URL)
conn = engine.connect()

# Definizione della base per le classi modello
Base = declarative_base()

# definizione delle tabelle del mio database
class Categoria(Base):
    __tablename__ = "CATEGORIA"

    ID_CAT = Column(Integer, primary_key=True, autoincrement=True)
    DENOMINAZIONE = Column(String(30), nullable=False)

    prodotti = relationship("Prodotto", back_populates="categoria")

class Prodotto(Base):
    __tablename__ = "PRODOTTO"

    ID_PRODOTTO = Column(CHAR(10), primary_key=True)
    NOME = Column(String(50), nullable=False)
    DESCRIZIONE = Column(TEXT, nullable=False)
    IMG = Column(BLOB)
    PREZZO = Column(DECIMAL(8, 2), nullable=False)
    STAR = Column(DECIMAL(2, 1))
    ID_CAT = Column(Integer, ForeignKey("CATEGORIA.ID_CAT"))

    categoria = relationship("Categoria", back_populates="prodotti")
    declinazioni = relationship("Declinazioni", back_populates="prodotto")
    feedback = relationship("Feedback", back_populates="prodotto")

class Declinazioni(Base):
    __tablename__ = "DECLINAZIONI"

    SUBCODE = Column(Integer, primary_key=True, autoincrement=True)
    TAGLIA = Column(CHAR(5))
    COLORE = Column(CHAR(10), nullable=False)
    ID_PRODOTTO = Column(CHAR(10), ForeignKey("PRODOTTO.ID_PRODOTTO"))

    prodotto = relationship("Prodotto", back_populates="declinazioni")
    scorte = relationship("ScorteMagazzino", back_populates="declinazione")
    carrelli = relationship("Carrello", back_populates="declinazione")

class Magazzini(Base):
    __tablename__ = "MAGAZZINI"

    ID_MAGAZZINO = Column(Integer, primary_key=True, autoincrement=True)
    CITTA = Column(String(30), nullable=False)
    TELEFONO = Column(Integer, nullable=False)

    scorte_magazzino = relationship("ScorteMagazzino", back_populates="magazzino")

class ScorteMagazzino(Base):
    __tablename__ = "SCORTE_MAGAZZINO"

    ID_MAGAZZINO = Column(Integer, ForeignKey("MAGAZZINI.ID_MAGAZZINO"), primary_key=True)
    SCORTE = Column(SmallInteger)
    SUBCODE = Column(Integer, ForeignKey("DECLINAZIONI.SUBCODE"), primary_key=True)

    magazzino = relationship("Magazzini", back_populates="scorte_magazzino")
    declinazione = relationship("Declinazioni", back_populates="scorte")

class Utente(Base):
    __tablename__ = "UTENTE"

    ID_UTENTE = Column(Integer, primary_key=True, autoincrement=True)
    NOME = Column(String(30), nullable=False)
    COGNOME = Column(String(30), nullable=False)
    EMAIL = Column(String(30), nullable=False)
    PASSWORD = Column(String(30), nullable=False)
    TIPO = Column(CHAR(14))

    indirizzi = relationship("IndirizzoSpedizione", back_populates="utente")
    carrelli = relationship("Carrello", back_populates="utente")
    feedback_utente = relationship("Feedback", back_populates="utente")
    coupon = relationship("Coupon", back_populates="utente")

class IndirizzoSpedizione(Base):
    __tablename__ = "INDIRIZZO_SPEDIZIONE"

    ID_INDIRIZZO = Column(Integer, primary_key=True, autoincrement=True)
    VIA = Column(String(30), nullable=False)
    CITTA = Column(String(30), nullable=False)
    CAP = Column(Integer, nullable=False)
    STATO = Column(String(30), nullable=False)
    PRESSO = Column(String(30))
    ID_UTENTE = Column(Integer, ForeignKey("UTENTE.ID_UTENTE"))

    utente = relationship("Utente", back_populates="indirizzi")

class Carrello(Base):
    __tablename__ = "CARRELLO"

    ID_CARRELLO = Column(Integer, primary_key=True, autoincrement=True)
    QUANTITA = Column(SmallInteger, nullable=False, default=1)
    SUBCODE = Column(Integer, ForeignKey("DECLINAZIONI.SUBCODE"), primary_key=True)
    ID_UTENTE = Column(Integer, ForeignKey("UTENTE.ID_UTENTE"))

    declinazione = relationship("Declinazioni", back_populates="carrelli")
    utente = relationship("Utente", back_populates="carrelli")
    acquisto = relationship("Acquisto", back_populates="carrello")

class Acquisto(Base):
    __tablename__ = "ACQUISTO"

    ID_ACQUISTO = Column(Integer, primary_key=True, autoincrement=True)
    TIPO_PAGAMENTO = Column(CHAR(20), nullable=False)
    PREZZOFINALE = Column(DECIMAL, nullable=False)
    DATA = Column(Date, nullable=False)
    TRACKING = Column(String(30), nullable=False)
    ID_CARRELLO = Column(Integer, ForeignKey("CARRELLO.ID_CARRELLO"))

    carrello = relationship("Carrello", back_populates="acquisto")

class Feedback(Base):
    __tablename__ = "FEEDBACK"

    ID_FEEDBACK = Column(Integer, primary_key=True, autoincrement=True)
    VOTO = Column(SmallInteger, nullable=False, default=1)
    ID_UTENTE = Column(Integer, ForeignKey("UTENTE.ID_UTENTE"))
    ID_PRODOTTO = Column(CHAR(10), ForeignKey("PRODOTTO.ID_PRODOTTO"))

    utente = relationship("Utente", back_populates="feedback_utente")
    prodotto = relationship("Prodotto", back_populates="feedback")

class Coupon(Base):
    __tablename__ = "COUPON"

    ID_COUPON = Column(Integer, primary_key=True, autoincrement=True)
    PREMIO = Column(DECIMAL(8, 2))
    SCADENZA = Column(Date)
    ID_UTENTE = Column(Integer, ForeignKey("UTENTE.ID_UTENTE"))

    utente = relationship("Utente", back_populates="coupon")

# crea le tabelle
#engine=innodb_engine
Base.metadata.create_all(engine)

# crea una sessione locale
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(sessionmaker(bind=engine))
print(Session())

def insert_data(db: Session): # type: ignore
    
    try:
        """Inserts sample data into the tables."""
        # Create sample Categoria
        categoria1 = Categoria(DENOMINAZIONE="Elettronica")
        categoria2 = Categoria(DENOMINAZIONE="Abbigliamento")
        db.add_all([categoria1, categoria2])
        db.commit()
        db.refresh(categoria1)
        db.refresh(categoria2)
        
        # Create sample Prodotto
        prodotto1 = Prodotto(ID_PRODOTTO="PROD001", NOME="Smartphone X", DESCRIZIONE="Ottimo smartphone", PREZZO=799.99, STAR=4.5, ID_CAT=categoria1.ID_CAT)
        prodotto2 = Prodotto(ID_PRODOTTO="PROD002", NOME="T-Shirt Cotone", DESCRIZIONE="T-shirt in puro cotone", PREZZO=25.50, STAR=4.2, ID_CAT=categoria2.ID_CAT)
        db.add_all([prodotto1, prodotto2])
        db.commit()
        db.refresh(prodotto1)
        db.refresh(prodotto2)

        # Create sample Declinazioni
        declinazione1 = Declinazioni(TAGLIA="M", COLORE="Nero", ID_PRODOTTO=prodotto1.ID_PRODOTTO)
        declinazione2 = Declinazioni(TAGLIA="L", COLORE="Blu", ID_PRODOTTO=prodotto2.ID_PRODOTTO)
        db.add_all([declinazione1, declinazione2])
        db.commit()
        db.refresh(declinazione1)
        db.refresh(declinazione2)

        # Create sample Magazzini
        magazzino1 = Magazzini(CITTA="Roma", TELEFONO=123456789)
        magazzino2 = Magazzini(CITTA="Milano", TELEFONO=987654321)
        db.add_all([magazzino1, magazzino2])
        db.commit()
        db.refresh(magazzino1)
        db.refresh(magazzino2)

        # Create sample ScorteMagazzino
        scorta1 = ScorteMagazzino(ID_MAGAZZINO=magazzino1.ID_MAGAZZINO, SUBCODE=declinazione1.SUBCODE, SCORTE=50)
        scorta2 = ScorteMagazzino(ID_MAGAZZINO=magazzino2.ID_MAGAZZINO, SUBCODE=declinazione2.SUBCODE, SCORTE=100)
        db.add_all([scorta1, scorta2])
        db.commit()

        # Create sample Utente
        utente1 = Utente(NOME="Mario", COGNOME="Rossi", EMAIL="mario.rossi@example.com", PASSWORD="password123", TIPO="cliente")
        utente2 = Utente(NOME="Luigi", COGNOME="Verdi", EMAIL="luigi.verdi@example.com", PASSWORD="securepass", TIPO="admin")
        db.add_all([utente1, utente2])
        db.commit()
        db.refresh(utente1)
        db.refresh(utente2)

        # Create sample IndirizzoSpedizione
        indirizzo1 = IndirizzoSpedizione(VIA="Via Roma 1", CITTA="Roma", CAP=12345, STATO="Italia", ID_UTENTE=utente1.ID_UTENTE)
        db.add(indirizzo1)
        db.commit()
        db.refresh(indirizzo1)

        # Create sample Carrello
        carrello1 = Carrello(QUANTITA=2, SUBCODE=declinazione1.SUBCODE, ID_UTENTE=utente1.ID_UTENTE)
        db.add(carrello1)
        db.commit()
        db.refresh(carrello1)

        # Create sample Acquisto
        acquisto1 = Acquisto(TIPO_PAGAMENTO="Carta di Credito", PREZZOFINALE=1599.98, DATA=date.today(), TRACKING="TRACK123", ID_CARRELLO=carrello1.ID_CARRELLO)
        db.add(acquisto1)
        db.commit()
        db.refresh(acquisto1)

        # Create sample Feedback
        feedback1 = Feedback(VOTO=5, ID_UTENTE=utente1.ID_UTENTE, ID_PRODOTTO=prodotto1.ID_PRODOTTO)
        db.add(feedback1)
        db.commit()
        db.refresh(feedback1)

        # Create sample Coupon
        coupon1 = Coupon(PREMIO=10.00, SCADENZA=date(2025, 5, 31), ID_UTENTE=utente1.ID_UTENTE)
        db.add(coupon1)
        db.commit()
        db.refresh(coupon1)

        print("Sample data inserted successfully.")
    except exc.IntegrityError:
     db.rollback()
    print("data already present")

def read_data(db: Session, table_name: str, item_id: int = None): # type: ignore
    """Reads data from a specified table. If item_id is provided, reads a specific record."""
    print(f"\n--- Reading data from table: {table_name} ---")
    if table_name.upper() == "PRODOTTO":
        if item_id:
            prodotto = db.query(Prodotto).filter(Prodotto.ID_PRODOTTO == item_id).first()
            if prodotto:
                print(f"ID: {prodotto.ID_PRODOTTO}, Nome: {prodotto.NOME}, Prezzo: {prodotto.PREZZO}")
            else:
                print(f"Prodotto with ID {item_id} not found.")
        else:
            prodotti = db.query(Prodotto).all()
            for prodotto in prodotti:
                print(f"ID: {prodotto.ID_PRODOTTO}, Nome: {prodotto.NOME}, Prezzo: {prodotto.PREZZO}")
    elif table_name.upper() == "CATEGORIA":
        if item_id:
            categoria = db.query(Categoria).filter(Categoria.ID_CAT == item_id).first()
            if categoria:
                print(f"ID: {categoria.ID_CAT}, Denominazione: {categoria.DENOMINAZIONE}")
            else:
                print(f"Categoria with ID {item_id} not found.")
        else:
            categorie = db.query(Categoria).all()
            for categoria in categorie:
                print(f"ID: {categoria.ID_CAT}, Denominazione: {categoria.DENOMINAZIONE}")
    elif table_name.upper() == "DECLINAZIONI":
        if item_id:
            declinazione = db.query(Declinazioni).filter(Declinazioni.SUBCODE == item_id).first()
            if declinazione:
                print(f"Subcode: {declinazione.SUBCODE}, Taglia: {declinazione.TAGLIA}, Colore: {declinazione.COLORE}, Prodotto ID: {declinazione.ID_PRODOTTO}")
            else:
                print(f"Declinazione with Subcode {item_id} not found.")
        else:
            declinazioni = db.query(Declinazioni).all()
            for declinazione in declinazioni:
                print(f"Subcode: {declinazione.SUBCODE}, Taglia: {declinazione.TAGLIA}, Colore: {declinazione.COLORE}, Prodotto ID: {declinazione.ID_PRODOTTO}")
    elif table_name.upper() == "MAGAZZINI":
        if item_id:
            magazzino = db.query(Magazzini).filter(Magazzini.ID_MAGAZZINO == item_id).first()
            if magazzino:
                print(f"ID: {magazzino.ID_MAGAZZINO}, Città: {magazzino.CITTA}, Telefono: {magazzino.TELEFONO}")
            else:
                print(f"Magazzino with ID {item_id} not found.")
        else:
            magazzini = db.query(Magazzini).all()
            for magazzino in magazzini:
                print(f"ID: {magazzino.ID_MAGAZZINO}, Città: {magazzino.CITTA}, Telefono: {magazzino.TELEFONO}")
    elif table_name.upper() == "SCORTE_MAGAZZINO":
        # Reading specific record requires both primary keys
        print("Reading a specific record in SCORTE_MAGAZZINO requires both ID_MAGAZZINO and SUBCODE.")
        scorte = db.query(ScorteMagazzino).all()
        for scorta in scorte:
            #print(f"Magazzino ID: {scorta.ID_MAGAZZINO}, Subcode: {scorta.SUBCODE}, Scorte: {scorta})
            print(f"Magazzino ID: {scorta.ID_MAGAZZINO}, Subcode: {scorta.SUBCODE}, Scorte: {scorta.SCORTE}")

insert_data(db=Session)

read_data(db=Session,table_name='PRODOTTO')
read_data(db=Session,table_name='SCORTE_MAGAZZINO')