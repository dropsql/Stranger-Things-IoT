from lib.logging import Logging
from lib.hashing import Hashing

from core.database import Database

console = Logging.console
database = Database()


while 1:

    try:
        console.clear()
        Logging.print_banner()

        Logging.print_info('enter a query to search into Stranger Things IoT')
        query = console.input(' [white]%[/white][cyan] ')

        results = database.search_query(query)

        if not len(results):
            Logging.print_failed(f'no results found for query: "{query}", press "enter" to continue...[black]')
            console.input()
            continue

        Logging.print_success(f'{len(results)} results found for query "{query}" !')

        hosts = {
            Hashing.make_headers_hash(port, headers): []
            for _, port, headers in results
        }

        for ip, port, headers in results:
            hosts[Hashing.make_headers_hash(port, headers)].append((ip, port, headers))

        for _hash, reports in hosts.items():
            _hosts = [ip for ip, port, headers in reports]
            table = Logging.render_host_table(
                '\n'.join(_hosts),
                str(port),
                headers
            )
            console.print(table)
            
        Logging.print_info('done, press "enter" to continue...[black]')
        console.input()
        continue    

    except KeyboardInterrupt:
        break
    except Exception as e:
        Logging.console.print_exception()
        Logging.print_info('done, press "enter" to continue...[black]')
        console.input()  
