from fastapi import APIRouter

from app.schemas.visitor import ScenarioType, VisitorRequest, VisitorResponse
from app.service.visitor_service import get_visitor_profile,create_visitor_profile

router = APIRouter()


@router.get("/visitor", response_model=VisitorResponse)
async def get_visitor(scenario: ScenarioType = "pass") -> VisitorResponse:
    return get_visitor_profile(scenario)


@router.post("/visitor", response_model=VisitorResponse)
async def create_visitor_profile_route(
    payload: VisitorRequest,
    scenario: ScenarioType = "pass",
) -> VisitorResponse:
    return create_visitor_profile(payload,scenario)
