from sqlalchemy import Column, Integer, String, Date, Double
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Projects(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_code = Column(Integer, nullable=False)
    segment = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    loanched_at = Column(Date, nullable=False)
    partner = Column(String, nullable=False)
    status = Column(String, nullable=False)
    quotation_issued_at = Column(Date, nullable=True)
    quotation_no = Column(String, nullable=True)
    contracted_at = Column(Date, nullable=True)
    contracted_no = Column(String, nullable=True)
    completed_at = Column(Date, nullable=True)
    canceled_at = Column(Date, nullable=True)
    invoice_no = Column(String, nullable=True)
    remark = Column(String, nullable=True)
    contract_type = Column(String, nullable=True)
    quotation_amount = Column(Integer, nullable=True)
    quotation_cost = Column(Integer, nullable=True)
    quotation_profit = Column(Integer, nullable=True)
    contract_amount = Column(String, nullable=True)
    contract_cost = Column(Integer, nullable=True)
    contract_profit = Column(Integer, nullable=True)
    tax_rate = Column(Double, nullable=True)
    tax = Column(Integer, nullable=True)
    completion_conditions = Column(String, nullable=True)
    reason_for_cancellation = Column(String, nullable=True)
    number_of_payments = Column(Integer, nullable=True)
    number_of_deposits = Column(Integer, nullable=True)
    ammount_of_payments = Column(Integer, nullable=True)
    amount_of_deposits = Column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"Project(project_code={self.project_code!r})"
