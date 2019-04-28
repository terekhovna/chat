#! /usr/bin/python3
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=50000, type=int)
    parser.add_argument('--data-json', dest="data", type=argparse.FileType('r', encoding="utf-8"),
                        default="./data/users.json")
    parser.add_argument('--dump-json', dest="data_out", type=argparse.FileType('w', encoding="utf-8"),
                        default="./data/users2.json")
    parser.add_argument('--dblogin', default='postgres')
    parser.add_argument('--dbpassword', default='asdf')
    parser.add_argument('--dbhost', default='127.0.0.1')
    parser.add_argument('--dbport', default='5432')
    parser.add_argument('--dbname', default='chatdb1')
    args = parser.parse_args()

    import settings
    settings.DB_URL = \
        f'postgresql+psycopg2://{args.dblogin}:{args.dbpassword}@{args.dbhost}:{args.dbport}/{args.dbname}'

    from app.database import init_db, dump_db
    import json
    import app.routes_api

    init_db(json.loads(args.data.read()))
    app.app.run('::', args.port, debug=True, threaded=True)
    dump_db(args.data_out)


if __name__ == '__main__':
    main()
