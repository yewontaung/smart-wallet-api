from sqlmodel import Session, select, func

from app.data.meta_models import District, Township
from app.data.models import Address
from app.dtos.base import ModificationResult
from app.dtos.manager.inputs import DistrictForm
from app.dtos.shared.outputs import DistrictInfo
from app.dtos.shared.searches import LocationSearch


def search(
    search: LocationSearch,
    session: Session
) -> list[DistrictInfo]:

    # =========================================================
    # Base query
    # =========================================================

    statement = (
        select(
            District,
            func.count(Address.address_id).label("township_users")
        )
        .outerjoin(
            Township,
            Township.district_id == District.district_id
        )
        .outerjoin(
            Address,
            Address.township_id == Township.township_id
        )
        .group_by(District.district_id)
    )

    # =========================================================
    # q - District name starts with q
    # =========================================================

    if search.q:
        statement = statement.where(
            District.district_name.ilike(f"{search.q}%")
        )

    # =========================================================
    # Date filters
    # =========================================================

    if search.date_from:
        statement = statement.where(
            District.created_at >= search.date_from
        )

    if search.date_to:
        statement = statement.where(
            District.created_at <= search.date_to
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
    # Execute
    # =========================================================

    results = session.exec(statement).all()

    return [
        DistrictInfo(
            district_id=district.district_id,
            district_name=district.district_name,
            townships=len(
                session.exec(
                    select(Township).where(
                        Township.district_id == district.district_id
                    )
                ).all()
            ),
            created_at=district.created_at,
            updated_at=district.updated_at,
        )
        for district, township_users in results
    ]


def save_district(
    form: DistrictForm,
    user_id: int,
    session: Session
) -> ModificationResult:
    return