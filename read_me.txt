資料夾作用
    1.api:api設定層邏輯
    2.base:原初被繼承物件集合
    3.core: Settings 與 logger 原始設定（環境參數在這邊讀取）
    4.cornjon_api: cornjon用api設定層邏輯
    5.from_set: 框架內部物件轉換用設定
    6.lib: 自行開發工具集合
    7.models: 資料表設定集合
    7.schemas: 輸入及輸出值，檢查與定義集合
    8.services: 底層基礎邏輯層
    9.views: 主要商業邏輯層

檔案作用
    1.env: 環境參數設定點
    2.datebase.py：設定資料庫連接點
    3.main.py: 程式主要發動點
    4:requirements.txt：外掛安裝集合
    5.initializedb.py 建立DB

建立ＤＢ
    1. 變更model
    2. python 執行 initializedb.py

資料庫進版工具：alembic的使用方式
    python 資料庫遷移工具 alembic

    安裝：
    pip install alembic
    alembic init alembic

    生成遷移腳本
    alembic revision --autogenerate -m "e"

    遷移資料庫指令
    alembic upgrade head：将数据库升级到最新版本。
    alembic downgrade base：将数据库降级到最初版本。
    alembic upgrade <version>：将数据库升级到指定版本。
    alembic downgrade <version>：将数据库降级到指定版本。
    alembic upgrade +2：相对升级，将数据库升级到当前版本后的两个版本。
    alembic downgrade +2：相对降级，将数据库降级到当前版本前的两个版本。


    常見錯誤
    1.
        (.venv) ➜  server alembic revision --autogenerate
    INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    ERROR [alembic.util.messaging] Target database is not up to date.
      FAILED: Target database is not up to date.

    出现该错误的原因是没有使用 Alembic 更新数据库，如果你没有手动创建数据表可以使用 alembic upgrade head 命令消除该错误，如果你已经通过命令行或其他方式创建了数据表，可以使用 alembic stamp head 命令来设置 Alembic 的状态。

    如果需要遇到 Alembic 無法正常作用
    只需刪除 Alembic_tables 重新建立版本即可，不需要刪除整個資料庫