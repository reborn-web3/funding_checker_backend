import redis.asyncio as redis
import asyncio


async def main():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)

    # Запишем тестовое значение
    await r.set("foo", "bar")

    # Прочитаем обратно
    val = await r.get("foo")
    print("Из Redis получили:", val)


if __name__ == "__main__":
    asyncio.run(main())
