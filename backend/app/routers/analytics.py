from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.sales import Sales, SaleItem
from app.models.inventory import Inventory
from app.models.emipayment import Emi, EmiPayment, EmiStatus

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard/{business_id}")
def get_dashboard_stats(
    business_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    today = date.today()
    today_str = today.strftime("%d/%m/%Y")
    current_month = today.month
    current_year = today.year

    # ── Gross Sales Today ─────────────────────────────────────────
    today_sales_total = db.query(
        func.coalesce(func.sum(Sales.total_amount), 0.0)
    ).filter(
        Sales.business_id == business_id,
        Sales.transaction_date == today_str
    ).scalar()

    # ── Cash Collected Today (non-EMI sales only) ─────────────────
    cash_today = db.query(
        func.coalesce(func.sum(Sales.total_amount), 0.0)
    ).filter(
        Sales.business_id == business_id,
        Sales.transaction_date == today_str,
        Sales.is_emi == False
    ).scalar()

    # ── Today's Profit ────────────────────────────────────────────
    profit_today = db.query(
        func.coalesce(func.sum(Sales.total_profit), 0.0)
    ).filter(
        Sales.business_id == business_id,
        Sales.transaction_date == today_str
    ).scalar()

    # ── EMI Received Today ────────────────────────────────────────
    emi_received_today = db.query(
        func.coalesce(func.sum(EmiPayment.amount), 0.0)
    ).filter(
        EmiPayment.business_id == business_id,
        EmiPayment.date == today_str
    ).scalar()

    # ── EMI Due Today ─────────────────────────────────────────────
    emi_due_today = db.query(
        func.coalesce(func.sum(Emi.next_billing_amount), 0.0)
    ).filter(
        Emi.business_id == business_id,
        Emi.next_due_date == today_str,
        Emi.status == EmiStatus.ACTIVE
    ).scalar()

    # ── GST Summary (current month) ───────────────────────────────
    all_sales = db.query(Sales).filter(
        Sales.business_id == business_id
    ).all()

    output_gst = 0.0   # GST collected from customers
    input_gst = 0.0    # GST paid on purchases (from inventory)

    for sale in all_sales:
        try:
            sale_date = datetime.strptime(
                sale.transaction_date, "%d/%m/%Y"
            )
            if (sale_date.month == current_month and
                    sale_date.year == current_year):
                for item in (sale.items or []):
                    output_gst += (item.tax_amount or 0.0)
        except Exception:
            pass

    # Input GST from inventory purchases this month
    all_inventory = db.query(Inventory).filter(
        Inventory.business_id == business_id
    ).all()
    for inv in all_inventory:
        try:
            if inv.last_restock_date:
                restock_date = datetime.strptime(
                    inv.last_restock_date, "%d/%m/%Y"
                )
                if (restock_date.month == current_month and
                        restock_date.year == current_year):
                    input_gst += (inv.purchase_tax_amount or 0.0)
        except Exception:
            pass

    net_gst = output_gst - input_gst

    # ── Today's margin % ─────────────────────────────────────────
    margin_pct = 0.0
    if today_sales_total and today_sales_total > 0:
        margin_pct = (profit_today / today_sales_total) * 100

    return {
        "gross_sales_today": float(today_sales_total or 0),
        "cash_collected_today": float(cash_today or 0),
        "profit_today": float(profit_today or 0),
        "margin_pct": round(float(margin_pct or 0), 1),
        "emi_received_today": float(emi_received_today or 0),
        "emi_due_today": float(emi_due_today or 0),
        "output_gst": round(float(output_gst or 0), 2),
        "input_gst": round(float(input_gst or 0), 2),
        "net_gst": round(float(net_gst or 0), 2),
    }