from corona.__init__ import cli

if __name__ == "__main__":
    cli(_anyio_backend="asyncio")
