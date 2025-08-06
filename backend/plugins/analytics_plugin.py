from typing import Annotated
import os

import pyodbc
import msal
import struct
from itertools import chain, repeat
from semantic_kernel.functions import kernel_function

from backend.utils.connection_manager import connection_manager


class AnalyticsPlugin:
    """Queries the Microsoft Fabric analytics ecosystem for podcast episodes"""

    def __init__(self):
        tenant_id = os.getenv("TENANT_ID")
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        server = os.getenv("FABRIC_SQL_ENDPOINT")
        database = os.getenv("FABRIC_SQL_DATABASE")

        # --- Authenticate with MSAL ---
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        scope = ["https://database.windows.net/.default"]

        app = msal.ConfidentialClientApplication(
            client_id=client_id, client_credential=client_secret, authority=authority
        )

        result = app.acquire_token_for_client(scopes=scope)
        access_token = result["access_token"]

        token_as_bytes = bytes(
            access_token, "UTF-8"
        )  # Convert the token to a UTF-8 byte string
        encoded_bytes = bytes(
            chain.from_iterable(zip(token_as_bytes, repeat(0)))
        )  # Encode the bytes to a Windows byte string
        token_bytes = (
            struct.pack("<i", len(encoded_bytes)) + encoded_bytes
        )  # Package the token into a bytes object
        self.attrs_before = {1256: token_bytes}

        self.connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server},1433;Database=f{database};Encrypt=Yes;TrustServerCertificate=No"

    @kernel_function(description="get the latest podcast episode")
    async def query_latest_episode(
        self,
    ) -> Annotated[str, "Returns the latest podcast episode."]:

        await connection_manager.broadcast_tool_call("Fabric SQL Tool - Latest Episode")

        connection = pyodbc.connect(
            self.connection_string, attrs_before=self.attrs_before
        )
        cursor = connection.cursor()
        cursor.execute(
            """
                         SELECT
                            title,
                            publish_date
                        FROM sysk_silver_lh.dbo.episodes
                        WHERE publish_date = (SELECT MAX(publish_date) FROM sysk_silver_lh.dbo.episodes);
                    """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    @kernel_function(
        description="""
            Receives a tsql query as a string and sends that to the database
            Here is the table schema to reference when using this tool

            Tablename: sysk_silver_lh.dbo.episodes

            COLUMN_NAME	DATA_TYPE	CHARACTER_MAXIMUM_LENGTH	IS_NULLABLE
            guid	varchar	8000	YES
            title	varchar	8000	YES
            publish_date	date	NULL	YES
            description	varchar	8000	YES
            """
    )
    async def query_sql(
        self, sql_query: Annotated[str, "MUST be a tsql query string ONLY"]
    ) -> Annotated[str, "Returns query results from podcast table"]:

        await connection_manager.broadcast_tool_call("Fabric SQL Tool - General Query")

        try:
            connection = pyodbc.connect(
                self.connection_string, attrs_before=self.attrs_before
            )
            cursor = connection.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except:
            return "Query failed, try again with a correctly formatted tsql query"
