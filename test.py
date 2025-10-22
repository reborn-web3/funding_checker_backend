# test_connection.py
import asyncio
import asyncpg
DATABASE_DSN = "postgresql://myuser:mypassword@db:5432/funding"

async def test_db():
    try:
        # Попробуйте разные варианты DSN
        dsn_variants = [
            "postgresql://myuser:mypassword@localhost:5432/funding",
            "postgresql://myuser:mypassword@db:5432/funding"
        ]
        
        for dsn in dsn_variants:
            try:
                print(f"Testing: {dsn}")
                conn = await asyncpg.connect(dsn)
                print(f"✅ SUCCESS: {dsn}")
                await conn.close()
                return dsn
            except Exception as e:
                print(f"❌ FAILED: {dsn} - {e}")
                
    except Exception as e:
        print(f"All connections failed: {e}")

asyncio.run(test_db())