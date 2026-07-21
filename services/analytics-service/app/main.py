from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .clickhouse import get_clickhouse_client
from .schemas import AnalyticsEvent, AnalyticsResponse


app = FastAPI(
    title="Analytics Service",
    description="Stores frontend analytics in ClickHouse",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes are mounted under /api/analytics to match the ALB ingress path
# rule. The ALB ingress controller does not rewrite/strip the matched
# prefix, so the service must expose routes at the same path the ingress
# forwards.
router = APIRouter(prefix="/api/analytics")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Analytics Service is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    try:
        client = get_clickhouse_client()
        result = client.query("SELECT 1")

        if result.result_rows[0][0] != 1:
            raise RuntimeError("Unexpected ClickHouse response")

        return {
            "status": "healthy",
            "clickhouse": "connected",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="ClickHouse connection failed",
        ) from exc


@router.post(
    "/track",
    response_model=AnalyticsResponse,
    status_code=201,
)
def track_event(event: AnalyticsEvent) -> AnalyticsResponse:
    try:
        client = get_clickhouse_client()

        client.insert(
            "web_analytics",
            [[
                event.session_id,
                event.event_type,
                event.page,
                event.element,
                event.user_agent,
            ]],
            column_names=[
                "session_id",
                "event_type",
                "page",
                "element",
                "user_agent",
            ],
        )

        return AnalyticsResponse(
            message="Analytics event recorded"
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to store analytics event",
        ) from exc

app.include_router(router)
