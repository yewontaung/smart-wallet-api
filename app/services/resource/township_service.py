from sqlmodel import Session, select

from app.data.meta_models import District, Township
from app.dtos.base import ModificationResult, PageResult
from app.dtos.manager.inputs import TownshipForm
from app.dtos.shared.outputs import TownshipInfo
from app.dtos.shared.searches import LocationSearch


def search(
    search: LocationSearch,
    page: int,
    size: int,
    session: Session
) -> PageResult[TownshipInfo]:

    statement = (
        select(Township, District)
        .join(District, Township.district_id == District.district_id)
    )

    # Search township name or district name
    if search.q:
        keyword = f"%{search.q}%"

        statement = statement.where(
            (Township.township_name.ilike(keyword))
            | (District.district_name.ilike(keyword))
        )

    # Get total count before pagination
    results = session.exec(statement).all()
    total = len(results)

    # Pagination
    offset = (page - 1) * size

    paginated_results = results[offset:offset + size]

    items = [
        TownshipInfo(
            township_id=township.township_id,
            township_name=township.township_name,
            district_id=district.district_id,
            district_name=district.district_name,
            created_at=township.created_at,
            updated_at=township.updated_at,
        )
        for township, district in paginated_results
    ]

    return PageResult[TownshipInfo](
        items=items,
        page=page,
        size=size,
        total=total,
    )


def save_district(
    form: TownshipForm,
    user_id: int,
    session: Session
) -> ModificationResult:
    return