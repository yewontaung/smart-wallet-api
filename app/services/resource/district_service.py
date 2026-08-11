from sqlmodel import Session, select, func

from app.data.meta_models import District, Township
from app.dtos.base import ModificationResult
from app.dtos.manager.inputs import DistrictForm
from app.dtos.shared.outputs import DistrictInfo
from app.dtos.shared.searches import LocationSearch


def search(search: LocationSearch, session: Session) -> list[DistrictInfo]:
    statement = (
        select(
            District,
            func.count(Township.township_id).label("townships")
        )
        .outerjoin(Township, Township.district_id == District.district_id)
        .group_by(District.district_id)
    )

    if search.q:
        statement = statement.where(
            District.district_name.ilike(f"%{search.q}%")
        )

    results = session.exec(statement).all()

    return [
        DistrictInfo(
            district_id=district.district_id,
            district_name=district.district_name,
            townships=township_count,
            created_at=district.created_at,
            updated_at=district.updated_at,
        )
        for district, township_count in results
    ]


def save_district(
    form: DistrictForm,
    user_id: int,
    session: Session
) -> ModificationResult:
    return