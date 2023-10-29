# Migration Database

## Create new revision file

```bash
$ alembic revision -m <messages>
```

The revision file name was set up in `alembic.ini` file:

```ini
file_template = %%(year)d%%(month).2d%%(day).2d%%(hour).2d%%(minute).2d%%(second).2d_%%(slug)s
```

## Execute migration

- Upgrade db to the latest version

    ```bash
    $ alembic upgrade head
    ```

- Downgrade db to the initial version

    ```bash
    $ alembic downgrade base
    ```

- Upgrade/Downgrade db to specify version

    ```bash
    $ alembic upgrade <Revision ID>
    $ alembic downgrade <Revision ID>
    ```

## Other command

- Show history

    ```bash
    $ alembic history
    ```
- Show heads

    ```bash
    $ alembic heads
    ```

- Show current

    ```bash
    $ alembic current
    ```
