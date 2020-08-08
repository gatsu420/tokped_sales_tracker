# Tokped sales tracker
## Functionality
What this project is supposed to do:
1. Get sold, view and review count from certain products (first search page only)
2. Run frequently per interval to see traction

## DB config
At the moment, I use MariaDB version 10.3.22. You can check whether yours is compatible with the script.

The script relies on two tables; `keywords` and `recent_update`, with each tables contain these columns:

1. `keywords`
    1. `keyword_id` (PK)
    2. `keyword`

2. `recent_update`
    1. `update_id` (PK)
    2. `keyword_id` (FK to `keywords.keyword_id` using `RESTRICT` constraint for update and delete actions)
    3. `product_name`
    4. `product link` (not an ad tracking link, which usually starts with `https://ta.tokopedia.com`)
    5. `sold_count`
    6. `review_count`
    7. `view_count`
    8. `inserted_time` (time a record is inserted)

## Env var placeholder
1. `TP_KEYWORDS`: directory to keywords table in `database_name.table_name` format

2. `TP_RECENT_UPDATE`: directory to recent updates table in `database_name.table_name` format

3. `HAKASETEST_HOST`: database address

4. `HAKASETEST_USER`: database username

5. `HAKASETEST_PASS`: database password

Airflow will run the script using environment variables stored in GUI and any file the OS would boot into (example: `/etc/environment`).

## Cron config
This is what I use, please adjust accordingly;

`python3 /home/{username}/tokped_sales_tracker/scraper.py >> /home/{username}/tokped_sales_tracker/logs.txt`

Sometimes the script may fail due to various reasons (unstable internet, site going down, etc). The failed script will leave Chrome browser unclosed. To avoid unclosed browsers clogging the system, `chromedriver` and `Xvfb` will be killed manually by scraper. Thus, no longer need `killall` command separately.

## License
Copyright (C) 2020 Ranggalawe Istifajar

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/.