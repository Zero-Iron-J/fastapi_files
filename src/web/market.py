from fastapi import APIRouter
from model.market import Market
import service.market as market

router = APIRouter(prefix = "/market")


@router.get("/")
def get_all() -> list[Market]:
    return market.get_all()

@router.get("/{market_name}")
def get_market(market_name) -> Market | None:
    return market.get_market(market_name)