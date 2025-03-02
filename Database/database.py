import os
import uuid
from sqlalchemy import ARRAY, UUID, DateTime, Integer, Column, String,Double, create_engine, ForeignKey, func
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from sqlalchemy.dialects import postgresql

Base = declarative_base()

class Lottery(Base):
    __tablename__ = "Lotteries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    startDate = Column(DateTime(timezone=False))
    poolSize = Column(Double)
    userCount = Column(Integer)

    users = relationship("LotteryUser", back_populates="lottery")
    
class LotteryUser(Base):
    __tablename__ = "LotteryUsers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    lotteryId = Column(UUID(as_uuid=True), ForeignKey('Lotteries.id'), nullable=False)
    ticketAmount = Column(Double)
    
    lottery = relationship("Lottery", back_populates="users")
    user = relationship("User", back_populates="lotteries")

class Settings(Base):
    __tablename__ = "Settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    walletAddress = Column(String)
    lastTimeStampPull = Column(Double)
    lastBlockId = Column(Integer)
    adminIds = Column(postgresql.ARRAY(Integer))

class Transaction(Base):
    __tablename__ = "Transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    walletId = Column(UUID(as_uuid=True), ForeignKey('Wallets.id'), nullable=True)
    txn_id = Column(String)
    from_wallet = Column(String)
    to_wallet = Column(String)
    amount = Column(Double)
    transactionDate = Column(DateTime(timezone=False), server_default=func.now())
    
    wallet = relationship("Wallet", back_populates="transactions")

class Wallet(Base):
    __tablename__ = "Wallets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    balance = Column(Double)
    current_walletaddress = Column(String)
    
    transactions = relationship("Transaction", back_populates="wallet")
    user = relationship("User", back_populates="wallet")
    
class User(Base):
    __tablename__ = "Users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegramId = Column(String)
    inviteby_telegramId = Column(String)
    joinDate = Column(DateTime(timezone=False), server_default=func.now())
    
    wallet = relationship("Wallet", back_populates="user")
    lotteries = relationship("LotteryUser", back_populates="user")

    

class Database:
    _instance = None
    _initialized = False
    
    def __init__(self, username, password, host, port, database):
        if not self._initialized:
            self._initialized = True
            
            DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

            print(f"Connecting to : {DATABASE_URL}")
            # Create an engine to connect to the PostgreSQL database
            engine = create_engine(DATABASE_URL, echo=True)  # echo=True will log SQL

            # Create all tables in the database
            Base.metadata.create_all(bind=engine)
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            )
            

            session = self.SessionLocal()
            exist_setting = session.query(Settings).one_or_none()
            if exist_setting == None:
                settings = Settings()
                settings.walletAddress = ""
                settings.lastTimeStampPull = 0
                settings.adminIds = []
                
                session.add(settings)
                session.commit()
                session.close()
            
            print(f"Database {database} initialized !")
    
    def __new__(cls, username, password, host, port, database):
        """
        Control the creation of the single Database instance.
        If _instance is None, create a new one; otherwise, return the existing one.
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    @contextmanager
    def session_scope(self, close = True):
        """Provide a transactional scope around a series of operations."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            if close:
                session.close()
            

db_host = os.getenv('DB_HOST', "localhost")
db_port = os.getenv('DB_PORT', 5432)
db_user = os.getenv('DB_USER', "postgres")
db_password = os.getenv('DB_PASSWORD', "Saleh-1379")
db_name = os.getenv('DB_NAME', "LotteryBotDB")

db = Database(db_user, db_password, db_host, db_port, db_name)