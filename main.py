from lib.logging import Logging
from lib.hashing import Hashing

from core.database import Database

console = Logging.console
database = Database()

while 1:

    try:
        console.clear()
        Logging.print_banner()
        
        Logging.print_info(f'enter a query to search into Stranger Things IoT\n[green underline]total database rows count:[/green underline] [white]{database.get_rows_count()}[/white]')
        query = console.input(' [red][[white]%[/white]][/red][white] ')

        if len(query) <= 2:
            Logging.print_failed('query must be longer than 2 chars, press "enter" to continue...')
            console.input()
            continue

        results = database.search_query(query) # search the query into the sqlite database

        if not len(results):
            Logging.print_failed(f'no results found for query: "{query}", press "enter" to continue...[black]')
            console.input()
            continue

        Logging.print_success(f'{len(results)} results found for query "{query}" !')

        """ here's a little code to make single boxs with multi ips (only if port & headers are the sames) """
        hosts = {
            Hashing.make_headers_hash(port, headers): []
            for _, port, headers in results
        }

        for ip, port, headers in results:
            hosts[Hashing.make_headers_hash(port, headers)].append((ip, port, headers))

        for _hash, reports in hosts.items():
            _hosts = [ip for ip, port, headers in reports]

            """ highlight the query """
            _headers = []
            for line in headers:
                if query.lower() in line.lower():
                    start_pos = line.lower().find(query.lower())
                    end_pos = start_pos + len(query)
                    _headers.append(f'{line[:start_pos]}[red]{line[start_pos:end_pos]}[/red]{line[end_pos:]}')
                    continue
                _headers.append(line)

            """ finally generate & print the table """
            table = Logging.render_host_table(
                '\n'.join(_hosts),
                str(port),
                _headers
            )
            console.print(table)
            
        Logging.print_info('done, press "enter" to continue...[black]')
        console.input()

    except KeyboardInterrupt:
        break

    except Exception as e:
        Logging.console.print_exception()
        Logging.print_info('done, press "enter" to continue...[black]')
        console.input()  
