from typing import Dict, List, Union

from app.database import get_dev_db, get_mvc_db
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from . import crud
from .schemas import *

router = APIRouter(prefix="/overview")


@router.get(
    "",
    response_model=OverviewList,
    response_model_by_alias=False,
)
async def read_overview_list(
    category: str
    | None = Query(None, description="firmName, bizrNo, jurirNo, stockCode"),
    keyword: str | None = None,
    limit: int = 50,
    page: int = 1,
    db: Session = Depends(get_dev_db),
):
    try:
        search_category = ""
        if category == "firmName":
            search_category = "firm"
        elif category == "bizrNo":
            search_category = "bizr_no"
        elif category == "jurirNo":
            search_category = "corp_cls"
        elif category == "stockCode":
            search_category = "stock_code"

        result, total_count = crud.get_overview_list(
            category=search_category, keyword=keyword, limit=limit, page=page, db=db
        )
        response = {"length": total_count, "data": result}
        return response
    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=List[Dict[str, Union[int, str]]])
async def read_company_items_by_category(
    term: str = Query(..., description="Search term"),
    category: str = Query(
        ..., description="Search category: 'firm' or 'bizr_no' or 'jurir_no"
    ),
    db: Session = Depends(get_dev_db),
):
    items = crud.get_company_items_by_category(term=term, category=category, db=db)
    return items


# @router.get("/index", response_model=DepsList, response_model_by_alias=False)
# def read_deps(db: Session = Depends(get_db)):
#     result = crud.get_deps(db=db)
#     return {"length": len(result), "data": result}


@router.get(
    "/{corp_code}/description",
    response_model=OverviewDetail,
    response_model_by_alias=False,
)
async def read_overview_detail(corp_code: str, db: Session = Depends(get_mvc_db)):
    try:
        dart_corp_info = crud.get_dart_corp_info(corp_code=corp_code, db=db)
        if dart_corp_info == None:
            return HTTPException(status_code=404, detail="dart data not found")

        corp_class = None
        if dart_corp_info.corp_cls:
            if dart_corp_info.corp_cls.lower() == "y":
                corp_class = "유가"
            elif dart_corp_info.corp_cls.lower() == "k":
                corp_class = "KODAQ"
            elif dart_corp_info.corp_cls.lower() == "n":
                corp_class = "KONEX"
            elif dart_corp_info.corp_cls.lower() == "e":
                corp_class = "etc"

        crno = dart_corp_info.jurir_no  # 법인등록번호
        openapi_outline = crud.get_openapi_outline(crno=crno, db=db)
        if openapi_outline == None:
            return HTTPException(
                status_code=404, detail="openapi outline data not found"
            )

        is_sm_corp = None
        if openapi_outline.smenpyn:
            if openapi_outline.smenpyn.lower() == "y":
                is_sm_corp = True
            elif openapi_outline.smenpyn.lower() == "n":
                is_sm_corp = False

        affiliate_result = crud.get_openapi_affiliate_list(crno=crno, db=db)
        affiliate_list = [
            Affiliate(corpName=affiliate[1]) for affiliate in affiliate_result
        ]

        sub_corp_result = crud.get_openapi_sub_company_list(crno=crno, db=db)
        sub_corp_list = [SubCorp(corpName=sub_corp[0]) for sub_corp in sub_corp_result]

        response = OverviewDetail(
            stock_name=dart_corp_info.stock_name,
            stock_code=dart_corp_info.stock_code,
            bizr_no=dart_corp_info.bizr_no,
            jurir_no=dart_corp_info.jurir_no,
            corp_name=dart_corp_info.corp_name,
            corp_name_eng=dart_corp_info.corp_name_eng,
            corp_name_history=None,
            corp_cls=corp_class,
            est_dt=dart_corp_info.est_dt,
            kospi={
                "listDate": openapi_outline.enpxchglstgdt,
                "delistDate": openapi_outline.enpxchglstgaboldt,
            },
            kosdaq={
                "listDate": openapi_outline.enpkosdaqlstgdt,
                "delistDate": openapi_outline.enpkosdaqlstgaboldt,
            },
            konex={
                "listDate": openapi_outline.enpkrxlstgdt,
                "delistDate": openapi_outline.enpkrxlstgaboldt,
            },
            hm_url=dart_corp_info.hm_url,
            phn_no=dart_corp_info.phn_no,
            adres=dart_corp_info.adres,
            ceo_nm=dart_corp_info.ceo_nm,
            affiliate_list=affiliate_list,
            smenpyn=is_sm_corp,
            isVenture=None,
            sub_corp_list=sub_corp_list,
            shareholder_num=None,
            enpempecnt=openapi_outline.enpempecnt,
            enppn1avgslryamt=openapi_outline.enppn1avgslryamt,
            audtrptopnnctt=openapi_outline.audtrptopnnctt,
            acc_mt=dart_corp_info.acc_mt,
            issuerRate=None,
            enpmainbiznm=openapi_outline.enpmainbiznm,
            classList=[],
        )
        return response

    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code=500, detail=str(e))