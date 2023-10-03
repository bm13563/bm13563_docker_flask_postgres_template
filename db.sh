#!/bin/bash

case $1 in
    create-migration)
        export DB_HOST=localhost
        python -c"from schema.db_tools import create_migration; create_migration('$2')"
    ;;
    migrate)
        export DB_HOST=localhost
        python -c"from schema.db_tools import migrate; migrate()"
    ;;
    create-db)
        export DB_HOST=localhost
        python -c"from schema.db_tools import create_db; create_db()"
    ;;
    destroy-db)
        export DB_HOST=localhost
        python -c"from schema.db_tools import destroy_db; destroy_db()"
    ;;
    reset-db)
        export DB_HOST=localhost
        python -c"from schema.db_tools import destroy_db; destroy_db()"
        python -c"from schema.db_tools import create_db; create_db()"
    ;;
    dump)
        export DB_HOST=localhost
        python -c"from schema.db_tools import dump_db; dump_db()"
    ;;
    restore)
        export DB_HOST=localhost
        python -c"from schema.db_tools import restore_db; restore_db()"
    ;;
esac