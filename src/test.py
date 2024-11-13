from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

#연결설정
db_url = "mysql+mysqldb://test_user:1234@127.0.0.1:3306/test_db"
engine = create_engine(db_url, echo=True)

# 데이터베이스 객체 준비
class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "Customer"

    name : Mapped[str] = mapped_column(primary_key=True)
    call_num : Mapped[str] = mapped_column(String(40))
    home : Mapped[str] = mapped_column(String(40))
    email : Mapped[str] = mapped_column(String(40))

#세션에 데이터를 올리고 전송
with Session(engine) as session:
    spongebob = Customer(
        name = "spongebob",
        call_num = "010-1111-1111",
        home = "under water",
        email = "spnge@gmail.com"
    )

    session.add_all([spongebob])
    session.commit()

#데이터를 가져오기
from sqlalchemy import select

with Session(engine) as session:
    stmt = select(Customer).where(Customer.name.in_(["spongebob", "jane"]))
    print(stmt)
    for customer in session.scalars(stmt):
        print(customer)

#데이터를 수정하기

with Session(engine) as session:
    stmt = select(Customer).where(Customer.name == "spongebob")
    spongebob = session.scalars(stmt).one()
    spongebob.email = "sponge@naver.com"
    session.commit()

# 데이터 삭제하기

with Session(engine) as session:
    stmt = select(Customer).where(Customer.name == "spongebob")
    spongebob = session.scalars(stmt).one()
    session.delete(spongebob)
    session.commit()