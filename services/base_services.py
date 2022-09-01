from sqlalchemy.orm import Session
from models.brands import brands
from models.brands import brands_test
from models.brands import brands_test_v2
from schemas.brands import brands as BrandsSchema, brands_test_to_db, brands_to_db, brand_edit, BrandsGetOne
from schemas.brands import brands_test as BrandsTestSchema
from schemas.brands import brands_test_edit as BrandsTestEditSchema
from schemas.brands import brands_test_v2_to_db as BrandsTestV2EditSchema
# from schemas.brands import brands_test as BrandsTestSchema


# 指定查詢符合 User.id 的 user table 資料
def get_base(db: Session, id: int):
    return db.query(brands).filter(brands.id == id).first()

# 查詢所有 user 資料，並限制每次查詢數量
def get_brands(db: Session, skip: int = 0, limit: int = 10):
    return db.query(brands).offset(skip).limit(limit).all()

# 建立 user table 資料
def craete_brand(db: Session, brand_in: BrandsSchema):
    # 轉化 pydantic model to orm model

    to_db_obj = brands_to_db(**brand_in.dict()).dict()

    created_brand = brands(**to_db_obj)
    # add instance object into database session
    # 增加 user orm model 所建立的 instance 到 database session
    db.add(created_brand)
    # 提交 transaction to database (該 instance 會確實保存在 database)
    db.commit()
    # refresh instance (從 database 抽取該 instance 資料)
    db.refresh(created_brand)
    return created_brand

def edit_brand(db: Session, brand_in: brand_edit):
    # 轉化 pydantic model to orm model
    # update_brand = brands(**brand_in.dict())

    # 增加 user orm model 所建立的 instance 到 database session
    old_obj = db.query(brands).filter(brands.id == brand_in.dict().get('id')).first()
    '''
    version = Column(Integer, default=1)
    is_deleted = Column(Boolean, default=False)
    type = Column(Integer)
    name = Column(String)
    alias = Column(String)
    code = Column(String)
    is_online = Column(Boolean, default=False)
    order_weighting = Column(Integer, default=1)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    eshop_name = Column(String)
    eshop_url = Column(String)
    foodpanda_url = Column(String)
    facebook_fanpage_url = Column(String)
    line_official_account = Column(String)

    intro = Column(String)
    about = Column(String)
    small_logo = Column(String)
    large_logo = Column(String)
    subbrands_img = Column(String)
    subbrands_info = Column(String)
    '''
    old_obj.version = brand_in.dict().get('version')
    old_obj.is_deleted = brand_in.dict().get('is_deleted')

    old_obj.type = brand_in.dict().get('type')
    old_obj.name = brand_in.dict().get('name')

    old_obj.alias = brand_in.dict().get('alias')
    old_obj.code = brand_in.dict().get('code')

    old_obj.is_online = brand_in.dict().get('is_online')
    old_obj.order_weighting = brand_in.dict().get('order_weighting')

    old_obj.start_date = brand_in.dict().get('start_date')
    old_obj.end_date = brand_in.dict().get('end_date')

    old_obj.eshop_name = brand_in.dict().get('eshop_name')
    old_obj.eshop_url = brand_in.dict().get('eshop_url')

    old_obj.foodpanda_url = brand_in.dict().get('foodpanda_url')
    old_obj.facebook_fanpage_url = brand_in.dict().get('facebook_fanpage_url')

    old_obj.line_official_account = brand_in.dict().get('line_official_account')

    old_obj.intro = brand_in.dict().get('intro')
    old_obj.about = brand_in.dict().get('about')

    old_obj.small_logo = brand_in.dict().get('small_logo')
    old_obj.large_logo = brand_in.dict().get('large_logo')

    old_obj.subbrands_img = brand_in.dict().get('subbrands_img')
    old_obj.subbrands_info = brand_in.dict().get('subbrands_info')

    db.add(old_obj)
    # 提交 transaction to database (該 instance 會確實保存在 database)
    db.commit()
    # refresh instance (從 database 抽取該 instance 資料)
    db.refresh(old_obj)
    return old_obj

def delete_brand(db: Session, brand_in: BrandsGetOne):
    # 轉化 pydantic model to orm model

    old_obj = db.query(brands).filter(brands.id == brand_in.dict().get('id')).first()

    # update_brand = brands(**brand_in.dict())

    # 增加 user orm model 所建立的 instance 到 database session
    db.delete(old_obj)
    # 提交 transaction to database (該 instance 會確實保存在 database)
    db.commit()
    # refresh instance (從 database 抽取該 instance 資料)
    # db.refresh(update_brand)
    return old_obj

def craete_brand_test(db: Session, brand_in: BrandsTestSchema):
    # 轉化 pydantic model to orm model

    # print(created_brand.d)

    created_brand = brands_test(**brands_test_to_db(**brand_in.dict()).dict())

    # add instance object into database session
    # 增加 user orm model 所建立的 instance 到 database session
    db.add(created_brand)
    # 提交 transaction to database (該 instance 會確實保存在 database)
    db.commit()
    # refresh instance (從 database 抽取該 instance 資料)
    db.refresh(created_brand)
    return created_brand

def edit_brand_test(db: Session, brand_in: BrandsTestEditSchema, old_obj: object):
    # 轉化 pydantic model to orm model
    created_brand = brands_test(**brand_in.dict())

    old_obj = db.query(brands_test).filter(brands_test.id == brand_in.dict().get('id')).first()
    # add instance object into database session
    # 增加 user orm model 所建立的 instance 到 database session
    old_obj.version = 10

    db.add(old_obj)
    # 提交 transaction to database (該 instance 會確實保存在 database)
    db.commit()
    # refresh instance (從 database 抽取該 instance 資料)
    db.refresh(old_obj)
    return created_brand

def craete_brand_v2_test(db: Session, brand_in: BrandsTestV2EditSchema):
    # 轉化 pydantic model to orm model

    # print(created_brand.d)

    created_brand = brands_test_v2(**BrandsTestV2EditSchema(**brand_in.dict()).dict())

    # add instance object into database session
    # 增加 user orm model 所建立的 instance 到 database session
    db.add(created_brand)
    # 提交 transaction to database (該 instance 會確實保存在 database)
    db.commit()
    # refresh instance (從 database 抽取該 instance 資料)
    db.refresh(created_brand)
    return created_brand
