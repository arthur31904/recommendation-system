import requests
from core.logger import Logger, LogLevel
import traceback
from schemas.exception import BizException


def get_rule_type(rule_set):

    if rule_set.biz_brand_point_settings != "" and rule_set.biz_point_keywords != "" and rule_set.biz_point_seller_taxid != "":
        rule_type = 1
    elif rule_set.biz_brand_point_settings != "" and rule_set.biz_point_keywords != "":
        rule_type = 2
    elif rule_set.biz_point_seller_taxid != "" and rule_set.biz_point_keywords != "":
        rule_type = 3
    elif rule_set.biz_point_seller_taxid != "" and rule_set.biz_brand_point_settings != "":
        rule_type = 4
    elif rule_set.biz_point_seller_taxid != "":
        rule_type = 5
    elif rule_set.biz_brand_point_settings != "":
        rule_type = 6
    elif rule_set.biz_point_keywords != "":
        rule_type = 7

    Logger.log(LogLevel.INFO, "get_rule_type", rule_set, None, "success")

    return rule_type


def set_payload(rule_type, ES_obj, brand_obj, obj):

    if rule_type==1:
        kws = obj.biz_point_keywords.split(',')
        kws_2 = obj.biz_brand_point_settings.split(',')
        payload = {
                "search": {
                    "id": ES_obj.get('_id'),
                    "brand_id": brand_obj.id,
                    "rule_type": "open",
                    "query": {
                        "bool": {
                            "filter": [
                                {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "biz_brand_point_settings": {
                                                        "query": kw2
                                                    }
                                                }
                                            } for kw2 in kws_2
                                        ],
                                        "minimum_should_match": 1
                                    }
                                },
                                {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "biz_point_keywords": {
                                                        "query": kw
                                                    }
                                                }
                                            } for kw in kws
                                        ],
                                        "minimum_should_match": 1
                                    }
                                }
                            ],
                            "must": [
                                {
                                    "match_phrase": {
                                        "biz_point_seller_taxid": {
                                            "query": obj.biz_point_seller_taxid
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
    elif rule_type==2:
        kws = obj.biz_point_keywords.split(',')
        kws_2 = obj.biz_brand_point_settings.split(',')
        payload = {
                "search": {
                    "id": ES_obj.get('_id'),
                    "brand_id": brand_obj.id,
                    "rule_type": "open",
                    "query": {
                        "bool": {
                            "filter": [
                                {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "biz_brand_point_settings": {
                                                        "query": kw2
                                                    }
                                                }
                                            } for kw2 in kws_2
                                        ],
                                        "minimum_should_match": 1
                                    }
                                },
                                {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "biz_point_keywords": {
                                                        "query": kw
                                                    }
                                                }
                                            } for kw in kws
                                        ],
                                        "minimum_should_match": 1
                                    }
                                }
                            ]
                        }
                    }
                }
            }
    elif rule_type==3:
        kws = obj.biz_point_keywords.split(',')
        payload = {
                "search": {
                    "id": ES_obj.get('_id'),
                    "brand_id": brand_obj.id,
                    "rule_type": "open",
                    "biz_point_seller_taxid": obj.biz_point_seller_taxid,
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "biz_point_keywords": {
                                            "query": kw
                                        }
                                    }
                                } for kw in kws
                            ],
                            "minimum_should_match":1
                        }
                    }
                }
            }
    elif rule_type==4:
        kws = obj.biz_brand_point_settings.split(',')
        payload = {
                "search": {
                    "id": ES_obj.get('_id'),
                    "brand_id": brand_obj.id,
                    "rule_type": "open",
                    "biz_point_seller_taxid": obj.biz_point_seller_taxid,
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "biz_brand_point_settings": {
                                            "query": kw
                                        }
                                    }
                                } for kw in kws
                            ],
                            "minimum_should_match":1
                        }
                    }
                }
            }
    elif rule_type==5:
        payload = {
                "search": {
                    "id": ES_obj.get('_id'),
                    "brand_id": brand_obj.id,
                    "rule_type": "open",
                    "biz_point_seller_taxid": obj.biz_point_seller_taxid,

                }
            }
    elif rule_type==6:
        kws = obj.biz_brand_point_settings.split(',')
        payload = {
                "search": {
                    "id": ES_obj.get('_id'),
                    "brand_id": brand_obj.id,
                    "rule_type": "open",
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "biz_brand_point_settings": {
                                            "query": kw
                                        }
                                    }
                                } for kw in kws
                            ],
                            "minimum_should_match":1
                        }
                    }
                }
            }
    elif rule_type==7:
        kws = obj.biz_point_keywords.split(',')
        payload = {
                "search": {
                    "id": ES_obj.get('_id'),
                    "brand_id": brand_obj.id,
                    "rule_type": "open",
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "biz_point_keywords": {
                                            "query": kw
                                        }
                                    }
                                } for kw in kws
                            ],
                            "minimum_should_match":1
                        }
                    }
                }
            }

    Logger.log(LogLevel.INFO, "set_payload", ES_obj, None, "success")

    return payload


