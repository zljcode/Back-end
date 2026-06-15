from fastapi import APIRouter,Request


from app.schemas.visitor import ScenarioType, VisitorRequest, VisitorResponse
from app.service.visitor_service import get_visitor_profile,create_visitor_profile

router = APIRouter()


@router.get("/visitor", response_model=VisitorResponse)
async def get_visitor(scenario: ScenarioType = "pass") -> VisitorResponse:
    return get_visitor_profile(scenario)


@router.post("/visitor", response_model=VisitorResponse)
async def create_visitor_profile_route(
    request:Request,
    payload: VisitorRequest,
    scenario: ScenarioType = "pass",
) -> VisitorResponse:
    client_ip = _extract_client_ip(request)
    
    return create_visitor_profile(payload,scenario,client_ip)

def _extract_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()

    if request.client:
        return request.client.host

    return "unknown"
