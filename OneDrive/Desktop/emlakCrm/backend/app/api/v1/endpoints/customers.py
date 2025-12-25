from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate, LeadCreate
from app.services.customer import CustomerService

router = APIRouter()


@router.get("/", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Müşteri listesi"""
    service = CustomerService(db)
    customers = service.get_customers(skip=skip, limit=limit)
    return customers


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """Müşteri detayları"""
    service = CustomerService(db)
    customer = service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    return customer


@router.post("/", response_model=CustomerResponse, status_code=201)
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    """Yeni müşteri oluştur"""
    service = CustomerService(db)
    customer = service.create_customer(customer_data)
    return customer


@router.post("/leads", status_code=201)
async def create_lead(
    lead_data: LeadCreate,
    db: Session = Depends(get_db)
):
    """Yeni lead kaydı oluştur (müşteri aktivitesi)"""
    service = CustomerService(db)
    lead = service.create_lead(lead_data)
    return lead


@router.put("/{customer_id}/score", response_model=CustomerResponse)
async def update_customer_score(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """Müşteri lead skorunu güncelle"""
    service = CustomerService(db)
    customer = service.update_lead_score(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    return customer

