from sqlmodel import Session, select, func

from app.data.meta_models import Township, District
from app.data.models import Address
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

    # =========================================================
    # Base query
    # =========================================================

    statement = (
        select(
            Township,
            District.district_name,
            func.count(Address.address_id).label("users")
        )
        .join(
            District,
            Township.district_id == District.district_id
        )
        .outerjoin(
            Address,
            Address.township_id == Township.township_id
        )
        .group_by(
            Township.township_id,
            District.district_name
        )
    )

    # =========================================================
    # q - Township name starts with q
    # =========================================================

    if search.q:
        statement = statement.where(
            Township.township_name.ilike(f"{search.q}%")
        )

    # =========================================================
    # Date filters
    # =========================================================

    if search.date_from:
        statement = statement.where(
            Township.created_at >= search.date_from
        )

    if search.date_to:
        statement = statement.where(
            Township.created_at <= search.date_to
        )

    # =========================================================
    # User count filters
    # =========================================================

    if search.users_from is not None:
        statement = statement.having(
            func.count(Address.address_id) >= search.users_from
        )

    if search.users_to is not None:
        statement = statement.having(
            func.count(Address.address_id) <= search.users_to
        )

    # =========================================================
    # Count total
    # =========================================================

    results = session.exec(statement).all()

    total = len(results)

    # =========================================================
    # Pagination
    # =========================================================

    offset = (page - 1) * size

    paginated_results = results[offset:offset + size]

    pages = (total + size - 1) // size if total > 0 else 0

    # =========================================================
    # Response
    # =========================================================

    items = [
        TownshipInfo(
            township_id=township.township_id,
            township_name=township.township_name,
            district_id=township.district_id,
            district_name=district_name,
            created_at=township.created_at,
            updated_at=township.updated_at,
        )
        for township, district_name, users in paginated_results
    ]

    return PageResult[TownshipInfo](
        items=items,
        page=page,
        size=size,
        total=total,
        pages=pages
    )


def save_district(
    form: TownshipForm,
    user_id: int,
    session: Session
) -> ModificationResult:
    return